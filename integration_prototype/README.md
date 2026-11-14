# Integrazione geometrica nel tracking

Codice attuale per il ciclo osservazione → confronto causale → associazione → aggiornamento geometrico → ricostruzione. Le reti restano preaddestrate; i filtri di fusione non sono stati ricalibrati.

## Componenti

| Moduli | Responsabilità |
|---|---|
| shape_adapter, geometry_matcher | Confronto delle forme e correzione dei logits; riuso del matcher originale |
| frame_coordinator | Tutte le query prima degli aggiornamenti; associazioni effettive del tracker |
| cloud_memory, cloud_updater | Registrazione candidata e memoria limitata dei soli punti osservati |
| deferred_superflex | Richieste versionate, worker reale, pausa e replay con cache |
| experiment_runner, run_experiments | Varianti W0/G0/S-separata/S-accumulo/P-accumulo con tracker indipendenti |
| tracking_evaluation, evaluate_experiments | IDF1/mPCL originali, export e controllo della provenienza |
| summarize_experiments, run_pipeline | Tabelle e comando unico con stati di errore/attesa |
| frontend_inputs | Contratto e import della cache verificata, non rigenerazione neurale da RGB |
| prepare_video_bundle | Intera sequenza di feature ufficiali, join geometrici esatti e hash; nessun limite di prefisso implicito |
| audit_video_run | Copertura completa, correzioni effettive dei logits, uso causale di SuperFlex e memoria finale |
| validate_tracking_evaluator_hpc | Verifica esplicita del valutatore su riferimenti esterni forniti tramite argomenti |

## Ambiente e test

Python 3.11 o successivo. Usare un ambiente dedicato e installare il nucleo geometrico con le dipendenze dei test:

```bash
python -m pip install -e './SuperFlex[images]'
python -m pip install -r integration_prototype/requirements-test.txt
```

I test del matcher e del valutatore leggono i metodi originali degli autori, non una loro copia riscritta. Predisporre il sorgente [Whareformer](https://github.com/jacobchalk/Whareformer) al commit `82dd349957e1f04f92a2979b4c92c2f3fed445c5`, poi indicare la sua directory `src`:

```powershell
$env:WHAREFORMER_SRC = 'C:/percorso/Whareformer/src'
python -m unittest discover -s integration_prototype -p 'test_*.py' -v
```

```bash
WHAREFORMER_SRC=/percorso/Whareformer/src python -m unittest discover -s integration_prototype -p 'test_*.py' -v
```

La cartella `Whareformer/` di questa repository contiene la consegna del collega e non sostituisce il sorgente degli autori. I test IDF1 richiedono motmetrics; gli skip devono essere riportati, non contati come successi eseguiti.

## Esecuzione

Il runner richiede anche PyTorch, PyYAML, pandas e le dipendenze del sorgente originale; per SuperFlex servono ambiente e checkpoint degli autori. Il bundle esterno deve contenere input_manifest.json, dati numerici, configurazione effettiva, checkpoint e original_src verificati. Non viene distribuito insieme al codice. [Provenienza e asset](../context/memory/LEGGIMI_PASSAGGIO_AI.md).

```bash
python integration_prototype/run_pipeline.py --root <bundle_verificato> --config integration_prototype/variants_zero.example.json --output <nuova_run> --cache <cache_dedicata> --policy integration_prototype/evaluation_prefix.example.json
```

In alternativa a `--root`, usare `--frontend-manifest <manifest.json>` per importare dati in cache verificati. Per il worker reale aggiungere `--superflex-runtime <config_runtime.json>`. Scegliere output nuovi; richieste senza risultato producono uno stato di attesa. Gli esempi zero controllano la parità e non sono una calibrazione.

### Primo video completo con cache dichiarata

`prepare_video_bundle.py --inputs <feature_ufficiali> --template <bundle_compatibile> --tracks <tracks_by_id.json> --joined <join_verificati.json> --geometry-manifest <observations.json> --geometry-root <radice_geometria> --output <nuovo_bundle> --video P01_01 --fps 60` verifica gli input ufficiali e tutti gli abbinamenti prima di esportare la sequenza completa. `--max-frame` limita esplicitamente un controllo diagnostico. I pickle sono ammessi soltanto dalla distribuzione ufficiale fidata con hash di acquisizione verificati; non usare pickle non fidati. Il template deve fornire codice originale, checkpoint e configurazione compatibili: la sua presenza non certifica automaticamente un video diverso.

Per P01_01, `first_full_video.example.json` abilita S-accumulo DA con peso 0.1, non calibrato. Usare `evaluation_full_video.example.json` con l'orizzonte originale 99135; per altri video leggere i metadati anziché copiare tale numero. Le 33310 osservazioni temporali delle feature P01_01 terminano al frame 98099: sono tutti i frame del protocollo originale, non tutti i 99135 RGB del video.

```bash
python integration_prototype/run_pipeline.py --root <bundle_completo> --config integration_prototype/first_full_video.example.json --output <nuova_run> --cache <nuova_cache> --policy integration_prototype/evaluation_full_video.example.json --superflex-runtime <runtime_robust.json>
python integration_prototype/audit_video_run.py --bundle <bundle_completo> --inference <nuova_run/inference> --cache <nuova_cache> --output <nuovo_audit> --baseline <tracks_by_id.json>
```

L'audit accetta anche il riferimento `.json.gz`. I JSONL includono distanza, correzione effettiva e provenienza di ciascun confronto valido; `<variante>_memory/` contiene punti osservati, hash e riepilogo della memoria finale. È un export geometrico, non un checkpoint per riprendere il tracker. Le ricostruzioni e i parametri sono nella cache di richieste versionate. Il riuso delle forme per osservazione non è una nuova estrazione dalle immagini; SuperFlex sulla memoria viene eseguito dopo ogni ammissione con il worker reale.

## Evidenze e limiti

Prima run completa attiva: job 764454 concluso 0:0, 72 test HPC eseguiti/passati, 33310 frame/110590 osservazioni, 18 inizializzazioni, sette fusioni e 25 nuove SuperFlex riuscite. Audit 764474 e verifica locale della provenienza: forme da fusioni usate in 76 confronti futuri, memoria dei soli punti osservati verificata. Nessuna assegnazione diversa dalla baseline. [Resoconto e limiti](../context/evidence/full_video_20261114/REPORT.md).

Le metriche riproducono il protocollo originale per nomi oggetto e XYZ stimati, non identità fisiche indipendenti. Non confrontare mPCL del prefisso diagnostico con quello del video completo. Il frontend rigenerato, la copertura e la calibrazione restano aperti. [Attività correnti](../context/memory/TODO.md).

I vecchi piloti con percorsi locali e i runner sostituiti non fanno parte dell'interfaccia corrente. Sono recuperabili nel commit precedente `519e2b1`, senza duplicati eseguibili nel ramo attuale.
