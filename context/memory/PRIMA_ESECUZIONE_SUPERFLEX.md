# Prima esecuzione SuperFlex robust sull'HPC

7 novembre 2026. Responsabile: **Marco, persona B**. Stato: **installazione, prima inferenza e controllo visivo dell'esempio completati**. Risultati recuperati in `outputs/setup_744144/`; esito e limiti in `VERIFICA_SUPERFLEX_744144.md`. Le annotazioni di revisione pendente sotto descrivono lo stato precedente al recupero e all'ispezione locale.

## Esito del job 744144

Lo screenshot condiviso da Marco riporta installazione SuperFlex riuscita, `No broken requirements found`, `SUPERFLEX_SMOKE_OK` e `SETUP_AND_SMOKE_OK`. Input lamp.ply: 4096 punti, seed 42; 7 primitive attive; checkpoint/config con gli stessi hash registrati localmente. PyTorch 2.6.0+cu124 su A100 MIG 4g.40gb, primo forward circa 0,787 s (singola esecuzione, non benchmark). Output remoto in `~/cv_project/runs/setup_744144/`; import/compilazione, checkpoint, forward e export hanno superato i controlli dello script. Lo stato contabile del job non è ancora acquisito e i file non sono ancora stati recuperati localmente.

La disconnessione SSH compare dopo il completamento: non richiede un rilancio. Prossimo passo: scaricare l'intera cartella del run in `outputs/` locale, verificare i file e confrontare `smoke/input.ply` con `smoke/reconstruction.ply`. Solo dopo la revisione visiva si può concludere il controllo dell'esempio. Non è ancora una prova su EPIC né una dimostrazione di qualità del completamento da viste parziali.

Le sezioni seguenti conservano preparazione e verifiche precedenti al lancio.

## Esito del primo job diagnostico e prossimo lancio

Il job **744133**, inviato da Marco, ha prodotto i log condivisi in screenshot: nodo `gnode02`, istanza **A100 MIG 4g.40gb** (40.192 MiB riportati), driver 610.43.02, modulo CUDA 12.4 caricato, `nvcc` 12.4.99, GCC/G++ 11.5.0, Conda 26.1.1. `CUDA_HOME` non è impostata dal modulo, ma `nvcc` è disponibile; il job successivo ricava il percorso dal compilatore. La schermata non mostra un errore conclusivo; stato contabile SLURM non ancora acquisito. Rilevamento riuscito, non prova di compatibilità già superata.

Dettagli personali di accesso HPC omessi dalla copia condivisa; configurazione conservata solo localmente.

Scelta iniziale di compatibilità, da provare: Python 3.11, PyTorch 2.6.0 e torchvision 0.21.0 per CUDA 12.4, NumPy 1.26.4, PyG 2.6.1 e torch-cluster 1.6.3 con wheel `pt26cu124`. Il resto dei requirements ufficiali viene risolto sotto questi vincoli e registrato con `pip freeze` ed export Conda. Non è l'ambiente esatto degli autori (requirements non fissati), né una compatibilità garantita. Fonti consultate il 7 novembre: [distribuzioni ufficiali PyTorch](https://pytorch.org/get-started/previous-versions/), [documentazione PyG 2.6.1](https://pytorch-geometric.readthedocs.io/en/2.6.1/install/installation.html), [wheel PyG per PyTorch 2.6/CUDA 12.4](https://data.pyg.org/whl/torch-2.6.0+cu124.html).

La prova usa il modello e le funzioni geometriche degli autori, con seed 42 e `examples/lamp.ply`. Controlla esattamente le chiavi del checkpoint (senza accettare silenziosamente teste mancanti), esegue un forward, verifica valori finiti e primitive attive e salva NPZ, input PLY, ricostruzione PLY e report JSON. Nessun training e nessun server Viser. Output in `cv_project/runs/setup_JOBID/`; la revisione visiva resta necessaria anche dopo un esito numerico positivo.

Verifica locale effettuata: sintassi Python, comando di aiuto e formato Linux dello script SLURM. Compilazione CUDA, installazione, caricamento dei pesi e inferenza **non ancora eseguiti**. Se il job fallisce, esaminare stdout e stderr prima di rilanciarlo.

**Accesso verificato il 7 novembre:** Marco è collegato via SSH. L'output condiviso mostra partizione `stud` attiva, miniconda3 e moduli CUDA 12.1/12.2/12.3/12.4/12.8. `lquota` riporta **47,5 GB usati su 50 GB**; il limite corrente prevale sui 100 GB delle slide. Prima dell'installazione occorre esaminare l'occupazione e verificare spazio alternativo o materiale eliminabile con autorizzazione di Marco. Non è ancora stata assegnata/verificata una GPU per il modello.

## Risultato da ottenere

