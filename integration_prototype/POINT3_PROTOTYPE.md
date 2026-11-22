# Memoria accumulata: uso del prototipo

## Perimetro chiarito successivamente — 22 novembre 2026

Questo documento riguarda il prototipo semplificato a singola forma. Marco richiede ora di predisporre il sistema multi-ipotesi discusso originariamente. Il funzionamento e gli export qui descritti non ne certificano l’implementazione. [Confronto e requisiti mancanti](../context/archive/CONFRONTO_MEMORIA_ORIGINARIA_20261122.md). Nessuna modifica algoritmica in questa revisione.

## Politica corrente

Revisione approvata da Marco il 22 novembre 2026: ogni vista DA allineata alla
scena viene registrata sulla forma dell'oggetto e verificata prima della fusione,
anche quando l'oggetto è stato spostato. Non si richiede prima una certificazione
di staticità. Il percorso precedente a stati rimane nei suoi moduli per confronto.
Questa è una semplificazione del prototipo, non una dimostrazione di accuratezza.

La prima vista inizializza una memoria candidata; occorrono almeno due viste
accettate per pubblicare la forma. La prima vista non gode di conservazione o
peso speciali. I punti sono fusi in celle con media pesata e decadimento temporale;
la copertura unica non viene cancellata. Forma in coordinate oggetto e ultima
trasformazione verso la scena rimangono distinte. Il tracker conserva il suo XYZ.

`registered_scene_memory.RegisteredObjectMemory` usa la registrazione candidata
esistente, convertendo esplicitamente la convenzione delle matrici. Le sue vecchie
soglie producono diagnostiche ma non decidono l'ammissione: decide il verificatore
appreso e il punto operativo selezionato sulla calibrazione simulata. Mancanza
del modello, allineamento invalido, punti insufficienti o verifica negativa non
modificano la forma confermata. `RegisteredMemoryUpdater` si collega al coordinatore
originale; il worker storico che ricampiona casualmente rimane escluso.

## Dati e modello

- `prepare_verifier_data.py`: superfici osservate, crop/rumore/movimento noti,
  target geometrico continuo. Nessun gate usato come etichetta.
- `verify_verifier_data.py`: ricalcolo indipendente dei target e verifica file.
- `train_verifier_baseline.py`: regressione lineare sulle otto diagnostiche
  già disponibili. Training su 13 identità, calibrazione su due, valutazione
  descrittiva su altre due entro P01_01. Il modello principale sulla coppia
  di punti non è stato implicitamente scelto o addestrato.
- `select_conservative_policy.py`: alternativa prudente, con budget empirico
  di false ammissioni richiesto esplicitamente e soglia scelta sulla calibrazione.
  Il budget non è una garanzia statistica o fisica. Non modifica il modello.
- `validate_registered_motion.py`: esercizio diagnostico con movimento noto e
  ritaglio su superfici reali; non ground truth di movimento reale.

Consultare i report numerici: la baseline presenta false ammissioni rilevanti.
Il corretto funzionamento del software non rende le memorie dati geometrici
certificati. Non usare questi risultati come prova di beneficio nel tracking.

## Export per il punto 2

`export_point3_training.py` legge i target originali e le nuvole dell'audit.
Tutte le query di un frame vedono le memorie prima di qualsiasi aggiornamento
di quel frame, anche quando ci sono più oggetti. Poi vengono applicate le
associazioni oracle originali e aggiornate le memorie. Si esportano:

- `examples.json`: query, candidate nello stesso ordine originale, target,
  riferimenti alle memorie strettamente precedenti, mancanti espliciti;
- `training_inputs.npz`: copia byte-identica di input numerici e label originali;
- `features/`: descrittori D2/spettro esistenti e punti normalizzati, marcati
  esplicitamente come osservati, senza fingere ricostruzioni SuperFlex;
- `shapes/`: input FPS di 4096 punti, normalizzazione e inversa, provenienza,
  cronologia, versione e configurazione della forma;
- `versions.json`, `events.jsonl`, `configurations.json`, `summary.json`;
- `verification.json`: esito del verificatore indipendente dell'export.

Le impostazioni di risoluzione/densità/decadimento sono scelte ingegneristiche
esplicite del prototipo, relative al raggio della prima nuvola valida; non sono
state ottimizzate guardando metriche del tracker. P01_01 resta sviluppo.
Il campione originale non contiene esempi Nuova track: non è tutto il training
necessario al punto 2. Nessuna distanza finale o modifica al matcher viene
imposta dal lettore; il confronto delle forme resta il punto 1 del TODO generale.

Uso dal codice del compagno, con questi moduli nel percorso Python:

```python
from point3_training_data import AccumulatedTrainingData
data = AccumulatedTrainingData("cartella_export")
sample = data.example("P01_01/frame_0000003465__d0")
# sample: numerical_input, original_label, query, candidate_memories,
# geometry_available, candidate_track_ids, target_class.
```

I mancanti sono `None` con maschera booleana; non vanno trasformati in distanza
zero. `completed=True` legge invece il file con ricostruzioni effettivamente
collegate e rifiuta di mescolare completamenti e punti osservati.

## SuperFlex

`prepare_query_reconstructions.py` prepara anche gli input della vista corrente,
che non entrano mai nelle memorie candidate dello stesso esempio.
`scene_superflex_worker.py` usa gli array FPS già salvati, senza ricampionamento
casuale dell'ingresso. Richiede ambiente GPU e checkpoint/configurazione fidati
esistenti; ne verifica gli hash. Riusa modello, denormalizzazione e gestore delle
primitive degli autori; conserva mesh e descrittori separati dai punti osservati.

```text
python scene_superflex_worker.py --export CARTELLA_EXPORT --runtime CONFIG_PIPELINE.json
python attach_scene_reconstructions.py CARTELLA_EXPORT
```

Il worker conserva gli esiti ready/failed. In ripresa salta i risultati esistenti,
anche quelli falliti: per ritentare un fallimento conservare il precedente e
usare una nuova cartella di esecuzione. L'aggancio controlla input, versione,
hash e disponibilità temporale; dopo un fallimento conserva l'ultimo completamento
riuscito precedente. Gli output dei test non sono ammessi nell'export di produzione.
Le ricostruzioni della memoria sono disponibili solo per query di frame successivi;
quelle delle query descrivono solo l'osservazione corrente.

Prova GPU ridotta: pacchetto di due memorie e due query preparato localmente,
script `strumenti_hpc/esegui_point3_fps_smoke.bat` e scarico separato
`scarica_point3_fps_smoke.bat`. Nessun job è inviato dall'esecuzione dei test locali.
Il pacchetto completo di training resta locale; la prova GPU trasferisce solo
quattro input e il codice del worker, senza dati numerici originali del tracker.

## Stato da distinguere

1. Pipeline software e replay oracle: verificabili localmente.
2. Ricostruzioni SuperFlex nuove: richiedono esecuzione GPU e verifica dei risultati.
3. Efficacia scientifica: richiede confronto di tracking con baseline e test
   indipendente; né oracle né supervisione simulata lo sostituiscono.
