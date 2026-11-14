# Stato del lavoro e ripresa

## Passaggio a un altro provider AI — 14 novembre 2026

Marco richiede memoria e contesto autosufficienti nella cartella e su GitHub. Guida corrente: [LEGGIMI_PASSAGGIO_AI.md](LEGGIMI_PASSAGGIO_AI.md), che distingue implementato/verificato/pendente, decisioni, dipendenze e prossimi passi. Pubblicazione selettiva preparata dalla main del collega fc5aa30: codice integrazione, memoria, mappa corrente ed evidenze leggere; dati grandi, pesi e accessi esclusi. Nessun nuovo esperimento, filtro invariato. Gli stati storici di attesa frontend, output collega mancanti e job 763531 attivo sono superati dalle verifiche successive. Consegna pubblicata su main, riferimento remoto verificato al commit 6d7a8b7; dettagli in docs/CONDIVISIONE.md e inventario in context/evidence/publication_inventory.json. Nessun job nuovo.

## Cartella mappa e ripresa — 14 novembre

Mappa nella cartella dedicata mappa_interattiva/ della repository locale, con README.md canonico, inventario, avvio e istruzioni di ripresa in altra chat. LEGGIMI rimanda al README; backup esclusi da Git. Nessuno spostamento dei file applicativi, nessun commit/push. contenuti.json invariato per hash; preservare le schede manuali B01/B02/B03 ed E01/E02/E03.


## Salvataggio revisione mappa verificato — 14 novembre

Verificata persistenza della revisione manuale di B01/B02/B03 ed E01/E02/E03: JSON valido, copia JS offline e servizio identici; 12 backup, nessun temporaneo residuo. Browser con conferma Salva e nessun modulo aperto. Verifica del salvataggio, non approvazione scientifica; contenuti invariati.


## Frontend approvato e percorso cache verificato — 14 novembre

Ok di Marco ricevuto. Implementati contratto e import cache verificato, ingresso --frontend-manifest nel comando unico; dieci detection nei tre frame con intera storia di 3398 frame, quattro file dati byte-identici. 72 casi locali (70 passati, due skip motmetrics). Rigenerazione da RGB ancora non eseguita: pesi/revisione DINOv2, provenienza PCA e scala/ambiente scena da verificare, inventario circoscritto senza prova di assenza globale. [Avanzamento e limiti](FRONTEND_AVANZAMENTO_20261114.md). Piano parzialmente eseguito, non dichiarato completo; filtri invariati. 763531 concluso 0:0 in 23m24s, nove varianti zero completate e valutate; nessun nuovo job del frontend. Le note di attesa dell’ok e job ancora attivo sono storiche.

Completati i tre segnaposto di B01/B02 nella mappa: EPIC-KITCHENS, provenienza VISOR e modulo di segmentazione (SAM 2 come esempio da valutare, con inizializzazione esplicita). Resto dei campi preservato. Marco chiarisce che le parentesi quadre nei suoi testi sono richieste di completamento da parte dell’assistente. Nessuna adozione o implementazione di un segmentatore. Fonte primaria consultata: https://github.com/facebookresearch/sam2.


## Piano frontend preparato, attesa dell’ok — 14 novembre

Marco richiede pianificazione prima dell’esecuzione. Proposto collegamento preprocessing → runner: inventario dipendenze, manifest unico, import/rigenerazione con cache, comando unico e piccolo pilota P01_01 mantenendo la storia del tracker. [PIANO_FRONTEND_UNIFICATO_20261114.md](PIANO_FRONTEND_UNIFICATO_20261114.md). Piano non ancora approvato: nessuna implementazione o nuovo job per questo step prima dell’ok. Filtri ancora rinviati; job precedentemente autorizzati invariati, senza nuovo controllo di stato in questa fase.

## Schede più comprensibili e collegamenti modificabili — 14 novembre

Marco estende la modifica alle descrizioni dei collegamenti e richiede testi comprensibili anche alla giuria. Implementati editor/salvataggio frecce con backup e conflitti, menu Collegamenti per selezionarle. Titoli: Possibili miglioramenti, Coerenza dei dati, Possible points of failure. Riscritti solo funzione/evidenze/coerenza di Maschere 2D · VISOR; contenuti manuali di RGB e altri campi della maschera preservati e confrontati. Verificati salvataggio freccia su copia isolata e modulo/conferma nel browser senza alterare testo della freccia reale. Regola editoriale: funzione concreta e termini spiegati, senza formule telegrafiche comprensibili solo a chi ha sviluppato il codice. Nessun esperimento o modifica al metodo scientifico.


