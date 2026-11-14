# Passaggio di consegne AI — 14 novembre 2026

Questa guida è il punto di ingresso aggiornato per continuare con qualsiasi provider AI. Non serve la cronologia della chat. Le ultime decisioni esplicite di Marco prevalgono sulle note storiche; i resoconti conservano anche stati intermedi superati. La pubblicazione non certifica che una nuova macchina abbia dati, pesi e ambienti necessari.

## Ordine di lettura

1. Questa guida, ISTRUZIONI_SUPERVISORE_SCIENTIFICO.md, STATO_LAVORO.md, TODO.md e ultime voci di REGISTRO_DECISIONI.md.
2. ROADMAP_CICLO_GEOMETRICO.md e INTEGRAZIONE_DISCUSSIONE.md per il metodo; FRONTEND_AVANZAMENTO_20261114.md e PIANO_FRONTEND_UNIFICATO_20261114.md per lo step attivo.
3. COMPLETAMENTO_PIPELINE_20261114.md, RIPRESA_HPC_20261114.md e i resoconti dei moduli per prove e limiti.
4. Codice integration_prototype/ e relativa README; mappa_interattiva/README.md per modificare la mappa.

Nella cartella locale questa guida e i documenti sono alla radice di `lavoro di gruppo`. Su GitHub sono in `context/memory/`; il punto di ingresso della repository è START_HERE.md. Codice e mappa sono rispettivamente `integration_prototype/` e `mappa_interattiva/` alla radice GitHub. I richiami storici a `../outputs`, `shared_exports` o percorsi HPC indicano archivi esterni al clone, non file garantiti nel repository. Gli estratti pubblicati sono in `context/evidence/` con inventario SHA-256.

## Obiettivo approvato e ciclo causale

Verificare se la forma 3D migliori l'associazione oggetto del frame → track di Whareformer, mantenendo baseline aspetto/XYZ. I due contributi sono parti dello stesso ciclo: forma dell'osservazione → confronto con memoria precedente → associazione Whareformer → registrazione/accumulo dei punti osservati ammessi → SuperFlex → memoria per i frame futuri. Tutte le detection dello stesso frame interrogano la stessa memoria precedente, prima degli aggiornamenti. Le completazioni predette non vengono aggiunte ai punti osservati.

DA e MoGE restano percorsi distinti; distinguere coordinate camera della forma e coordinate scena della baseline. Reti preaddestrate congelate, nessun training da zero. SuperFlex dopo ogni aggiornamento geometrico ammesso, inizializzazione compresa, senza politica a intervalli. Controlli con punti e con forme; nessun beneficio di tracking ancora dimostrato. Non usare track predette, categorie o ID di annotazione come GT fisica persistente certificata.

## Stato del codice effettivo

- shape_adapter.py e geometry_matcher.py: confronto causale, correzione dei logits e wrapper che riusa inferenza/softmax/greedy originali; modalità disabilitata/diagnostica/attiva e controllo peso zero.
- frame_coordinator.py: associazioni effettive, query prima del commit, nuova istanza per video. Errori del tracker richiedono ripartenza con istanza nuova; non esiste rollback generale o checkpoint completo.
- cloud_memory.py e cloud_updater.py: registrazione candidata PCA/multistart/ICP, memoria limitata dei soli punti osservati, provenienza/versioni; rifiuti ed errori preservano la geometria valida.
- deferred_superflex.py: richieste e risultati legati a hash/versioni, worker reale tramite shape_tools.pipeline.superflex; pausa e replay seriale con cache. Risultati dei test distinti da produzione, nessuna importazione retroattiva.
- experiment_runner.py e run_experiments.py: W0, G0, S-separata, S-accumulo, P-accumulo, tracker indipendenti; costi/replay/provenienza, budget geometrici confrontabili. L'esempio a nove configurazioni usa pesi zero, non parametri calibrati.
- tracking_evaluation.py, evaluate_experiments.py, summarize_experiments.py: IDF1/mPCL originali verificati via sorgente, scope dichiarato, export/hash, tabelle senza aggregare provenienze incompatibili. Risultati parziali non vengono valutati come completi.
- run_pipeline.py: comando input preparati → inferenza → valutazione → tabella, con errori e attese espliciti. Accetta alternativamente --root o --frontend-manifest.
- frontend_inputs.py: manifest e import di cache verificata. Pilota reale: dieci detection in tre frame, storia completa di 3398 frame preservata; quattro file dati byte-identici. NON è ancora un estrattore neurale completo da RGB.

## Risultati consolidati, non job da rilanciare

