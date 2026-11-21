# Punto 3: prima implementazione della memoria a stati

Questa versione implementa il nucleo software del piano approvato. Non contiene
pesi del verificatore principale, etichette certificate di staticità o parametri
calibrati su EPIC. Non è una nuova campagna sperimentale.

## Moduli e limiti

- `scene_geometry.py`: allineamento affine DA/profondità scena, retroproiezione
  e trasformazione camera→scena. Richiede profondità scena già renderizzata,
  intrinseci, posa e unione delle maschere di tutti gli oggetti. Usa lo stesso
  obiettivo least-squares di Whareformer, aggiungendo controlli espliciti di
  validità; non è una certificazione di parità integrale della pipeline.
  Se il fit fallisce restituisce un esito senza punti, mai DA grezza da fondere.
- `scene_memory.py`: celle osservate con media pesata, contributi per vista
  anziché per numero di pixel, filtro di densità sugli input, decadimento dei
  pesi senza cancellare copertura unica; ipotesi di collocazione, conferma
  temporale e una sola forma in coordinate oggetto. Nessuna vista è mantenuta
  obbligatoriamente. Le soglie geometriche del vecchio ICP non sono chiamate.
- `registration_verifier.py`: contratto di errore predetto sulla coppia,
  baseline regressiva sulle diagnostiche con gruppi train/validazione separati,
  adattatore di inferenza per un futuro checkpoint TorchScript sulla coppia.
  Nessuna architettura neurale è stata scelta o addestrata implicitamente.
- `run_scene_memory.py`: replay locale di osservazioni già preparate, con hash,
  provenienza, associazioni esplicite, eventi e input FPS versionati. Non esegue
  Whareformer, rendering, DA o SuperFlex.

La staticità non viene dedotta dall'identità o da un piccolo spostamento del
centroide: ogni osservazione porta `staticity` e `evidence_id` da un componente
esterno ancora da validare con l'audit. Senza evidenza non si fonde. Senza modello
sono conservate ipotesi non confermate: nessuna accettazione di ripiego.

## Configurazione

`SceneMemoryConfig` richiede tutti i parametri senza numeri predefiniti di
accettazione: dimensione delle celle, emivita in secondi, conferme minime (almeno
due frame), peso di conferma, errore predetto massimo, raggio/minimo vicini del
filtro, budget delle celle e delle ipotesi, provenienza della selezione.
Questi valori devono essere selezionati sullo sviluppo. La stringa di provenienza
documenta la scelta, non ne verifica automaticamente l'onestà o l'adeguatezza.
I numeri in `test_scene_memory.py` sono solo parametri di test sintetici.

Le ipotesi deboli possono essere eliminate entro il budget; la forma confermata
e le collocazioni confermate non vengono eliminate. Superare il budget delle
celle interrompe l'aggiornamento senza modificare lo stato precedente. Il costo
e l'eventuale compattazione per video lunghi restano da misurare.

Il filtro di densità include il punto stesso nel conteggio dei vicini; può
penalizzare parti sottili e deve essere valutato, non considerato già calibrato.
Una vista non è scartata perché aggiunge superficie fuori dalla parte comune.

## Forma e movimento

Una collocazione è confermata solo dopo supporto temporale e verifiche apprese
fra viste già nel riferimento scena. La prima collocazione confermata definisce
un riferimento oggetto arbitrario, senza privilegiare i punti di una prima vista.
Le altre collocazioni conservano i propri punti senza sostituire la forma.

Nella prima tappa `fuse_after_motion=False`. Il percorso
`merge_placement(state_id, world_to_object, ...)` è già predisposto e testato su
trasformazioni note: richiede abilitazione esplicita, stato confermato,
registrazione rigida fornita dal chiamante e verifica appresa. Non cerca ancora
autonomamente la trasformazione. Dopo la fusione la stessa trasformazione vale
per le successive viste nello stesso stato fermo. Questo non certifica il caso
reale dopo spostamento: servono registratore, supervisione e validazione.

## Input SuperFlex