## Valutatore e comando unico collegati — 14 novembre

Implementati export delle osservazioni/assegnazioni con hash, IDF1/mPCL originali con scope esplicito e comando input preparati → varianti → valutazione → tabella. 763498 COMPLETED/0:0 (33 s), otto test; 763530 COMPLETED/0:0 (45 s), 69 test tutti eseguiti, riprodotti IDF1 73.269735% e mPCL 70.465504% su predizioni registrate train. 763531 RUNNING a 10m50s nell’ultima osservazione: nove configurazioni zero, CPU e cache esistente; esito ancora da acquisire. [COMPLETAMENTO_PIPELINE_20261114.md](COMPLETAMENTO_PIPELINE_20261114.md).

**GPU concluso:** 763324 COMPLETED/0:0 (43m30s), sei ricostruzioni reali ready e controllo zero esatto, ma nessuna fusione multivista ammessa. Filtri invariati e revisione ancora rinviata. Mancano unificazione del frontend dati, copertura sufficiente e calibrazione/test; il comando attuale parte da input preparati. Le precedenti note di metriche non collegate e GPU ancora attivo sono storiche.

## Descrizioni della mappa salvabili nei file — 14 novembre

Scelte esplicite di Marco: servizio locale, sole descrizioni dei riquadri, campi separati con Modifica/Salva. Implementati server.cjs e Avvia mappa.cmd; contenuti.json è la sorgente, contenuti.js la copia offline aggiornata. Backup prima di ogni modifica effettiva e protezione da aggiornamenti concorrenti; titoli/fonti/collegamenti non modificabili dall’editor. Verificati persistenza/backup e rifiuto conflitti/campi vietati su copia isolata; nel browser osservati modulo e conferma Salva senza alterare il testo originale. Guida aggiornata in [mappa_interattiva/LEGGIMI.md](mappa_interattiva/LEGGIMI.md). Non modifica i Markdown scientifici; disposizione e revisione dei filtri rimangono rinviate.


## UX/UI mappa aggiornata — 14 novembre

Pannello sinistro richiudibile e chiuso inizialmente, zoom con rotella/pulsanti, pan dello sfondo, vista completa e 100%, disposizione orizzontale e stile aggiornato. Verificati visivamente nel browser apertura/chiusura, zoom (100→165%), pan e ritorno alla vista completa. Layout salvati preservati: Ripristina disposizione applica quello nuovo. Contenuti scientifici invariati. Guida: [mappa_interattiva/LEGGIMI.md](mappa_interattiva/LEGGIMI.md).


## Revisione filtri di fusione rinviata — 14 novembre

Marco conferma che i filtri di ammissione delle nuvole vanno rivisti, ma non ora. Attività pendente esplicita in TODO.md: riesaminare soprattutto simmetrie/ambiguità e parzialità/supporto bidirezionale. Criteri numerici scelti dall’assistente come diagnostica provvisoria, non imposti dai paper o calibrati. Non avviare la revisione né cambiare soglie/codice in questa fase; resto del lavoro invariato.

## Prima mappa HTML interattiva — 14 novembre

Su richiesta di Marco creata [mappa_interattiva/index.html](mappa_interattiva/index.html): 19 nodi trascinabili, 34 collegamenti selezionabili, pannello laterale, modifica delle schede, salvataggio nel browser e import/export JSON. Prime proposte di contenuto per RGB, maschere, aspetto e tre collegamenti; altre schede esplicitamente da compilare. File e modalità di modifica in [LEGGIMI.md](mappa_interattiva/LEGGIMI.md). Verificati sintassi, caricamento e selezione/spostamento da tastiera nel browser; nessuna sincronizzazione automatica con Markdown o collaborazione simultanea. Prossimo passo documentale: discutere le prime schede in chat, poi completare geometria e posizione. Nessun nuovo esperimento o controllo HPC.

## Causa dei rifiuti verificata — 14 novembre

Audit dei log 763323: tagliere 5099 respinto solo per ambiguità, con supporto/residuo ammessi in DA/MoGE; a 7508 tagliere e coltello falliscono supporto/residuo, con ambiguità aggiuntive salvo coltello MoGE. Gate provvisori del candidato, non imposti dai paper o calibrati. Asimmetria 99%/42.3% del tagliere MoGE compatibile anche con parzialità; simmetrie possono rendere troppo severo il gate di ambiguità. Nessuna soglia modificata; diagnosi necessaria, non prova di associazioni errate. [Audit e valori](RIPRESA_HPC_20261114.md).