| Job HPC | Esito acquisito | Significato |
|---|---|---|
| 761899 | COMPLETED, 11m35s | Prefisso 3398 frame/10264 osservazioni, quattro rappresentazioni, zero mismatch registrati |
| 761905 | COMPLETED, 20s | IDF1 baseline registrata riprodotto |
| 763322 | COMPLETED, 9m56s | Controllo zero aggiornato esatto |
| 763323 | COMPLETED, 12m11s | 12 inizializzazioni, 12 rifiuti, zero fusioni su quattro rappresentazioni |
| 763324 | COMPLETED 0:0, 43m30s | Sei ricostruzioni SuperFlex reali ready, controllo zero esatto; nessuna fusione multivista |
| 763498 | COMPLETED 0:0, 33s | Otto test valutatore e metriche full-video riprodotte |
| 763530 | COMPLETED 0:0, 45s | 69 test tutti eseguiti e passati |
| 763531 | COMPLETED 0:0, 23m24s | Nove varianti zero completate e valutate, tutte zero_baseline_exact |

Ultima suite locale: 72 casi, 70 passati e due saltati per motmetrics non disponibile localmente. I tre nuovi test frontend non sono stati eseguiti su HPC. Nessun nuovo job frontend. Gli stati RUNNING/attesa di questi job nei vecchi paragrafi sono storici; nessuna interrogazione nuova della coda effettuata per questa consegna.

Le 12 inizializzazioni del 763323 sono tre osservazioni ripetute nelle quattro rappresentazioni: tagliere/track 4/frame 2893, coltello/track 6/frame 5099, padella/track 9/frame 7508. Tre successive osservazioni candidate (tagliere 5099 e 7508, coltello 7508), ciascuna nelle quattro rappresentazioni, sono state respinte dai filtri. Associazione e fusione sono stadi distinti; nessuna fusione non implica associazione fallita. Le sei ricostruzioni del 763324 provengono da inizializzazioni a vista singola.

Baseline completa registrata P01_01 train: 52 track, 110590 osservazioni, 33310 frame; IDF1 73.2697350574193%, mPCL circa 70.46550449586455%. Non sono risultati del metodo migliorato né di test held-out. Valutazione originale raggruppa per nome oggetto e usa XYZ stimati; non è una GT fisica indipendente. Il mPCL originale contiene 145 scale con non supportate a zero: un prefisso diagnostico non si confronta con il full-video. Media sulle sole scale supportate separata come diagnostica.

Join collega: 71/73 geometrie verificate esattamente, 146 hash delle nuvole; due alias VISOR/RGB esclusi (22583→22584, 40873→40874) in attesa di provenienza JPEG. Non confondere annotation_index con detection_idx: diversi in 69/71 casi verificati. Report/input completi del collega sono già nella repository in Whareformer/; non sono più una dipendenza mancante.

## Decisioni da rispettare

**Filtri di fusione: revisione richiesta ma esplicitamente RINVIATA da Marco.** Non cambiare soglie o registratore, non aggirare i rifiuti per ottenere fusioni. Gate numerici provvisori scelti dall'assistente, non prescritti dai paper né calibrati. Supporto bidirezionale e ambiguità possono penalizzare viste parziali e simmetrie. Dettaglio in RIPRESA_HPC_20261114.md e audit pubblicato. La diagnosi non prova associazioni errate o impossibilità fisica della fusione.

Il piano frontend ha ricevuto l'ok: non chiedere di nuovo approvazione per proseguirlo nel suo perimetro. È parzialmente eseguito, non completo. La calibrazione estesa e la matrice di metodi sono roadmap successiva; non avviarle implicitamente durante la consegna o la revisione rinviata dei filtri. Cambi di domanda/dataset/protocollo o conclusioni principali richiedono decisione di Marco.

Mappa: contenuti.json è la fonte, contenuti.js la copia offline. Preservare le modifiche manuali B01/B02/B03 ed E01/E02/E03; non rigenerarla dai Markdown. Le parentesi quadre nei testi di Marco chiedono completamento. SAM 2 è solo esempio da valutare, non scelta implementata. Testi comprensibili anche alla giuria. Editor salva nodi e collegamenti tramite servizio locale con backup/conflitti; nessuna sincronizzazione automatica con la memoria Markdown.

## Prossimo lavoro concreto

