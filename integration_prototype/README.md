# Integrazione geometrica nel tracking

## Percorso corrente

La memoria opzione A assegna le viste a stati di posizione tramite coerenza di riproiezione e ammette separatamente i punti nella forma persistente con un verificatore appreso. [Metodo e limiti](../context/memory/MEMORIA_OPZIONE_A_E_SELEZIONE_20261122.md), [stato](../context/memory/STATO_LAVORO.md), [mappa](../mappa_interattiva/README.md).

| Moduli | Uso |
|---|---|
| position_state_memory, multi_hypothesis_pipeline | Stati di posizione e ciclo con tracker |
| scene_geometry, scene_memory, registration_verifier | Allineamento, celle pesate e verifica appresa |
| prepare_observation_superflex, scene_superflex_worker, deferred_scene_superflex | FPS-4096 per osservazione/memoria e completamenti causali |
| run_memory_grid | W0 e configurazioni esplicite sul sistema completo |
| export_point3_training, point3_training_data, verify_point3_export | Export causale e contratto per il matcher |
| geometry_retention, drive_delivery e relativi strumenti | Conservazione, recupero e consegna; configurazione esterna richiesta |
| shape_adapter, geometry_matcher, frame_coordinator | Correzione esterna e ordinamento causale |
| tracking_evaluation, run_pipeline e gestori di esperimenti | Valutatore originale e runner di riferimento |

I percorsi scene_memory, registered_scene_memory e multi_hypothesis_memory restano disponibili per confronti e riproducibilità. [SCENE_MEMORY](SCENE_MEMORY.md) e [POINT3_PROTOTYPE](POINT3_PROTOTYPE.md) descrivono queste fasi: non sostituiscono la specifica corrente. Gli strumenti di acquisizione e conservazione sono eseguibili solo con input/configurazioni dichiarati; non sono installatori HPC universali.

## Ambiente

Python 3.11 o successivo, ambiente dedicato:

```bash
python -m pip install -e './SuperFlex[images]'
python -m pip install -r integration_prototype/requirements-test.txt
```

Per i test che leggono il codice originale Whareformer, acquisire separatamente il commit 82dd349957e1f04f92a2979b4c92c2f3fed445c5 e impostare WHAREFORMER_SRC alla sua directory src. La cartella Whareformer della repository contiene il contributo del collega, non sostituisce il sorgente degli autori.

```bash
WHAREFORMER_SRC=/percorso/Whareformer/src python -m unittest discover -s integration_prototype -p 'test_*.py' -v
```

In PowerShell impostare prima $env:WHAREFORMER_SRC. Il runner neurale richiede anche PyTorch e le dipendenze originali; SuperFlex richiede ambiente CUDA, configurazione e checkpoint esterni. Le prove CPU sintetiche non sono inferenze neurali o misure di tracking.

## Esecuzione

```bash
python integration_prototype/run_memory_grid.py --help
python integration_prototype/export_point3_training.py --help
python integration_prototype/run_pipeline.py --help
```

Usare bundle verificati e nuove cartelle di output. Nessuna configurazione di esempio è una calibrazione finale. Le ricostruzioni pendenti devono essere risolte prima del frame successivo; un fallimento dichiarato conserva l'ultima forma valida. [Asset e cache esterni](../context/evidence/ASSET_ESTERNI.md).