## Diagnosi dei rifiuti verificata — 14 novembre

Letti motivi e soglie reali del 763323: tagliere 5099 (DA/MoGE) supera supporto/residui ma viene rifiutato solo per posa ambigua; al 7508 i quattro allineamenti falliscono supporto/residui, tre anche ambiguità. Gate provvisori del nostro prototipo, non regole dei due modelli; nessuna soglia cambiata o incompatibilità fisica dimostrata. [Numeri e criteri](RIPRESA_HPC_20261114.md).

## Conteggi delle inizializzazioni chiariti — 14 novembre

Verificati i log del job 763323: 12 inizializzazioni = tagliere/track 4 (2893), coltello/track 6 (5099), padella/track 9 (7508), ciascuna in quattro rappresentazioni. Tre successive osservazioni candidate alla fusione (due del tagliere, una del coltello) ripetute nelle quattro configurazioni, tutte rifiutate; padella con una sola vista, nessun suo tentativo di fusione. Track predette/categorie non nuove identità GT. Audit e dettaglio in [RIPRESA_HPC_20261114.md](RIPRESA_HPC_20261114.md).

## Runner comune e misure implementati — 14 novembre

Disponibili W0/G0/S-separata/S-accumulo/P-accumulo, DA/MoGE, memorie e modelli indipendenti, controllo sui punti ammessi e report JSONL/JSON/CSV con copertura, fallimenti, byte di payload e costi dei replay. 58 test locali superati; esempio a peso zero, tracking metrics ancora non calcolate. Nessuna nuova run reale del runner comune né modifica dei job esistenti. [RUNNER_VARIANTI_20261114.md](RUNNER_VARIANTI_20261114.md). Prossimo: collegare valutatore tracking e protocollo/copertura di calibrazione-test.

**HPC verificato durante il lavoro:** 763322 COMPLETED/0:0 (9m56s), 763323 COMPLETED/0:0 (12m11s), zero esatto; nel secondo solo 12 inizializzazioni e 12 rifiuti, nessuna fusione, conteggi sulle quattro rappresentazioni. 763324 RUNNING a 29m19s con almeno un risultato neurale reale ready; esito complessivo ancora da acquisire. [Dettagli HPC](RIPRESA_HPC_20261114.md). Le indicazioni precedenti di job CPU attivi/GPU in attesa sono storiche.

## Selezione e calibrazione autonome approvate — 14 novembre

