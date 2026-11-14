# Prototipo autonomo dell'adattatore geometrico

## Stato corrente e precedenza — 14 novembre 2026

Leggere prima LEGGIMI_PASSAGGIO_AI.md (su GitHub: context/memory/). 763531 concluso con tutte le nove varianti zero esatte e valutate; frontend cache verificato, rigenerazione ancora pendente. Ultima suite locale 72 casi: 70 passati, due skip motmetrics; precedente suite HPC 69/69. Le sezioni seguenti conservano fasi storiche, inclusi job allora attivi e metriche allora assenti. Filtri di fusione invariati, revisione rinviata.

## Pipeline da input preparati a confronto — 14 novembre

`tracking_evaluation.py` e `evaluate_experiments.py` collegano IDF1/mPCL originali agli export verificati; `run_pipeline.py` concatena inferenza, valutazione e tabelle con stato/log per fase. Nessuna revisione dei filtri.

```text
python integration_prototype/run_pipeline.py --root <bundle_verificato> --config integration_prototype/variants_zero.example.json --output <nuova_run> --cache <cache_dedicata> --policy integration_prototype/evaluation_prefix.example.json
```

Richiede ambiente esistente con motmetrics; niente installazione automatica. Export/hash e scope obbligatori: vecchi report senza campi di osservazione non vengono riempiti con GT inventata. Risultati incompleti restano non valutati; un prefisso breve ha scale mPCL non supportate e non si confronta col video completo. Protocollo degli autori per nome oggetto/XYZ stimati, non GT fisica indipendente.

HPC: 69 test tutti eseguiti e passati, metriche note del video completo riprodotte; prima run della pipeline comune 763531 in corso nell’ultima osservazione. Il frontend RGB/maschere/metadati non è ancora unificato nel comando, che usa asset preparati. Pacchetto locale `../shared_exports/common_runner_20261114_v2/`; dettagli `../COMPLETAMENTO_PIPELINE_20261114.md`. Le note sottostanti sulle metriche ancora da collegare sono storiche.

## Runner comune delle varianti — 14 novembre

`experiment_runner.py`: W0, G0, S-separata, S-accumulo, P-accumulo, ciascuna con tracker/modello/memoria autonomi. Stesso registro/budget di accumulo, DA/MoGE separati. P-accumulo ora pubblica i descrittori dei punti osservati ammessi per confronti successivi, senza SuperFlex.

```powershell
# Ambiente e PYTHONPATH esistenti; nessun lancio HPC implicito.
python integration_prototype/run_experiments.py --root <bundle_verificato> --config integration_prototype/variants_zero.example.json --output <nuovo_report> --cache <cache_dedicata>
python integration_prototype/summarize_experiments.py --reports <summary.json> --output <nuova_tabella>
```

Esempio zero: nove esecuzioni, non configurazione calibrata. La CLI verifica input/hash e rifiuta spectrum sui bundle contenenti solo D2. Worker reale solo con --superflex-runtime <pipeline_config.json>; altrimenti report parziale in attesa. Nuovi tracker al replay, cache e ledger dei costi preservati; cartelle output esistenti rifiutate.

Misure per frame e variante con denominatori/fallimenti, byte di payload distinti da RSS, tempi annidati e costi di replay. IDF1/mPCL non ancora collegati, restano nulli/celle vuote; dati controllati e provenienze diverse separati. 58 test locali passati, otto nuovi del runner; nessuna esecuzione neurale/ufficiale del nuovo runner. Report `../RUNNER_VARIANTI_20261114.md`; pacchetto codice `../shared_exports/common_runner_20261114_v1/`. I job HPC precedenti usano snapshot immutati.

## SuperFlex differita e ritorno al matcher — 14 novembre

`deferred_superflex.py` lega ogni richiesta a video/track/sorgente/frame/versione/hash, configurazione e normalizzazione. Il worker riusa `shape_tools.pipeline.superflex`, senza training o nuovo modello.

```python
from deferred_superflex import DeferredSuperflex
coordinator = FrameCoordinator(tracker, ObservedCloudUpdater(), DeferredSuperflex(cache_dir))
transaction = coordinator.step(detections, metadata, keys, features, geometry_inputs)
# Prima del frame successivo: eseguire i worker delle richieste pendenti.
events = coordinator.resolve_reconstructions()
```

Solo per rappresentazioni SuperFlex abilitate. In assenza di esiti il coordinatore resta bloccato; su esito esplicitamente fallito conserva la vecchia forma. Risultati controllati dei test rifiutati di default. Forme pronte sostituiscono i confronti della track dai frame successivi; non entrano nei punti osservati.

