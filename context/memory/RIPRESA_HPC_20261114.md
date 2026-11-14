# Ripresa HPC e lancio dei job arretrati — 14 novembre 2026

## Esito finale del ciclo GPU acquisito — 14 novembre

763324 COMPLETED/0:0 in 43m30s: sette replay, sei ricostruzioni reali SuperFlex ready, zero logits/associazioni esatti e nessuna differenza dal collega. Dodici ammissioni tutte inizializzazioni, dodici rifiuti e zero fusioni nelle quattro rappresentazioni. Le sei ricostruzioni sono delle tre inizializzazioni DA/MoGE, non di accumuli multivista riusciti. Copie result.json/controller_summary.json in outputs/hpc_ripresa_20261114/reconstruct_763324/. Nuovo valutatore e comando unico in COMPLETAMENTO_PIPELINE_20261114.md. Le indicazioni precedenti di questo job ancora attivo sono storiche.

## Aggiornamento durante lo sviluppo del runner comune

I due job CPU sono completati, con controlli zero superati. Il conteggio di accumulo è sulle quattro rappresentazioni: due riusano ciascuna sorgente di punti; non sono 12 esperimenti fisici indipendenti né vanno sommati al vecchio pilota 0/12. Le ammissioni sono tutte inizializzazioni, nessuna fusione reale. Controller JSON acquisiti in outputs/hpc_ripresa_20261114/. GPU avviato dopo il successo CPU, risultato finale ancora da leggere nell’ultima osservazione. Nessuna nuova esecuzione del runner comune o alterazione degli snapshot HPC.

## Mandato e accesso osservato

Marco chiede di verificare HPC e, se disponibile, lanciare i job rimasti in sospeso; altrimenti continuare lo sviluppo. SSH riuscito su slnode01, accounting e coda leggibili; partizione stud disponibile. Nessuna modifica alla rete o all'accesso. Prima del nuovo lancio, coda personale vuota.

## Risultati preesistenti recuperati

- **761899 COMPLETED/0:0**, 11m35s. Replica del precedente prototipo sul prefisso reale P01_01: 3398 frame, 10264 detection, quattro rappresentazioni, 3397 confronti dei logits per rappresentazione. Logits/associazioni a peso geometrico zero esatti, **zero frame differenti dall'export del collega**, 12 track finali. Otto distanze geometriche valide per rappresentazione. Inferenza effettiva circa 668.29 s. Certifica quel prefisso/runner storico, non automaticamente il wrapper/coordinatore successivi o l'intero video.
- **761905 COMPLETED/0:0**, 20 s. IDF1 sulle predizioni registrate dell'intero P01_01: **73.2697350574193%**, IDTP 81029, IDFP 29561, IDFN 29561; 33310 frame. Non nuova inferenza: evaluator originale, convenzione per nome oggetto/deduplicazione/IoU. Video train, non test indipendente; nessuna nuova GT fisica certificata. Rimane mPCL 70.4655% già verificato dal CSV.

Copie e controlli in `outputs/hpc_ripresa_20261114/`: JSON dei due job, transazioni del prefisso, hash e `recovered_verification.json`. I job completati non rilanciati. Contratto/baseline soddisfatti per questo prefisso verificato; restano i due alias JPEG fuori prefisso, senza promozione automatica a join exact.

## Nuovi pacchetti e controllo prima del lancio

Preparato `shared_exports/real_prefix_v4/`: stesso prefisso e nuovi moduli, punti camera e hash. Audit completo delle 110590 osservazioni ripetuto durante preparazione: zero differenze di ordine/metadati/XYZ. Archivio trasferito e tutti gli hash preparati verificati sul server.

