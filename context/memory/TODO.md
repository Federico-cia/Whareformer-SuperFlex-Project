# To-do corrente — collegamento alla baseline reale

## Passaggio a un altro provider AI — 14 novembre 2026

Marco richiede memoria e contesto autosufficienti nella cartella e su GitHub. Guida corrente: [LEGGIMI_PASSAGGIO_AI.md](LEGGIMI_PASSAGGIO_AI.md), che distingue implementato/verificato/pendente, decisioni, dipendenze e prossimi passi. Pubblicazione selettiva preparata dalla main del collega fc5aa30: codice integrazione, memoria, mappa corrente ed evidenze leggere; dati grandi, pesi e accessi esclusi. Nessun nuovo esperimento, filtro invariato. Gli stati storici di attesa frontend, output collega mancanti e job 763531 attivo sono superati dalle verifiche successive. Esito della pubblicazione in docs/CONDIVISIONE.md e context/evidence/publication_inventory.json sul remoto.

- [x] Mappa nella cartella dedicata mappa_interattiva/ della repository locale, con README.md canonico, inventario, avvio e istruzioni di ripresa in altra chat. LEGGIMI rimanda al README; backup esclusi da Git. Nessuno spostamento dei file applicativi, nessun commit/push. contenuti.json invariato per hash; preservare le schede manuali B01/B02/B03 ed E01/E02/E03.


- [x] Verificata persistenza della revisione manuale di B01/B02/B03 ed E01/E02/E03: JSON valido, copia JS offline e servizio identici; 12 backup, nessun temporaneo residuo. Browser con conferma Salva e nessun modulo aperto. Verifica del salvataggio, non approvazione scientifica; contenuti invariati.


## Frontend approvato e percorso cache verificato — 14 novembre

Ok di Marco ricevuto. Implementati contratto e import cache verificato, ingresso --frontend-manifest nel comando unico; dieci detection nei tre frame con intera storia di 3398 frame, quattro file dati byte-identici. 72 casi locali (70 passati, due skip motmetrics). Rigenerazione da RGB ancora non eseguita: pesi/revisione DINOv2, provenienza PCA e scala/ambiente scena da verificare, inventario circoscritto senza prova di assenza globale. [Avanzamento e limiti](FRONTEND_AVANZAMENTO_20261114.md). Piano parzialmente eseguito, non dichiarato completo; filtri invariati. 763531 concluso 0:0 in 23m24s, nove varianti zero completate e valutate; nessun nuovo job del frontend. Le note di attesa dell’ok e job ancora attivo sono storiche.

- [x] Completati i tre segnaposto di B01/B02 nella mappa: EPIC-KITCHENS, provenienza VISOR e modulo di segmentazione (SAM 2 come esempio da valutare, con inizializzazione esplicita). Resto dei campi preservato. Marco chiarisce che le parentesi quadre nei suoi testi sono richieste di completamento da parte dell’assistente. Nessuna adozione o implementazione di un segmentatore. Fonte primaria consultata: https://github.com/facebookresearch/sam2.


- [x] Preparare piano del frontend unificato, senza eseguirlo.
- [x] Ricevuto ok di Marco per il frontend.
- [x] Implementare contratto/cache e verificare pilota reale con storia preservata.
- [ ] Identificare asset/provenienza DINOv2/PCA/scena, implementare e verificare rigenerazione sul pilota; piano ancora parziale.

## Piano frontend preparato, attesa dell’ok — 14 novembre

Marco richiede pianificazione prima dell’esecuzione. Proposto collegamento preprocessing → runner: inventario dipendenze, manifest unico, import/rigenerazione con cache, comando unico e piccolo pilota P01_01 mantenendo la storia del tracker. [PIANO_FRONTEND_UNIFICATO_20261114.md](PIANO_FRONTEND_UNIFICATO_20261114.md). Piano non ancora approvato: nessuna implementazione o nuovo job per questo step prima dell’ok. Filtri ancora rinviati; job precedentemente autorizzati invariati, senza nuovo controllo di stato in questa fase.

- [x] Abilitare modifica/salvataggio descrizioni dei collegamenti e semplificare scheda maschere/titoli, preservando le modifiche manuali.
- [ ] Nella compilazione delle prossime schede usare spiegazioni comprensibili anche alla giuria, definendo i termini necessari.

