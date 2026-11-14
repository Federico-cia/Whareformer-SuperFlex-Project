# Completamento della pipeline: stato e prossimo sviluppo — 14 novembre 2026

## Confine operativo

Il ciclo software è collegato: osservazione → associazione → proposta geometrica → ricostruzione → confronti successivi. Il runner attuale parte però da **input preparati e verificati** (annotazioni/maschere, feature d'aspetto, XYZ e artefatti geometrici), non da un video RGB arbitrario. Questo confine va distinto da una pipeline completa di acquisizione/preprocessing e da un sistema multivista validato sperimentalmente.

| Componente | Stato effettivo |
|---|---|
| DA/MoGE, punti e SuperFlex per osservazione | Pipeline portabile disponibile e già eseguita; non ancora unita al frontend Whareformer in un ingresso unico dai frame/maschere/metadati |
| Whareformer + confronto geometrico, coordinatore e memorie | Collegati; controlli reali a peso zero passati sul prefisso P01_01 |
| Registrazione e accumulo | Candidato collegato, ma zero fusioni reali ammesse nei job; revisione dei filtri esplicitamente rinviata |
| SuperFlex differita e ritorno al matcher | Job 763324 completato: sei ricostruzioni reali pronte, controllo zero passato; provengono da inizializzazioni, non da fusioni multivista riuscite |
| Varianti e telemetria | Runner comune con cinque modalità, sorgenti separate, costi/copertura/fallimenti e controllo punti |
| Valutazione tracking | Collegata in questa fase al valutatore originale con origine delle annotazioni e policy esplicite |
| Esecuzione unica da input preparati a tabelle | Nuovo comando disponibile; prima run completa comune in corso, non ancora risultato concluso |
| Copertura, calibrazione e test separato | Da completare nel piano approvato; il pilota geometrico sparso non basta a sostenere beneficio sul tracking |

## Sviluppo eseguito in questa fase

`integration_prototype/tracking_evaluation.py` riusa via AST le funzioni originali di IDF1 e PCL con hash normalizzati LF verificati, senza importare il frontend neurale. Export delle predizioni ordinato per ID effettivi, annotazioni/box/XYZ separati dalle assegnazioni, copertura completa controllata. Il runner include ora i campi di valutazione nei JSONL; lo SHA di ciascun export viene legato al summary.

`evaluate_experiments.py` controlla hash e scope degli export, valuta solo esecuzioni complete e produce un nuovo report/CSV preservando gli originali. Errori, campi mancanti o risultati parziali non diventano punteggi zero. Mantiene la convenzione degli autori per nome oggetto/deduplicazione, IoU e posizione stimata: non introduce identità fisiche GT indipendenti o misure 3D metriche certificate.

`EvaluationPolicy` richiede fps, frame finale e scope espliciti. Per un prefisso il frame finale deve coincidere con l'ultimo frame processato: non viene esteso silenziosamente a un futuro non elaborato. mPCL originale usa 145 scale temporali e attribuisce contributo zero alle scale senza campioni; viene esportata anche la media sulle sole scale supportate, etichettata come diagnostica distinta. Un prefisso breve non è confrontabile direttamente con il video completo. Il valore 0.3 della valutazione è quello originale del benchmark; nessun gate di fusione modificato.

`run_pipeline.py` concatena esecuzione delle varianti → valutazione → tabella, con log ed esiti per fase. Arresta la catena su errore o attesa dei risultati differiti e controlla che gli artefatti attesi siano stati prodotti. Nuovo output per ogni tentativo; cache riutilizzabile e costi di replay conservati. Non sceglie metodi, soglie o split e non rigenera le feature di ingresso.

Esempio da ambiente esistente:

```text
python integration_prototype/run_pipeline.py --root <bundle_verificato> --config integration_prototype/variants_zero.example.json --output <nuova_run> --cache <cache_dedicata> --policy integration_prototype/evaluation_prefix.example.json
```

Runtime SuperFlex esplicito opzionale per nuove richieste; con risultati reali già in cache non serve una nuova inferenza. Moduli/configurazioni nel pacchetto locale `shared_exports/common_runner_20261114_v2/`, esclusi dati e pesi.

## Verifiche e job

- Locale: suite di 69 casi, 67 passati e due casi motmetrics saltati per dipendenze locali assenti. Sintassi e help controllati; log/hash in `outputs/tracking_evaluation_20261114/`. Non mascherati come test eseguiti.
- **763498 COMPLETED/0:0**, 33 s: otto test del valutatore eseguiti senza skip nell'ambiente HPC; IDF1 **73.2697350574193%**, mPCL **70.46550449586454%** riprodotti sulle 110590 predizioni registrate/33310 frame P01_01 train. È scoring di dati esistenti, non nuova inferenza.
- **763530 COMPLETED/0:0**, 45 s: **69 test tutti eseguiti e passati**, compresi round-trip su file e pipeline di orchestrazione controllata; stesso controllo delle metriche sul video completo. Output `~/cv_project/evaluator_20261114_v2/result_763530/`, log `~/cv_project/eval_bridge_763530.out/.err`.
- **763531 RUNNING**, 10m50s nell'ultima osservazione: nove configurazioni a peso zero sul prefisso reale, pipeline comune → valutazione → tabelle. Due CPU/16 GB, limite 90 minuti, dipendenza dal successo di 763530. Riusa copie della cache delle sei ricostruzioni del 763324, senza GPU o nuove inferenze. Output `~/cv_project/evaluator_20261114_v2/pipeline_763531/output/`, cache dedicata nella stessa directory; log `~/cv_project/pipeline_zero_763531.out/.err`. Esito finale ancora da leggere.

Il completamento del precedente GPU 763324 è verificato, 43m30s e sette replay (sei pause per richieste, settimo completato): sei risultati SuperFlex ready, zero baseline esatto, nessuna differenza dal collega, zero fusioni e sole inizializzazioni ammesse. Dettagli in RIPRESA_HPC_20261114.md. Non è validazione della ricostruzione multivista.

## Che cosa manca ancora

1. **Consolidare la prima esecuzione unificata:** acquisire esito 763531 e controllare report, metriche, fallback/copertura e costi; correggere eventuali problemi software senza cambiare i filtri.
2. **Unificare l'ingresso dai dati:** collegare gli estrattori originali di aspetto/PCA e posizione e la pipeline geometrica al formato comune, con cache e mapping per osservazione. Per EPIC, maschere e metadati camera/scena sono ingressi dichiarati; non è stato scelto un nuovo segmentatore automatico né promesso RGB-only/strettamente online.
3. **Dare copertura sufficiente alla geometria:** il prefisso ripercorre 3398 frame, ma contiene solo sei osservazioni geometriche di tre track. Predisporre segmenti/casi e budget coerenti con la valutazione, riusando gli asset disponibili; non trasformare il pilota sparso in prova di efficacia globale.
4. **Rivedere registrazione/ammissione quando Marco lo richiederà:** attività rinviata, resta un limite alla validazione multivista. Nessuna revisione o allentamento in questa fase.
5. **Calibrare e valutare secondo il piano approvato:** sviluppo separato dal test, metodi/parametri congelati prima del test, confronto delle cinque modalità e delle sorgenti con fallimenti inclusi. Nessun beneficio del contributo geometrico dimostrato dai job a peso zero.

La pipeline può essere completa come software da input preparati a report e restare scientificamente non validata per accumulo e miglioramento tracking. Conclusioni e limiti devono mantenere entrambe le distinzioni.
