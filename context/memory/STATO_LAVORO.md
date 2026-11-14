# Stato corrente — 14 novembre 2026

Il ciclo causale tra forme, matcher e memoria è implementato. Il comando comune esegue varianti, valutazione e confronto da input preparati; il frontend importa cache verificate. La rigenerazione neurale completa da RGB non è ancora implementata/verificata.

## Evidenze acquisite

- Nove configurazioni zero completate e valutate, tutte esatte rispetto alla baseline (763531, COMPLETED 0:0, 23m24s).
- Sei ricostruzioni SuperFlex reali ready da inizializzazioni singole (763324, COMPLETED 0:0, 43m30s). Nessuna fusione multivista.
- Accumulo: 12 inizializzazioni e 12 rifiuti nelle quattro rappresentazioni (763323, COMPLETED, 12m11s). Sono tre osservazioni iniziali e tre successive, ripetute per rappresentazione.
- Valutatore originale riprodotto su baseline registrata P01_01 train: IDF1 73.269735%, mPCL 70.465504%. Nessun beneficio del nuovo metodo dimostrato.
- Frontend cache: dieci detection su tre frame, intera storia di 3398 frame e quattro file dati byte-identici al riferimento.
- Test prima del riordino: 72 casi locali, 70 passati e due skip motmetrics; precedente suite HPC 69/69.

Report e log già acquisiti sono in [evidenze](../evidence/README.md). Nessun nuovo controllo della coda HPC o esperimento neurale durante il riordino. Gli stati di attesa nei [resoconti storici](README.md) non descrivono la situazione corrente.

## Prossimo passo e vincoli

Proseguire il [frontend approvato](PIANO_FRONTEND_UNIFICATO_20261114.md): identificare asset DINOv2, provenienza PCA, scala della scena e ambiente; poi rigenerare e verificare il piccolo pilota. [Avanzamento e dipendenze](FRONTEND_AVANZAMENTO_20261114.md).

Marco ha esplicitamente rinviato la revisione dei filtri: non modificare soglie o registratore. Preservare la mappa manuale, i punti osservati separati dalle completazioni e l'ordine query → associazione → aggiornamento. [Guida tecnica](LEGGIMI_PASSAGGIO_AI.md).

Repository riordinata su richiesta di Marco: README unico ingresso, codice corrente separato dalla storia, vecchi piloti rimossi dalla versione attuale ma recuperabili in Git. La verifica della pubblicazione e dei controlli di questa revisione è registrata in [condivisione](docs/CONDIVISIONE.md).
