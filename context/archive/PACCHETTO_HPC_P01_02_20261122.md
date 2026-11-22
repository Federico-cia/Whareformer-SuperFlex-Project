# Consegna HPC P01_02 — 22 novembre 2026

## Esecuzione

Richiesta di Marco: adeguare il driver e preparare gli script per il compagno su P01_02; successivamente proposta la condivisione tramite repo. Nuovo driver corrente `integration_prototype/full_video_enrichment.py`, allineamento separato `align_video_scene.py`, sette test e guida `P01_02_PACKAGE_README.md`. Il driver storico `full_p01_enrichment.py` resta conservato per le cache firmate P01_01 e non viene distribuito come ingresso P01_02. Nessuna modifica ai file runtime dell'HPC.

Implementati parametri video/percorsi/ambienti, acquisizione da archivio ufficiale fornito, join originale ID/nome/bbox, manifest e hash, DA-only con pixel_policy=source, blocchi sequenziali, guard quota e lock per blocco, cache e aggregazione senza geometrie pregresse P01_01, esportazione portabile verificata. Nessun auto-invio di successori. Allineamento affine del background con renderer/pose originali Whareformer estratti senza modifiche; guardie operative e fallimento esplicito senza fallback grezzo. SuperFlex applicato separatamente a grezzo/allineato; world points e trasformazioni conservati, nessuna fusione o training.

## Pacchetti

- `shared_exports/p01_02_da_hpc_v1.zip`: script, runtime congelato della campagna, sorgenti degli autori, checkpoint/config SuperFlex robust verificati, installazione proposta e guida. DA scaricato a revisione fissata; dati P01_02 esterni.
- `shared_exports/p01_02_da_hpc_repo_v1.zip`: versione leggera con struttura `tools/p01_02_hpc/`, senza pesi/dati/ambienti/accessi; download SuperFlex dalla cartella ufficiale robust con verifica dei due hash. Cartella non compressa omonima disponibile. Nessun push o invio eseguito.

Dimensioni e SHA-256 esatti: `outputs/p01_02_package_validation/verification.json`.

## Verifiche effettive e limiti

Sette test superati nel sorgente e ripetuti nel pacchetto: parser/troncamenti, selezione DA-only e hash checkpoint, ambienti/PATH Ninja, quota, aggregazione di mancanti/fallimenti, fit affine sintetico e generazione/esportazione concreta di 64 punti da profondita sintetica senza file MoGE. Verificati entrambi i manifest SHA256SUMS, CRC ZIP, sintassi di tutte le sorgenti Python negli archivi e assenza di pesi nella versione repo. Ricerca delimitata su script/config/testi della versione repo senza riscontri per utente HPC storico, nome utente locale, password, chiavi private o pattern token GitHub; non e una garanzia assoluta di assenza di dati sensibili.

Nessuna installazione Linux, compilazione CUDA, inferenza neurale, rendering EGL, accesso HPC, trasferimento, pubblicazione o prova reale P01_02. Setup con versioni esplicite e snapshot storici ripuliti, ma ambiente del destinatario non validato. Mancano input ufficiali P01_02 verificati e risorse/account del compagno; il pilota reale e il controllo comune restano necessari. Il pacchetto non e autonomo rispetto ai dati e non attesta capacita sufficiente. Conservazione completa degli intermedi, nessuna compattazione/cancellazione implicita. Se si interrompe Slurm puo restare un lock da rimuovere solo dopo aver verificato che il job sia terminato. Nessuna modifica della mappa o dei criteri appresi di ammissione.