## Valutatore e comando unico collegati — 14 novembre

Implementati export delle osservazioni/assegnazioni con hash, IDF1/mPCL originali con scope esplicito e comando input preparati → varianti → valutazione → tabella. 763498 COMPLETED/0:0 (33 s), otto test; 763530 COMPLETED/0:0 (45 s), 69 test tutti eseguiti, riprodotti IDF1 73.269735% e mPCL 70.465504% su predizioni registrate train. 763531 RUNNING a 10m50s nell’ultima osservazione: nove configurazioni zero, CPU e cache esistente; esito ancora da acquisire. [COMPLETAMENTO_PIPELINE_20261114.md](COMPLETAMENTO_PIPELINE_20261114.md).

**GPU concluso:** 763324 COMPLETED/0:0 (43m30s), sei ricostruzioni reali ready e controllo zero esatto, ma nessuna fusione multivista ammessa. Filtri invariati e revisione ancora rinviata. Mancano unificazione del frontend dati, copertura sufficiente e calibrazione/test; il comando attuale parte da input preparati. Le precedenti note di metriche non collegate e GPU ancora attivo sono storiche.

- [x] Salvataggio diretto delle sole descrizioni dei riquadri tramite servizio locale: Modifica/Salva, backup e controllo conflitti; guida aggiornata.

- [x] Revisione UX/UI mappa: pannello sinistro richiudibile, zoom/pan e vista completa; verifica visiva e interazioni effettive nel browser.


## Revisione dei filtri di fusione — rinviata da Marco

- [ ] Rivedere criteri e soglie provvisori introdotti nel prototipo per ammettere la fusione delle nuvole, in particolare ambiguità di posa/simmetrie e sovrapposizione bidirezionale con viste parziali. **Non avviare ora: Marco ne richiede esplicitamente il rinvio.** Separare associazione alla track e ammissione dei punti; confrontare i criteri con evidenze indipendenti prima di modificarli. Le soglie attuali non sono prescrizioni dei paper né parametri calibrati. Nessuna modifica al codice o ai job in questa fase.

- [x] Prima mappa HTML locale: nodi trascinabili, schede di nodi/frecce, modifica e import/export; [guida](mappa_interattiva/LEGGIMI.md).
- [ ] Revisionare con Marco le prime schede RGB/maschere/aspetto e i tre collegamenti; completare progressivamente gli altri contenuti. Segnaposto distinti da informazioni verificate.

- [x] Estrarre cause e valori dei gate del 763323: audit numerico in RIPRESA_HPC_20261114.md.
- [ ] Verificare simmetrie/pose equivalenti e penalizzazione delle viste parziali nei rifiuti, con controlli indipendenti; nessuna soglia allentata automaticamente.

- [x] Audit dei motivi di rifiuto 763323: isolati due casi tagliere 5099 respinti per sola ambiguità; restanti quattro per supporto/residui.
- [ ] Diagnosticare equivalenza delle pose simmetriche e gate per viste parziali senza assumere errate le associazioni o rilassare automaticamente le soglie. [Dettagli](RIPRESA_HPC_20261114.md).

- [x] Scomporre le 12 inizializzazioni del 763323: tre track in quattro rappresentazioni; solo tagliere/coltello hanno viste successive, padella esclusa dai tentativi di fusione. [Audit](RIPRESA_HPC_20261114.md).

## Runner comune e misure implementati — 14 novembre

Disponibili W0/G0/S-separata/S-accumulo/P-accumulo, DA/MoGE, memorie e modelli indipendenti, controllo sui punti ammessi e report JSONL/JSON/CSV con copertura, fallimenti, byte di payload e costi dei replay. 58 test locali superati; esempio a peso zero, tracking metrics ancora non calcolate. Nessuna nuova run reale del runner comune né modifica dei job esistenti. [RUNNER_VARIANTI_20261114.md](RUNNER_VARIANTI_20261114.md). Prossimo: collegare valutatore tracking e protocollo/copertura di calibrazione-test.