**Download locali verificati il 7 novembre:** codice presente in `SuperFlex-repo/`, con tutti i 76 file corrispondenti agli hash dell'inventario GitHub già salvato per il commit fissato; checkpoint in `SuperFlex-repo/robust/ckpt.pt` (24.025.089 byte), configurazione in `robust/config.yaml`, esempio in `examples/lamp.ply`. Checksum salvati in `manifests/superflex_archive.json`. Il checkpoint è un contenitore ZIP PyTorch leggibile come archivio; non è ancora stato caricato dal modello. La configurazione è una configurazione di training degli autori: per la prima inferenza useremo solo la sezione architetturale `superflex`, senza avviare training o logging W&B.

**Spazio HPC dopo la pulizia:** screenshot di Marco con `lquota` indica **0,5 GB usati su 50 GB**, circa 49,5 GB liberi. Ambiente personale qwen7b rimosso; restano gli ambienti condivisi. Il job diagnostico ora carica esplicitamente `cuda/12.4`, disponibile nell'elenco mostrato da Marco; la compatibilità effettiva con driver e ambiente verrà verificata dai log.

Caricare il checkpoint SuperFlex robust ufficiale, elaborare una nuvola di punti fornita dagli autori e salvare punti, parametri e una ricostruzione visualizzabile. Un esempio riuscito verifica la pipeline; non dimostra ancora qualità su EPIC o utilità nel tracking.

## Materiale minimo

- [Codice ufficiale, ZIP del commit consultato](https://github.com/GabrielTavernini/superflex/archive/15b63b23375c6a80c3ce0dec4be0c9b11055c722.zip). È separato da Whareformer. Il materiale già presente in `../tmp/pdfs/repos/superflex` è una copia preparatoria da verificare prima di usarla come sorgente eseguibile.
- [Checkpoint robust supervisionato degli autori](https://drive.google.com/drive/folders/1cHbtZLToQRontte6CyzvQpL5IHUqk-x4?usp=sharing), con checkpoint e relativa configurazione. Il README distingue robust da robust unsupervised: registrare quale variante usiamo. Il nome previsto dalla demo è `ckpt.pt` con `config.yaml` nella stessa cartella; verificare i nomi realmente rilasciati.
- Esempio iniziale previsto dalla demo: `examples/lamp.ply`, da verificare nel codice scaricato. Nessun download completo di ShapeNet richiesto.

I link derivano dal README e dall'inventario locali del commit consultato. Il tentativo web del 7 novembre di aprire i file a quel commit non è riuscito; accesso e download odierni non ancora verificati.

## Ordine operativo

1. Collegarsi al cluster tramite SSH, su rete Bocconi o VPN. Server documentato: `slogin.hpc.unibocconi.it`.
2. Trasferire `scripts/hpc_probe.sbatch` e inviarlo con SLURM. Il job diagnostico richiede una GPU, due CPU, 4 GB di RAM e cinque minuti. Registra GPU visibile, ambiente Conda, moduli disponibili, compilatore CUDA/C++ e quota. Non installa pacchetti.
3. Leggere i log e scegliere ambiente Python, PyTorch e toolchain CUDA compatibili. Preparare un ambiente separato da Whareformer. I requirements SuperFlex non fissano le versioni: registrare quelle effettivamente usate, senza assumere compatibilità automatica delle ultime release.
4. Trasferire codice, checkpoint robust ed esempio; verificarne versione e checksum. L'installazione segue le regole del cluster. Eseguire import e compilazione sul nodo di calcolo tramite job, non sul nodo di accesso.
5. Preparare una piccola esecuzione senza server grafico: campionamento a 4096 punti, normalizzazione degli autori, forward con checkpoint robust, salvataggio degli input, trasformazioni e output. Seed e configurazione registrati. Terminare il processo dopo il salvataggio.
6. Verificare caricamento dei pesi, output finiti, primitive attive e ricostruzione visiva. Solo dopo passare agli input EPIC.

## Riscontri nell'ispezione del codice

- `superflex/functional/backend.py` usa `torch.utils.cpp_extension.load` per compilare sorgenti C++/CUDA: GPU/driver da soli non bastano, servono toolchain e ambiente compatibili.
- `demo_viser.py` sceglie di default `checkpoints/superflex`, non `checkpoints/robust`: va indicato il checkpoint corretto. Avvia Viser e termina con un ciclo infinito; non è una prova batch che si chiude da sola.
- Il sampler compilato tramite `setup_sampler.py` è indicato nel README come necessario al training; non confonderlo con l'estensione point-voxel richiesta anche dall'inferenza.
- Il caricamento dei pesi nel modello tollera alcune chiavi mancanti per compatibilità con checkpoint più vecchi. Per la variante robust vanno controllate esplicitamente le chiavi: non dichiarare riuscito il caricamento soltanto perché non solleva un'eccezione.

Queste verifiche riguardano la copia locale consultata. Restano da confermare sul codice e sui pesi effettivamente trasferiti sull'HPC. Nessuna modifica ai modelli o scelta definitiva della memoria delle track è stata effettuata.
