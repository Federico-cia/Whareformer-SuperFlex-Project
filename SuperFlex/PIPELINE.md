# Pipeline e memoria autonome

Il pacchetto elabora RGB e maschere già disponibili, con DA oppure MoGE e SuperFlex robust congelato. Non scarica dati, pesi o repository; non contiene le reti degli autori. Il mapping alle detection Whareformer resta non verificato.

## Avvio

```bash
pip install -e './SuperFlex[images]'
python -m unittest discover -s SuperFlex/tests
python SuperFlex/examples/memory_demo.py
```

Il terzo comando è un esempio sintetico completamente eseguibile su CPU. Le associazioni mostrate sono illustrative; non sono predizioni di tracking.

Per dati reali, adattare `examples/observations_input.json` e `examples/pipeline_config.json`. I percorsi dei dati sono relativi al manifest, quelli dei pesi al file di configurazione. Ogni osservazione richiede chiave univoca, video, indice temporale intero, RGB, maschera binaria mono-canale e categoria. `intrinsics=[fx,fy,cx,cy]` serve per DA e deve corrispondere alla risoluzione dell'RGB. RGB e maschera devono avere esattamente la stessa risoluzione; nessun ridimensionamento implicito. Più oggetti possono riferirsi allo stesso RGB, inferito una sola volta.

Usare gli ambienti degli autori già funzionanti, con questo `src` in `PYTHONPATH`: DA richiede Torch/Transformers/Pillow, MoGE il repository MoGE-2 e le sue dipendenze, SuperFlex il repository degli autori con OmegaConf e le estensioni CUDA già compilate. Il nucleo richiede le versioni in `pyproject.toml`. Per le reti sono stati riusati gli ambienti HPC esistenti; non si promette compatibilità con tutte le combinazioni di CUDA/Torch. Le versioni effettive e gli hash dei sorgenti sono registrati nella verifica della consegna.

Eseguire sotto SLURM, nei rispettivi ambienti:

```bash
python -m shape_tools.pipeline da --manifest observations.json --config config.json --output run
python -m shape_tools.pipeline moge --manifest observations.json --config config.json --output run
python -m shape_tools.pipeline clouds --manifest observations.json --config config.json --output run
python -m shape_tools.pipeline superflex --manifest observations.json --config config.json --output run
python -m shape_tools.pipeline export --manifest observations.json --config config.json --output run
```

`examples/run_pipeline.sbatch` coordina entrambi i rami; impostare le variabili indicate e le opzioni della propria coda. Per un solo ramo, usare `sources=["da"]` oppure `["moge"]` ed omettere lo stadio neurale non selezionato. `pixel_policy="common"` usa gli stessi pixel validi nei rami richiesti; `"source"` usa i pixel validi di ciascuno e non definisce un confronto appaiato sullo stesso supporto. Il controllo scientifico corrente usa `common`.

DA usa il processor della revisione fissata, RGB in [0,1], interpolazione bicubica della profondità e clamp a zero. MoGE usa le impostazioni esplicite nel JSON. Nessun allineamento a mesh di scena è necessario. I punti sono camera-frame, X destra/Y basso/Z avanti; la scala stimata non è accuratezza metrica certificata. SuperFlex usa 4096 punti, seed 42, campionamento con rimpiazzo soltanto sotto 4096 punti, centratura e scala degli autori. L'orientamento non è canonicalizzato. Soglia di esistenza 0.5 e risoluzione mesh 30 restano quelle del percorso già usato.

## Ripresa, errori e provenienza

Ripetere gli stessi comandi nello stesso output riusa risultati e fallimenti registrati, verificando gli hash degli artefatti. Un cambiamento di input/configurazione/codice blocca la ripresa: usare una nuova directory. Per riprovare un fallimento transitorio usare una nuova directory; non cancellare selettivamente fallimenti dal confronto scientifico. I processi devono essere sequenziali: non lanciare due scrittori nella stessa directory. Un'interruzione prima del report di un elemento può ripeterne il calcolo, senza riusare file parziali come successi.

La provenienza comprende RGB, maschera, configurazione, codice locale, checkpoint SuperFlex/MoGE, revisione immutabile DA, sorgenti Python del backend e versioni Torch/CUDA. Conservare anche il manifest dei pacchetti dell'ambiente e le revisioni dei repository esterni. I file `run.json` contengono percorsi assoluti operativi: sono artefatti locali, da ripulire prima di condividere. I report per elemento distinguono successo/fallimento e registrano tempo e memoria GPU. Un job completato può contenere osservazioni fallite: controllare `observations.json`, non soltanto il codice d'uscita SLURM.

## Contratto d'uscita

`run/observations.json` contiene una riga per osservazione, anche con forme mancanti. `representations` espone punti e SuperFlex per ciascuna sorgente, con `status`, percorso relativo a `run`, SHA-256, firma dello stadio ed eventuale motivo di indisponibilità. I parametri di forma sono separati in `shape_parameters.npz` (scale, rotation, translation, exponents, exist, tapering, bending; tutti i 16 slot). `prediction.npz` conserva l'output diagnostico completo degli autori, incluso input/assegnazioni. Le mesh e le normalizzazioni restano disponibili. `detection_idx=null` e `detection_mapping_status="unverified"` sono intenzionali.

```bash
shape-tools compare run/observations.json --root run --output distances.csv
shape-tools evaluate distances.csv identity_review.csv --output separation.json
python -m shape_tools.report --observations run/observations.json --distances distances.csv --review identity_review.csv --output report --plot
```

Per le figure installare l'extra `reports`. Non ricalcolare le coppie storiche: usare il CSV già consegnato. `evaluate` mantiene separate le etichette visivamente verificate; non le ricava dalla geometria.

## Memoria candidata

`ShapeMemory(video, MemoryConfig(representation, capacity=1, metric="d2", reduction="minimum"))` accetta anche spettro di covarianza e riduzione media. La regola è FIFO sulle ultime forme valide; una forma mancante conserva quelle precedenti. Non fonde nuvole e non media parametri di primitive. Capacità e riduzione sono opzioni implementate, non iperparametri validati.

Caricare le feature con `observation_features(row, root, config.representation)`, che controlla percorso e hash, poi passare la mappa chiave→feature a `score(video, frame_index, observations, track_ids)`. Si ottengono distanze, maschera `valid`, ordine di righe/colonne ed evidenza delle osservazioni passate consultate. Solo dopo l'associazione del tracker chiamare `commit({observation_key: track_id})`; le associazioni devono essere uno-a-uno. `abort()` annulla la transazione; `forget(track_id)` rimuove una track terminata.

Usare una memoria distinta per video, sorgente/rappresentazione e configurazione dei descrittori. Passare solo i candidati ammessi dal tracker. `NaN` con `valid=False` significa contributo geometrico indisponibile: il chiamante deve lasciare il segnale baseline neutro, senza trasformarlo in distanza zero favorevole. Anche con D2 la forma può essere instabile o non discriminativa. Il modulo non altera logits, non crea identità, non decide New Track e non prova equivalenza alla baseline a peso zero.

## Dati e condizioni d'uso

RGB, maschere, pesi e copie degli autori restano esterni a Git. VISOR: [formato e licenza degli autori](https://github.com/epic-kitchens/VISOR-VIS); usare le citazioni EPIC-KITCHENS e VISOR e rispettare CC BY-NC 4.0 delle annotazioni. Per reti, pesi e altri dati valgono le licenze delle rispettive fonti. La disponibilità di questo adattatore non modifica tali condizioni.