**HPC verificato durante il lavoro:** 763322 COMPLETED/0:0 (9m56s), 763323 COMPLETED/0:0 (12m11s), zero esatto; nel secondo solo 12 inizializzazioni e 12 rifiuti, nessuna fusione, conteggi sulle quattro rappresentazioni. 763324 RUNNING a 29m19s con almeno un risultato neurale reale ready; esito complessivo ancora da acquisire. [Dettagli HPC](RIPRESA_HPC_20261114.md). Le indicazioni precedenti di job CPU attivi/GPU in attesa sono storiche.

## Piano approvato — 14 novembre

- [x] Registrare autonomia per selezione/calibrazione, confronto finito e qualità per fase nel [piano corrente](ROADMAP_CICLO_GEOMETRICO.md); confermati SuperFlex dopo ogni aggiornamento ammesso e perimetro limitato sulla contaminazione.
- [ ] Completare runner comune, controllo punti e aggregatore usando gli esiti già avviati, senza duplicare run.
- [ ] Predisporre casi/split di sviluppo, viste escluse, criteri e budget di ricerca; verificare mapping RGB→3D e texture.
- [ ] Implementare e confrontare alternative geometriche/calibrazione automatica: 24 combinazioni nominali più riferimento esistente; salvare configurazioni e fallimenti.
- [ ] Valutare finaliste in SuperFlex/tracking e calibrare contributo geometrico; verificare interazioni con ablation comparabili.
- [ ] Congelare scelte e svolgere test separato, riportando qualità, copertura, variabilità e costi. Approvazione distinta dai risultati ancora mancanti.

- [x] Recuperare esiti 761899/761905 e lanciare le verifiche approvate sviluppate durante il blocco HPC.
- [x] Acquisire controller e verifica zero di 763322/763323; 763321 completato.
- [x] Acquisire esito finale 763324: sei ricostruzioni da inizializzazioni e zero fusioni; nessun beneficio dedotto dal controllo zero.
- [ ] Acquisire esito 763531, prima pipeline unificata a peso zero con valutazione/tabelle.
- [ ] Unificare ingresso dei frame/maschere/metadati e preprocessing nel formato comune, senza scegliere un nuovo segmentatore o promettere RGB-only.

## HPC ripristinato, arretrati inviati — 14 novembre

SSH/accounting/coda accessibili. Recuperati 761899 (prefisso storico a peso zero esatto, 3398 frame/10264 detection, zero differenze dal collega) e 761905 (IDF1 73.2697% sulle predizioni registrate train, non test). Nuovi job: 763321 COMPLETED/0:0, 50 test ambiente passati; 763322 replica aggiornata e 763323 accumulo RUNNING nell’ultima osservazione; 763324 SuperFlex differita PENDING per dipendenza dai due CPU. Nessun nuovo esito sperimentale ancora dichiarato; prossima acquisizione dei risultati. [RIPRESA_HPC_20261114.md](RIPRESA_HPC_20261114.md). Le note precedenti sul blocco DNS e sui due esiti ancora da leggere sono storiche.

## Discussione precedente all'approvazione — 14 novembre

- [x] Valutare pulizia/FPFH-RANSAC-ICP/accumulo/SuperFlex/Chamfer rispetto allo stato corrente: [parere](PARERE_PROPOSTA_COLLEGA_20261114.md).
- [x] Spiegare problemi e alternative con pro/contro; approfondimento nello stesso parere. Nessuna variante adottata automaticamente.
- Il confronto FPFH e la calibrazione sono ora inclusi nel piano approvato in apertura; esecuzione e risultati restano pendenti. Le indicazioni precedenti di sola raccomandazione sono superate.

## SuperFlex differita collegata — 14 novembre

Implementate richieste da nuvola/versione ammessa, worker sulla pipeline esistente, verifica/importazione e pubblicazione della forma nei soli frame successivi. Replay seriale bloccato fino agli esiti, ultima forma conservata su fallimento; completamenti esclusi dai punti osservati. 43 controlli locali passati con sostituti dichiarati, nessuna nuova inferenza reale/HPC. Runner predisposto con --accumulate --reconstruct; prossimo confronto comune delle varianti e aggregazione delle misure. [SUPERFLEX_DIFFERITA_20261114.md](SUPERFLEX_DIFFERITA_20261114.md). Le note precedenti sul collegamento SuperFlex ancora mancante sono storiche; validazione reale 2B e risultati HPC pendenti invariati.

## Registrazione/accumulo collegati — 14 novembre