Marco approva ottimizzazione di parametri/metodo e confronto delle alternative, perseguendo qualità in ogni fase e beneficio finale nel tracking. Piano corrente e criteri nel [piano d'azione](ROADMAP_CICLO_GEOMETRICO.md): esiti esistenti → geometria/calibrazione → finaliste nel ciclo → test separato. Confermati inferenza SuperFlex dopo ogni aggiornamento ammesso e nessun filone autonomo sulla contaminazione generale. Prossimo: acquisire i risultati già avviati e predisporre runner/metriche comuni e confronto geometrico; nessuna nuova calibrazione, implementazione o esecuzione in questo aggiornamento. Stati HPC sotto conservati come ultime osservazioni, non ricontrollati qui.

## HPC ripristinato, arretrati inviati — 14 novembre

SSH/accounting/coda accessibili. Recuperati 761899 (prefisso storico a peso zero esatto, 3398 frame/10264 detection, zero differenze dal collega) e 761905 (IDF1 73.2697% sulle predizioni registrate train, non test). Nuovi job: 763321 COMPLETED/0:0, 50 test ambiente passati; 763322 replica aggiornata e 763323 accumulo RUNNING nell’ultima osservazione; 763324 SuperFlex differita PENDING per dipendenza dai due CPU. Nessun nuovo esito sperimentale ancora dichiarato; prossima acquisizione dei risultati. [RIPRESA_HPC_20261114.md](RIPRESA_HPC_20261114.md). Le note precedenti sul blocco DNS e sui due esiti ancora da leggere sono storiche.

## Parere sulla proposta del collega — 14 novembre

Approfondite su richiesta di Marco le opzioni con pro/contro: pulizia conservativa, alternative di posa/RGB/scala, ammissione compatibile con viste parziali, budget/frequenza SuperFlex e valutazione visibile con controlli tracking. Precisato che simmetrie reali possono rendere pose diverse geometricamente equivalenti; nessuna modifica automatica ai gate. Analisi nel parere collegato sotto; nessuna nuova scelta o esecuzione.

Valutata la sequenza pulizia → FPFH/RANSAC/ICP → accumulo → SuperFlex → valutazione: baseline candidata plausibile, con controlli su posa/scala, rifiuti e identità; Chamfer simmetrica contro una vista parziale insufficiente come unica misura. Il candidato attuale è PCA/multistart + ICP: 0/12 non è un test di FPFH. Raccomandato piccolo confronto diagnostico alla ripresa, non adottata una sostituzione né modificato il protocollo. [Parere e fonti](PARERE_PROPOSTA_COLLEGA_20261114.md). Nessun nuovo esperimento o risultato; priorità software e stato HPC invariati.

## SuperFlex differita collegata — 14 novembre

Implementate richieste da nuvola/versione ammessa, worker sulla pipeline esistente, verifica/importazione e pubblicazione della forma nei soli frame successivi. Replay seriale bloccato fino agli esiti, ultima forma conservata su fallimento; completamenti esclusi dai punti osservati. 43 controlli locali passati con sostituti dichiarati, nessuna nuova inferenza reale/HPC. Runner predisposto con --accumulate --reconstruct; prossimo confronto comune delle varianti e aggregazione delle misure. [SUPERFLEX_DIFFERITA_20261114.md](SUPERFLEX_DIFFERITA_20261114.md). Le note precedenti sul collegamento SuperFlex ancora mancante sono storiche; validazione reale 2B e risultati HPC pendenti invariati.

## Registrazione/accumulo collegati — 14 novembre

Collegato il candidato esistente al coordinatore: inizializzazione, registrazione rigida e accumulo ammesso, con isolamento delle sorgenti, versioni/provenienza e conservazione dello stato su rifiuto/errore. 35 test locali passati; input sintetici e componenti controllati, nessun replay reale o HPC. Runner predisposto con --accumulate (default disattivato), preparatore con punti camera/hash; non eseguiti in questa fase. Prossimo: SuperFlex differita dalla nuvola accettata. Il matcher usa ancora forme separate; risultato reale 2B invariato (0/12). [COLLEGAMENTO_ACCUMULO_20261114.md](COLLEGAMENTO_ACCUMULO_20261114.md). Le indicazioni precedenti sul collegamento ancora mancante sono storiche.

## Coordinatore del frame completato — 14 novembre

Implementato e collegato al runner: confronto/associazioni prima, commit delle forme e proposte geometriche dopo; versioni distinte, stato valido preservato per mancanti/rifiuti/errori. 27 controlli locali passati (11 nuovi), con metodi originali e componenti controllati; nessuna verifica Torch o run HPC. Il runner aggiorna ancora solo forme separate: prossimo collegamento del candidato registrazione/accumulo, poi SuperFlex differita. Esiti HPC e validazione 2B invariati. Resoconto: [COORDINATORE_FRAME_20261114.md](COORDINATORE_FRAME_20261114.md). Le indicazioni sottostanti sul coordinatore ancora da implementare sono storiche.

## Mappa del risultato atteso — 14 novembre

Marco richiede revisione della nuova mappa e annotazioni per ciascun riquadro/collegamento (stato e alternative, motivi, miglioramenti). Preparata una **proposta**, non ancora approvata: mappa essenziale con schede collegate, contratti dei collegamenti ed evidenza distinta dall'implementazione. Correzioni ed esempi in [PROPOSTA_ANNOTAZIONI_MAPPA_20261114.md](PROPOSTA_ANNOTAZIONI_MAPPA_20261114.md). Nessuna modifica alla lavagna esterna, alla selezione scientifica o ai job; compilazione sistematica delle schede ancora da fare.

Precisata con lettura del codice originale locale la provenienza degli XYZ EPIC: profondità da RGB allineata alla scena, centro bounding box/maschera, intrinseci e posa camera. La maschera alimenta anche il ramo posizione; le feature d'aspetto non lo generano. Dettagli e limiti in [MAPPA_FLUSSO_SISTEMA.md](MAPPA_FLUSSO_SISTEMA.md). Nessuna rigenerazione o modifica della baseline; priorità operative in apertura invariate.

Marco esplicita il flusso RGB → maschera/nuvola → SuperFlex → associazione → aggiornamento delle memorie. Preparata [MAPPA_FLUSSO_SISTEMA.md](MAPPA_FLUSSO_SISTEMA.md), coerente con il ciclo approvato: aspetto dalla regione mascherata, posizione baseline, contributo geometrico tramite adattatore e nuova forma disponibile ai frame successivi. Distinti inizializzazione, aggiornamenti rifiutati e stato effettivo; nessuna nuova implementazione o validazione. Prossimo lavoro software invariato: punto 2 del piano senza HPC.

**Consegna collaborativa ancora aperta:** Marco chiede prima Miro, poi una slide e uno spazio di lavoro in stile Miro in ChatGPT Space. Miro richiede login, non effettuato; richiesta successiva indirizzata a Space. Creata e collegata presentazione privata vuota «Ciclo Whareformer–SuperFlex», Page ID `page_f951f11ecfbc81a48983567d55429f5d`. Inserimento della mappa bloccato: servizio di modifica slide non eseguibile nell'ambiente corrente («requires MXC»), nessun editor esposto nel browser. Nessun contenuto inserito, nessuna condivisione o lavagna creata; riusare la presentazione esistente alla ripresa, senza duplicarla. La mappa locale resta disponibile.

## Punto 1 software completato — 14 novembre

Implementato componente riutilizzabile con tre modalità, quattro rappresentazioni e delega al matcher originale; runner e preparatore aggiornati. Passati 16 controlli locali (7 adapter + 9 wrapper), con modello/tensor controllati; verifica Torch/frame reali rinviata. Nessun accesso HPC o nuovo esperimento. Prossimo lavoro: punto 2, coordinatore causale e stato geometrico versionato. Resoconto: [INTEGRAZIONE_RIUTILIZZABILE_20261114.md](INTEGRAZIONE_RIUTILIZZABILE_20261114.md).

## Priorità corrente — sviluppo senza HPC, 14 novembre

Marco dispone di sviluppare il progetto e rimandare gli esperimenti. Sospesi i tentativi di connessione come attività prioritaria; il recupero di 761899/761905 resta pendente alla ripresa. Ordine operativo: integrazione riutilizzabile → coordinatore causale → interfaccia SuperFlex differita → runner/controlli locali → pacchetto sperimentale. Piano e criteri in [PIANO_SVILUPPO_SENZA_HPC_20261114.md](PIANO_SVILUPPO_SENZA_HPC_20261114.md). Nessun nuovo esperimento o risultato; 2B resta non validato, parametri/protocollo finale non fissati da questa revisione.

Aggiornamento: 14 novembre 2026. Prevale sulle indicazioni operative storiche.

## Integrazione reale in corso — 13 novembre

Arrivato anche fc5aa30: configurazione/comandi/patch Windows e CSV acquisiti; checkpoint locale corrispondente verificato. Input ufficiali P01_01 recuperati autonomamente e controllati su tutte le 110590 osservazioni, zero differenze di metadati/XYZ. Job CPU 761872 COMPLETED/0:0 (28 s), 120 casi a peso zero sul modello reale superati. Tentativi prefisso 761893 FAILED/1:0 (25 s, LMDB) e 761895 FAILED/1:0 (29 s, deserializzazione CUDA su CPU), corretti nel runner isolato e conservati. **761899 RUNNING nell'ultima osservazione riuscita (9m50s, almeno 3000/3398 frame), stato attuale ed esito non acquisiti**. Metriche registrate: 761902 FAILED/1:0 (12 s, xmltodict), corretto nel pacchetto; **761905 COMPLETED/0:0 (20 s), valore IDF1 ancora da leggere**. CSV del collega verificato: mPCL 70.4655% sul singolo video train, non test separato. Percorsi, hash e limiti in [INTEGRAZIONE_BASELINE_REALE_20261113.md](INTEGRAZIONE_BASELINE_REALE_20261113.md). Coda generale non ancora ricontrollata.

**Blocco di accesso del 14 novembre:** hostname HPC non risolto (NXDOMAIN anche al DNS Wi-Fi e tramite resolver HTTPS esterno). Marco conferma solo Wi-Fi universitario, senza VPN Bocconi. Nessuna responsabilità di Norton dimostrata; rete invariata, job non rilanciati. Prossimo passo: provare VPN Bocconi e recuperare accounting/output di 761899/761905; nessuna equivalenza su tutto il prefisso o IDF1 numerico dichiarati prima di leggerli. Le precedenti note di assenza di configurazione/checkpoint/feature sono superate; restano due alias JPEG e la validazione 2B.

## Nuova consegna Whareformer verificata — 13 novembre

Remoto main osservato a bbf0e5e; ricevuti e preservati i due manifest completi. Audit reale passato: 71/73 exact, 52 track/110590 righe; 146 nuvole verificate. I due mancanti sono alias VISOR/RGB di un indice, verificati nei record/mapping originali ma non riclassificati exact prima di controllare il JPEG delle feature. In 69/71 casi annotation_index non coincide con detection_idx; lookup esplicito necessario. Revisionate tavole delle track 4/36/9/35, segnali di contaminazione e possibile frammentazione. Report [VERIFICA_CONSEGNA_WHAREFORMER_20261113.md](VERIFICA_CONSEGNA_WHAREFORMER_20261113.md), output `outputs/github_handoff_bbf0e5e/`, segmento registrato di tre frame/dieci detection preparato. Nessuna inferenza né job; sola lettura HPC mirata, coda non ricontrollata. Step 1 chiuso per acquisizione/audit dei manifest, aperto per provenienza temporale e feature, configurazione/versione/checkpoint della run e metriche. Prevale sulle precedenti note di assenza dei due JSON. Lo sviluppo autonomo rimane disponibile.

## Esito corrente step 2B — 13 novembre

Implementati registrazione rigida candidata e memoria limitata di punti osservati; sette nuovi test finali superati. Nei piloti DA/MoGE, 12/12 aggiornamenti reali rifiutati su nove osservazioni di tre identità visive; inizializzazioni conservate, nessuna fusione reale accettata. Prima versione del controllo corretta e preservata; nessuna soglia rilassata per le viste reali. Report [RISULTATI_REGISTRAZIONE_ACCUMULO_20261113.md](RISULTATI_REGISTRAZIONE_ACCUMULO_20261113.md); output `outputs/registration_pilot_v1/` (storico), `registration_pilot_v2/` e `registration_close_views_v1/`. Controlli artificiali positivi non certificano la posa reale. Nessuna nuova inferenza SuperFlex, mancando un accumulo reale ammesso; nessun job o coda HPC ricontrollata. Prossima incertezza: posa ambigua e geometria/scala variabile, da diagnosticare separatamente. 2A con forme separate resta disponibile; 2B candidato implementato ma non validato. Prevale sulle note precedenti che indicano ancora accumulatore non implementato.

## Avanzamento autonomo precedente — 13 novembre

Marco richiede di avanzare sugli step indipendenti ed eventualmente replicare una baseline minima. Step 2A avviato con `integration_prototype/`: adattatore candidato, sette test superati (120 confronti a peso zero col greedy originale) e replay tecnico di tre frame/cinque osservazioni P03_04 su punti/SuperFlex DA/MoGE, 20 artefatti verificati. Evidenza `outputs/independent_adapter_pilot_v1/`. Nessuna inferenza Whareformer: logits di prova e associazioni annotate esterne; nessun beneficio tracking o accumulo validato. Resoconto e piano: [AVANZAMENTO_AUTONOMO_20261113.md](AVANZAMENTO_AUTONOMO_20261113.md). Prossimo lavoro autonomo: registrazione/accumulo controllati su punti disponibili, poi nuova inferenza SuperFlex solo quando esiste un accumulo accettato. Lo step 1 resta dipendente dai manifest della run del collega, ma non blocca questi sviluppi. Nessun nuovo job o controllo HPC in questa fase.

## Step 1 avviato — roadmap approvata

Marco approva la roadmap e avvia lo step 1. Remoto ancora ab5a946; manifest completi e asset baseline non trovati nel workspace o nella ricerca delimitata dello spazio personale HPC. Stato e richiesta minima in [STEP1_CONTRATTO_TRACKING.md](STEP1_CONTRATTO_TRACKING.md); evidenza `outputs/step1_tracking_contract/status.json`. Preparato controllo JSON, sei casi sintetici superati; non eseguito sui dati reali mancanti. Prossimo passo dipendente dalla disponibilità di manifest/configurazione/input del collega, senza invio automatico di messaggi. Nessuna nuova inferenza o job; nessuna verifica attuale della coda. Step 1 non concluso.

## Direzione corrente — chiarimento successivo del 13 novembre

Marco conferma il ciclo unitario: forma→associazione→aggiornamento della ricostruzione→confronti futuri. Superata la precedente lettura dell’accumulo come sola estensione esterna. Roadmap dopo rilettura dei paper in [ROADMAP_CICLO_GEOMETRICO.md](ROADMAP_CICLO_GEOMETRICO.md); registro voce 31. Prossimo passo: contratto baseline/join reale, poi confronto/matcher e registrazione/accumulo, prima verificati separatamente e quindi collegati. Roadmap successivamente approvata da Marco; dettagli numerici e protocollo da calibrare/verificare secondo il piano. FIFO disponibile, accumulatore e ciclo completo non implementati. Nessun nuovo job o controllo HPC in questa fase.

## Stato corrente

**Consegna autonoma completata**, entro il mandato dell'11 novembre: pipeline portabile DA/MoGE → punti → SuperFlex, export, confronto e memoria causale configurabile. Rapporto unico: [CONSEGNA_RAMO_GEOMETRICO.md](CONSEGNA_RAMO_GEOMETRICO.md), con risultati, costi, verifiche e limiti. Guida `shared_exports/publish_candidate/SuperFlex/PIPELINE.md`; codice sul ramo `prepare/superflex-core`. Nessun beneficio tracking o metodo definitivo dichiarato.

Riutilizzate 8797 coppie e 299 osservazioni; nessun rilancio del confronto 200. Audit di cinque archivi VISOR: 183312 record frame, 632169 maschere, 200 annotazioni selezionate verificate. ID di maschera unici, nessun ID globale fisico nei campi verificati; non esclude altre risorse. Conservate 37 osservazioni/sette identità visive e i loro limiti. Nove coppie entro intervallo aggiungono solo una diagnostica locale, separata dalle identità. DA, MoGE e controllo sui punti restano attivi.

## Job ed evidenze verificate

- 755696 GPU COMPLETED/0:0, 5m37s: primo percorso portabile.
- 755697 CPU FAILED/1:0, 1m46s: audit assumeva un solo record per frame; corretta la gestione degli intervalli alternativi.
- 755699 CPU COMPLETED/0:0, 2m14s: audit completo dei cinque archivi.
- 755709 GPU COMPLETED/0:0, 5m36s: versione finale, sei nuvole/cinque superfici e fallimento MoGE atteso, export compatto e ripresa. Undici test superati; hash del codice pipeline corrispondenti, controlli locali e statici superati.

Output `~/cv_project/runs/portable_validation_755709/` e `~/cv_project/runs/visor_original_audit.json`; log `~/cv_project/portable_755696.out/.err`, `portable_755709.out/.err`, `visor_audit_755697.out/.err`, `visor_audit_755699.out/.err`. Copie e verifiche in `outputs/geometric_closure_v1/`; export storico `observations.json` con radice geometrie `outputs/compare200_749968/`. Archivio finale scaricato con hash corrispondente. **Nessun job attivo nell'ultima lettura della coda.**

Il contratto è verificato; equivalenza numerica esatta alle vecchie inferenze no: errore relativo L2 massimo punti 0.0006212, differenza D2 fra superfici fino a 0.00513. Non cambiate le distanze scientifiche storiche. Memoria FIFO/D2/spettro è un candidato implementato, non una scelta validata.

## Asset e prossima fase

Worktree condivisibile `shared_exports/publish_candidate/`, repository `https://github.com/Federico-cia/Whareformer-SuperFlex-Project`, sviluppo sul ramo `prepare/superflex-core`, destinazione condivisa `main` approvata da Marco il 12 novembre. Archivio locale con storia indipendente: non pubblicare main né importare lo storico. Dati/pesi/accessi fuori Git. Memoria condivisa in `context/memory/`; risultati essenziali in `SuperFlex/results/geometric_closure_v1/`.

HPC e quattro ambienti esistenti riusati; accesso con chiave già configurata, riferimento personale `scripts/abilita_accesso_hpc.ps1`, da non rieseguire. Non creare chiavi o chiedere password. Conservare run storici e quelli nuovi.

Prossimo passo: verificare i manifest completi del nuovo ponte offline P01_01 e la baseline effettiva, poi integrazione nel matcher, controllo a contributo zero, calibrazione sviluppo e test tracking separato. Il mapping ha ora codice e report del collega, ma non ancora una riproduzione indipendente sui suoi output. Obiettivo finale invariato, scadenza 23 novembre.

## Stato della pubblicazione — 12 novembre

**Pubblicazione su `main` completata e verificata**, su indicazione di Marco. Codice portabile, esempi, risultati essenziali e memoria ripulita ora visibili all'apertura della [repository comune](https://github.com/Federico-cia/Whareformer-SuperFlex-Project). `SuperFlex/` contiene il componente geometrico, `context/memory/` la memoria; dati grezzi, pesi e configurazioni personali restano esterni. `main` avanzato da `78eefcc` alla consegna `7cb56da`, senza conflitti o forzature; ramo `prepare/superflex-core` allineato. Entrambi i riferimenti remoti verificati. La storia indipendente del main locale non è stata pubblicata.

Controllo di riservatezza su 72 file e snapshot dei nuovi commit, inclusa revisione visiva dei due grafici: nessun segreto rilevato, nei limiti del controllo. Evidenza locale `shared_exports/publication_security_pre_main.json`. Il precedente blocco del push è storico e superato; nessun nuovo esperimento o beneficio tracking aggiunto dalla pubblicazione.

## Discussione successiva — adattatore

Marco chiede opzioni architetturali prima di procedere. Confronto e raccomandazione, non scelta adottata, nel registro voce 28. Nessun adattatore Whareformer implementato o nuovo esperimento in questa discussione.

## Pacchetto per il collegamento ai track

Preparato `shared_exports/compare200_tracking_inputs_v1.zip` (73.1 MB): 200 RGB, 299 maschere, 598 nuvole originali DA grezzo/MoGE, input compare200 con `selection_final.json`, script originale `acquire_compare200.py` e indice `observations_for_tracking.json`. CRC e SHA-256 di tutti i file verificati; RGB, maschere e nuvole concordano con la provenienza originale. Ricevuta tramite Marco richiesta del collega per mapping ai track e sperimentazione dell'accumulo: attività riferita, non verificata o adottata come metodo del progetto. Mapping detection/track non certificato; nuvole camera-frame da registrare prima della fusione, con gestione di scala e movimento dell'oggetto. Nessun nuovo job; checksum in `shared_exports/compare200_tracking_inputs_v1.json`. Il successivo caricamento richiesto da Marco è documentato sotto.

Marco richiede il caricamento del pacchetto su GitHub, ordinato e visibile su `main`. Collocazione selezionata: `SuperFlex/data_packages/compare200/`, archivio originale con README e checksum; eccezione puntuale alle esclusioni Git. Controllo interno su 1118 file completato, nessun pattern di segreto rilevato. **Pubblicazione riuscita su [main](https://github.com/Federico-cia/Whareformer-SuperFlex-Project/tree/main/SuperFlex/data_packages/compare200)**, commit del pacchetto `ee652a2`, riferimento remoto verificato. README collegato dall’indice principale e checksum disponibili; dati originali invariati.

## Prima analisi del collega — 13 novembre, prima del chiarimento sul ciclo

Le evidenze tecniche sotto restano valide; la raccomandazione di trattare l’accumulo come estensione separata è superata dalla direzione corrente in apertura e dalla voce 31 del registro.

Letti integralmente i sei file dei commit del 12 novembre `31e3943` e `ab5a946`; remoto `main` osservato a `ab5a946c1f94018edad90e69bc5544306f913569`. Eseguito soltanto fetch: worktree candidato ancora alla nostra revisione `71ce4f1`, nessun merge/push. Analisi autorevole: [ANALISI_AGGIORNAMENTO_GITHUB_20261113.md](ANALISI_AGGIORNAMENTO_GITHUB_20261113.md).

Implementati dal collega recupero ID delle osservazioni dalle predizioni e join alle nuvole compare200 per P01_01. Report: 110590 righe ricondotte esattamente alle annotazioni, 52 track; 71/73 geometrie collegate a 18 track, 9 con più osservazioni. Controllati accordo JSON/CSV e manifest originale; quattro controlli sintetici sui due script superati. Evidenza `outputs/github_review_20261113/verification.json`. Conteggi reali non riprodotti: non caricati output completi, manifest dei join, configurazione/checkpoint e metriche baseline. Track 9, 18 osservazioni di padella: coerenza visiva riferita dal collega, non ricontrollata qui. Track 4/36 con categorie miste: revisione prioritaria, non identità fisiche certificate.

**Conseguenza:** il ponte dati è avviato concretamente, il matcher geometrico resta assente dai nuovi upload. Acquisire/verificare manifest e baseline reali, diagnosticare i due mancati join e le track, quindi collegare la memoria causale e verificare peso zero. Accumulo multivista proposto nel README del collega: estensione distinta, non nuovo obiettivo adottato. Nessun job HPC avviato o coda ricontrollata in questa analisi; l'ultima osservazione HPC resta quella della consegna precedente.
