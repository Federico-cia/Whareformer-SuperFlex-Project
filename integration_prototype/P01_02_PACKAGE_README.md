# P01_02: generazione geometrica DA e SuperFlex

Pacchetto per Linux/Slurm. Marco elabora P01_01; il destinatario elabora P01_02.
DA su tutte le osservazioni; MoGE escluso dalla produzione. Nessun training o
tracking. Codice e checkpoint SuperFlex robust inclusi con hash; DA viene
scaricato alla revisione fissata. Dati ufficiali P01_02 **non inclusi**.

La variante per GitHub contiene gli stessi script e sorgenti ma esclude i pesi:
`setup.sh` li scarica dalla cartella ufficiale robust tramite
`download_superflex.py` e richiede gli stessi hash. Pubblicare la cartella
leggera in `tools/p01_02_hpc/`, non lo ZIP completo con pesi. Nella variante
leggera `SHA256SUMS` copre solo i file effettivamente inclusi.

## 1. Installazione e dati

Estrarre lo ZIP in una directory persistente, accessibile anche dai compute node.
Evitare spazi nel percorso del pacchetto. Non cambiare posizione dopo `prepare`.
Verificare lo ZIP sul PC con l'hash comunicato da Marco; poi:

```bash
cd p01_02_da_hpc_v1
python3 full_video_enrichment.py verify
cp settings.example.json settings.json
```

Servono conda, compilatore C++ e toolkit CUDA compatibili con PyTorch 2.6/cu124
per l'estensione SuperFlex, Ninja e rendering offscreen EGL. Caricare i moduli
del proprio centro PRIMA dell'installazione e dei job. `setup.sh` propone due
ambienti separati (DA Python 3.13, SuperFlex Python 3.11), con versioni esplicite; non è stato eseguito sul computer del
destinatario. Gli snapshot storici ripuliti sono in `reference_environment/`;
non attestano identità completa con il nuovo ambiente. Il pilota GPU è necessario.

```bash
bash setup.sh
```

Il download DA usa la cache Hugging Face: mantenere lo stesso `HF_HOME` fra
installazione e job. Le inferenze sono offline. Se il centro richiede un proprio
PyOpenGL/OSMesa, adeguare installazione e `PYOPENGL_PLATFORM`; conservare le
versioni effettive e rifare il pilota. Nessuna credenziale è inclusa o richiesta
dagli script del pacchetto.

Procurarsi questi input **tutti relativi a P01_02**, nelle posizioni indicate in
`settings.json` oppure modificare quei percorsi:

| File | Contenuto richiesto |
|---|---|
| `data/P01_02/frames.json` | Lista originale ordinata `[{"frame":"frame_0000000001","annotations":[{"id":1,"name":"...","bounding_box":[x0,y0,x1,y1]}]}]`; mantenere l'ordine originale delle detection, non ordinare per categoria/ID e non derivarlo dai risultati del tracker. Bounding box nel riferimento VISOR 854×480. È il contratto già usato dal bundle P01_01. |
| `data/P01_02/annotations.zip` | ZIP ufficiale VISOR con un JSON `video_annotations`; segmenti poligonali nel riferimento 854×480. |
| `data/mappings.json` | Mapping VISOR→RGB: `{"P01_02":{"P01_02_frame_0000000001.jpg":"frame_0000000001.jpg"}}`. Usare il mapping ufficiale effettivo, non assumere indici uguali. |
| `data/P01_02/fields.json` | EPIC-Fields: `camera.width`, `camera.height`, `camera.params=[fx,fy,cx,cy]`, modello PINHOLE; `images` mappa nomi JPEG a pose COLMAP `[qw,qx,qy,qz,tx,ty,tz]`. |
| `data/P01_02/P01_02.tar` | Archivio RGB ufficiale dello stesso video, con nomi JPEG compatibili col mapping. |
| `data/P01_02/mesh.ply` | Mesh di scena nello stesso riferimento e scala delle pose EPIC-Fields; non mesh dell'oggetto o di P01_01. |