1. Leggere l'inventario frontend e gli estrattori originali. Identificare pesi/revisione DINOv2 compatibili, provenienza della PCA preaddestrata, asset/convenzione scala della scena e ambiente di estrazione. La PCA locale esiste ma il legame alle feature ufficiali non è certificato. fields.json/mesh.ply presenti su HPC; una ricerca limitata in tre directory non prova assenza globale degli altri asset.
2. Implementare e verificare il ramo rigenerato sul piccolo pilota approvato (P01_01, frame 2893/5099/7508), mantenendo la storia del tracker. Niente sostituzione silenziosa di modelli, fit PCA o MVS implicito. Il riuso della cache non certifica la provenienza del JPEG delle vecchie feature.
3. Dopo il completamento frontend, estendere copertura e confronti/calibrazione secondo roadmap e split espliciti. La revisione dei filtri resta separatamente rinviata finché Marco non la riattiva.

Due persone, circa due ore al giorno ciascuna; scadenza 23 novembre. Marco geometria, collega tracking. Non ripetere job costosi già conclusi per ricostruire il contesto.

## File, ambienti e riproduzione

GitHub: https://github.com/Federico-cia/Whareformer-SuperFlex-Project . La consegna aggiorna main a partire dal commit collega fc5aa30, senza riscrivere la storia. START_HERE.md distingue guida, codice, evidenze e materiali esterni.

Sorgente autori Whareformer: https://github.com/jacobchalk/Whareformer, commit 82dd349957e1f04f92a2979b4c92c2f3fed445c5. I test estraggono metodi originali da `<radice>/Whareformer-repo/src`: occorre predisporre questa copia alla versione indicata (non la cartella Whareformer/ del collega). Inventario con hash in context/manifests/ sul remoto, manifests/ localmente. Il bundle numerico contiene le proprie dipendenze original_src per il runner; non è un insieme di soli dieci oggetti isolati.

Dipendenze secondo percorso: NumPy/SciPy/trimesh/Pillow per nucleo e test; PyTorch/PyYAML/pandas/motmetrics/xmltodict per tracking/metriche; ambienti originali e checkpoint per inferenze. Ambiente locale esistente shared_exports/code_review_env/Scripts/python.exe: mancano Torch/pandas/motmetrics/PyYAML. Ambiente HPC verificato cv-superflex: Torch 2.6.0+cu124, NumPy 1.26; motmetrics 1.4.0 e xmltodict 0.14.2 forniti separatamente nei job. Non assumere che un clone installi automaticamente tutto.

Da clone GitHub, con dipendenze e sorgenti predisposti:

```powershell
$env:PYTHONPATH = (Resolve-Path 'SuperFlex/src').Path
python -m unittest discover -s integration_prototype -p 'test_*.py' -v
python integration_prototype/run_pipeline.py --root <bundle_verificato> --config integration_prototype/variants_zero.example.json --output <nuovo_output> --cache <cache_dedicata> --policy integration_prototype/evaluation_prefix.example.json
# Alternativa al --root: --frontend-manifest <manifest.json>
# Worker reale opzionale: --superflex-runtime <config_runtime.json>
```

Nella cartella di lavoro locale PYTHONPATH è shared_exports/publish_candidate/SuperFlex/src. In assenza di risultati SuperFlex il runner si arresta in attesa; non trasformare una pausa in successo. Output nuovi, non sovrascrivere run. Percorsi assoluti nei manifest vanno predisposti sulla nuova macchina e rivalidati, non sostituiti mantenendo vecchi hash.

Asset esclusi dalla nuova pubblicazione: RGB/maschere/input numerici grandi, pesi, sorgenti degli autori e credenziali. Il pacchetto compare200 precedentemente autorizzato resta in SuperFlex/data_packages/compare200; non equivale al bundle completo del prefisso. Localmente: data/compare200/P01_01/ready, data/whareformer_official_P01_01_v2, outputs/frontend_20261114/bundle_v2, outputs/ e shared_exports/ per archivio e runtime. Gli estratti numerici pubblicati permettono audit dei risultati, non sostituiscono gli input delle reti. Per migrare il calcolo occorre accesso agli asset locali/HPC o acquisizione dalle fonti originali.

Checkpoint tracking SHA-256: 5b2e6692461f837ec662d0ac75a5f8c08e4fa9778e5c1b9833598cf90a58ee1d.
SuperFlex robust verificato: ~/cv_project/SuperFlex-repo/robust/ckpt.pt, SHA-256 5bd1ba9818dc7322400d4234262d47500b05fb40bad3b0edc1e6b8847833b842; config ff468f8baaec1622db6cd26edae26ec32c7c8c828b95a0012811078f51b031bf. Non usare il diverso checkpoint trovato in external/superflex_unsup_robust. Gli hash non sostituiscono pesi/accessi.

Aggiornare autonomamente memoria, decisioni e attività dopo novità rilevanti, in italiano; non salvare chiavi/token o conversazione informale. Conservare storia e limiti. Questa consegna documentale non introduce nuovi risultati scientifici.