Collegato il candidato esistente al coordinatore: inizializzazione, registrazione rigida e accumulo ammesso, con isolamento delle sorgenti, versioni/provenienza e conservazione dello stato su rifiuto/errore. 35 test locali passati; input sintetici e componenti controllati, nessun replay reale o HPC. Runner predisposto con --accumulate (default disattivato), preparatore con punti camera/hash; non eseguiti in questa fase. Prossimo: SuperFlex differita dalla nuvola accettata. Il matcher usa ancora forme separate; risultato reale 2B invariato (0/12). [COLLEGAMENTO_ACCUMULO_20261114.md](COLLEGAMENTO_ACCUMULO_20261114.md). Le indicazioni precedenti sul collegamento ancora mancante sono storiche.

## Coordinatore del frame completato — 14 novembre

Implementato e collegato al runner: confronto/associazioni prima, commit delle forme e proposte geometriche dopo; versioni distinte, stato valido preservato per mancanti/rifiuti/errori. 27 controlli locali passati (11 nuovi), con metodi originali e componenti controllati; nessuna verifica Torch o run HPC. Il runner aggiorna ancora solo forme separate: prossimo collegamento del candidato registrazione/accumulo, poi SuperFlex differita. Esiti HPC e validazione 2B invariati. Resoconto: [COORDINATORE_FRAME_20261114.md](COORDINATORE_FRAME_20261114.md). Le indicazioni sottostanti sul coordinatore ancora da implementare sono storiche.

- [x] Rappresentare il risultato atteso in una mappa del ciclo input → associazione → memorie, distinguendo architettura obiettivo e stato effettivo: [MAPPA_FLUSSO_SISTEMA.md](MAPPA_FLUSSO_SISTEMA.md).
- [x] Proporre correzioni e struttura delle schede per blocchi/frecce della mappa: [PROPOSTA_ANNOTAZIONI_MAPPA_20261114.md](PROPOSTA_ANNOTAZIONI_MAPPA_20261114.md); proposta documentale, non ancora approvata.
- [ ] Compilare sistematicamente le schede dei riquadri e dei collegamenti a partire dalle evidenze correnti, con stato software distinto dai risultati sperimentali; formato ancora proposto.
- [x] Precisare gli ingressi del ramo posizione EPIC nel diagramma tramite lettura del codice locale: RGB/profondità, maschera/bounding box, intrinseci, posa e scena baseline; nessuna rigenerazione.
- [ ] Trasferire la mappa in un supporto collaborativo in Space: presentazione privata vuota già creata, editor bloccato nell'ambiente corrente; Page ID e limite in STATO_LAVORO.md. Nessuna lavagna o condivisione completata.

- [x] Punto 1: integrazione riutilizzabile implementata e controllata localmente.
- [x] Coordinatore causale: associazioni effettive, versioni/stato valido e interfaccia di proposta controllati localmente.
- [x] Collegare candidato registrazione/accumulo al coordinatore; controlli locali superati, validazione reale pendente.
- [x] Collegare nuvola/versione ammessa a SuperFlex differita e pubblicazione causale; verifiche locali superate, inferenza reale rinviata.
- [x] Runner/configurazioni comuni, controllo punti accumulati e aggregazione misure/costi/copertura/fallimenti; 58 controlli locali, nessuna valutazione reale del nuovo runner.
- [x] Collegare valutatore tracking originale ai nuovi export con hash/scope; otto test metriche e suite completa 69 verificati su HPC.
- [ ] Predisporre/congelare copertura e calibrazione-test nel piano approvato prima della valutazione finale.

## Punto 1 software completato — 14 novembre

Implementato componente riutilizzabile con tre modalità, quattro rappresentazioni e delega al matcher originale; runner e preparatore aggiornati. Passati 16 controlli locali (7 adapter + 9 wrapper), con modello/tensor controllati; verifica Torch/frame reali rinviata. Nessun accesso HPC o nuovo esperimento. Prossimo lavoro: punto 2, coordinatore causale e stato geometrico versionato. Resoconto: [INTEGRAZIONE_RIUTILIZZABILE_20261114.md](INTEGRAZIONE_RIUTILIZZABILE_20261114.md).

## Priorità corrente — sviluppo senza HPC, 14 novembre