Controller `integration_prototype/run_hpc_backlog.py`, pacchetto `shared_exports/backlog_20261114_v1/`; directory remota `~/cv_project/backlog_20261114_v1/`. Ogni esperimento copia gli input in una directory nuova legata al job, senza modificare quelli precedenti. Per il ramo differito il controller esegue il prefisso, processa serialmente le richieste reali su GPU e ripercorre dall'inizio usando la cache fino al completamento, con numero massimo di replay limitato dagli input geometrici. Conserva log per replay e riepilogo; non considera validata l'inferenza GPU se nessuna ricostruzione reale è pronta. Nessun checkpoint completo o cambio automatico di soglie/metodo.

Il primo tentativo di lancio si è fermato **prima di qualsiasi sbatch**, perché il percorso storico `external/superflex_unsup_robust/` conteneva checkpoint/config diversi da quelli attesi. Individuati con hash e riusati gli asset corretti `~/cv_project/SuperFlex-repo/robust/ckpt.pt` e `config.yaml`, corrispondenti al nucleo portabile. Configurazione definitiva `runtime_robust.json` e script `reconstruct_robust.sbatch`; la configurazione iniziale rimane storica e non usata. Nessuna inferenza con il checkpoint alternativo, nessuna installazione o download pesi.

## Job inviati e ultimo stato verificato

| Job | Scopo | Stato osservato | Output principale |
|---|---|---|---|
| 763321 | Regressione nell'ambiente HPC | **COMPLETED/0:0**, 30 s; **50 test passati** | `~/cv_project/backlog_cv_contract_763321.out/.err` |
| 763322 | Nuovo wrapper/coordinatore sul prefisso, peso zero | **COMPLETED/0:0**, 9m56s; zero esatto e nessuna differenza dal collega | `~/cv_project/backlog_20261114_v1/zero_763322/` |
| 763323 | Associazioni → accumulo candidato, peso zero | **COMPLETED/0:0**, 12m11s; 12 inizializzazioni, 12 rifiuti, zero fusioni | `~/cv_project/backlog_20261114_v1/accumulate_763323/` |
| 763324 | Accumulo → SuperFlex reale → forma futura, peso zero | **COMPLETED/0:0**, 43m30s; sei ricostruzioni reali ready, controllo zero esatto, zero fusioni | `~/cv_project/backlog_20261114_v1/reconstruct_763324/` |

763322/763323 dipendono dal successo di 763321; 763324 dipende dal successo di entrambi i job CPU. Risorse: due CPU, 16 GB per esperimento; limiti 25/35/150 minuti, un GPU soltanto per 763324. Test iniziali due CPU/8 GB, limite 10 minuti. Log generali `~/cv_project/backlog_cv_zero_763322.out/.err`, `backlog_cv_accum_763323.out/.err`, `backlog_cv_sf_cycle_763324.out/.err`. Stato/ID locali in `outputs/hpc_ripresa_20261114/submitted_jobs.json`.

I 50 test sono regressioni controllate nell'ambiente, inclusi i sette test del registratore precedentemente separati; non equivalgono a 50 esperimenti su video o a inferenza SuperFlex reale. I nuovi esperimenti sono inviati, **non ancora conclusi**. Nessuna metrica o nuova fusione reale dichiarata prima di acquisirne gli esiti. I risultati storici 0/12 restano validi per i piloti precedenti, non una previsione dei nuovi job.

## Passo successivo e perimetro

Leggere accounting/log e scaricare `result.json`, `controller_summary.json`, transazioni e report delle richieste quando disponibili; in caso di errore correggere la causa senza rigenerare asset o cancellare evidenze. Distinguere inizializzazioni e fusioni reali ammesse, ricostruzioni riuscite/fallite, copertura e costi dei replay. Il peso geometrico è zero: questi job verificano l'integrazione, non un miglioramento tracking.

Non lanciati FPFH/RANSAC, nuovi split/calibrazioni, nuove profondità o training: nel parere restavano raccomandazioni non adottate. Valutazione finale e runner generale delle ablation restano lavoro successivo; nessun push o messaggio a terzi.

## Scomposizione verificata delle 12 inizializzazioni

