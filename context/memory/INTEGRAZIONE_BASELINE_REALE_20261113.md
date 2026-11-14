# Collegamento alla baseline reale — 13 novembre 2026

## HPC ripristinato, arretrati inviati — 14 novembre

SSH/accounting/coda accessibili. Recuperati 761899 (prefisso storico a peso zero esatto, 3398 frame/10264 detection, zero differenze dal collega) e 761905 (IDF1 73.2697% sulle predizioni registrate train, non test). Nuovi job: 763321 COMPLETED/0:0, 50 test ambiente passati; 763322 replica aggiornata e 763323 accumulo RUNNING nell’ultima osservazione; 763324 SuperFlex differita PENDING per dipendenza dai due CPU. Nessun nuovo esito sperimentale ancora dichiarato; prossima acquisizione dei risultati. [RIPRESA_HPC_20261114.md](RIPRESA_HPC_20261114.md). Le note precedenti sul blocco DNS e sui due esiti ancora da leggere sono storiche.

Mandato di Marco: procedere dopo la ricezione dei manifest. Durante l'avvio è arrivato anche il commit `fc5aa30`, con README della run, configurazione effettiva, patch Windows e `results.csv`. Nessun push o modifica al lavoro del collega.

## Provenienza ora disponibile

- Codice dichiarato: Whareformer `82dd349957e1f04f92a2979b4c92c2f3fed445c5`. Otto sorgenti di modello/matcher/tracker/memoria confrontati con quel commit via GitHub, identici dopo normalizzazione LF. Verificati anche `utils/config.py` e l'evaluator per i controlli successivi. Le patch launcher Windows sono documentate dal collega e non necessarie al runner isolato HPC.
- Checkpoint locale individuato in `Whareformer-repo/Starting_checkpoint_whareformer/whareformer.pt`; SHA-256 `5b2e6692461f837ec662d0ac75a5f8c08e4fa9778e5c1b9833598cf90a58ee1d`, identico a quello dichiarato. La precedente ricerca mirata non aveva individuato questo nome/percorso: non era prova di assenza generale del peso.
- Configurazione effettiva: inferenza CPU, PCA 256, DenStream per aspetto, finestra recente per posizione, P01_01 nel train, architettura hidden 64/depth 1/heads 32. Nessun training. Snapshot con hash in `outputs/github_handoff_fc5aa30/`.
- Il CSV ha 145 righe; verificata l'identità `PCL=100*correct/total` con errore massimo circa 1.42e-14. La media secondo il codice ufficiale sul singolo video è **70.4655% mPCL**. Non prestazione held-out, replica del benchmark completo o risultato della forma.

## Recupero indipendente degli input

Il collegamento ufficiale alle feature è accessibile senza nuovi accessi utente. Individuato l'archivio `epic_osnom.tar.gz` da 3.53 GB. Non salvato l'archivio intero: lettura gzip in streaming e conservazione dei soli tre file P01_01. Prima prova limitata a 300 MiB fermata prima del video richiesto; conservata in `data/whareformer_official_P01_01_v1/acquisition.json`. Una lettura iniziale separata di un MiB ha verificato l'ordine dell'archivio, che inizia da altri video.

Seconda acquisizione completata in circa 435 s, letti circa 2.10 GB compressi fino ai file richiesti; salvati circa 131 MB di annotazioni, feature PCA-256 e XYZ allineati, con hash. Percorso `data/whareformer_official_P01_01_v2/`, inventario `acquisition.json`. Sessione anonima di download non salvata. Dati e checkpoint non pubblicati.

**Audit completo degli input:** 33310 frame/110590 osservazioni; dimensioni, valori finiti, ordine e corrispondenza ID/categoria/box/XYZ contro l'export del collega verificati, zero differenze. Eseguito anche `audit_tracking_contract.py` con le annotazioni originali: passato, ordine delle annotazioni controllato. Le feature rilasciate confermano il dato preestratto, non il JPEG originariamente usato per ciascuna feature; i due alias temporali restano separati.

## Primo controllo con checkpoint reale

Job CPU **761872 COMPLETED/0:0**, 28 s. Con input controllati, 120 casi: logits a peso geometrico zero identici, softmax PyTorch identica e assegnazione greedy originale identica. Scarto massimo logits zero; percorso attivo esercitato senza metriche di tracking. Risultato `outputs/pretrained_zero_761872/result.json`; remoto `~/cv_project/pretrained_zero_v1/result.json`, log `zero_whare_761872.out/.err`.

Questo controllo usa il modello e i pesi reali ma non le feature del video, quindi non è la riproduzione della baseline P01_01.

## Replica con feature originali e memoria geometrica