Marco dispone di sviluppare il progetto e rimandare gli esperimenti. Sospesi i tentativi di connessione come attività prioritaria; il recupero di 761899/761905 resta pendente alla ripresa. Ordine operativo: integrazione riutilizzabile → coordinatore causale → interfaccia SuperFlex differita → runner/controlli locali → pacchetto sperimentale. Piano e criteri in [PIANO_SVILUPPO_SENZA_HPC_20261114.md](PIANO_SVILUPPO_SENZA_HPC_20261114.md). Nessun nuovo esperimento o risultato; 2B resta non validato, parametri/protocollo finale non fissati da questa revisione.

Mandato esecutivo approvato l'11 novembre: sviluppare codice ed eseguire le run HPC necessarie per concludere la parte autonoma. Piano e criteri: [PIANO_CHIUSURA_RAMO_GEOMETRICO.md](PIANO_CHIUSURA_RAMO_GEOMETRICO.md). Stato verificato e asset: [STATO_LAVORO.md](STATO_LAVORO.md).

## Consegna autonoma — completata

- [x] Pipeline portabile DA/MoGE → punti → SuperFlex, provenienza, fallimenti e ripresa verificati.
- [x] Audit delle annotazioni originali: documentate semantica, alternative e limiti; nessuna identità globale inventata.
- [x] Valutazione consolidata su risultati disponibili: stabilità/discriminatività, copertura, fallimenti e costi; diagnostica locale separata.
- [x] Export di 299 osservazioni e memoria causale configurabile; 11 test ed esempio eseguibile verificati.
- [x] Codice, figure e istruzioni consegnati; rapporto [CONSEGNA_RAMO_GEOMETRICO.md](CONSEGNA_RAMO_GEOMETRICO.md).

## Pubblicazione richiesta il 12 novembre

- [x] Consegna selezionata pubblicata su `main`: codice, esempi, risultati essenziali e memoria ripulita. Riferimento remoto verificato; esclusa la storia indipendente del main locale.

## Direzione corrente

Ciclo unitario confermato da Marco: aggiornamento geometrico parte dell’integrazione, non sola estensione esterna. Piano e criteri in [ROADMAP_CICLO_GEOMETRICO.md](ROADMAP_CICLO_GEOMETRICO.md). Le note precedenti su accumulo opzionale sono superate da questo chiarimento.

## Avanzamento autonomo autorizzato

- [x] Individuare componenti indipendenti; implementare candidato di adattatore 2A, sette test superati e replay tecnico su geometrie esistenti di tre frame, senza inferenza tracking. Evidenze e limiti in [AVANZAMENTO_AUTONOMO_20261113.md](AVANZAMENTO_AUTONOMO_20261113.md).
- [x] Implementare il candidato accumulatore e registrazione con export di trasformazioni/qualità: sette nuovi test finali e due piccoli piloti reali eseguiti. Tutti i 12 aggiornamenti reali rifiutati; implementazione verificata nei controlli, efficacia reale non validata. Report [RISULTATI_REGISTRAZIONE_ACCUMULO_20261113.md](RISULTATI_REGISTRAZIONE_ACCUMULO_20261113.md).
- [ ] Diagnosticare separatamente ambiguità di posa e differenze di geometria/scala; progettare controlli con informazione RGB indipendente e/o similarità esplicita, senza limitarsi a rilassare i gate.
- [ ] Su accumulo reale accettato eseguire SuperFlex e collegare la forma aggiornata al prototipo con ordine causale. Non avviato: nessun accumulo reale supera attualmente i controlli.
- [x] Recuperare checkpoint/feature ufficiali e verificare configurazione/versione: acquisiti, audit su 110590 osservazioni senza differenze di metadati/XYZ. Report [INTEGRAZIONE_BASELINE_REALE_20261113.md](INTEGRAZIONE_BASELINE_REALE_20261113.md).
- [x] Controllo con checkpoint reale e input controllati: job 761872 completato, 120 casi a peso zero superati. Non equivale a replica sul video.
- [ ] Recuperare esito della replica reale 761899 (3398 frame/10264 detection; ultima osservazione RUNNING a 3000 frame) e IDF1 numerico di 761905 (COMPLETED). Dal 14 novembre accesso bloccato da DNS; provare VPN Bocconi. Non rilanciare prima di verificare gli output esistenti.