Non sono disponibili qui gli input P01_02 verificati: non sostituirli con quelli
del video 1. `fetch_asset.py URL DEST --sha256 HASH` consente download con checksum
atteso, quando si dispone del riferimento ufficiale e del relativo hash. Fonti:
[EPIC-KITCHENS](https://epic-kitchens.github.io/),
[VISOR](https://epic-kitchens.github.io/VISOR/),
[EPIC-Fields](https://epic-kitchens.github.io/epic-fields/).
Feature DINO/PCA, XYZ precalcolati e checkpoint Whareformer non servono alla sola
generazione; serviranno per il collegamento e la valutazione del tracker.

## 2. Quota e preparazione

`quota_site.py` riconosce l'HPC originale (myquota/BeeGFS pool_home). Su un centro
diverso sostituire `quota_command` in settings con un comando che restituisca
SOLO JSON `{"free_bytes":12345678900,"free_files":123456}` della **quota personale**,
non dello spazio globale. In assenza di quota leggibile la produzione si ferma.
Riserva iniziale 2 GiB/12000 file, modificabile in settings; non garantisce che
un blocco arbitrario vi rientri. Nessuna pulizia automatica degli artefatti.

Impostare account, partizione ed eventuale modello GPU richiesti dal proprio
centro; nessun account personale è precompilato:

```bash
export CV_ACCOUNT=il_proprio_account  # omettere se non richiesto
export CV_PARTITION=la_propria_partizione
export CV_RAM=24G
export CV_TIME=02:00:00
export CV_GRES=gpu:1
bash submit.sh prepare
```

`prepare` estrae solo i JPEG richiesti, verifica ID/nome/bbox, risoluzione,
maschere e pose, conserva alias temporali, mancanti e conflitti; genera manifest
e blocchi da 512. Non contiene riuso delle 446 geometrie del video 1. Verificare
`work/P01_02/coverage.json` prima del pilota. Gli hash bloccano riprese con
input/configurazione/codice cambiati: usare un nuovo task in quel caso.
Non avviare due preparazioni o due job sullo stesso task contemporaneamente.

## 3. Pilota, produzione e ripresa

Per una prova piccola impostare `batch_size=8` PRIMA di prepare; mantenerlo poi
immutato nello stesso task. Per blocchi 512 creare un nuovo task e rifare prepare.

```bash
bash submit.sh pilot
```

Il pilota elabora il blocco 0: preflight CUDA/pesi/Ninja, DA, punti osservati,
SuperFlex grezzo, allineamento alla scena, SuperFlex allineato, esportazione.
Non invia automaticamente la produzione. Prima di continuare verificare log,
stati per osservazione, riproiezione/sovrapposizione alla scena e spazio/inode
consumati. Confrontare anche poche osservazioni P01_01 note su task separato
fornito da Marco: il pacchetto non contiene tale fixture reale né dichiara
equivalenza numerica fra HPC già dimostrata.

```bash
bash submit.sh production
```

Un solo job, blocchi sequenziali, nessun auto-invio di successori. Se termina il
tempo Slurm o si esaurisce la riserva, conservare i risultati e reinviare lo
stesso comando dopo aver verificato la coda: gli stadi riusano la cache firmata.
Un blocco interrotto prima dell'indice finale viene ricalcolato usando le cache
disponibili. Un lock `block_XXXX.lock` evita due scrittori: dopo un kill Slurm
rimuoverlo solo quando il relativo job è certamente terminato. Le inferenze
fallite già registrate restano tali; per riprovarle usare task separato, senza
cancellare selettivamente fallimenti dal confronto.

Per evitare sprechi di tempo, dimensionare durata/numero blocchi in base al
pilota. Non si promette che il video completo entri in quota o in un singolo job.
La produzione conserva gli intermedi: compattazione/cancellazione non fanno
parte di questa consegna. Il completamento HPC non implica copertura riuscita.

## 4. Output da restituire a Marco

`work/P01_02/all_geometry.json` e `final_status.json` separano completamenti,
fallimenti e blocchi ancora mancanti. Ogni osservazione ha video/frame,
detection_idx verificato nel join, annotation_id (non nuova identità fisica),
camera/pose, hash RGB/maschera e flag alias.

- `geometry/XXXX`: nuvole DA **grezze**, colori/pixel, input e parametri
  SuperFlex, diagnostiche e `reconstruction.ply`.
- `aligned/XXXX`: nuvole osservate allineate, coordinate world e c2w,
  alpha/beta, numero di pixel statici, hash mesh; SuperFlex e mesh calcolati
  dalle nuvole allineate. I punti world sono in unità EPIC-Fields, non metri
  fisicamente certificati. Gli output camera restano X destra/Y basso/Z avanti.
- `completed/XXXX.json`: distingue `representations` grezze e
  `aligned_representations` (`da_aligned_points`, `da_aligned_superflex`).

Allineamento affine via minimi quadrati sul background, esclusa l'unione delle
maschere delle osservazioni originali del frame, con le funzioni camera/render
degli autori Whareformer. Maschere originali incomplete, fit degenere o pendenza/
profondità non positive impediscono l'allineamento: mai sostituirlo con DA grezzo.
Le guardie sono controlli operativi del progetto, non criteri appresi di fusione.
Non si esegue fusione/memoria/tracking né si certifica correttezza geometrica.
SuperFlex completa la forma: le sue mesh non sostituiscono i punti osservati.

A produzione finita, dal pacchetto:

```bash
envs/sf/bin/python full_video_enrichment.py deliver --settings settings.json
```

Produce `work/P01_02/P01_02_geometry.tar.gz`: indice portabile, artefatti
verificati con hash, configurazione scientifica, copertura e checksum. Lo spazio
per questa copia va previsto; il comando non elimina originali. Conservare e
passare separatamente anche log e ricevute di ambiente, controllando eventuali
percorsi personali. L'archivio non contiene RGB né pesi. Conservare gli input
originali fino alla verifica del destinatario.

## Verifiche già eseguite e limiti

Sette test locali superati: driver con dipendenze controllate, fit affine
sintetico e generazione/esportazione DA-only reale da profondità sintetiche;
compilazione sintattica e checksum del pacchetto. Nessuna inferenza CUDA,
installazione Linux, rendering EGL o elaborazione reale P01_02 eseguiti in questa
preparazione. Per testare nuovamente: `python -m unittest test_full_video_enrichment`.
Lo stesso seed non garantisce uguaglianza bit per bit su GPU/ambienti diversi;
concordare tolleranze numeriche per il controllo comune. P01_02 condivide il
partecipante P01: non dichiararlo automaticamente test indipendente.

Codici degli autori e checkpoint restano soggetti alle rispettive licenze;
licenze incluse in authors. Fonti SuperFlex: repository ufficiale
https://github.com/gabrieltavernini/superflex .