Preparato un prefisso completo dall'inizio dei dati fino al frame 7508: **3398 frame con osservazioni, 10264 detection**. Mantiene la storia necessaria ai tre frame geometrici 2893/5099/7508; ripartire soltanto da quei tre avrebbe cambiato la baseline. Sei osservazioni geometriche, 24 artefatti punti/SuperFlex DA/MoGE letti con hash. Nessuna nuova inferenza di profondità o SuperFlex.

Runner `integration_prototype/run_real_prefix.py`: un tracker originale e quattro copie con adattatore a peso zero, rappresentazioni separate e memoria aggiornata dopo le associazioni prodotte da ciascuna copia. Nessun forcing delle track del collega e nessuna etichetta oracle. Logits e assegnazioni comparati frame per frame; il confronto con l'export del collega viene misurato separatamente. Feature originali, non fixture. Mancanti senza correzione diretta; due alias fuori dal prefisso e non utilizzati.

Sorgenti di calcolo originali invariati. Due adattamenti del solo runner isolato: namespace tracking senza l'import del punto d'ingresso VideoInstance/LMDB non usato; copia del checkpoint serializzata su CPU con tutti i tensori verificati identici. FPS ripreso dalla convenzione originale Config: il valore CSV 59.94… è convertito a 60, anziché passato come float alla memoria.

Tentativi conservati:

- **761893 FAILED/1:0**, 25 s: import del punto d'ingresso richiedeva LMDB. Nessuna inferenza del prefisso completata.
- **761895 FAILED/1:0**, 29 s: il loader originale senza map_location tentava di ripristinare gli storage CUDA in un job CPU. Nessun risultato di tracking da questo tentativo.
- **761899 RUNNING nell'ultima osservazione riuscita**, 9m50s, almeno 3000/3398 frame elaborati; limite 15 minuti, due CPU/8 GB. Questo è uno stato storico osservato, non lo stato corrente certificato. Percorso `~/cv_project/real_prefix_v3/`, log `~/cv_project/real_whare_761899.out/.err`. Bundle locale `shared_exports/real_prefix_v3/`. Esito finale ancora da acquisire; non sono noti il confronto finale con il collega e l'esito dell'intero prefisso.

In parallelo **761902 FAILED/1:0**, 12 s, per dipendenza xmltodict assente. Corretto il pacchetto isolato aggiungendo la wheel xmltodict 0.14.2 con hash verificato; **761905 COMPLETED/0:0**, 20 s. Calcolo IDF1 dalle predizioni registrate, senza nuova inferenza: worker originale, ricostruzione dei campi necessari dal JSON, motmetrics 1.4.0 da PyPI con hash verificato e dipendenze confinate nel pacchetto del job. Non modificati gli ambienti esistenti. Segue la convenzione di identità per nome dell'evaluator originale, non nuova GT fisica. Output finale `~/cv_project/recorded_metrics_v2/result.json`, log `~/cv_project/metric_whare_761905.out/.err`, bundle locale `shared_exports/recorded_metrics_v2/`. Stato di completamento osservato, ma valore numerico IDF1 non ancora acquisito: non riportarlo come risultato noto.

## Accesso ai risultati — 14 novembre 2026

Alla ripresa SSH non risolve `slogin.hpc.unibocconi.it`, hostname confermato nelle dispense del corso. NXDOMAIN osservato con DNS del sistema, interrogazione diretta al DNS Wi-Fi universitario e richiesta HTTPS al resolver Google (Status 3, risposta indicata da DNS autorevole Bocconi). Marco conferma solo Wi-Fi universitario, senza VPN Bocconi. Presenti adattatori Norton VPN, ma non dimostrata la loro responsabilità. Nessuna modifica alla rete, nessun rilancio dei job. Provare il collegamento con VPN Bocconi; se il nome resta non risolvibile, serve verifica del servizio/nome lato università. Non inferire lo stato corrente dei job dal problema di accesso.

Appena ripristinato l'accesso: leggere accounting e output di 761899/761905, scaricare result.json/log e geometry_transactions.json del prefisso, verificare conteggi/equivalenza/confronto con export. La coda generale non è stata ricontrollata. Il blocco riguarda l'acquisizione degli esiti, non prova di fallimento del calcolo.

## Limiti e passaggio successivo

Un confronto a peso zero prova il collegamento software, non il beneficio della forma. Il prefisso non sostituisce la valutazione del video completo o il test separato. L'aggiornamento qui conserva forme separate: i 12 rifiuti di registrazione 2B non vengono aggirati o trasformati in fusioni valide. Il prossimo passaggio scientifico resta la calibrazione sullo sviluppo del contributo di forma e la diagnosi dell'accumulo, dopo verifica degli esiti in corso.