## Avvio step 1 — roadmap approvata

- [x] Registrare approvazione di Marco, ricontrollare remoto e cercare gli asset nei percorsi accessibili; nessun nuovo upload completo trovato.
- [x] Preparare riferimento P01_01 e controllo del contratto JSON; sei casi sintetici superati. Dettagli in [STEP1_CONTRATTO_TRACKING.md](STEP1_CONTRATTO_TRACKING.md).
- [x] Ricevuti i manifest completi a bbf0e5e: audit reale del join passato (71/73), 146 nuvole e 71 box VISOR verificati; tavole delle track 4/36/9/35 revisionate. Report [VERIFICA_CONSEGNA_WHAREFORMER_20261113.md](VERIFICA_CONSEGNA_WHAREFORMER_20261113.md).
- [x] Verificare configurazione/versione/checkpoint, input e ordine feature/XYZ della run; acquisiti anche README/patch/CSV a fc5aa30, mPCL del singolo video ricalcolato secondo aggregatore originale.
- [ ] Completare provenienza JPEG dei due alias VISOR/RGB e verifica finale della replica baseline sul prefisso. Step 1 completo ancora aperto; non richiedere nuovamente gli asset già acquisiti.

## Dipendenze della fase comune

- [x] Preparato e verificato pacchetto RGB/maschere/nuvole/manifest/script per il mapping ai track: `shared_exports/compare200_tracking_inputs_v1.zip`. Caricato su `main` in `SuperFlex/data_packages/compare200/`, con README e checksum; contenuto e limiti in `STATO_LAVORO.md`.
- [x] Analizzare l'upload del collega del 12 novembre: due script di mapping, report P01_01 e README. Verificate coerenza dei report, corrispondenze nel pacchetto e quattro casi sintetici; dettagli in [ANALISI_AGGIORNAMENTO_GITHUB_20261113.md](ANALISI_AGGIORNAMENTO_GITHUB_20261113.md).
- [x] Acquisire/verificare manifest e join reale a bbf0e5e, provenienza della run e CSV a fc5aa30.
- [x] Verificare ordine detection/feature/XYZ su tutte le osservazioni ufficiali; hash nuvole e revisione visiva disponibili effettuati. Questo non certifica identità fisiche globali.
- [ ] Completare provenienza temporale/JPEG dei due alias. Non convertire track predette in ground truth.
- [ ] Completare il collegamento nel ciclo reale delle detection e della memoria; altri quattro video compare200 non coperti dai report caricati. Definire la copertura geometrica necessaria alla valutazione tracking prima di nuovi calcoli.
- [ ] Integrare il contributo geometrico e verificare equivalenza alla baseline con contributo zero; calibrare sullo sviluppo e valutare tracking su test separato con associazioni predette.

- [ ] Sviluppare e verificare il ramo associazione→registrazione/accumulo→nuova inferenza SuperFlex su associazioni baseline fisse, con rifiuto degli aggiornamenti non affidabili.
- [ ] Chiudere il ciclo completo con memoria precedente comune al frame, associazioni predette e aggiornamenti successivi; verificare causalità, recupero a peso zero e conservazione dello stato valido.
- [ ] Confrontare baseline, accumulo senza influenza sul matching, forme separate, ciclo accumulativo e controllo punti; fissare protocollo/copertura e calibrare solo sullo sviluppo.

La roadmap mantiene la direzione unitaria approvata. I job diagnostici sopra sono stati eseguiti; il loro stato osservato non certifica un beneficio tracking né fissa automaticamente i parametri scientifici.

## Già concluso — riusare

Setup dei modelli, piloti e diagnostici, confronto 200, precalcolo 8797 coppie, prima revisione visiva, validazione numerica del nucleo pubblicato e accesso HPC senza password. Evidenze e limiti in `STATO_LAVORO.md` e resoconti collegati. Job di chiusura conclusi, nessun job attivo nell’ultima verifica; dettagli nello stato.

Registrazione e accumulo entrano nel ciclo da sviluppare secondo il chiarimento corrente; la consegna autonoma storica resta conclusa. SAM3, training da zero ed estensioni robotiche non diventano prerequisiti. DA e MoGE restano entrambi attivi; il test finale non si usa per scegliere il metodo.
