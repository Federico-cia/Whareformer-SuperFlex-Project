# Punto 3: prima implementazione — 21 novembre 2026

## Mandato ed esito

Marco autorizza l'implementazione secondo le decisioni già approvate, iniziando
dalle parti indipendenti dai risultati dell'audit. Implementato il nucleo della
memoria a stati e il relativo percorso di replay/adattamento al coordinatore.
Non è ancora una pipeline neurale completa o un criterio validato sui video.

Contratti e istruzioni: [SCENE_MEMORY.md](../../integration_prototype/SCENE_MEMORY.md).
Decisioni scientifiche in [SUPERVISIONE_AMMISSIONE_20261121.md](SUPERVISIONE_AMMISSIONE_20261121.md).

## Lavoro eseguito

- `scene_geometry.py`: allineamento affine DA/scena con esclusione delle
  maschere, retroproiezione e trasformazione rigida; fallimento esplicito senza
  ripiego DA grezzo. Riceve la profondità scena dal renderer esistente, non ne
  implementa una nuova ricostruzione.
- `scene_memory.py`: celle osservate pesate, filtro di densità, decadimento senza
  cancellazione della copertura unica, ipotesi di collocazione confermate nel
  tempo, una forma separata dalle collocazioni. Configurazione richiesta
  esplicitamente, con provenienza della selezione su sviluppo: nessun valore
  di test promosso a parametro reale.
- Percorso dopo spostamento predisposto: registrazione rigida fornita dal
  chiamante e controllo del verificatore prima della fusione. Prima tappa
  statica come default; il registratore e il verificatore reali non sono
  sostituiti da decisioni sintetiche.
- FPS deterministico di 4096 punti e NPZ versionati con inversa della
  normalizzazione e provenienza. Punti ripetuti se la copertura contiene meno
  celle: non sono nuove osservazioni.
- `registration_verifier.py`: uscita di errore predetto, baseline regressiva
  sulle diagnostiche addestrabile con target indipendenti e gruppi separati,
  adattatore per futuro modello diretto sulla coppia in formato TorchScript.
  Senza modello nessuna ipotesi viene confermata/fusa. Architettura principale,
  checkpoint e addestramento reale ancora mancanti.
- Target geometrico di supporto: distanza NN simmetrica fra la stessa superficie
  sotto trasformazioni note, distinta dallo spostamento degli stessi indici;
  testata l'equivalenza di simmetrie discrete nel campione. Non risolve da sola
  la supervisione reale su coppie parziali.
- `SceneMemoryUpdater` collegabile al coordinatore: aggiornare un'ipotesi non
  significa cambiare la forma; nessuna modifica dell'associazione originale.
  Il coordinatore impedisce l'uso col vecchio worker di ricostruzione, che
  ricampionerebbe casualmente e non ha il nuovo contratto.
- `run_scene_memory.py`: replay di manifest preparati, binding tramite hash,
  eventi e input SuperFlex salvati senza sovrascrivere risultati precedenti.
  Il runner storico non è stato commutato al nuovo percorso.

## Verifiche effettive

Suite locale finale: **105 casi, 103 superati e 2 saltati** per motmetrics non
disponibile, nessun fallimento/errore. Inclusi **23 nuovi test**, tutti superati:
19 del nucleo/replay/verificatore e 4 di integrazione col `tracker.update`
originale mediante tensori controllati. Le regressioni coprono anche i moduli
precedenti; nessuna inferenza neurale reale o misura di tracking nuova.

Scoperto e corretto nei test un problema numerico di assegnazione alle celle
dopo traslazioni: coordinate entro poche ULP dal bordo sono ricondotte allo
stesso indice, senza cambiare il raggio geometrico di fusione.

Ambiente locale: Python 3.13 di Miniconda e dipendenze installate soltanto in
`tmp/point3_test_deps`, senza modifica dell'ambiente HPC. NumPy 2.5.5, SciPy
1.18.1, trimesh 5.2.1, Pillow 13.0.0, PyYAML 6.0.4: ambiente diverso dalle versioni
fissate nei vecchi requirements. Log e ricevuta con hash in
`outputs/point3_implementation_20261121/`. Non certificata esecuzione sull'HPC,
né inferenza dell'adattatore TorchScript con un checkpoint reale.

## Audit: cosa serve da Marco

Avvio degli script riservato a Marco, come richiesto in AGENTS; nessun accesso
diretto dell'assistente. Eseguire in `strumenti_hpc/`:

1. `esegui_controllo_hpc.bat` per accounting/progresso dell'arricchimento.
2. `esegui_scarica_audit.bat` per esiti e log del job già inviato **783586**.

Scarico reso robusto: identifica il job esatto, recupera anche output parziali,
accounting e hash, usa una nuova cartella locale per ogni tentativo, controlla
gli errori e scompatta l'archivio. Non invia/riprende job e non crea archivi
remoti. Anche senza `summary.json` i log possono spiegare il fallimento.
Non eseguito in questa sessione: verifica degli script tramite lettura locale,
non prova di autenticazione o trasferimento. Leggere i file risultanti prima
di qualsiasi decisione di ripresa. Stato attuale HPC ancora ignoto.

## Lavoro ancora necessario

1. Acquisire e interpretare audit/accounting: staticità non certificata e vecchia
   misura di errore punto-a-punto da non usare come target invariante.
2. Verificare il collegamento ai renderer/loader reali e costruire evidenze di
   staticità indipendenti dai gate; congelare parametri scelti su sviluppo.
3. Costruire dati, architettura, training/validazione del verificatore diretto;
   selezionare il criterio operativo sull'utilità della memoria.
4. Collegare gli input FPS al worker reale senza ricampionamento casuale e
   pubblicare le ricostruzioni soltanto per i frame successivi; verificare replay
   causale completo e comportamento sui fallimenti di SuperFlex.
5. Integrare/validare il registratore reale dopo spostamento. Il percorso
   software predisposto non dimostra ancora questo obiettivo sui video.
6. Test set indipendente e coordinamento delle memorie con il compagno.

Nessuna nuova scelta scientifica principale, training EPIC, inferenza reale,
modifica della mappa, job HPC o pubblicazione in questa fase. La regressione
di base è stata adattata soltanto su dati sintetici nei test.