Non dodici viste dello stesso oggetto: tre inizializzazioni di track ripetute nelle quattro rappresentazioni. Track 4/tagliere al frame 2893, track 6/coltello al frame 5099, track 9/padella al frame 7508. Nel sottoinsieme geometrico il tagliere ha tre osservazioni, il coltello due, la padella una. I tentativi successivi sono tagliere 5099/7508 e coltello 7508, ripetuti quattro volte (due sorgenti, due rappresentazioni); tutti rifiutati. La padella non ha una seconda vista in questo prefisso e non contribuisce al test di fusione. Nomi da annotazioni preparate, track da associazioni predette; non nuova certificazione di identità fisica. Audit/transazioni acquisiti in outputs/hpc_ripresa_20261114/initialization_breakdown.json e accumulate_763323_geometry_transactions.json.

## Motivi effettivi dei rifiuti

Audit dei sei allineamenti unici per frame/track/sorgente (duplicati nelle due rappresentazioni): tagliere al 5099, DA e MoGE, rifiutato solo per ambiguità di posa; supporto/residui superano i gate. Al 7508 tagliere DA/MoGE e coltello DA falliscono supporto, residui e ambiguità; coltello MoGE fallisce supporto/residui, senza ambiguità.

Gate diagnostici del prototipo, non stabiliti da Whareformer/SuperFlex né calibrati sullo sviluppo: supporto almeno 65% in entrambe le direzioni entro 0.08 della scala RMS del riferimento fit; residuo q90 sulla frazione più vicina (80%) non oltre 0.15 in entrambe le direzioni; rifiuto di alternative entro 5% di score fit (più epsilon numerico) con rotazione diversa oltre 15 gradi oppure spostamento del centroide oltre 0.08 della stessa scala. Query di validazione escluse da fitting/selezione, ma non viste indipendenti. Nessun centimetro o accuratezza metrica certificata implicati.

Il rifiuto per sola ambiguità non dimostra una fusione errata: simmetrie geometricamente equivalenti e criteri di supporto troppo restrittivi su viste parziali restano ipotesi da diagnosticare. Nessun gate modificato. Dettagli numerici in outputs/hpc_ripresa_20261114/rejection_criteria_audit.json.

## Cause effettive dei rifiuti e soglie provvisorie

Audit dei sei confronti distinti per vista/sorgente (i rami punti/SuperFlex ripetono la stessa registrazione). Gate correnti del candidato, non prescrizioni dei paper né soglie calibrate: supporto almeno 65% in entrambe le direzioni entro 0.08R; q90 sull'80% dei punti più vicini al massimo 0.15R in entrambe le direzioni; nessuna alternativa di fit entro circa 5% dal migliore con rotazione diversa oltre 15 gradi o spostamento del centro oltre 0.08R. R è il raggio RMS del campione di riferimento. Query di validazione escluse dalla stima/selezione della posa; non nuove viste indipendenti.

Tagliere 5099, DA/MoGE: supporto minimo 86.3%/84.3%, residuo massimo 0.0529R/0.0450R; supera i primi due gate, rifiutato solo per ambiguità (5/2 alternative). Tagliere 7508: supporto minimo 40%/42.3%, residuo massimo 0.3029R/0.2716R, anche ambiguità. Coltello 7508: supporto minimo 43%/53.3%, residuo massimo 0.3217R/0.1859R; ambiguità aggiuntiva solo per DA.

Limite concreto: per il tagliere MoGE 7508 il 99% dei punti correnti è vicino al riferimento, ma solo il 42.3% nell'altra direzione. Questa asimmetria è compatibile anche con una vista parziale; non dimostra da sola posa errata. Pose diverse possono essere equivalenti per simmetrie: il gate conservativo attuale può rifiutare fusioni legittime. È un'ipotesi da verificare, non una fusione certificata o motivo per abbassare automaticamente le soglie. Nessuna regola modificata. Dettaglio numerico in outputs/hpc_ripresa_20261114/rejection_criteria_audit.json.