`export_superflex(path)` crea un nuovo NPZ con punti osservati in coordinate
oggetto, FPS deterministico di 4096 punti, indici, normalizzazione e inversa,
versione della forma, configurazione e storia delle osservazioni. Quando ci sono
meno di 4096 celle si ripetono indici: non sono inventate nuove osservazioni.
La normalizzazione resta centro medio del campione e scala pari a due volte la
massima coordinata assoluta centrata, come nel preparatore esistente.

Il vecchio worker ricampiona a caso: NON deve essere applicato a questi input
come se rispettasse FPS. Il collegamento al worker neurale, al completamento e
alla successiva pubblicazione dei descrittori resta da implementare e verificare.
Il modulo non presenta i completamenti come punti osservati.

## Collegamento al tracker

`SceneMemoryUpdater` si può passare come `geometry_updater` al `FrameCoordinator`,
senza il vecchio `DeferredSuperflex`. Il coordinatore rifiuta quella combinazione
prima di eseguire il tracker. Le associazioni originali precedono gli aggiornamenti
e non vengono modificate dal rifiuto geometrico.

Un aggiornamento `accepted` del coordinatore significa che è stato salvato lo
stato (anche candidato o un evento di rifiuto), NON che siano entrati punti nella
forma. Leggere `diagnostics.status`, `shape_changed` e `shape_version`.
Il nome di rappresentazione legacy `da_raw_points`/`da_raw_superflex` è mantenuto
solo per l'interfaccia esistente: il payload nuovo accetta esclusivamente
`SceneObservation(source='da_aligned', observed_only=True)` in coordinate scena.
Il runner storico NON viene commutato automaticamente al nuovo updater.

## Replay con input preparati

```text
python run_scene_memory.py --manifest osservazioni.json --out nuova_cartella
```

Manifest JSON `schema="point3-scene-replay-v1"`: `video`, `association_source`
(`predicted` oppure `oracle-development`), `config` con tutti i campi sopra,
`verifier` opzionale e lista `observations` in ordine di frame. Ogni riga contiene
`key`, `frame`, `timestamp` in secondi, `track_id`, `source="da_aligned"`,
`coordinate_frame="scene"`, `observed_only=true`, `alignment_valid`,
`alignment_provenance`, `staticity` (`stationary`, `moving`, `unknown`),
`evidence_id` e `points={"path": ..., "sha256": ...}`. I file NPZ contengono
`world_points` e devono essere dentro la cartella del manifest. Una riga con
allineamento fallito non richiede punti. Oracle significa diagnostica, mai prova
di efficacia con associazioni predette.

`verifier=null` è ammesso per provare il flusso senza dichiarare fusioni. Per la
baseline: `backend="diagnostic-error"`, percorso e hash dell'artefatto JSON.
Per il modello diretto futuro: `backend="torchscript-pair-error"`, percorso/hash
del checkpoint e `sample_points` esplicito; due tensori `[1,N,3]`, centro/scala
comuni del target, un errore normalizzato non negativo. Torch è importato solo
quando quel backend viene istanziato. L'adattatore Torch non è stato verificato
con un checkpoint reale.

## Supervisione e verifiche

`surface_error` confronta due insiemi di punti della stessa superficie sotto
trasformazioni note, con distanza NN media simmetrica normalizzata. Tiene conto
delle simmetrie rappresentate nel campione. Non usare la distanza fra due viste
parziali diverse come ground truth della posa. Copertura incompleta e superfici
simulate restano limiti del target, da verificare con l'audit e viste escluse.

Test: memoria/causalità, separazione forma-collocazione, movimento sintetico,
filtri, trasformazioni/scala, FPS/inversa, hash, isolamento train/validazione e
integrazione con `tracker.update` originale con tensori controllati.
Non sono inferenze reali, training EPIC o evidenze di miglioramento del tracking.

## Dipendenze

Nucleo: Python, NumPy, SciPy. Adapter del coordinatore: stesse dipendenze del
runner esistente e `shape_tools`. Nessun nuovo servizio o accesso HPC richiesto.