Worker su ambiente esistente: `python deferred_superflex.py --request <directory> --config <pipeline_config.json>`. Richiede pesi/config corrispondenti e GPU per la pipeline originale; nessuna installazione o inferenza eseguita in questa fase. Percorsi relativi al JSON, un worker per richiesta, risultati esistenti preservati.

Nuovo runner: `run_real_prefix.py --root <nuovo_bundle> --accumulate --reconstruct`. Esporta richieste, si ferma quando manca un risultato, poi si ripercorre dall'inizio usando cache esatta. Nessuna ripresa da checkpoint e nessuna importazione retroattiva. Bundle futuri includono le dipendenze portabili; quelli storici non modificati. Runner verificato sintatticamente, non eseguito con Torch.

43 controlli locali: otto nuovi in `test_deferred_superflex.py`, con produzione GPU simulata e risultati controllati, non ricostruzioni della rete. Report `../SUPERFLEX_DIFFERITA_20261114.md`. La successiva descrizione di SuperFlex ancora da collegare è storica.

## Aggiornatore della nuvola collegato — 14 novembre

`cloud_updater.py` collega il registratore e la memoria esistenti al coordinatore. Uso con tracker/wrapper nuovi:

```python
from frame_coordinator import FrameCoordinator
from cloud_updater import ObservedCloudUpdater, ObservedCloudInput
coordinator = FrameCoordinator(tracker, geometry_updater=ObservedCloudUpdater())
# payload ha camera_points osservati, source da/moge, convenzioni dichiarate e provenienza.
transaction = coordinator.step(detections, metadata, keys, features, geometry_inputs)
```

Ogni valore in geometry_inputs deve essere ObservedCloudInput; le chiavi coincidono con le detection disponibili. Controlli di scope/sorgente/versioni/convenzioni e osservato vs completato. Una prima vista inizializza; solo le successive ammesse vengono fuse. Le forme separate possono aggiornarsi anche se la fusione viene rifiutata: sono memorie diverse.

Futuri bundle includono observed_clouds.npz e manifest; sul runner `--accumulate` abilita il candidato mantenendo il peso matching zero. Default disattivato. I bundle esistenti non hanno necessariamente questi input: non attivare l'opzione su di essi e non sovrascriverli. Preparatore/runner aggiornati ma non eseguiti in questa fase. Non rilasciare risultati di efficacia; resta da collegare SuperFlex alla nuvola ammessa. Stato completo in memoria, summary JSON senza array; nessun ripristino persistente.

35 test locali complessivi. Nuova suite: `python -m unittest discover -s integration_prototype -p test_cloud_updater.py -v`, con ambiente/PYTHONPATH già descritti sotto. Casi sintetici e controllati; nessuna nuova prova su viste reali. Report `../COLLEGAMENTO_ACCUMULO_20261114.md`.

## Coordinatore del frame — 14 novembre

`frame_coordinator.py` coordina il wrapper e il tracker originali. Il runner reale usa ora questo percorso. Esempio dopo aver costruito un tracker nuovo con GeometryMatcher:

```python
from frame_coordinator import FrameCoordinator
coordinator = FrameCoordinator(tracker)
# Per ogni frame, nell'ordine delle detection effettive:
transaction = coordinator.step(detections, metadata, keys, features)
assignments = transaction['assignments']
```

Non chiamare anche `tracker.update` o `matcher.commit`: lo fa il coordinatore. In disabled omettere features o passare solo None. `geometry_inputs` e `geometry_updater` sono un'interfaccia opzionale per proposte pure: accettate dopo associazione, con vecchio stato conservato su rifiuto/errore. Non è ancora collegata al registratore o a SuperFlex; il runner conserva forme separate. Se fallisce il nucleo tracker, l'istanza resta bloccata e richiede ricostruzione/replay. Gli snapshot non sono checkpoint persistenti. Uso seriale, nuovo tracker/coordinatore per video.

27 test locali complessivi, inclusi 11 nuovi del coordinatore; comando aggiuntivo con PYTHONPATH già impostato:

```powershell
& 'shared_exports/code_review_env/Scripts/python.exe' -m unittest discover -s integration_prototype -p test_frame_coordinator.py -v
```

Test con metodi originali e componenti controllati, non Torch/inferenza reale. Report `../COORDINATORE_FRAME_20261114.md`.

## Componente riutilizzabile — 14 novembre

Punto 1 completato: `geometry_matcher.py` avvolge il matcher originale con modalità `disabled`, `diagnostic`, `active`; DA/MoGE e punti/SuperFlex configurabili. Nessuna copia di inferenza/softmax/assegnazione. In diagnostica e active a peso zero passa lo stesso tensor originale. `run_real_prefix.py` usa ora questo componente; il preparatore lo include nei nuovi bundle, senza modificare quelli storici.

Esempio dopo aver costruito il tracker originale e caricato feature della rappresentazione scelta:

```python
import json
from geometry_matcher import GeometryConfig, GeometryMatcher

with open('geometry_config.example.json') as stream:
    config = GeometryConfig(**json.load(stream))
tracker.matcher = GeometryMatcher(tracker.matcher, video_id, config)
# Per ogni frame, keys e features corrispondono all'ordine effettivo delle detection.
tracker.matcher.set_frame(frame_index, keys, features)
tracker.update(detections, metadata)
tracker.matcher.commit(predicted_observation_to_actual_track_id)
```

In `disabled` chiamare solo `tracker.update`, senza contesto/commit. Configurazione di esempio diagnostica, non calibrata. Il componente richiede inferenza seriale, un matcher/modello per istanza; nuovo tracker/wrapper per nuovo video. `abort` annulla la sola geometria, non il tracker. I percorsi di import sono quelli del progetto; dipendenza `shape_tools` da aggiungere a PYTHONPATH come sotto.

Verifica aggiuntiva, da `lavoro di gruppo`, dopo aver impostato PYTHONPATH:

```powershell
& 'shared_exports/code_review_env/Scripts/python.exe' -m unittest discover -s integration_prototype -p test_geometry_matcher.py -v
```

Nove nuovi test con metodi originali compilati dal sorgente e modello/tensor NumPy controllati, più sette test adapter passati. Nessun test Torch/checkpoint reale in questa fase. Dettagli e limiti in `../INTEGRAZIONE_RIUTILIZZABILE_20261114.md`. Il seguito descrive il prototipo storico.

Stato 13 novembre: candidati NumPy per adattatore e registrazione/memoria dei punti; non wrapper del tracker completo. Risultato 2B in `../RISULTATI_REGISTRAZIONE_ACCUMULO_20261113.md`: sette nuovi test, 0/12 aggiornamenti reali ammessi. Contesto, prove e limiti: `../AVANZAMENTO_AUTONOMO_20261113.md`.

- `shape_adapter.py`: logits → correzione geometrica causale; `commit` dopo assegnazione esterna con ID track effettivi. Nuovo adattatore per video/reset.
- `test_shape_adapter.py`: sette test; il greedy viene estratto dalla copia locale originale via AST, con hash registrato nel replay.
- `run_available_pilot.py`: tre frame/cinque osservazioni P03_04, DA/MoGE punti/SuperFlex; hash degli input verificati. Logits di prova e associazioni annotate esplicite, nessuna inferenza Whareformer.

Da `lavoro di gruppo`, PowerShell con l'ambiente locale esistente:

```powershell
$env:PYTHONPATH = (Resolve-Path 'shared_exports/publish_candidate/SuperFlex/src').Path
& 'shared_exports/code_review_env/Scripts/python.exe' 'integration_prototype/test_shape_adapter.py' -v
& 'shared_exports/code_review_env/Scripts/python.exe' 'integration_prototype/run_available_pilot.py' --output 'outputs/independent_adapter_pilot_new'
```

Il runner rifiuta output esistenti. Richiede gli artefatti locali già prodotti, non presenti tutti in un clone pulito. Il confronto a peso zero è sul confine NumPy e sul greedy, non sull'intera rete Torch. Nessun peso/soglia scientifico fissato; nessun punto accumulato o inferenza SuperFlex su accumuli in questo prototipo.


## Registrazione e accumulo candidati

`cloud_memory.py` restituisce trasformazione e diagnostiche; budget per vista, ancora preservata e rifiuto senza modifica dei punti validi. `test_cloud_memory.py` contiene sette test finali. `run_registration_pilot.py` salva il piano prima dei punteggi e rifiuta output esistenti; `--selection close_views_selection.json` usa il diagnostico temporale separato. `plot_registration.py` mostra anche proposte rifiutate, che non sono fuse. Nessun nuovo output SuperFlex da accumuli reali.

```powershell
& 'shared_exports/code_review_env/Scripts/python.exe' 'integration_prototype/test_cloud_memory.py' -v
& 'shared_exports/code_review_env/Scripts/python.exe' 'integration_prototype/run_registration_pilot.py' --output 'outputs/registration_new'
```

## Frontend cache verificato

frontend_inputs.create_manifest(bundle, ready, targets, output) produce il contratto con RGB/annotazioni/camera verificati. run_pipeline.py accetta --frontend-manifest al posto di --root; mantiene la storia completa e importa i dati numerici verificati. Non è estrazione neurale rigenerata. Inventario, prove e dipendenze pendenti in ../FRONTEND_AVANZAMENTO_20261114.md.
