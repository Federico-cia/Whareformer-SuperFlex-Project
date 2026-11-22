> **Archivio storico, congelato prima del riordino del 22 novembre 2026.** Gli stati e le istruzioni qui riportati possono essere superati. [Stato corrente](../../memory/STATO_LAVORO.md) · [Indice storico](README.md). Contenuto originale conservato; solo collegamenti relativi adattati nella copia leggibile. Originale byte per byte in originali.zip.

# Stato del lavoro e ripresa

## Dataset Drive e allineamento — 22 novembre 2026, ore 21:30

- **786129** (riorganizzazione per tipo): 15/15 blocchi divisi, verificati (MD5 Drive) e rimossi dall'HPC, circa 7.5 GB liberati; alle 21:14 ancora RUNNING sul caricamento degli input della run. Riepilogo finale, README e CATALOGO da verificare con `drive_9`.
- Effetto collaterale: la rimozione delle mappe DA dense (19:48–20:52) è avvenuta mentre l'altra chat calcolava alpha/beta (786174); i blocchi 0000–0003 sono risultati `dense_map_missing` (1014 frame, 2045 osservazioni). Dati integri su Drive.
- **786275** `cv_ab_restore` inviato, PENDING per `QOSMaxJobsPerUserLimit` (massimo 2 job attivi): recupera da Drive le mappe DA di 0000–0003 in una radice d'appoggio e applica lo stesso `alpha_beta_p01.py`; output in `~/cv_project/alpha_beta_restore_20261122_v1/out/`.
- Preparati, non eseguiti: `strumenti_hpc/superflex_allineato/` — ricostruzione locale delle nuvole allineate a piena risoluzione di tutti i 15 blocchi (v2) e job GPU `cv_sf_aligned` (SuperFlex per osservazione, ingressi FPS-4096 come la memoria; ripartibile; caricamento su Drive in `03_nuvole/da_allineata`, `04_superquadriche/da_allineata`).
- Accesso di Federico al Drive: non prioritario (Marco).
- **786275 COMPLETED 0:0** (3m10s): alpha/beta per 1014 frame dei blocchi 0000–0003, 1006 allineamenti validi. Nuvole allineate v2 in `outputs/aligned_fullres_p01_20261122_v2/`: 8106 osservazioni (438 audit, 5635 da 786174, 2034 da 786275), 24 identità, 2427 frame; 19 escluse, 1 fallita (profondità non positiva). v1 interamente contenuta, identica su 300 nuvole campionate. Archivio di trasferimento `strumenti_hpc/superflex_allineato/aligned.tar` (sha256 42af0a76…), pronto per `cv_sf_aligned`.
- **786329** `cv_sf_aligned` RUNNING su gnode01 dalle 21:55 (nuvole e runtime verificati per hash all'invio); 786129 non più in coda.
- **786129 COMPLETED**: 15 riorganizzati, 0 falliti, 7 491 881 373 byte liberati sull'HPC, input della run caricati e verificati, `DRIVE_REORG_OK` (21:27).
- **786252** (prova CPU della griglia, frame ≤ 4300, 1321 frame): W0 in 15 s; `c05_m025` completata in 3108 s, con rallentamento concentrato negli ultimi frame (frame 1000 a 92 s, poi circa 9 s/frame); `c07_m025` in corso al controllo delle 21:58, limite del job 2 h. Costo della memoria per configurazione da profilare prima della prova GPU e della griglia: estrapolato al video intero non è sostenibile.
- File superati (script monouso conclusi, versioni sostituite, cache) raggruppati in `../_da_eliminare/` con `INDICE.md`; nessuna cancellazione.

## Una sola chat da qui in avanti — 22 novembre 2026, sera

Marco lavorerà con una sola chat: il vincolo di lavoro parallelo (memoria da una parte, Drive/HPC dall'altra) decade. Lo stato della parte memoria è completo in [MEMORIA_OPZIONE_A_E_SELEZIONE_20261122.md](../../evidence/ASSET_ESTERNI.md#asset-4e8c91f83dce) e nelle sezioni della sera qui sotto. Pendenti al passaggio: job 786252 `cv_mem_grid` (prova CPU) RUNNING all'ultimo controllo, esito da leggere con `strumenti_hpc/memory_grid/2_controlla_prova_griglia.bat`; prova GPU `4_invia_prova_gpu.bat` preparata, non inviata; recupero da Drive delle mappe dense dei blocchi 0000–0003; conferma che la rimozione delle mappe dense dall'HPC durante `cv_drive_reorg` 786129 fosse voluta.

## Prova CPU della griglia in corso, prova GPU completa pronta — 22 novembre 2026, sera

Marco sceglie la strada A: prima la prova CPU (punti osservati), poi la prova completa su GPU con SuperFlex. **Job 786252 `cv_mem_grid` RUNNING su gnode02 dalle 21:00 (ora HPC)**; remoto `~/cv_project/memory_grid_smoke_20261122_v1/` (pacchetto verificato, `out_786252/`, `logs/grid_786252.*`). Quota al momento dell'invio 35.20/46.56 GiB, 367k/500k file. In coda anche `cv_drive_reorg` 786129 dell'altra chat. Controllo `strumenti_hpc/memory_grid/2_controlla_prova_griglia.bat`.

Prova GPU preparata, non inviata (`4_invia_prova_gpu.bat`, controllo `5_…`; job `cv_mem_grid_gpu`, 1 GPU, limite 4 h): calcola sull'HPC gli ingressi FPS-4096 delle 1403 osservazioni allineate (`prepare_observation_superflex.py`, 4 processi; 0.6 s/osservazione misurati in locale), SuperFlex con `scene_superflex_worker.py` e runtime `portable_validation_v1/config.json`, raccolta descrittori (`collect_query_features.py`), poi griglia in modalità `da_raw_superflex` (worker SuperFlex caricato una sola volta). Riusa le nuvole già caricate con la prova CPU. Primo uso reale del worker SuperFlex su ingressi FPS di scena: nessun esito precedente registrato.

Scelta tecnica dell'assistente, da confermare per il dataset: le forme SuperFlex per osservazione del pacchetto ricevuto sono calcolate su DA grezza in coordinate camera; la memoria usa DA allineata. La correzione affine della profondità cambia le proporzioni della nuvola (es. tagliere: terzo asse normalizzato 0.021 grezzo vs 0.027 allineato), quindi nella prova le forme delle osservazioni vengono ricalcolate sulle nuvole allineate, come fa il driver P01_02. Per il dataset condiviso conviene includere SuperFlex sulle nuvole allineate.

## Strumento della griglia sul sistema completo pronto, prova HPC da avviare — 22 novembre 2026, sera

`integration_prototype/run_memory_grid.py`: per ogni configurazione della memoria esegue tracker Whareformer originale del bundle (`full_video_20261114`), GeometryMatcher e memoria opzione A (`MultiHypothesisPipeline` con `position_config`), fino a `final_frame`, poi IDF1 e mPCL con il valutatore verificato degli autori (ambito `diagnostic_prefix`); include sempre la baseline W0. Parametri solo dal file della griglia (nessun valore predefinito); rappresentazione `da_raw_points` (CPU) oppure `da_raw_superflex` (worker GPU e descrittori SuperFlex delle osservazioni obbligatori). Verifica che le identità delle nuvole allineate coincidano con le detection del bundle. Aggiunta a `PositionStateMemory` la risoluzione relativa per traccia (voxel 0.04 R, densità 0.1 R del primo raggio valido, come nell'export), con test; suite memoria 18 casi OK.

Controlli locali: bundle fino al frame 4300 = 1321 frame annotati; 1403 osservazioni con nuvola allineata, zero discrepanze di identità; descrittori delle osservazioni 0.16 s ciascuno. Il tracker richiede PyTorch, non installabile nell'ambiente di lavoro dell'assistente: esecuzione reale sull'HPC (ambiente `cv-superflex`, motmetrics dalle ruote `recorded_metrics_v2` come nella campagna del 15 novembre).

Prova di funzionamento preparata in `strumenti_hpc/memory_grid/` (non avviata): pacchetto 105 MB (codice, sottoinsieme delle nuvole fino al frame 4300, verificatore prudente, `grid_smoke.json` con W0 + due configurazioni e peso del matcher 0.1 come segnaposto del punto 2). Serve solo a verificare il collegamento end-to-end, non a scegliere parametri. Avvio `1_invia_prova_griglia.bat`, controllo `2_…`, scarico `3_…`. Spostato in `_to_delete/` un file vuoto creato per errore (`test_position_state_memory.py.tmp`): eliminazione non consentita nella cartella.

## Nuvole allineate a piena risoluzione pronte — 22 novembre 2026, sera

Scaricati gli esiti del job 786174 (`strumenti_hpc/alpha_beta_p01/out/`). Costruite in locale con `integration_prototype/build_aligned_fullres.py` le nuvole allineate a piena risoluzione: `outputs/aligned_fullres_p01_20261122_v1/` (459 MB), 6073 osservazioni (438 del campione con alpha/beta dell'audit, 5635 dei blocchi 0004–0014), 21 identità, 1362 frame, 44.5 milioni di punti, nessun fallimento; hash delle nuvole grezze verificati. Per tutte le 438 osservazioni del campione i punti dell'audit sono contenuti nella nuvola completa (distanza massima 5.3e-7). Identità più frequenti: chopping board 1179, carrot 1123, tap 1080, sink 876, knife 852, courgette 607, pan 187. Restano fuori 2045 osservazioni dei blocchi 0000–0003 (mappe dense da recuperare da Drive). Prossimo passo: memoria opzione A su queste nuvole, configurazione iniziale ed export per il compagno; runner end-to-end sul segmento.

## Job alpha/beta 786174: esito — 22 novembre 2026, sera

**786174 COMPLETED 0:0**, 2m47s, gnode04 (`strumenti_hpc/alpha_beta_p01/esito_job.txt`, 20:25 ora HPC). Riproduzione dell'audit: 40/40 osservazioni del campione con alpha e beta identici (differenza massima 0.0) e stessi pixel statici: la procedura coincide con quella dell'audit 783586. Blocchi 0004–0014: 1035 frame, tutti `ok` e allineamento valido. Blocchi 0000–0003: 1014 frame `dense_map_missing`. Al controllo delle 19:58 i blocchi 0002 e 0003 avevano ancora le mappe (221 e 112): sono state rimosse fra il controllo e l'avvio, mentre era in esecuzione `cv_drive_reorg` 786129 dell'altra chat (inferenza dalla tempistica, non verificata nei suoi log). Le mappe mancanti risultano archiviate su Drive (ricevute ok della chat Drive/HPC); recupero da concordare. Risultati remoti in `~/cv_project/alpha_beta_p01_20261122_v1/out/`, da scaricare con `3_scarica_alpha_beta.bat`.

## Riferimento corrente per la memoria geometrica — 22 novembre 2026, sera

**Leggere prima [MEMORIA_OPZIONE_A_E_SELEZIONE_20261122.md](../../evidence/ASSET_ESTERNI.md#asset-4e8c91f83dce)**: decisioni di Marco (opzione A, criterio C, nuovo stato al ritorno, piena risoluzione, selezione dei parametri sul sistema completo), funzionamento attuale, procedura di scelta, ostacoli, costo SuperFlex e checklist. Le sezioni sottostanti della stessa sera sono cronologia; dove divergono prevale il documento. Prossimo passo: leggere l'esito del job 786174 (`strumenti_hpc/alpha_beta_p01/2_controlla_alpha_beta.bat`), ricostruire le nuvole allineate a piena risoluzione, preparare il runner end-to-end sul segmento di 75 s; chiedere al compagno stato e formato del punto 2.

## Pulizia locale dei duplicati — 22 novembre 2026, sera

Su autorizzazione di Marco eliminati dal PC due archivi duplicati (circa 2.05 GB): `outputs/compare200_749968.tar.gz` (1018535812 byte; 6186 file tutti in `outputs/compare200_749968/`) e `shared_exports/handoff_20261110_194816_586349/compare200_geometry_and_inputs.tar.gz` (1035952068 byte; 6432 file in `outputs/compare200_749968/`, `data/compare200/`, `data/epic_pilot/`). Prima della cancellazione `tar --compare` su tutti i file: nessuna differenza di contenuto o dimensione, solo permessi/proprietario. Nota nel pacchetto handoff. Conservati: data/, output del punto 3 e del verificatore, pacchetto P01_01 per il compagno (eliminabile dopo la consegna), ambienti locali. Proposta non eseguita: spostare su Drive `outputs/hpc_storage_recovery_20261121` (archivio da non perdere) e `outputs/full_video_20261114` prima di liberarli.

## Selezione dei parametri della memoria sul sistema completo — 22 novembre 2026, sera

**Indicazione di Marco:** la scelta di soglia e margine del test di posizione non deve essere una soluzione provvisoria su una metrica sostitutiva; va pensata e valutata con la memoria collegata al resto del sistema (tracking completo). Superata la proposta di selezione sull'utilità prequenziale come criterio finale.

Analisi dell'assistente, nessuna esecuzione. Ostacoli verificati nei documenti: (1) il consumatore della memoria nel matcher (punto 2, compagno) non è concluso; con l'adattatore geometrico esistente le 29 configurazioni della campagna del 15 novembre hanno dato assegnazioni identiche alla baseline (IDF1 73.269735%, mPCL 70.465504%), quindi oggi ogni soglia darebbe la stessa metrica; (2) geometria disponibile su 15/216 blocchi di P01_01 (circa 7% del video, più il campione sparso): il tracking su video intero richiede nuvole per tutte le osservazioni, bloccate dalla capacità HPC; (3) il punto 2 verrà addestrato su export della memoria, quindi configurazione della memoria e punto 2 dipendono l'una dall'altro. Proposta: la selezione finale diventa parte della taratura del sistema completo (griglia di configurazioni della memoria × pipeline intera con il punto 2 addestrato, metriche ufficiali IDF1/mPCL su P01_01 e P01_02), preparando ora il runner su segmento e una configurazione iniziale dichiarata come inizializzazione per generare i dati del punto 2. Da chiarire con il compagno: stato del punto 2 e se usa punti osservati o forme SuperFlex (in quel caso ogni configurazione richiede inferenza GPU per ogni versione della forma).

## Job alpha/beta 786174 in esecuzione — 22 novembre 2026, sera

Primo invio rifiutato dallo scheduler (`QOSMaxSubmitJobPerUserLimit`: array di 16 task oltre il limite di invii per utente), nessun job creato; esito conservato in `strumenti_hpc/alpha_beta_p01/esito_invio_tentativo1_QOS.txt`. Riscritto come job unico con quattro processi in parallelo (4 CPU, 12 GB, limite 3 h). **Job 786174 `cv_alpha_beta` RUNNING su gnode04** alle 20:05 (ora HPC); in coda anche `cv_drive_reorg` 786129 dell'altra chat. Remoto: `~/cv_project/alpha_beta_p01_20261122_v1/` (`out/block_NNNN.jsonl`, `out/check_audit.jsonl`, riepiloghi, `logs/`); sha256 script b4fd1988…, sbatch d6fea787…. Controllo `2_controlla_alpha_beta.bat`, scarico `3_scarica_alpha_beta.bat` (avvio da Marco). Esito non ancora verificato.

Verificata in locale la ricostruzione a piena risoluzione: osservazione frame 2893 (tagliere), nuvola grezza 14512 punti + alpha/beta/c2w dell'audit → i 2048 punti dell'audit sono un sottoinsieme esatto (distanza massima 0.0).

## HPC per alpha/beta delle nuove nuvole: controllo e job pronto — 22 novembre 2026, sera

Controllo in sola lettura (`strumenti_hpc/esito_controllo_allineamento.txt`, 19:58): in coda solo `cv_drive_reorg` 786129 RUNNING dell'altra chat (`cv_drive_archive` 785976 COMPLETED). Blocchi 0000–0001 con `ARCHIVIATO.json` e senza mappe DA dense sull'HPC (archiviati su Drive); blocchi 0002–0014 con 1453 `prediction.npz` (31–80 MB per blocco). Presenti 216 batch, 110580 maschere, 247 mappe dense del campione, cartella dell'audit con mesh e `files.sha256`, sorgente Whareformer e ambiente `cv-epic-geometry-cpu`. L'assistente non raggiunge l'HPC dal proprio ambiente e l'accesso a Esplora file è stato rifiutato: i `.bat` li avvia Marco.

Preparato `strumenti_hpc/alpha_beta_p01/` (non eseguito): `alpha_beta_p01.py` importa le funzioni dell'audit (maschere, simboli Whareformer, PyrenderScene) e scrive solo alpha/beta, pixel statici, c2w e hash della mappa per frame, senza nuvole; nessuna sovrascrittura. Job array CPU `cv_alpha_beta` (0–14 blocchi, 15 = riproduzione di alpha/beta dell'audit su 40 osservazioni del campione con maschere complete). Prova locale con scena simulata: alpha 2, beta 1 recuperati, maschera esclusa, mappa mancante registrata, rifiuto di sovrascrittura. Avvio: `1_invia_alpha_beta.bat`, controllo `2_…`, scarico `3_…`. Blocchi 0000–0001 da recuperare in seguito da Drive (area dell'altra chat).

## Risoluzione delle nuvole e ruolo di P01_02 nella selezione — 22 novembre 2026, sera

Verificato: le nuvole grezze ricevute localmente sono a piena risoluzione (es. tagliere frame 2893: 14512 punti con `camera_points`, `pixels_xy`, colori); l'audit 783586 le ha sottocampionate a 2048 (`SAMPLE = 2048` in `audit_ammissione.py`) e salva alpha/beta per osservazione. L'allineamento DA→scena è affine sulla profondità: sull'HPC serve calcolare solo alpha/beta per frame (mappe dense DA + render della mesh + maschere); le nuvole allineate a piena risoluzione si ricostruiscono in locale dalle grezze, senza occupare quota HPC. Il valore 4096 riguarda l'ingresso SuperFlex campionato con FPS dalla forma accumulata, non le singole viste in ingresso alla memoria. Proposta: memoria alimentata a piena risoluzione nella selezione e nella pipeline finale, con risoluzione fissata dalla griglia di celle; campione da 446 ricostruito anch'esso a piena risoluzione dagli alpha/beta dell'audit.

Marco non è del tutto d'accordo nell'usare P01_02 solo come controllo: selezionare anche su P01_02 riduce l'overfitting; se il progetto lavorerà solo su P01_01 e P01_02, accetterebbe il rischio. Proposta dell'assistente: validazione incrociata per video (selezione su un video, misura sull'altro, poi configurazione finale scelta su entrambi). Segnalato: se i risultati finali fossero riportati sugli stessi video usati per la selezione (e per l'addestramento di Whareformer), andrebbero dichiarati come risultati di sviluppo, non come prova di generalizzazione; resta aperta la scelta del test indipendente (TODO prioritario del 21 novembre).

## Struttura Drive approvata e job di riorganizzazione pronto — 22 novembre 2026, sera

Marco approva la struttura video → run → tipo (01_input, 02_profondita, 03_nuvole, 04_superquadriche, 05_indici sempre necessario, _archivio_completo; modelli/ ed esperimenti/ previsti) e autorizza la cancellazione dall'HPC dei dati pesanti dei blocchi 0000–0014 dopo verifica. Preparati `strumenti_hpc/drive/drive_8_riorganizza_e_libera.bat` (job `cv_drive_reorg`) e `drive_9_esito_riorganizza.bat`: per blocco controllo sha256 della copia locale contro la ricevuta su Drive, divisione per cartella di primo livello con controllo che l'unione sia esattamente il blocco, archivio per tipo verificato con MD5 Drive, manifest ed elenco file in 05_indici, spostamento dei tar interi in _archivio_completo, poi `ARCHIVIATO.json` e rimozione solo delle cartelle da/moge/clouds_*/superflex_*; indici, marker e input restano sull'HPC. Carica anche input della run, metadati, CATALOGO.json e README. Provato su archivio simulato locale: ricomposizione identica, blocco alterato rifiutato e non cancellato, rilancio idempotente. Non ancora eseguito sull'HPC. README dell'archivio per valutatori esterni: `strumenti_hpc/drive/README_ARCHIVIO_DRIVE.md` (autori da completare).

## Archivio Drive dei 15 blocchi P01_01 concluso — 22 novembre 2026, sera

Job **785976 COMPLETED 0:0**, 34m41s, gnode01: blocchi 0001–0014 archiviati (0000 dal pilota), falliti 0, `DRIVE_ARCHIVE_OK`. 15 ricevute `ok: true` su Drive in `CV_Whareformer_SuperFlex/P01_01/p01_full_enrichment_20261121_v1/geometry/`; verifica per blocco hash locale = MD5 Drive (riscaricamento completo solo nel pilota). Totale circa 9.59 GB (blocco 0000 1.30 GB, gli altri 0.45–0.56 GB); 7680 osservazioni. Copie HPC non cancellate: quota invariata, produzione ancora bloccata dalla capacità. Restano: caricamento automatico e rilascio locale nel driver (cancellazione da autorizzare), input RGB/maschere nel dataset, pacchetto per il compagno, rinnovo del token comparso in chat. Sezione scritta dalla chat Drive/HPC.

## Dati per la selezione della tolleranza e pseudo-etichette di spostamento — 22 novembre 2026, sera

Le 8126 nuvole ricevute (`shared_exports/p01_01_correction_received/`, ricevuta: 446 del campione + 15 blocchi da 512) sono DA grezze in coordinate camera, `scene_alignment_certified: false`: la memoria lavora nel riferimento scena, quindi non sono utilizzabili senza allineamento DA→scena (`align_video_scene.py`, mappe dense DA conservate nei blocchi HPC + render della mesh + maschere). Copertura: 2443 frame, 7680 nuove osservazioni quasi tutte contigue fra i frame ~937 e ~5500 (circa 75 s, intervallo mediano 1 frame), 24 categorie dominate da chopping board, carrot, tap, sink, knife, courgette; pan solo 190 (campione). Le uniche nuvole allineate oggi restano le 438 dell'audit 783586 (campione sparso, intervallo mediano fra viste consecutive della stessa traccia 73 frame).

Scaricate le annotazioni ufficiali EPIC-KITCHENS-100 (train) da GitHub; salvato solo il sottoinsieme P01_01 (329 azioni) in `data/epic100_annotations/` con provenienza e hash del file completo; uso solo di sviluppo. Controllo sulle 395 coppie consecutive mappabili, punteggio del criterio C con parametri provvisori (margine 0.25 R, fattore 2): presa e posa dell'oggetto fra le due viste 9 coppie, punteggio mediana 0.00 (q90 ≤ 0.06); altre azioni sull'oggetto 56 coppie, mediana 0.00–0.07; nessuna azione annotata 330 coppie, mediana 0.72 ma q10 0.01, con quota sotto 0.3 dell'8% entro 6 frame, 20–23% fra 6 e 300 frame, 41% oltre 300. Gli spostamenti non sono annotati in modo esaustivo (es. spatola usata in «stir rice» senza il sostantivo spatula): l'assenza di azioni non certifica che l'oggetto sia fermo. Le traiettorie XYZ ufficiali dense hanno salti fra frame consecutivi con q99 0.15–0.36 su estensioni di 1.4–3.4 unità: utili solo per spostamenti grandi. Conclusione: «spostato» ricavabile con buona affidabilità solo per poche coppie, «fermo» no; pseudo-etichette come controllo indipendente, non come criterio di selezione.

Marco indica che la selezione può girare sull'HPC. Proposta, non eseguita: job di allineamento delle 7680 nuove osservazioni (vincoli: quota ~4.6 GiB libera all'ultimo controllo e lavoro parallelo dell'altra chat su HPC/Drive), poi griglia della selezione come job array CPU su campione + dati densi.

## Opzione A implementata (criterio C), tolleranza da selezionare — 22 novembre 2026, sera

Marco sceglie il criterio C (riproiezione silhouette/spazio libero) e la creazione di un nuovo stato quando l'oggetto torna nella posizione di uno stato precedente. Implementato in `integration_prototype/position_state_memory.py` (`PositionStateMemory`, policy `position-state-memory-v1`), separato dalla v1 che resta come confronto. Assegnazione: test di posizione sugli stati attivi, confermati poi deboli; punteggio = minimo fra test diretto (punti dello stato nella camera corrente) e inverso (vista corrente nelle camere delle ultime tre viste dello stato); compatibile = sulla silhouette e non davanti alla superficie osservata oltre `depth_margin`·raggio dello stato. Nessuno stato compatibile → nuovo stato debole. Quando uno stato confermato riceve una vista, gli altri confermati vengono chiusi. Dentro lo stato il verificatore decide la fusione vista per vista; la vista respinta resta nello stato (`withheld_keys`), non apre stati e non viene riprovata. Stato dopo spostamento: registrazione dello stato sulla forma; la posa si fissa solo se almeno una vista è ammessa, altrimenti si riprova alla vista successiva.

Collegati `SceneObservation.camera` (campo opzionale), `export_point3_training.py --policy position --position-config` (ora predefinita; camere da c2w dell'audit e intrinseci del catalogo, immagine 456×256) e `MultiHypothesisPipeline(position_config=...)`. Verifica della convenzione: tutte le 438 nuvole allineate proiettate con c2w+intrinseci cadono nel proprio bbox. Test: 7 nuovi casi (lato opposto stesso stato, nuova posizione, spostamento lungo il raggio della camera, vista respinta trattenuta, ritorno → nuovo stato, camera obbligatoria/atomicità, coordinatore); suite completa nell'ambiente Linux di lavoro con Python 3.13: 157 casi, OK, 2 saltati (motmetrics).

Controllo preliminare sul campione (coppie consecutive stessa traccia, parametri provvisori margine 0.25 R, fattore silhouette 2): coppie entro 6 frame n=28, punteggio mediana 0.98, q10 0.48; stesse coppie con spostamento sintetico 0.5 R mediana 0.23 (q90 0.53), 1 R mediana 0.01 (q90 0.14); intervallo >300 frame n=102 mediana 0.14. Il criterio separa fermo e spostato sintetico, ma non è ancora una selezione.

Marco chiede la configurazione ottima per la pipeline finale, non un test con budget arbitrario. Proposta in attesa di conferma: scegliere `minimum_consistency` e `depth_margin` su P01_01 massimizzando l'utilità prequenziale della memoria (quanto la forma collocata dallo stato attivo prima della vista t spiega la vista t, meno la parte prevista dove ora c'è spazio libero), griglia 7×3, regola di un errore standard verso la soglia più severa; controllo indipendente con pseudo-etichette di spostamento dalle traiettorie dense ufficiali solo sui casi netti. Replay v2 non ancora eseguito; parametri dei test non selezionati.

## Criterio di posizione per l'opzione A: proposta in attesa di scelta — 22 novembre 2026, sera

Riletti AGENTS, documenti di memoria, `multi_hypothesis_memory.py`, `scene_memory.py` ed `export_point3_training.py`. Nel codice attuale lo stato di una vista è scelto dal verificatore (`_verify` contro ogni stato) e ogni vista non ammessa apre un'ipotesi; inoltre `_merge_confirmed` riverifica insieme tutte le viste non fuse dello stato, quindi una vista respinta pesa sulle successive. Blocchi da riallineare: assegnazione in `_update` e verifica in `_merge_confirmed`.

Proposti a Marco tre criteri di posizione, nel riferimento scena: (A) distanza fra centri robusti normalizzata sul raggio dello stato; (B) sovrapposizione delle celle della vista con le celle dello stato dilatate; (C) coerenza di riproiezione silhouette/spazio libero con le camere della vista e dello stato, raccomandato. Tolleranza proposta solo su P01_01 (sviluppo): budget di falsi «nuova posizione» fissato prima di guardare, coppie reali a breve intervallo e spostamenti sintetici noti; selezione sulle 13 identità di training della partizione del verificatore, controllo sulle 4 di validazione; nessun uso di esiti del verificatore, metriche di tracking, replay v1 o test.

Misura preliminare (414 viste valide, coppie consecutive della stessa traccia, distanza fra mediane dei punti divisa per il raggio RMS della vista): intervallo ≤3 frame n=18, mediana 0.08, q90 0.17; 3–30 frame n=97, mediana 0.23, q90 1.05; 30–300 frame n=180, mediana 0.34; >300 frame n=102, mediana 0.85. Coppie reali quasi certamente ferme molto poche (18 entro 3 frame, 28 entro 6). Nuvole del campione sottocampionate (mediana 2048 punti). Su un esempio controllato gli XYZ ufficiali di Whareformer non sono nella scala delle nuvole DA allineate (rapporto circa 1.9–2.0): non mescolarli senza verifica.

Domande aperte a Marco: criterio; ritorno nella posizione di uno stato precedente = riapertura o nuovo stato; budget di falsi «nuova posizione». Nessuna modifica al codice né replay eseguiti.

## Drive: pilota riuscito, archivio dei blocchi pronto — 22 novembre 2026, sera

Accesso SSH del PC passato a chiave ed25519 (prima solo password: causa della connessione chiusa). Rclone v1.76.0 collegato al Drive di Marco (scope drive.file, app OAuth in Testing: rinnovo ogni 7 giorni con `drive_5`); configurazione e binario installati sull'HPC. **Pilota 785954 COMPLETED, ok true**, gnode01: `CV_Whareformer_SuperFlex/P01_01/p01_full_enrichment_20261121_v1/geometry/blocco_0000.tar`, 5098 file, 1300428800 byte; sha256/MD5 locale = MD5 Drive = riscaricamento, confronto di ripristino ok; caricamento 101 s, riscaricamento 65 s. I nodi di calcolo raggiungono Drive. Sorgente HPC non cancellata. Token e client secret comparsi in uno screenshot in chat: rinnovo (revoca su myaccount + `drive_5`) da fare. Preparati `drive_6_archivia_blocchi.bat`/`drive_7_esito_archivio.bat`: job `cv_drive_archive` su tutti i blocchi con marker completed, formato `cv-drive-block-v1` uguale al pilota, verifica MD5 Drive per blocco (riscaricamento completo opzionale), salta blocchi già verificati; provato su remoto simulato locale, non ancora sull'HPC. Proposta per il compagno (opzione 2, caricamento con collegamento al Drive di Marco) discussa, non ancora decisa.

## Memoria opzione A e collegamento Drive preparato — 22 novembre 2026, sera

Marco sceglie l'opzione A: memoria a stati multipli per traccia, un nuovo stato nasce quando l'oggetto viene messo in una nuova posizione. Verifica: i documenti approvati descrivono così gli stati (stati della collocazione, SUPERVISIONE_AMMISSIONE «Sintesi corrente» punto 3; sequenza fermo → in mano → posato → nuovo stato consolidato). Il codice `multi_hypothesis_memory.py` invece crea un nuovo stato per ogni vista valida non accettata dal verificatore rispetto agli stati esistenti nel riferimento scena: la causa può essere uno spostamento, ma anche un lato non ancora visto, bassa sovrapposizione o errore di allineamento. Misura sul replay `outputs/point3_multi_hypothesis_20261122_v1/` (mediana dei punti della vista contro mediana delle viste dello stato più vicino, unità scena non certificate metriche): 282 nuove ipotesi create in presenza di stati, 54 (19%) entro 0.05, 112 (40%) entro 0.10, mediana 0.125. Indizio, non prova, che parte delle 299 ipotesi pendenti sia nella stessa posizione; la mediana di viste parziali non è il centro dell'oggetto e non esistono etichette di spostamento.

Collegamento Drive: script pronti in `strumenti_hpc/drive/` (guida LEGGIMI_DRIVE.md), non eseguiti. Scelta operativa dell'assistente, reversibile: scope `drive.file` per limitare l'accesso del token salvato sull'HPC. Pilota: job CPU `cv_drive_pilot` sul blocco geometry/0000, archivio tar ordinato in streaming, verifica hash locale/MD5 Drive/riscaricamento e confronto con i file sorgente, nessuna cancellazione. Testato localmente solo il determinismo del tar e il confronto; rclone, rete dai nodi di calcolo e Drive non provati.

Prossimo passo: Marco crea il client OAuth ed esegue gli script 1–4; sul codice, sostituire il criterio di nuovo stato con un test di posizione (proposta da discutere).

## Priorità di Marco e ruolo di SuperFlex — 22 novembre 2026, sera

Marco fissa l'ordine: (1) dataset condiviso con RGB e nuvole prodotte sull'HPC, archiviato su Google Drive da 1 TB accessibile a lui e al compagno; (2) aggiornamento della memoria geometrica con funzionamento analogo alla memoria di appearance; (3) test della pipeline, soprattutto Whareformer + informazione geometrica e aggiornamento della memoria.

Analisi dell'assistente, nessuna esecuzione: SuperFlex serve per le forme per osservazione (precalcolabili sull'HPC con le nuvole, da includere nel dataset) e per le forme della memoria dopo ogni aggiornamento ammesso (non precalcolabili: dipendono dalla politica di aggiornamento e, con peso attivo, dalle associazioni). Sviluppo del punto 2 e test a punti osservati non richiedono SuperFlex. Il backend SuperFlex (PVCNN) compila sorgenti .cu con cpp_extension: senza GPU NVIDIA e toolchain CUDA non gira sul PC senza modificare il codice degli autori. Marco conferma una GPU NVIDIA sul PC (modello, VRAM e driver non ancora registrati): SuperFlex locale possibile previa installazione CUDA/compilazione, non ancora provata. Vincoli HPC e accesso Drive: [piano aggiornato](../ARCHIVIAZIONE_DRIVE_PIANO_20261122.md).

Replay multi-ipotesi concluso dopo l'ultima nota: `outputs/point3_multi_hypothesis_20261122_v1/verification.json` status passed, 446 esempi, 53 versioni di forma, 17 tracce, 2403 riferimenti strettamente passati, zero contaminazioni, input byte-identici, target preservati; tests.txt 143 casi, 141 superati e due saltati. Sommario: 8 tracce confermate, 345 query con memoria corretta precedente, stati 45 fused_confirmed_state, 62 confirmed_state_separate, 299 hypothesis_pending, 8 initialized_confirmed_shape, 32 esclusi; 166 ipotesi attive finali. Nessuna ricostruzione neurale; quota elevata di ipotesi pendenti e la voce failed_versions 1 in tests.txt non ancora interpretate.

## Ripristino multi-ipotesi autorizzato e implementazione in verifica — 22 novembre 2026

Marco autorizza il ripristino del sistema originario, ciclo completo ed export aggiornati, senza vincolo di riuso del codice. Implementato MultiHypothesisMemory separato dai percorsi storici: compatibilità nel riferimento scena, priorità a stati confermati poi deboli, nuova ipotesi per vista valida incompatibile, promozione temporale, decadimento/potatura ispirati a FeatureDenStream, conservazione della forma persistente, registrazione automatica degli stati confermati dopo spostamento e ri-tentativo delle fusioni non verificate. Nuovo ponte DeferredSceneSuperflex con contratto FPS verificato dal coordinatore, attesa/risultati versionati e conservazione dell'ultimo completamento valido sui fallimenti. Otto test mirati passati, incluso ciclo coordinatore/worker controllato/pubblicazione causale. Nessuna inferenza neurale reale attestata.

Replay completo sul campione originale in esecuzione locale, directory nuova `outputs/point3_multi_hypothesis_20261122_v1/`; non dichiarare ancora conteggi finali/export verificato. Modello e soglia prudenti restano quelli già addestrati, con limiti noti. Profilo di sviluppo esplicito per il ciclo: emivita 1000 s, almeno due frame e supporto 1.5, budget 16 stati deboli; non iperparametri calibrati per efficacia di tracking. La compatibilità geometrica non certifica staticità. Vecchi export preservati come confronti. Nessun job HPC o pubblicazione in questa fase.

## Obiettivo ripristinato: memoria geometrica multi-ipotesi — 22 novembre 2026

Marco richiede recupero della discussione originaria, confronto col codice e riallineamento al meccanismo di memoria dell'appearance prima di ulteriori modifiche. [Confronto verificato e lavoro mancante](../CONFRONTO_MEMORIA_ORIGINARIA_20261122.md). Recuperati cronologia disponibile, riassunto allegato originale del passaggio da altro provider e documenti scientifici; non disponibile una trascrizione integrale della discussione esterna. Letti FeatureDenStream originale, configurazioni clusters, percorsi del tracker/matcher e i due nuclei geometrici.

Risultato: RegisteredObjectMemory usato dagli export del 22 novembre ha una sola voce registered-shape; viste incompatibili respinte, senza nuova ipotesi, conferma solo iniziale. Non realizza il ciclo multi-ipotesi discusso. SceneObjectMemory del 21 novembre contiene stati multipli, supporto/decadimento, promozione e API di fusione fra collocazioni, ma richiede staticità esterna, non automatizza il registratore e non replica potatura/demozione temporale di DenStream. FeatureDenStream rende disponibili al matcher anche i centroidi deboli: non affermare che mostri soltanto i promossi. Memoria FIFO dei descrittori e memoria dei punti sono due componenti distinte; DenStream sui descrittori rimane da concordare col compagno.

La precedente approvazione di registrazione per vista senza certificare staticità non richiedeva di eliminare le ipotesi: conseguenza non chiarita dall'assistente. La richiesta corrente prevale sulla semplificazione e sulla priorità di migliorare soltanto regressione/soglia. Gli export e la padella mostrata restano risultati del percorso semplificato, conservati come confronto, non del sistema originario.

Prossimo passo: ripristinare come percorso effettivo il gestore multi-ipotesi, completare assegnazione/nuovi stati/promozione/potatura, separare conferma e fusione, collegare registrazione degli stati dopo movimento, poi verificare replay e rigenerare export. Riusare allineamento, celle, registratore, interfacce, FPS e worker. Chiarire l'adattamento del presupposto di staticità senza eliminarne tacitamente gli stati. Nessun nuovo algoritmo, training, runtime test, inferenza o accesso HPC eseguiti in questo confronto; nessuna equivalenza o affidabilità già dimostrata.

## Consegna P01_01 per correzione Whareformer in preparazione — 22 novembre 2026

Marco richiede pacchetto autonomo con 8126 geometrie, input, annotazioni, codice e istruzioni. Dopo proposta di avvio manuale, autorizza esplicitamente l'assistente ad avviare lo scarico: eccezione corrente al vincolo organizzativo di avvio HPC riservato a Marco. Esportazione CPU in sola lettura **785638 COMPLETED 0:0**, 15m00s, su gnode02; archivio locale concluso di 2390530916 byte con 8126 osservazioni/2443 frame in `shared_exports/p01_01_correction_received/geometry_received.tar.gz`, log `download_stud.log`. Nessuna nuova inferenza, cancellazione o output geometrico persistente remoto; PLY compattati rigenerati in RAM con SHA originale. Primo tentativo rifiutato dalla partizione predefinita prima dell'esportazione; corrente su stud/QoS stud. Core locale con storia completa P01_01 e checkpoint pronto, lettore/contratto di correzione e quattro test passati; riferimento446 riprodotto esattamente con NumPy 1.26.4/PyTorch 2.6 CPU; importazione/verifica delle geometrie ed esempi estesi ancora in corso. Nessuna consegna completa o pubblicazione gia attestata.

## Affidabilità del verificatore: diagnosi e proposta — 22 novembre 2026

Marco chiede se 30/194 false ammissioni (15.5% dei casi eccessivamente errati) siano troppe e come migliorare senza complicare il progetto. Precisazione: 30 errori fra 125 ammissioni totali nella valutazione sintetica prudente = 24% delle fusioni ammesse; non è una stima su video reale, campioni dipendenti e due identità soltanto. Funzionamento del prototipo non equivale ad affidabilità sufficiente.

Proposta non ancora adottata: generare esempi eseguendo il registratore effettivo su crop con trasformazioni note, includendo i suoi allineamenti errati/ambigui, anziché sole perturbazioni casuali; riusare le otto diagnostiche e provare un piccolo modello non lineare solo se necessario; selezionare il punto operativo controllando la quota di errori fra le ammissioni e la copertura, su gruppi separati. Non abbassare la soglia direttamente guardando le due identità di valutazione già osservate. Budget di rischio da scegliere; nessun miglioramento promesso, nessun retraining, nuova soglia o fusione eseguiti in questa discussione. Conservati gli export precedenti e i loro limiti.

## Google Drive da 1 TB: piano per lavorare entro quota HPC — 22 novembre 2026

Marco dichiara 1 TB su Drive e chiede come completare i blocchi entro 50 GB HPC. [Analisi e ciclo proposto](../ARCHIVIAZIONE_DRIVE_PIANO_20261122.md): un blocco alla volta, archivio verificato su Drive, rilascio locale, catalogo e recupero selettivo con cache limitata. Possibile spostare progressivamente gli 8–9 GiB di geometria dei 15 blocchi attuali e mantenere sull'HPC la base di circa 33 GiB più lavoro temporaneo; picco da verificare nel pilota. Ulteriore deduplicazione di profondità/pixel e coordinate proposta, non implementata.

La stima precedente di circa 160 GiB riguarda la configurazione storica DA+MoGE completa, non il budget aggiornato DA completo/MoGE campione già approvato nelle altre chat. Ricalcolare anche il costo DA allineato/world del nuovo driver. Non cancellare i risultati MoGE esistenti. API pubblica Google raggiungibile dal login; rclone non rilevato nei percorsi controllati, connettore app indisponibile. Nessun account collegato, upload, nuova cancellazione o rilancio. Prossimo passo proposto: configurazione autorizzata e prova completa di upload/recupero prima di adeguare produzione e lettori.

## Esempio visivo della memoria — 22 novembre 2026

Su richiesta di Marco preparato confronto 3D reale della padella, prima osservazione filtrata (1689 celle) e memoria dopo quattro viste accettate (4824 punti), con riferimento/scala comuni. [Provenienza e limiti](../../evidence/ASSET_ESTERNI.md#asset-7e4baebff148). Visualizzazione campionata, nessuna nuova inferenza o validazione geometrica; stato del prototipo invariato.

## Punto 3: consegna locale verificata, variante prudente raccomandata — 22 novembre 2026

[Report leggibile e stato finale](../REPORT_PUNTO3_20261122.md). Conclusi per il prototipo: dati simulati, baseline addestrata, registrazione/verifica per vista anche dopo movimento, memoria osservata pesata, replay oracle, export e lettore per il punto 2. Il precedente requisito di certificare staticità/coppie reali non blocca il prototipo, come rivisto da Marco. Nessuna validazione fisica o efficacia di tracking già dimostrata.

Conservati due export. Iniziale: 263 versioni, 14 tracce confermate, 353/446 esempi con memoria corretta precedente. Prudente: `outputs/point3_training_conservative_proposal_20261122_v1/`, 33 versioni, sei tracce, 267/446 esempi; 414 query, 1559 coppie query-candidata con geometria, 907 file con hash. Verifica indipendente prudente: 1679 riferimenti strettamente passati, target preservati, input originali byte-identici, zero contaminazioni temporali rilevate. Lettore verificato su tutti i 446 esempi. Suite: 131 casi, 129 passati e due skip motmetrics; tre test mirati ripetuti dopo correzione dei separatori dei percorsi.

Variante prudente assunta come raccomandazione operativa dopo il successivo «vai» di Marco; il nome proposal conserva la provenienza, non un'approvazione scientifica definitiva. Soglia 0.06727060374286488 scelta sulla calibrazione per un budget empirico di false ammissioni del 5% per identità, senza garanzia su nuovi dati. Stesso modello della versione iniziale. Su due identità di valutazione sintetica: ancora 30/194 errori eccessivi ammessi; su 17 prove di movimento noto, otto fusioni ammesse e zero oltre tolleranza (iniziale: 16 ammesse, sette oltre). Limitazioni conservate nel report.

**Non concluso:** nuove ricostruzioni SuperFlex GPU. Worker FPS e input di tutte le query/memorie pronti, test locali superati; prova ridotta di due memorie iniziali e due query in `outputs/point3_gpu_smoke_20261122_v1.tgz`, 851133 byte, hash acbe63c8e4f06eed6d477c6ec14a045d4c802ced6e3edc24b7a5a51316e158b1. Avvio/scarico tramite script di Marco: `esegui_point3_fps_smoke.bat` / `scarica_point3_fps_smoke.bat`. Nessun job inviato dall'assistente, nessun identificativo/esito osservato, nessuna promessa di coda o capacità. Poi verificare output GPU ed elaborare i completamenti del campione scelto. Per ora il punto 2 può provare la rappresentazione osservata accumulata; il campione senza Nuova track non equivale a training completo. Scelta del test indipendente e beneficio sul tracking restano separati. Nessun push o invio al compagno.

## Punto 3: baseline e replay locale verificati, GPU ancora da eseguire — 22 novembre 2026

Baseline diagnostica addestrata sui 3312 esempi simulati: 13 identità training, due calibrazione e due valutazione descrittiva. Replay completo del percorso approvato registrazione-per-vista: 446 esempi originali, 414 query utilizzabili, 263 versioni di forma, 14 tracce confermate; 353 query con memoria corretta precedente. Verifica indipendente: 3391 riferimenti strettamente passati, input numerici byte-identici e target preservati, zero contaminazioni temporali rilevate. Suite locale: 131 casi, 129 passati e due saltati (motmetrics).

Limite rilevante: nella valutazione simulata la politica iniziale ammette 62/194 errori eccessivi. Alternativa prudente preparata come proposta (preferenza di Marco ancora pendente), budget empirico 5% per identità di calibrazione, soglia scelta solo lì; su due identità di valutazione ammette 30/194 errori eccessivi. Prova di movimento noto: iniziale 16/17 ammesse, sette eccessivamente errate; prudente 8/17 ammesse, tutte entro la tolleranza. Nessuna garanzia su movimento reale o beneficio di tracking.

Export iniziale in `outputs/point3_training_export_20261122_v1/`; replay comparativo prudente in preparazione, non dichiararlo già concluso. Input FPS/worker/lettore per il punto 2 realizzati e testati; ricostruzioni neurali nuove NON eseguite. Prova HPC limitata a quattro input preparata e proposta a Marco tramite `strumenti_hpc/esegui_point3_fps_smoke.bat`; nessun job di questa prova inviato dall'assistente, nessun identificativo osservato. Guida: [POINT3_PROTOTYPE.md](../../../integration_prototype/POINT3_PROTOTYPE.md). Il campione originale non contiene Nuova track: non equivale al training completo del punto 2.

## Driver P01_02 e pacchetti pronti — 22 novembre 2026

Su richiesta di Marco implementato driver portabile DA-only e allineamento scena separato, con SuperFlex grezzo/allineato, join originale, quota/cache/lock e consegna portabile. ZIP completo circa 22 MB e versione repo circa 128 kB senza pesi/dati/accessi; [resoconto, verifiche e limiti](../PACCHETTO_HPC_P01_02_20261122.md). Sette test locali passati, hash/CRC/sintassi verificati. Nessuna pubblicazione o esecuzione HPC. Input P01_02, ambiente Linux/CUDA e pilota reale ancora da verificare. Il vecchio driver P01_01 resta storico per le cache esistenti: nessuna migrazione della run attuale eseguita. Questa voce supera le note di driver/pacchetto ancora da implementare, non i limiti operativi.

## Compattazione HPC conclusa, capacità complessiva ancora insufficiente — 22 novembre 2026

Approvazione esplicita di Marco; [risultati, ricevute e recupero](../COMPATTAZIONE_HPC_20261122.md). **785105 COMPLETED 0:0** (45m14s), **785556 COMPLETED 0:0** (audit, 4m09s). Tutti i 15 blocchi compattati: **46080 derivati** non conservati per intero (15360 per tipo input/PLY/diagnostica), rigenerati e verificati singolarmente prima della rimozione. Conservati nuvole, mappe, parametri, matrici originali in archivio e palette. Rigenerazione CPU byte-identica; 18 prove iniziali, tre recuperi finali reali, descrittori e ripartenza verificati, otto test locali di sicurezza passati.

Recupero netto circa **3.3 GiB**; quota finale **41.92/46.56 GiB**, circa **4.64 GiB liberi**, circa 440040/500000 file. Wrapper e conservazione futura abilitati nel driver, backup/hash mantenuti, nessun cambio scientifico. **Coda personale vuota**, campagna ancora 15/216 blocchi: non rilanciata. Proiezione attuale ordine **160 GiB complessivi** e troppi inode: la pulizia non basta per i 201 restanti. Prossimo intervento: ciclo di consumo delle mappe dopo allineamento, contenitori dei dati conservati e/o capacità persistente. Guida `integration_prototype/GEOMETRY_RETENTION.md`; non trattare assenze registrate come inferenze mancanti. Le note precedenti di mancata autorizzazione/migrazione attiva sono storia superata per questa manutenzione; il lavoro scientifico delle altre sezioni resta distinto.

## Revisione approvata del punto 3 — 22 novembre 2026

Marco autorizza completamento autonomo del prototipo e approva esplicitamente registrazione di ogni vista sulla forma accumulata, con fusione solo dopo verifica appresa, anche dopo movimento. Per questo prototipo è superato il requisito preventivo di certificare la staticità e mantenere collocazioni separate; il percorso storico resta disponibile. Campione simulato sufficiente per iniziare, con limiti dichiarati; non bloccare il training su una certificazione completa delle coppie reali. Baseline leggera autorizzata per il prototipo, non sostituzione implicita del modello principale negli esperimenti definitivi. Implementazione/verifiche in corso; nessuna efficacia reale già dimostrata.

## Dati del verificatore: componente simulata pronta — 22 novembre 2026

Su autorizzazione di Marco preparati e verificati 3312 esempi da 414 nuvole locali, con crop/rumore e trasformazioni rigide note; nessun gate usato come etichetta. Partizione diagnostica per identità entro P01_01: 1432 training / 1880 validazione, non test indipendente. Tre test passati e verifica indipendente di tutti i target/hash, differenza massima 8.43e-16. [Dati, codice e limiti](../DATI_VERIFICATORE_20261122.md).

Il primo passaggio è completato solo per i dati simulati: zero coppie reali certificate statiche, realismo delle perturbazioni da validare. Nessun training, inferenza, accesso HPC o export della memoria per il punto 2. Prossimo passo: evidenze reali indipendenti e prove del verificatore sul campione; non dichiarare concluso il punto 3. Configurazione e split diagnostici non fissano il protocollo finale.

## DA completo, MoGE campione e P01_02 — 22 novembre 2026

**Decisione approvata:** DA per la generazione completa; MoGE solo confronto su campione. Compagno su P01_02, Marco su P01_01. Per la memoria resta DA allineato alla scena. [Ruoli, evidenze, materiali e blocchi concreti](../RUOLI_DA_MOGE_E_CONSEGNA_P01_02_20261122.md). Superate le indicazioni di doppia sorgente su tutta la copertura e di divisione dei blocchi dello stesso video fra i due account. Driver ancora specifico P01_01, input P01_02 e risorse del compagno non verificati. Nessun codice/job/trasferimento/cancellazione eseguito; risultati precedenti preservati.

## Secondo HPC del compagno - 22 novembre 2026

Marco intende usare anche HPC del compagno per generare nuvole coerenti. Raccomandati runtime/configurazione/pesi/input identici, blocchi esclusivi e prova comune. Driver locale con auto-invio indice +2 e aggregazione globale da adattare prima della distribuzione. Nessun nuovo pacchetto, trasferimento o job eseguito. Limite verificato: disco/inode; RAM/VRAM non diagnosticate. Capacità complessiva ancora da verificare.

## Capacità HPC: ridondanze verificate e proposta di conservazione — 22 novembre 2026

Su domanda di Marco analizzati codice e dimensioni dei contenuti di NPZ campione remoti: predizione SuperFlex completa, input, parametri e PLY si sovrappongono; cache densa per RGB limitata al singolo blocco. Esempio diagnostico DA: 126992 byte contro 3780 dei parametri già estratti, senza estendere questo rapporto a tutto l'output. [Analisi e proposta](../GESTIONE_SPAZIO_HPC_20261122.md).

Inventario delimitato concluso, globale **parziale** (4076 directory non percorse): almeno 12.88 GiB ambienti, 2.465 GiB pesi, 12.194 GiB geometria corrente. Negli artefatti dei 15 blocchi contati: 2.588 GiB diagnostiche e 1.721 GiB PLY contro 0.059 GiB parametri. Potenziale risparmio non equivale a cancellazione già sicura o soluzione dimostrata per 216 blocchi; dettagli e ricevute nel resoconto.

Chiarito il ciclo di vita per file nel resoconto: la matrice di assegnazione diagnostica non è contenuta nei soli parametri. Verifica esatta di `cached()`: un artefatto ready mancante provoca errore prima del recupero degli errori di `run_item`; la cancellazione manuale non è supportata come pulizia automatica. Nessuna eliminazione autorizzata da questa domanda.

Proposta: cache condivisa per frame, conservazione degli intermedi fino ai consumatori effettivi, parametri con mesh rigenerabili dopo verifica, contenitori indicizzati per blocco e compattazione progressiva. Prima prova isolata su un blocco e budget totale, adattando i contratti della cache. Non dimostrato il rientro in 50 GB; nessuna riduzione di nuvole/copertura/fonti o modifica scientifica approvata. Nessuna nuova cancellazione, inferenza o ripresa HPC; restano i 15 blocchi e la coda vuota dell'ultimo controllo datato sotto.

## HPC controllato: 15 blocchi conclusi, stop preventivo per quota — 22 novembre 2026

Verifica live delle 11:31:28: **coda vuota**, 15/216 blocchi (0–14), **7680 nuove osservazioni** esportate. Conteggi ricalcolati su tutti i 15 indici: 7680 ready per ciascuna delle quattro rappresentazioni DA/MoGE punti/SuperFlex. Sette blocchi in più dopo la pulizia; non conclusa la run. **45.30/46.56 GiB**, circa 1.26 GiB liberi; 485960/500000 file.

Ultimo blocco terminato con successo alle 00:26:02; **783835 e 783852** fermati preventivamente con codice **75**, spazio sotto la riserva di 2 GiB. Nessun job attualmente attivo/in attesa. Prossimi mancanti: ramo 0 blocco 16, ramo 1 blocco 15. [Accounting, percorsi e limiti](../CONTROLLO_HPC_20261122.md). Risolvere conservazione/compattazione degli output e quota file prima di nuovi invii. Nessun rilancio o cancellazione eseguiti; scelte scientifiche invariate. Questo stato supera le precedenti note RUNNING serali.


## Mesh SuperFlex: pacchetto pronto per il compagno — 22 novembre 2026

Su richiesta di Marco creato [pacchetto e documentazione](../PACCHETTO_MESH_SUPERFLEX_20261122.md): `shared_exports/compare200_superflex_meshes_v1.zip`, 54696713 byte (circa 55 MB), SHA-256 `22f14355067b613bb1fc2e61b9584257a675034b6d862dca85997289a6eea210`. Stesse 299 osservazioni del vecchio ZIP; 890 PLY (299 DA grezzo/293 DA allineato/298 MoGE), indice JSON e 897 righe CSV comprese sette assenze motivate, report e verificatore incluso. Hash delle nuvole rispetto a report e vecchio ZIP, geometria, normalizzazione, CRC e 1786 checksum verificati; nessuna nuova inferenza. Join observation_key, senza inventare detection_idx/track_id; coordinate camera, campione non intero video. Pronto localmente, nessun invio esterno o pubblicazione GitHub. Le note precedenti di pacchetto privo di mesh riguardano i due ZIP storici, non questa consegna.


## Disponibilità delle mesh richieste dal compagno — 22 novembre 2026

Marco riferisce la richiesta di `reconstruction.ply`. Verifica locale: nel campione compare200 sono presenti 890 file PLY di ricostruzione (299 DA grezzo, 293 DA allineato, 298 MoGE; configurazioni diverse, non 890 osservazioni indipendenti). Esempio DA: `outputs/compare200_749968/P01_01/predictions_da_raw/frame_0000002893__a00/reconstruction.ply`. Presenti ulteriori mesh nei risultati storici; non dedurne copertura completa P01_01 o stato live della nuova run.

Verificati gli ZIP: `shared_exports/compare200_tracking_inputs_v1.zip` contiene RGB/maschere/nuvole NPZ, zero PLY; `strumenti_hpc/campaign_20261115_v1_estratto.zip` contiene quattro file di metadati/tracce, zero PLY. La mancanza nel pacchetto GitHub non significa ricostruzioni assenti. Nessuna nuova inferenza, copia, pubblicazione o invio al compagno. Per un'eventuale consegna delle mesh mantenere indice osservazione/sorgente e chiarire campione richiesto.


## Pubblicazione verificata a chiusura della sessione

Su richiesta di Marco, controllo complessivo e push eseguiti. Commit
[5827c32](https://github.com/Federico-cia/Whareformer-SuperFlex-Project/commit/5827c323854d8a4f776d2417dd43e7c1ea4c328d)
pubblicato su **main**, riferimento remoto verificato identico tramite Git.
48 file: primo nucleo del punto 3, dati oracle/audit in codice portabile,
evidenze numeriche selezionate, schede confermate della mappa e memoria corrente.
Contributi del collega e storia preservati; nessun force-push.

Verifiche della copia pubblicabile: **105 casi, 103 superati e due saltati**
(motmetrics assente); 636 collegamenti, 53 sorgenti Python e 222 hash senza
errori; mappa 39 riquadri/49 collegamenti/792 campi e copia offline coerenti.
Scansione finale dei 48 file senza riscontri per pattern sensibili, dati pesanti
o accessi personali, nei limiti del controllo. Archivi completi, immagini,
nuvole, pesi e strumenti di accesso privati restano fuori da Git.

Il problema di capacità degli output è rinviato da Marco alla prossima sessione.
Il punto 3 resta incompleto sul piano di training e validazione; il push non
certifica efficacia scientifica. Gli stati HPC restano quelli datati negli
ultimi resoconti, senza nuova interrogazione durante la pubblicazione.
Le note precedenti di pubblicazione preparata/non eseguita sono cronologia.

## Spazio recuperato e nuova ripresa — 21 novembre 2026

**Verifica successiva delle 23:51:38:** 783790/783791 entrambi RUNNING a 3m56s su gnode03; superato l'arresto precedente nelle nuvole, ora blocco 8 con 309/312 report DA/MoGE e blocco 9 con 286/288. Quota 41.19/46.56 GiB (circa 5.37 GiB liberi), otto blocchi ancora conclusi; SuperFlex dei nuovi blocchi non ancora verificata.

Marco autorizza pulizia e, esplicitamente, copia/archiviazione dei tracciati conclusi sul PC. Verificati due volte 377 file (5.47 GiB) e conservati in archivio locale di 636594519 byte con ledger/hash, prima di rimuovere le sole copie remote. Runtime, geometrie e input attuali preservati. Quota scesa da 46.35 a 40.88 GiB su 46.56; archivio da NON eliminare. [Operazioni, percorsi e ripristino](../PULIZIA_E_RIPRESA_HPC_20261121.md).

**Job correnti:** 783790/783791, rami 0/1 dai blocchi 8/9, RUNNING su gnode03 al controllo 23:49:54 (2m11s). Preflight quota positivo anche sul nodo di calcolo. Otto blocchi conclusi a quel controllo. I tentativi 783750/751 sono falliti dopo MoGE anche su nodo diverso; 783782/783783 fermati prima delle inferenze per helper quota assente, poi corretto. Nessun precedente tentativo va considerato attivo.

Guard di quota a ogni blocco: riserva operativa 2 GiB/12000 file, stop esplicito codice 75 quando insufficiente; fallback nativo BeeGFS verificato. Tolta l'esclusione del nodo che non risolveva. Nessuna modifica scientifica. **Capacità ancora aperta:** costo misurato 0.64 GiB/blocco, estrapolazione circa 138 GiB/216 blocchi; la pulizia non basta a garantire completamento nella quota di 50 GB. Occorre compattare la conservazione senza perdere informazione necessaria o reperire capacità. Nessuna riduzione di copertura o sorgenti approvata in questa fase. Non promettere funzionamento ininterrotto notturno.


## Ripresa interrotta; quota personale quasi piena — 21 novembre 2026

Aggiornamento successivo: 783750/783751 hanno superato MoGE ma sono poi entrambi FAILED 1:0 alle 23:23:53 anche su gnode03, durante le nuvole. La precedente nota RUNNING è storica: il solo cambio di nodo non risolve. Diagnosi con `myquota`: 46.35 GiB usati su 46.56 GiB, circa 0.21 GiB disponibili; il precedente df del filesystem totale non misurava questo limite personale. Quota quasi esaurita è un problema verificato e spiegazione plausibile degli errori di scrittura/silenzi; risoluzione dello spazio e successiva ripresa ancora in corso. Nessun altro job inviato dopo questo arresto. I parziali sono preservati. Non dichiarare la run attualmente in avanzamento senza nuova verifica.


## HPC riavviato su richiesta di Marco — 21 novembre 2026, 23:23

Marco richiede «Fallo ripartire». Diagnosi e ripresa eseguite con accesso esistente autorizzato per l'azione: **783750 e 783751 RUNNING su gnode03**, rami 0/1 dai blocchi 8/9. **MoGE superato: 512/512 ready in entrambi**, DA già pronta, nuvole in costruzione. Ultimo controllo 23:23:51, rispettivamente 3m14s/3m08s; 8/216 blocchi ancora conclusi a quel momento. Catena automatica preesistente preservata, nessun duplicato o reset delle cache.

Escluso gnode02 dai job e successori come intervento controllato dopo quattro arresti osservati durante MoGE, senza pretendere diagnosi hardware conclusiva. Batch remoto salvato in backup e arricchito di log; dati/modelli/codice scientifico invariati. [Intervento, hash, log e ricevute](../RIPARTENZA_HPC_20261121.md). Non reinviare mentre i rami sono in coda. SuperFlex dei nuovi blocchi e completamento integrale ancora da verificare; nessuna sorveglianza permanente avviata. Questo stato supera le precedenti note di coda vuota/run ferma. Audit e sviluppo punto 3 restano nello stato documentato.


## Chiusura sessione e ripresa successiva — 21 novembre 2026

Marco chiede di chiudere la sessione e proseguire domani con il prossimo problema del TODO. Nessuna nuova scelta metodologica o attestazione di chiusura del punto 3: piano approvato, primo nucleo implementato e testato (103 test superati, due saltati), audit 783586 acquisito e interpretato. Riferimenti: [implementazione](../IMPLEMENTAZIONE_PUNTO3_20261121.md), [audit](../RISULTATI_AUDIT_AMMISSIONE_20261121.md).

**Situazione da non perdere:** arricchimento fermo a 8/216 blocchi, riprese 783490/783491 FAILED 1:0 e nessun job in coda nell'ultimo controllo delle 23:01. Non avanza automaticamente durante la notte. Diagnosi aggiornata predisposta ma non ancora eseguita: esito_diagnosi.txt è ancora quello delle 20:39 sui vecchi job. Marco può eseguire `strumenti_hpc/esegui_diagnosi_hpc.bat` alla ripresa; assistente senza accesso HPC diretto, nessun rilancio prima della lettura dell'esito.

**Punto 3 ancora aperto:** staticità/target reali da validare, dati e training del verificatore principale, parametri selezionati sullo sviluppo, worker SuperFlex con FPS e validazione del caso dopo spostamento. Le 438 nuvole allineate sono locali e consentono lavoro indipendente dalla run. Test set indipendente ancora prioritario; punto 2 al compagno. Le modifiche di questa sessione sono locali, non pubblicate. Non riaprire decisioni approvate né rilanciare audit concluso. Nessuna ulteriore azione indispensabile per chiudere la chat; riprendere da questi pendenti quando Marco torna.


## Audit acquisito; arricchimento fermo — 21 novembre 2026, esiti 23:01–23:06

Marco esegue gli script: **783586 COMPLETED 0:0, 16m53s**, sette hash verificati; 446 osservazioni, 438 allineamenti validi e nuvole locali finite, otto fit con alpha negativo. Confronto appaiato su 415 coppie: sovrapposizione mediana 3.27% grezza → 22.80% allineata (28.08% → 68.16% nel terzile di minore spostamento, non staticità certificata). 24 osservazioni con sole maschere del catalogo. Nessuna etichetta di fusione corretta ancora certificata: mantenere limiti di staticità, simmetrie ed errori condivisi. [Risultati, provenienza e interpretazione](../RISULTATI_AUDIT_AMMISSIONE_20261121.md).

**Arricchimento:** coda vuota, 8/216 blocchi, nessun riepilogo finale; riprese 783490 e 783491 entrambe FAILED 1:0. Causa non identificata dai log disponibili. Aggiornata la diagnosi di sola lettura per questi job e per gli stadi parziali; prossimo intervento di Marco: `strumenti_hpc/esegui_diagnosi_hpc.bat`, poi leggere `esito_diagnosi.txt` prima di riprendere. Nessun accesso diretto HPC, invio o training dell'assistente. Le nuvole locali consentono di proseguire la preparazione dei dati da trasformazioni note senza attendere la run completa. Decisioni metodologiche approvate invariate.


## Punto 3: prima implementazione autorizzata ed eseguita — 21 novembre 2026

Marco autorizza di procedere secondo il piano approvato iniziando dalle parti indipendenti dall'audit. Implementati allineamento DA→scena con fallimento esplicito, memoria pesata a stati senza vista fissa, separazione forma/collocazione e percorso esplicito dopo spostamento, FPS 4096 con provenienza, contratti del verificatore, baseline regressiva addestrabile e replay/adapter del coordinatore. [Dettagli, verifiche e limiti](../IMPLEMENTAZIONE_PUNTO3_20261121.md); [guida software](../../../integration_prototype/SCENE_MEMORY.md).

**Verificato localmente:** 105 casi, 103 superati e 2 saltati per motmetrics, inclusi 23 nuovi test tutti passati; nessuna inferenza neurale reale. Il verificatore principale non è addestrato: senza modello non si confermano/fondono ipotesi. Mancano evidenze validate di staticità, calibrazione sullo sviluppo, collegamento FPS al worker SuperFlex e validazione reale dopo spostamento. Il runner storico resta distinto e invariato nei suoi algoritmi; la nuova memoria non è già la pipeline sperimentale completa.

**Audit/HPC:** nessun accesso diretto o job in questa fase; stato live ignoto. Marco deve avviare `strumenti_hpc/esegui_controllo_hpc.bat` e `esegui_scarica_audit.bat`; scarico aggiornato per il job 783586, con accounting, hash e log anche parziali, nuova cartella a ogni tentativo. Poi interpretare gli esiti prima di training/ripresa. Nessun nuovo metodo principale, parametro calibrato, modifica della mappa o pubblicazione. Log e ricevuta in `outputs/point3_implementation_20261121/`.


## Ricognizione di ripresa — 21 novembre 2026

Confrontati riassunto dell'altra chat, documenti correnti, codice, ricevute locali e schede della mappa. [Stato consolidato, differenze e limiti dell'audit](../RICOGNIZIONE_RIPRESA_PUNTO3_20261121.md). Nessuna nuova scelta o esecuzione: piano approvato del verificatore/memoria ancora da implementare nei moduli correnti, che conservano gate fissi e prima vista. Scala 9–23% = variabilità del rapporto allineata/grezza, non errore vero certificato. Audit: staticità non certificata; errore denominato di superficie è spostamento punto a punto, non invariante alle simmetrie; non esporta tutte le pose candidate. Tenerne conto prima di costruire target.

Stato HPC corrente NON verificato: ultima verifica documentata squeue vuota, senza accounting/esiti successori; RUNNING storici non attuali. Prossimo passo: controllo e scarico audit avviati da Marco con gli script predisposti; assistente senza accesso diretto HPC. Preservate tutte le decisioni approvate e la storia; nessun training, job o pubblicazione in questa ricognizione.


## Passaggio corrente — 21 novembre 2026, sera

**Verifica operativa successiva:** acquisizione conclusa, 110580/110590 osservazioni abbinate e dieci mancanti; nessun job restituito nell'ultima interrogazione squeue, senza accounting/log correnti dei successori. Lo stato RUNNING di ripresa/audit riportato sotto è storico e non certifica avanzamento attuale. [Evidenze e prossimo controllo](../VERIFICA_ARRICCHIMENTO_CORRENTE_20261121.md). Marco deve eseguire `strumenti_hpc/esegui_controllo_hpc.bat` aggiornato; nessun nuovo job o rilancio. Rispettato il vincolo di non ripetere accessi diretti dopo la lettura della nuova istruzione.

**Questo blocco prevale sulle sezioni sottostanti, che sono cronologia.** Punto 3 (ammissione e aggiornamento della memoria geometrica) seguito da Marco; punto 2 dal compagno; punti 1 e 4 dopo. Decisioni e piano in [SUPERVISIONE_AMMISSIONE_20261121.md](../SUPERVISIONE_AMMISSIONE_20261121.md), sezione «Sintesi corrente»; registro in [REGISTRO_DECISIONI.md](REGISTRO_DECISIONI.md).

- **Decisioni del punto 3:** profondità DA allineata alla mesh della scena e riferimento scena tramite pose EPIC-Fields (procedura Whareformer); MoGE solo confronto; vista non fusa se l'allineamento fallisce. Memoria senza vista fissa; forma separata dalla collocazione; stati confermati nel tempo (DenStream adattato); accumulo con fusione dei duplicati e 4096 punti FPS per SuperFlex. Verificatore appreso sulla coppia allineata, classificatore sulle diagnostiche come base, verificatore preaddestrato come confronto. Prima versione con fusione solo da fermo; **obiettivo non negoziabile: fusione anche dopo uno spostamento**. Parametri scelti solo su sviluppo. Posizione per il tracking: quella di Whareformer.
- **Valutazione:** P01_01 è video di training, quindi sviluppo; il test set è priorità da discutere (TODO).
- **Operativo:** run di arricchimento P01_01 (110590 osservazioni, 216 blocchi) in corso con catena GPU; ripresa 783490/783491 dai blocchi 8/9. Audit del punto 3 783586 inviato. L'assistente non accede direttamente all'HPC: script in `strumenti_hpc/` avviati da Marco con doppio clic (controllo, diagnosi, ripresa, audit, scarico risultati). Nessun training avviato.
- **Mappa HTML:** schede R09, R12, R28, R32, R34 aggiornate con le decisioni (testi confermati da Marco); non ancora pubblicata.

## Pubblicazione GitHub preparata — 21 novembre 2026, sera (non ancora eseguita)

Su richiesta di Marco: memoria allineata (blocchi «Passaggio corrente», sintesi del punto 3, note su roadmap, README, AGENTS, docs/CODICE_PRODOTTO, README di integration_prototype). `full_p01_enrichment.py` locale reso portabile: account Slurm da `CV_SLURM_ACCOUNT` invece del numero di matricola; la copia in esecuzione sull'HPC resta quella con hash `0f73f716…66e9f`. Worktree di pubblicazione `shared_exports/handoff_ai_20261114` (base = main remoto 567321e) aggiornato con `shared_exports/prepare_github_point3_20261121.py`: 4 nuovi documenti di memoria, 5 sorgenti, campi della mappa, inventario hash. `tools/check_repository.py`: 567 collegamenti, 46 sorgenti Python, 202 hash, 0 errori; controllo dei pattern sensibili sui 24 file cambiati: nessun riscontro. Nove collegamenti a file locali non pubblicati resi come testo. Pubblicazione con `strumenti_git/pubblica_github.bat` (si ferma se il main remoto è cambiato), dopo conferma di Marco. **Pulizia eseguita su conferma di Marco:** eliminati localmente i 9 piloti superati di `integration_prototype/` (presenti nella cronologia GitHub), due copie temporanee e le cartelle `__pycache__`; README locale di `integration_prototype` sostituito con quello curato, con collegamenti adattati alla cartella locale. Resoconti storici, `scripts/` e `shared_exports/` conservati di proposito.

## Test indipendente: disponibilità dei dati — 21 novembre 2026

Chiarito con Marco: un miglioramento si può affermare solo su video mai usati né per addestrare Whareformer né per addestrare/calibrare/selezionare la componente 3D; P01_01 (training split) resta sviluppo. Verificato nel README del repository ufficiale: l'archivio pubblico degli autori contiene feature preestratte per **tutte** le osservazioni EPIC (anche split di test), IT3DEgo e HD-EPIC, **e la training LMDB**; le feature P01_01 locali provengono da quell'archivio (`epic_osnom/observations/P01_01`). La LMDB non è nei nostri file ma è pubblicata: correggere in questo senso la risposta al compagno. Split: 110 video in `EPIC_100_video_info.csv`, 56 training, 54 test. Per la parte 3D servono RGB, maschere VISOR dense, pose EPIC-Fields e mesh, tutti pubblici. Vincolo principale: costo, perché i 54 video di test sono circa 27 volte P01_01. Proposta non decisa: lista di video di test fissata prima, scelte congelate sullo sviluppo, valutazione una sola volta. Nessun download avviato.
Discussione successiva: Marco valuta di testare su pochi dei 54 video. Proposta dell'assistente, non decisa: è un test valido ma con meno potenza statistica, a condizione di scegliere i video prima (casuale con seme o stratificato), congelare le scelte, riportare risultati per video con incertezza e calcolare la baseline anche su tutti i 54 (feature già pubblicate) per giudicare la rappresentatività del sottoinsieme. Dimensione della training LMDB non verificata; per il compagno indicare il link ufficiale dell'archivio.

## Obiettivo della memoria — 21 novembre 2026

Marco fissa come obiettivo non negoziabile la fusione anche dopo uno spostamento; la fusione solo da fermo resta una tappa temporanea. Proposta per arrivarci: coppie reali di oggetti fermi con spostamento rigido noto applicato a una vista come supervisione realistica del caso «dopo spostamento». Mappa R34 aggiornata (backup `backup/contenuti_prima_obiettivo_fusione_20261121.*`), non pubblicata.

## Ripresa della run e audit del punto 3 — 21 novembre 2026, 21:10

Ripresa eseguita da Marco (`strumenti_hpc/esito_ripresa.txt`): **783490 (ramo 0, blocco 8) e 783491 (ramo 1, blocco 9) RUNNING** su gnode02; 8/216 blocchi completati. Non reinviare; controllo con `esegui_controllo_hpc.bat`, ripresa con `esegui_ripresa_hpc.bat`.

Audit approvato da Marco, preparato e non ancora inviato: `integration_prototype/audit_ammissione.py` (solo lettura degli input; DA grezza contro allineata con procedura e funzioni originali Whareformer, mesh P01_01 SHA-256 `59bcc1df…508de6`, pose del catalogo; riferimento di posa relativo dalle camere; registratore attuale confrontato col riferimento; coerenza delle dimensioni per identità; stratificazione per terzili dello spostamento XYZ ufficiale, nessuna soglia decisionale). Test locali della matematica di pose e retroproiezione superati; rendering e registratore non eseguibili localmente. Invio con `strumenti_hpc/esegui_audit_hpc.bat` (job CPU `cv_audit_p3`, 4 CPU, 12 GB, 1h30, ambiente `cv-epic-geometry-cpu`); risultati con `esegui_scarica_audit.bat`. Il job occupa uno dei due posti attivi QoS: può ritardare di poco un blocco GPU.

**Audit inviato da Marco: 783586 RUNNING a 9 s su gnode02** (21:45). Hash: script `47cdbab0…5455`, mesh `59bcc1df…508de6`, sbatch `facf0e50…399a`. Esito da scaricare con `esegui_scarica_audit.bat`; non reinviare.

## Avanzamento run P01_01 — controllo del 21 novembre 2026, 20:30

Correzione `ninja` efficace: **8/216 blocchi completati** (783119/783120, 783147/783148, 783169/783170, 783194/783195 COMPLETED 0:0, 9–10.5 minuti ciascuno), SuperFlex ready 1024 per blocco (512 osservazioni × DA/MoGE), zero fallimenti per osservazione. Stima rivista: circa 10 min per blocco, 108 blocchi per ramo, ~18 h di calcolo per ramo più attese in coda. **783207/783208 (blocchi 0008/0009) FAILED 1:0 dopo 2m40s, entrambi su gnode02**, log senza traceback visibile nell'estratto; catena ferma, coda vuota. Causa non ancora nota (ipotesi: memoria, nodo, errore nello stadio DA). Preparato `strumenti_hpc/esegui_diagnosi_hpc.bat` (sola lettura). Nessun reinvio prima della diagnosi.

**Diagnosi (20:39):** 783207/783208 FAILED 1:0 dopo 2m40s, entrambi su gnode02, MaxRSS ~3.4 GB su 16 GB richiesti (memoria non è la causa); nessun traceback nei log; stadio DA dei blocchi 0008/0009 completato, MoGE interrotto a metà (nessun indice MoGE). Spazio disco ampio. Causa non identificata; ipotesi più probabile: evento transitorio del nodo, non errore del codice (gli 8 blocchi precedenti, anche su gnode02, sono riusciti). Preparato `strumenti_hpc/esegui_ripresa_hpc.bat` (+ `riprendi_remoto.sh`): si ferma se ci sono job cv_p01 in coda, reinvia ogni ramo dal primo blocco non completato, riuso della cache. Non ancora eseguito.

**Mappa, terzo aggiornamento:** R32 «miglioramenti» (piano approvato del verificatore e alternative future), R34 «miglioramenti» (fusione dopo spostamento da testare con più dati). Backup `backup/contenuti_prima_piano_verificatore_20261121.*`; non pubblicato.

**Mappa, secondo aggiornamento (su istruzione di Marco):** R09 «miglioramenti» (stessa procedura di allineamento per la memoria; vista non fusa se l'allineamento non riesce), R12 «alternative» (DA allineata come direzione per la memoria, MoGE solo confronto) e «fallimenti» (errori di posa/scena condivisi fra ingresso e verifiche), R28 «miglioramenti» (nessuna fusione se l'allineamento fallisce; nuvola ancora utile per il confronto delle forme). Backup `backup/contenuti_prima_scala_MoGE_20261121.*`; JSON e copia offline coerenti; non pubblicato.

**Mappa:** applicato il testo confermato da Marco al campo «alternative» di R32 (criteri appresi: classificatore di base, verificatore sulla coppia allineata come direzione preferita, sovrapposizione per punto non scelta; ammissione per ipotesi e forme separate). JSON e copia offline coerenti, backup in `mappa_interattiva/backup/contenuti_prima_R32_20261121.*`. Non pubblicato su GitHub.

## Rilancio GPU P01_01 — 21 novembre 2026, 17:19

Eseguito da Marco `strumenti_hpc/esegui_rilancio_hpc.bat`: coda vuota, hash attesi, `ninja` verificato con il PATH corretto, nessun report SuperFlex o lock preesistente; DA/MoGE/nuvole dei blocchi 0/1 presenti e riusabili. File sostituito (SHA-256 `0f73f716…66e9f`, backup `.pre_ninja_fix` sull'HPC). **783119 (ramo 0, blocco 0) e 783120 (ramo 1, blocco 1) RUNNING a 18 s su gnode01.** Esito in `strumenti_hpc/esito_rilancio.txt`. Superamento dello stadio SuperFlex e durata del blocco ancora da osservare; monitoraggio con `strumenti_hpc/esegui_controllo_hpc.bat`, ora solo lettura (non ricrea lo ZIP).

## Esito osservato dei job P01_01 — 21 novembre 2026, 16:58

Controllo eseguito da Marco con `strumenti_hpc/esegui_controllo_hpc.bat` (sola lettura; esito in `strumenti_hpc/esito_hpc.txt`). **782990 COMPLETED 0:0, 41m10s**: 110580/110590 osservazioni con input, 10 mancanti espliciti, nessun conflitto di maschere, 32125 frame RGB verificati, alias temporali registrati, 216 blocchi, 446 geometrie riusate, 110134 inferenze pendenti. **782968 FAILED 1:0 (8m06s) e 782969 FAILED 1:0 (8m50s)** nello stadio `superflex` dei blocchi 0000/0001: `RuntimeError: Ninja is required to load C++ extensions`. Nessun blocco completato, nessun job successivo inviato, coda vuota. Causa molto probabile, verificata confrontando il codice: `lane()` in `full_p01_enrichment.py` invoca il Python dell'ambiente per percorso assoluto senza attivarlo, quindi `ninja` dell'ambiente non è nel PATH; la campagna del 15 novembre usava `conda activate`. Correzione proposta (PATH dell'ambiente per ogni stadio), non applicata; nuovo invio solo dopo conferma di Marco. Le note precedenti di job RUNNING/PENDING sono superate.

**Correzione preparata (21 novembre, dopo l'esito):** Marco autorizza la modifica dato che la coda risultava vuota. `lane()` ora antepone al PATH la cartella `bin` dell'ambiente di ogni stadio; nessun cambio di metodo o parametri. Applicata a `outputs/p01_full_enrichment_20261121_v1/full_p01_enrichment.py` e `integration_prototype/full_p01_enrichment.py` (SHA-256 `0f73f716…66e9f`, prima `6f782f47…07c7`; copie `.pre_ninja_fix`). Script `strumenti_hpc/esegui_rilancio_hpc.bat` + `rilancio_remoto.sh`: carica il file, si ferma se ci sono job cv_p01 in coda o hash inattesi, verifica `ninja`, conserva backup, aggiorna `runtime_revision.sha256` e invia solo i rami GPU 0/1; esito in `strumenti_hpc/esito_rilancio.txt`. Non ancora eseguito: lo esegue Marco. Blocchi 0/1 riprendono dalla cache firmata della pipeline (DA/MoGE/nuvole già prodotti).

ZIP per il compagno creato e scaricato: `strumenti_hpc/campaign_20261115_v1_estratto.zip`, 247/33310 righe integrali con features_available > 0 (446 feature complessive, frame 2893–97921), più i due manifest; integrità e JSON verificati, hash delle sorgenti nel README. Non ancora inviato al compagno.

## Richiesta dati del compagno — 21 novembre 2026

Il compagno chiede estratto del JSONL `runs/Sacc_moge_w10_n01/inference/Sacc_moge_w10_n01.jsonl` (righe complete con features_available > 0), `inputs/manifest.json` e `bundle/input_manifest.json` della campagna del 15 novembre, più disponibilità del training LMDB originale. Verificato: nessuno dei tre file è nella copia locale (`outputs/campaign_20261115_v1/` contiene solo report, accounting, selezione e snapshot di invio); restano sull'HPC, non raggiungibile da questo ambiente. Preparato per Marco un comando di estrazione in sola lettura da eseguire con il suo accesso; nessun file inviato. Training LMDB originale non trovato nell'inventario delimitato (`availability_summary.json`, `results/inventory.json`); disponibili solo bundle ufficiale P01_01, split dei 56 video, `manifest_builder.py` e `merge_lmdb.py` del repository.

## Punto 3 — politica di memoria e verifica appresa: discussione, 21 novembre 2026

Marco propone memoria pesata per recenza e contributo di copertura e chiede di valutare la replica dei meccanismi DenStream della memoria d'aspetto; chiede limiti appresi, non numeri fissi. Risposte, letteratura (PREDATOR; preprint Decision PCR, FACT, Deep-PE sulla verifica appresa) e proposta di separare memoria per il matching e memoria per la ricostruzione in [SUPERVISIONE_AMMISSIONE_20261121.md](../SUPERVISIONE_AMMISSIONE_20261121.md). Nessuna decisione presa.
Aggiornamento: Marco indica di eliminare la prima vista fissa e apprezza i pesi per punto se il costo resta contenuto. 4096 punti imposti dal paper SuperFlex (FPS; noi campionamento casuale). Verifica locale su compare200: rapporto profondità allineata/grezza variabile fra frame (CV 9–23%), coerente fra oggetti dello stesso frame; DA allineato calcolabile a posteriori dalle profondità salvate. Dettagli nel resoconto.
Successivo: raccomandazione DA allineato in riferimento scena (da confermare su oggetti fermi); iperparametri DenStream scelti dagli autori con piccola griglia valutata sul test EPIC (appendice E, Tab. 10; §4.5); proposta di DenStream geometrico per stati dell'oggetto e voxel pesati. Nessuna decisione.

## Supervisione indipendente per l'ammissione — analisi, 21 novembre 2026

Analisi della disponibilità di supervisione, nessuna decisione: [SUPERVISIONE_AMMISSIONE_20261121.md](../SUPERVISIONE_AMMISSIONE_20261121.md). Verificato localmente: pose EPIC-Fields per tutti i 33310 frame osservati di P01_01 e per le 446 osservazioni del campione; mesh di scena P01_01 disponibile; codice di riferimento Whareformer allinea DA alla mesh (`da_aligned`). La memoria attuale registra invece in coordinate camera, senza pose né scala di scena verificata. Conseguenza proposta: posa relativa dalle camere come riferimento indipendente nei soli intervalli statici; identità, posa e utilità restano target distinti. Indizio preliminare (XYZ ufficiali): 236/429 coppie consecutive con spostamento del centroide sotto 1% dell'estensione della scena, non prova di staticità. Stato HPC non ricontrollabile da questo ambiente (DNS); nessun job, soglia, codice o training. Prossimo passo proposto: audit CPU di fattibilità sulle 429 coppie, previa scelta di Marco su ruolo delle pose (solo riferimento o anche ingresso) e costo falsa ammissione/falso rifiuto.

## Acquisizione P01_01 avviata e SuperFlex accodata — 21 novembre 2026

**Ultima osservazione:** 782990 RUNNING a 9m19s, archivio RGB completo acquisito e 20805 maschere generate, log senza errori osservati. 782968/782969 ancora PENDING afterok su 782990. Acquisizione/verifica non ancora concluse; inferenza GPU non ancora osservata. Prosecuzione automatica predisposta, nessuna nuova conferma richiesta; controllare `coverage.json`, stati/log e ricevute dei blocchi. La seguente nota di invio è storica.

**Aggiornamento successivo:** RGB ufficiali scaricati integralmente. 782967 cancellato dopo 10m56s per evitare estrazione di JPEG non necessari; sostituito da **782990** (PENDING all'invio), con archivio e file completati preservati. **782968/782969** restano gli stessi, dipendenza aggiornata afterok su 782990; nessuna GPU duplicata. Log corrente `acquire_782990.out/.err`. Revisione runtime con filtro dei JPEG necessari e blocco esclusivo del riepilogo verificata per hash. Copertura maschere e avvio GPU ancora da osservare; il seguente stato iniziale è storico.

Su mandato esplicito avviati **782967** acquisizione (RUNNING a 30s), **782968/782969** GPU (PENDING afterok acquisizione). Archivio RGB ufficiale 1.72 GB raggiungibile, maschere VISOR esistenti da verificare per tutte le 110590 osservazioni. [Configurazione, log e ripresa](../ARRICCHIMENTO_COMPLETO_P01_20261121.md). Radice `~/cv_project/p01_full_enrichment_20261121_v1/`, log `acquire_782967.out/.err` e `geometry_<job>.out/.err`; ricevute iniziali `submitted_jobs.json`, successive `submissions/`. Due sorgenti DA/MoGE, riuso delle 446 forme, blocchi 512 e massimo due GPU con continuazione per ramo. Nessun nuovo training o modifica dei gate. Acquisizione/verifica e inferenza completa ancora pendenti; non rilanciare job già inviati. Stato attuale supera la precedente nota di preparazione senza job.

## Applicazione dei testi revisionati — 21 novembre 2026

Marco conferma e richiede applicazione e pubblicazione dei vecchi commenti revisionati. Applicati 135 campi a sette riquadri e otto collegamenti, con le ultime formulazioni generali senza riferimenti alle singole esecuzioni. Struttura e altre schede conservate; backup locale precedente disponibile. Pubblicazione completata su main: https://github.com/Federico-cia/Whareformer-SuperFlex-Project/commit/9fe32e6ed8752fddb2c5850e254682bab8f6e0a6. Verificati servizio, copia offline, collegamenti e integrità dei contenuti.

## Estensione geometrica a tutto P01_01 autorizzata — 21 novembre 2026

Marco richiede SuperFlex per tutte le 110590 osservazioni originali (33310 frame). Creato elenco completo in `outputs/p01_full_enrichment_20261121_v1/target_observations.json`: 446 geometrie già verificate, 110144 pendenti. Stato in `status.json`. Prima dipendenza: acquisire/verificare RGB e maschere completi, attualmente parziali; nessuna nuova inferenza o job avviato in questa preparazione. Conservare osservazioni mancanti/fallite esplicitamente, senza escluderle dal denominatore. Mandato di estensione approvato; sorgente geometrica e budget della run completa da rendere espliciti prima del lancio.

## Criteri di ammissione appresi — indicazione di Marco, 21 novembre 2026

Marco richiede che le soglie di accettazione siano apprese dai dati anziché imposte manualmente; obiettivo esplicito conservare viste parziali valide. Richiede spiegazione di parzialità, ambiguità, regole correnti e alternative di validazione con pro/contro. Direzione approvata: apprendimento del criterio; modello, target, loss e protocollo non ancora scelti. Nessun training, codice, soglia o job modificati.

Verificato cloud_memory.py/cloud_updater.py: trasformazione rigida senza stima scala; supporto in entrambe le direzioni almeno 0.65 entro 0.08R; q90 dell'80% più vicino non oltre 0.15R; alternative entro 5% dello score più epsilon rifiutate se differiscono oltre 15 gradi o spostano il centroide oltre 0.08R. Basta un gate fallito. R è il raggio RMS del riferimento fit; rapporto dei raggi registrato, non gate autonomo. Query separate dal fit, non viste indipendenti. Inizializzazione senza confronto con memoria precedente, con soli controlli di validità dell'input.

Proposte da discutere: classificatore leggero sulle diagnostiche, criterio condizionato alla sovrapposizione/affidabilità dei punti, oppure apprendimento dell'utilità della fusione. Evitare target ricavati dai gate stessi: replicherebbero le euristiche. Identità oracle non certifica posa o scala. Possibile supervisione automatica con trasformazioni note su dati sintetici/crop, verifiche RGB multivista e viste reali escluse; limiti rispettivi: domain gap, dipendenza da pose/visibilità/movimento, validazione geometrica reale non ancora disponibile. Vincolo precedente di nessuna nuova annotazione manuale preservato. Separare dati per oggetto/sequenza e valutare errori di ammissione/rifiuto e qualità della memoria; nessuna opzione già adottata. Fonti primarie consultate per fattibilità concettuale, non compatibilità EPIC verificata: PREDATOR (CVPR 2021, overlap appreso) e Deep Global Registration (CVPR 2020, affidabilità delle corrispondenze appresa).


## Priorità e divisione del lavoro aggiornate — 21 novembre 2026

Marco comunica che il compagno segue il punto 2 (integrazione della forma nel matcher), mentre Marco prende in carico il punto 3 (ammissione dei punti nella memoria geometrica). Punti 1 (confronto delle forme) e 4 (collocazione/aggiornamento nella scena) dopo la risoluzione di entrambi. Richiede di procedere sul punto 3 iniziando dal recap di stato e criticità: superato il precedente rinvio della revisione dei gate, conservato sotto come storia. Nessuna nuova soglia, alternativa o protocollo già adottati; nessuna modifica del codice o nuovo job in questo passaggio. Nessun metodo o risultato del compagno comunicato.

Ricognizione conclusa sui resoconti esistenti: 31 fusioni DA/40 MoGE per variante nella campagna, senza validazione fisica indipendente; audit del prefisso con rifiuti per sola ambiguità e sovrapposizione asimmetrica compatibile con parzialità. Prossimo passo proposto, da definire: validazione indipendente di ammissioni e rifiuti, distinguendo simmetrie, parzialità, scala e identità. I controlli di scala necessari alla registrazione restano nel punto 3. Evidenze e limiti in [campagna](../RISULTATI_CAMPAGNA_HPC_20261115.md) e [audit](../RIPRESA_HPC_20261114.md). Nessun nuovo esito sperimentale; stato del job di arricchimento non ricontrollato.


## Dati di training e campione supervisionato verificato — 21 novembre 2026

**782875 COMPLETED 0:0, 3m15s**, nessun job di questo lavoro attivo/in attesa. Creati 446 esempi / 247 frame / 17 identità benchmark da P01_01, con oracle e input originali, quattro rappresentazioni geometriche e archivio di viste solo precedenti. 429 query con geometria della candidata corretta già disponibile. Tre test locali/remoti e audit indipendente passati; confronto locale con tutte le 110590 annotazioni ufficiali riuscito. Copia numerica/metadati acquisita, geometrie grandi sull'HPC. **Zero esempi Nuova track nel campione:** diagnostico di sviluppo, non training completo. [Resoconto e inventario](../ARRICCHIMENTO_TRAINING_20261121.md), [guida ai dati](../../evidence/ASSET_ESTERNI.md#asset-ae0b21d1b03d). Radice `~/cv_project/training_enrichment_20261121_v1/`, log `enrich_782875.out/.err`, ricevute in `dataset/`. Disponibili completi feature/XYZ/annotazioni P01_01, non verificati gli ingressi completi degli altri 55 video; dati grezzi parziali su cinque. Prossimo passo: acquisire/localizzare input mancanti e ampliare copertura includendo Nuova track prima del training. Zero nuove inferenze/training/etichette manuali; filtri invariati, non rilanciare il job concluso.

## Revisione dei vecchi commenti — 21 novembre 2026

**Criterio editoriale aggiornato da Marco:** evitare nei commenti riferimenti a campagne o run specifiche, date, conteggi ed esiti legati alle singole esecuzioni. Sono ammesse indicazioni generali su implementazione, verifiche svolte e limiti; dettagli numerici e cronologia restano nei resoconti. Riformulate le proposte interessate in forma generale, senza applicarle alla mappa. La regola vale per i commenti futuri e per le revisioni; non autorizza modifiche automatiche ai testi già applicati.

Marco richiede la revisione dei testi conservati, con le stesse regole editoriali e proposta in chat prima dell’applicazione. Preparati tutti i nove campi per sette riquadri (R01, R02, R12–R15, R23) e otto collegamenti (C10–C13, C15, C23–C25), incluso C15 con testo manuale e precedente completamento. [Testi proposti](../../evidence/ASSET_ESTERNI.md#asset-a75d64057ac5) e [specifica con testi precedenti e hash](../../evidence/ASSET_ESTERNI.md#asset-31d5b121d98f). Sono proposte non approvate e non applicate; nessun nuovo push.

Riletti contenuti, provenienza, risultati della campagna, discussione delle integrazioni e codice pertinente. Chiariti campione di sviluppo, geometria stimata, ricostruzione della singola osservazione, superfici interne/sovrapposte nel campionamento del descrittore e separazione fra rete congelata e correzione esterna. Rimossa l’affermazione non dimostrata di maggiore costo del confronto diretto dei punti e la superiorità generale attribuita a SuperFlex. Verificati perimetro, 135 campi non vuoti e invariabilità SHA-256 dei dieci file della mappa. Nessun esperimento, job o modifica metodologica. Prossimo passo: revisione/conferma di Marco in chat, poi eventuale applicazione dei soli testi confermati.

## Pubblicazione GitHub conclusa — 21 novembre 2026

**Pubblicazione verificata.** Aggiornamento pubblicato su `main`, commit [c612cad](https://github.com/Federico-cia/Whareformer-SuperFlex-Project/commit/c612cad4c161fd3bfcca11ba31525102cee5ab58); riferimento remoto verificato tramite confronto GitHub, identico al commit pubblicato. Inclusi mappa Rami paralleli con 39 riquadri/49 collegamenti e testi confermati, interfaccia, fonti portabili, provenienza e memoria corrente. 34 file nel commit; contributi del collega e storia preservati. Controlli: 521 collegamenti, 41 sorgenti Python e 192 hash senza errori; servizio mappa, 792 campi, copia offline, estremi dei collegamenti e disegno verificati. JSON e copia offline identici ai file locali approvati; nessun pattern di credenziale rilevato nel controllo dei file modificati, nei limiti della ricerca. Connettore GitHub disponibile in lettura ma scrittura rifiutata (403); pubblicazione eseguita con Git autenticato e certificati di sistema. Nessun nuovo esperimento, training, job HPC o modifica dei filtri. Restano la revisione scientifica dei vecchi commenti e le decisioni metodologiche aperte.

## Ripresa della mappa e controllo repository — 21 novembre 2026

**Applicazione completata e HTML aperto.** Marco conferma i testi («Ok, aggiungi il testo. Poi aprimi qui l'html»). Applicati struttura Rami paralleli e commenti: 39 riquadri R01–R39, 49 frecce C01–C49, 792 campi identici alla specifica confermata. Schede manuali equivalenti conservate; revisione dei vecchi testi ancora distinta. Aggiornati JSON, copia offline e interfaccia con colori di provenienza, rombi, percorsi approvati, zoom/esplorazione, menu di navigazione, schede ed editor. Vecchie posizioni della versione 1 isolate per non alterare il nuovo flusso. [Ricevuta e backup](../../evidence/ASSET_ESTERNI.md#asset-02ba0b6a0060); guida corrente in [README della mappa](../../../mappa_interattiva/README.md).

Verificati sintassi, 39 elementi/49 frecce nel disegno, corrispondenza di tutti i testi e identità JSON/copia offline; servizio locale restituisce 88 revisioni. Nel browser verificati scheda nodo, scheda freccia, salvataggio invariato e spostamento da tastiera con ripristino. HTML lasciato aperto nella chat all'inizio del flusso, scheda del browser conservata come risultato. Servizio locale attivo nell'ultima osservazione su `127.0.0.1:8767` (processo avviato 10472); nessun nuovo job HPC, esperimento o push. Nessun ulteriore inserimento dei testi in attesa di conferma; restano le revisioni scientifiche dei vecchi commenti e i temi di metodo già aperti.

**Commenti per la struttura approvata.** Al successivo «Vai, procedi. Segui le mie regole», preparate le proposte per 28 schede di riquadro e 39 collegamenti nuovi/ridistribuiti, da consegnare in chat prima dell'inserimento. [Versione per revisione](../../evidence/ASSET_ESTERNI.md#asset-597cb4c6c15a), [tutti i campi](../../evidence/ASSET_ESTERNI.md#asset-077da30e5211), [specifica distinta](../../evidence/ASSET_ESTERNI.md#asset-1be0b98805d6). Coperti 39 riquadri/49 frecce con nove campi ciascuno; schede manuali equivalenti conservate, bozze precedenti riusate con stato non approvato. Riferimenti R/C soltanto per la revisione, non nuovi ID già applicati. Verificati campi non vuoti, riferimenti e conservazione delle schede manuali; contenuti correnti invariati per hash. Precisati fallback alle forme singole, ammissione distinta dal tracking e forma precedente con punti già aggiornati in caso di fallimento SuperFlex. Nessun nuovo esperimento o modifica metodologica. Prossimo passo: revisioni/conferma dei testi, poi applicazione della struttura e dei soli testi confermati.

**Approvazione successiva della struttura.** Marco conferma «Va bene questa mappa» sull'anteprima completa e chiede se siano stati aggiunti nodi/collegamenti. Confronto diretto verificato: originale 19/34, anteprima 39/49 (+20 nodi e +15 connessioni netti), con scomposizioni/accorpamenti di passaggi esistenti, senza nuovo metodo. Struttura complessiva approvata; i commenti completi e le nuove schede restano da revisionare, non implicitamente approvati. In questa risposta solo chiarimento e aggiornamento memoria; applicazione della mappa ancora non eseguita.

**Scelta visiva e anteprima completa.** Marco sceglie «Rami paralleli» e chiede di vedere l'intera mappa prima dell'applicazione. Preparata separatamente [l'anteprima complessiva](../../evidence/ASSET_ESTERNI.md#asset-c2a6dac1bf22), con versione SVG e tre ritagli; [struttura e limiti](../../evidence/ASSET_ESTERNI.md#asset-272ac4ae575d). La bozza copre tutti i 19 nodi precedenti, ridistribuiti in 39 elementi con 49 connessioni: separati rete/adattatore/assegnazione, le due memorie, inizializzazione tardiva, ammissione e fallimento della ricostruzione. Generazione e ispezione visiva eseguite, corretti testi fuori dai riquadri; contenuti correnti invariati per hash. La scelta riguarda lo stile: struttura complessiva e testi restano da revisionare prima dell'applicazione. Nessuna modifica alla mappa, inferenza o nuova esecuzione sperimentale.

**Accessibilità delle proposte.** Marco segnala di non riuscire a visualizzare le alternative nella risposta interattiva; causa non accertata. Esportate e ispezionate tre immagini PNG delle stesse disposizioni in `outputs/revisione_mappa_20261121/alternativa-1-rami-paralleli.png`, `alternativa-2-asse-centrale.png` e `alternativa-3-fasi-separate.png`, da mostrare direttamente in chat. Scelta visiva e approvazione dei testi ancora pendenti; mappa invariata.

**Chiarimenti successivi e bozze.** Marco conferma tutti i campi delle schede mancanti, «-» dove non c'è contenuto sostanziale; revisione degli esistenti rinviata. Approvata rappresentazione dell'implementazione attuale, alternative solo nelle schede, una sola mappa destinata soprattutto all'interfaccia interattiva. Autorizzata riorganizzazione di nodi e frecce; approvati rettangoli/processi, rombi/decisioni, colori e legenda di provenienza con risorse esterne neutre. Richieste diverse proposte visive prima della scelta e dell'applicazione. [Testi proposti](../../evidence/ASSET_ESTERNI.md#asset-b6532746ea52) pronti per nove nodi/tredici collegamenti e campo E10; tre anteprime separate («Rami paralleli», «Asse centrale», «Fasi separate») mostrano il ciclo critico associazione/aggiornamento/memoria. Anteprime consultate nel browser e apertura di una scheda verificata; sintassi controllata. Nessuna modifica ai contenuti o all'applicazione della mappa, nessuna nuova run. Prossimo passo: revisione dei testi e scelta visiva di Marco; eventuali schede dei nuovi blocchi da proporre dopo la scelta.

Marco richiede il completamento dei commenti mancanti, prima proposti in chat e applicabili alla mappa soltanto dopo conferma esplicita. Testi sintetici per valutatori con basi ML/CV ma estranei al progetto: nodi = processo dello step; collegamenti = perché e come l'output della sorgente serve alla destinazione. Richiesto anche riordino visivo dall'alto al basso, riduzione di incroci/sovrapposizioni, distinzione tra processi e decisioni e tra componenti originali Whareformer, originali SuperFlex e aggiunte del progetto. Chiarimenti su perimetro editoriale e grafico ancora da raccogliere; nessuna modifica alla mappa eseguita. Questo mandato supera il precedente rinvio del riordino grafico e consente in futuro l'applicazione dei testi da parte dell'assistente dopo conferma.

Controllo GitHub tramite connettore: `main` a [ccc1376](https://github.com/Federico-cia/Whareformer-SuperFlex-Project/commit/ccc1376c5a046a41ec2525d6ee6668f06b3b13e0), un commit dopo 0fce33b, solo memoria/documentazione e inventario; nessun aggiornamento del codice o della mappa nel confronto. Il ramo `prepare/superflex-core` non contiene commit aggiuntivi rispetto a 0fce33b. Nessun merge, pull o push. JSON locale riletto: nove nodi e tredici collegamenti segnaposto, più completamento E10; conteggi coerenti con l'ultima ricognizione. Prossimo passo: chiarimenti di Marco, poi bozze in chat e proposta grafica coerente con il perimetro concordato.

## Valutazione critica delle due strade

Su richiesta di Marco discussi rischi di segnale, confronto e valutazione: entrambe le architetture condividono la perdita d'informazione dell'eventuale distanza scalare; prima proposta è verificarne complementarità rispetto ad aspetto/posizione. [Dettaglio aggiornato](../FATTIBILITA_DUE_INTEGRAZIONI_20261116.md), registro voce 82. Nessuna nuova analisi quantitativa, scelta metodologica o run; entrambe le strade e divieto di nuove annotazioni manuali invariati.

## Direzione aggiornata: due integrazioni e solo dati già etichettati — 16 novembre 2026

Marco vuole tentare sia confronto geometrico esterno sia riaddestramento Whareformer, previa verifica di fattibilità/distanza. Esclude qualsiasi nuova etichettatura manuale; preferisce gli stessi dati di training originali. Questo supera l'alternativa condizionale e la proposta manuale della discussione precedente. [Verifiche e piano proposto](../FATTIBILITA_DUE_INTEGRAZIONI_20261116.md), registro voce 81: target generabili automaticamente mediante oracle originale; limiti delle identità EPIC basate sui nomi/esclusioni; manifest privi di storia geometrica completa. D2 esistente e Chamfer dopo allineamento sono candidati, non distanza finale scelta. Verificato anche export mesh come concatenazione di primitive, non superficie esterna dell'unione. Prossimo passo proposto: accessibilità dei dati originali, replay con provenienza e costo della geometria prima delle due prove. Nessun download/training/job nuovo; filtri invariati. Note precedenti conservate come storia, scelta finale del metodo ancora aperta.

## Brainstorming sul primo punto importante — 16 novembre 2026

Approfondimento successivo: Marco richiede che il peso abbia una stima scientificamente giustificata e dati di supervisione espliciti; altrimenti considera l'inserimento nel modello e il riaddestramento. Verificato che Whareformer combina due distanze attraverso embedding e Transformer appresi, senza due pesi manuali globali. [Analisi di architettura, stima e dati](../DISCUSSIONE_INTEGRAZIONE_FORMA_20261116.md); registro voce 80. Proposte non adottate. Prossima verifica proposta: disponibilità/granularità dei target originali e join alle geometrie; né nuovo dataset né fattibilità computazionale già accertati.

Marco chiede di iniziare la discussione dall'architettura dell'integrazione della forma nel matching. Discussione avviata distinguendo correzione esterna calibrata, fusione con pochi parametri appresi a reti congelate e adattamento della rete. Raccomandazione preliminare dell'assistente: chiarire prima se le distanze distinguono associazioni corrette/errate e come si rapportano ai margini della baseline; non è un'analisi già eseguita né una scelta approvata. Decisione condivisa con il compagno ancora aperta; nessuna nuova implementazione o run. Dettaglio: registro, voce 79.

## Aggiornamenti GitHub pubblicati — 15 novembre 2026

Aggiornamenti pubblicati su `main`, commit [0fce33b](https://github.com/Federico-cia/Whareformer-SuperFlex-Project/commit/0fce33b6acdea13d6d36bf557fcbf0c311b34ae7), riferimento remoto verificato dopo il push. Inclusi snapshot manuale della mappa, checklist di revisione, decisioni ancora pendenti e memoria corrente; corretto il README sui dati riusati rispetto alla geometria rigenerata. Codice e risultati della campagna erano già su remoto a d8fb991. Preservati contributi del collega e storia Git; nessun nuovo esperimento o cambio dei filtri. Controlli: 467 collegamenti, 41 sorgenti Python e 179 hash senza errori, servizio mappa in sola lettura superato; 13 file controllati senza pattern sensibili rilevati, nei limiti del controllo. Mappa copiata byte per byte dalla versione manuale locale.

## Conteggio delle schede salvate durante la revisione — 15 novembre 2026

Lettura diretta del JSON della mappa dopo la compilazione manuale di Marco: 10/19 nodi compilati, nove ancora segnaposto (B08/B09/B10/B11/B13/B15/B17/B18/B19); 21/34 frecce commentate, 13 ancora segnaposto (E07/E13/E14/E16/E17/E19/E24/E28/E30/E31/E32/E33/E34). Tra le 21 commentate: E10 conserva «[da espandere]» nelle alternative; E21 ha il solo campo miglioramenti vuoto, che può restare non applicabile. Conteggio di compilazione, non audit scientifico completo; nessuna modifica ai testi della mappa. I conteggi iniziali nella ricognizione descrivono lo snapshot precedente.

## Architettura del contributo di forma — discussione con il compagno pendente

Marco chiarisce che restano da decidere insieme al compagno sia il modo in cui la forma entra nei calcoli sia la sua influenza. Evidenziate nei to-do correzione esterna attuale, calibrazione/possibile apprendimento dei parametri a reti congelate e adattamento della rete. L'apprendimento supervisionato suggerito dall'assistente è una proposta non approvata. Preparata in chat nota per B12; mappa non modificata dall'assistente, nessuna nuova esecuzione o cambio di metodo. Per ora si documenta l'implementazione attuale come provvisoria.

## Duplice uso della forma da discutere — chiarimento durante B07

Precisazione successiva: la preoccupazione principale di Marco è la fattibilità della collocazione e dell'aggiornamento della superficie nella scena con scala, posizione e rotazione corrette. Tema distinto evidenziato nei to-do importanti e in C13: non basta il confronto di forma né il solo XYZ della traccia. Da discutere catena dei riferimenti/trasformazioni, coerenza della scala e movimento dell'oggetto; nessuna capacità di collocazione accurata assunta o nuova esecuzione autorizzata da questo promemoria.

Marco richiede memoria dei limiti di D2 (perdita d'informazione e scala assoluta rimossa) e chiarisce l'interesse a usare la ricostruzione anche come memoria geometrica dell'oggetto collocata nella scena, accanto all'XYZ della traccia. Intento da discutere, non nuova implementazione o validazione: distinguere descrittore per matching e forma conservata con inversa della normalizzazione; scala/riferimento/ancoraggio e orientamento restano da verificare. Tema evidenziato in TODO.md; nessun cambio a codice, mappa, filtri o job.

## Ammissione geometrica da discutere e validare — 15 novembre 2026

Precisazione durante E22: Marco richiede esplicitamente confronto con il compagno prima di considerare definitivi meccanismo e criteri di ammissione. Rafforzato il to-do esistente; preparate in chat descrizioni E22/B16 con funzionamento implementato e alternative discusse. I gate del prototipo non sono una decisione scientifica conclusiva del gruppo; nessuna modifica alla mappa da parte dell'assistente o nuova esecuzione.

Marco ribadisce che la decisione di ammettere punti nella memoria è cruciale e richiede discussione approfondita e test. Attività evidenziata in cima a TODO.md; è il tema dei filtri di fusione già rinviato, non un nuovo problema indipendente. Nessuna riattivazione automatica della revisione, modifica al metodo o nuova run. Altro tema scientifico distinto già aperto: descrittore/contributo della forma al matching e calibrazione (C11); non identificato con certezza come l'altro promemoria a cui Marco allude.

## Revisione guidata della mappa — 15 novembre 2026

Marco richiede analisi del contesto e assistenza alla revisione, riservando a sé la modifica dei testi della mappa. Ricognizione delle 19 schede di nodo e 34 collegamenti completata: 12 nodi e 26 frecce sono segnaposto; individuate anche affermazioni inesatte o superate nelle schede compilate. [Checklist con evidenze e ordine proposto](../REVISIONE_MAPPA_20261115.md). Testi e struttura della mappa invariati; nessuna nuova inferenza o verifica HPC. Prossimo passo: scrittura manuale di Marco e verifica progressiva in chat, partendo dagli input e dal confine tra dati riusati e rigenerazione. Le precedenti richieste di compilazione automatica della mappa sono superate per questa revisione; risultati della campagna e rinvio dei filtri restano invariati.

## Campagna estesa conclusa — 15 novembre 2026

[Resoconto e output](../RISULTATI_CAMPAGNA_HPC_20261115.md). Tutte le 29 configurazioni completate e valutate su 33310 frame/110590 osservazioni; nessuna assegnazione diversa da W0 e metriche identiche (IDF1 73.269735%, mPCL 70.465504%). Quattro controlli zero esatti, nessun timeout/errore di aggiornamento/worker fallito o richiesta pendente.

764678 COMPLETED 0:0 (4h13m00s), 764679 COMPLETED 0:0 (3h54m41s), riepilogo 765084 COMPLETED 0:0 (42s). Preflight/geometria/bundle già conclusi; nessun job della campagna attivo o in attesa. Nuvole/forme per tutte le 446 osservazioni pronte in entrambe le sorgenti. Per ogni variante con accumulo: DA 23 inizializzazioni/31 fusioni/392 rifiuti; MoGE 23/40/383. SuperFlex della memoria 54/63 pronte per variante, ripetizioni non indipendenti.

Report e accounting finali acquisiti localmente in outputs/campaign_20261115_v1/final_reports/; grandi tracce, nuvole e mesh di tutte le varianti ancora sull'HPC in ~/cv_project/campaign_20261115_v1/. Prossimo passo: analizzare margini, distanze, copertura di casi difficili e qualità delle fusioni. Nessun metodo selezionato né modifica dei filtri; revisione ancora rinviata. Non rilanciare i job conclusi.

Avanzamento precedente (storico): W0 concluso (codice 0); Sacc_da_zero osservato a 11432/33310 frame, gruppi 764678/764679 ancora RUNNING. Dettagli aggiornati in CAMPAGNA_HPC_20261115.md; risultati comparativi finali pendenti.

## Avvio della campagna — stato storico superato

Marco autorizza preparazione e avvio dopo i controlli. [Specifica, limiti e ripresa](../CAMPAGNA_HPC_20261115.md): 247 frame/446 osservazioni congelati prima dell'inferenza, geometria DA/MoGE rigenerata e 29 configurazioni sull'intera storia P01_01. Feature/PCA/XYZ ufficiali riusati; nessun nuovo training o filtro modificato. Campagna di sviluppo, non test held-out o beneficio assunto.

Preflight 764670 COMPLETED 0:0 (1m35s), 76 test tutti passati. 764674 COMPLETED 0:0 (11m38s), 764675 COMPLETED 0:0 (1m41s): tutte le 446 osservazioni hanno nuvole e forme pronte per DA/MoGE, feature baseline byte-identiche. 764678 e 764679 RUNNING per 19 trial CPU e dieci GPU. Riepilogo da inviare automaticamente al termine del primo gruppo, con dipendenza su entrambi. Risultati finali ancora pendenti. Ricevuta/stati remoti in ~/cv_project/campaign_20261115_v1/submitted_jobs.json e logs/; snapshot locale outputs/campaign_20261115_v1/.

Limite QoS rilevato: quattro job inviati/due attivi. Primo array respinto, nessun trial partito da quell'array; adattato il solo raggruppamento, senza duplicare i job esistenti. Concorrenza attuale un gruppo CPU/un gruppo GPU, massimo 9.5 ore GPU complessive. Non reinviare i job; acquisire prima stato e output. Revisione dei filtri ancora esplicitamente rinviata.

## Analisi dopo la prima run — proposta, non nuovo piano approvato

[Valutazione e pro/contro](../VALUTAZIONE_PRIMA_RUN_20261114.md): prima diagnosi mirata di qualità delle fusioni, discriminatività e calibrazione dei punteggi; poi ampliamento controllato della copertura e confronti appaiati. Frontend RGB resta necessario come percorso distinto. Nuovo punto C11 nel registro critico: tutte le 695 correzioni erano negative con distanza neutra zero; rischio di asimmetria per geometria mancante, senza effetto sulle assegnazioni osservato. Nessuna nuova run, modifica dei metodi o riattivazione della revisione filtri. La domanda di Marco richiede un parere, non autorizza automaticamente una nuova direzione decisiva.

## Prima run completa conclusa — 14 novembre 2026

Job 764454 COMPLETED 0:0 (8m40s), audit/valutazione 764474 COMPLETED 0:0 (53s); nessun job di questa run attivo/in attesa. Tutti i 33310 frame e 110590 osservazioni del protocollo ufficiale P01_01 elaborati (937–98099; metadati video 99135). Non tutti i RGB: feature/PCA/XYZ e 71 geometrie su 38 frame riusati con hash, nuova inferenza Whareformer e 25 nuove SuperFlex sugli stati ammessi. Copertura geometrica 0.0642% delle osservazioni.

S-accumulo DA, peso 0.1 non calibrato, filtri invariati: 18 inizializzazioni, 7 fusioni ammesse, 46 rifiuti, nessun errore o richiesta pendente. 695 logits modificati; 76 confronti futuri usano forme da fusioni. Memoria finale: 18 track, 38732 punti osservati, provenienza verificata; accuratezza fisica delle fusioni non certificata. Assegnazioni identiche alla baseline: 52 track, IDF1 73.269735%, mPCL 70.465504%, nessun miglioramento.

[Resoconto e output](../PRIMA_RUN_COMPLETA_20261114.md).

Percorso HPC `~/cv_project/full_video_20261114_v1/`; log `cv_full_active_764454.out/.err`, `cv_full_audit_764474.out/.err`, `tests_764454.log`; output `run_764454/`, `cache_764454/`, `final_evaluation/`, `final_comparison/`, `audit/`. Tutti gli output scaricati in `outputs/full_video_20261114/results/` nella cartella locale. La valutazione iniziale a 98099 è superata da quella finale con orizzonte originale 99135; nessuna nuova inferenza per correggerla.

Prossimo passo: discutere qualità/validazione indipendente delle fusioni e copertura prima di conclusioni di efficacia; frontend RGB rigenerato e calibrazione/test rimangono aperti. Revisione dei filtri ancora rinviata: non avviarla automaticamente. Prima esecuzione operativa chiusa; non rilanciare job conclusi. Pubblicazione verificata su main: 8694e4b (codice ed evidenze della run).

## Mandato: primo round e aderenza ai paper — 14 novembre 2026

Marco conferma: obiettivo n. 1 una run completa della pipeline; registrare onestamente punti critici, tradeoff e dubbi, poi affrontarli sistematicamente. Mantenere il metodo dei paper quando applicabile e funzionante; alternative solo annotate finché non necessarie. [REGISTRO_CRITICITA_PIPELINE.md](../../memory/REGISTRO_CRITICITA_PIPELINE.md) raccoglie la diagnosi iniziale e distinguerà metodo originale, adattamento nostro, evidenza e verifica pendente. L’obiettivo è dimostrare l’integrazione, senza assumere anticipatamente il beneficio.

Prima lettura operativa: feature ufficiali dell’intero P01_01 già disponibili; nel vecchio preparatore diagnostico l’arresto a 7508 è codificato nel nostro script. Questo non risolve ancora generazione/coprertura geometrica e frontend dalle immagini. Nessuna nuova run o modifica degli algoritmi; filtri ancora rinviati. Per il resoconto finale distinguere esecuzione completa, fusioni effettive ed efficacia misurata.

## Priorità esplicita: un video dall’inizio alla fine — 14 novembre 2026

Marco chiarisce che il primo obiettivo è chiudere una singola esecuzione integrata su un video completo, prima della selezione delle alternative o dell’ottimizzazione. La proposta precedente non va interpretata come obbligo di completare prima calibrazione, confronti o revisione dei filtri. Il codice esistente esegue il percorso da input preparati a report, verificato sul prefisso; non è ancora verificato l’ingresso completo da immagini per l’intero video.

Direzione approvata: costruire il percorso minimo completo con una configurazione esplicita e provvisoria, riusando modelli/componenti presenti e dichiarando gli input necessari (RGB, maschere, camera/pose e asset scena). Primo candidato operativo: P01_01 già disponibile, come video di sviluppo, non nuovo test indipendente. Preparare gli input per l’intera sequenza prevista dal protocollo, collegare il frontend, eseguire tracking/memoria/ricostruzioni ammesse e produrre output finale. La verifica sul piccolo prefisso serve solo a eliminare errori prima della run completa, non sostituisce il video completo richiesto.

Nessuna ottimizzazione o griglia di metodi come prerequisito. Filtri invariati e loro revisione ancora rinviata. Se tutte le fusioni vengono respinte, dichiararlo: il completamento dell’esecuzione non prova accumulo multivista funzionante o beneficio tracking. Le alternative e il tuning vengono dopo la prima esecuzione integrata. Il percorso non equivale a video arbitrario RGB-only: un segmentatore nuovo resta fuori dal primo traguardo.

## Roadmap di chiusura proposta — 14 novembre 2026

Su richiesta di Marco, riletto main remoto 0865949 e formulata [PROPOSTA_CHIUSURA_PIPELINE_20261114.md](../PROPOSTA_CHIUSURA_PIPELINE_20261114.md): asset → frontend rigenerato → copertura → verifica multivista quando riattivata → confronti a peso attivo → consegna riproducibile. Proposta, non nuova approvazione; frontend resta prioritario e già autorizzato, revisione filtri ancora rinviata. Nessun esperimento o nuovo controllo HPC; non modificata la roadmap approvata. Il documento distingue completezza tecnica ed efficacia, con criteri di uscita e finestre indicative fino al 23 novembre.

## Collegamenti fra riquadri B01–B07 — 14 novembre

Su richiesta di Marco compilati e revisionati i campi di E01–E06, E08 ed E09, inclusi i segnaposto delle tre frecce già modificate. Verificati codice del ritaglio Whareformer e pipeline geometrica, salvato tramite servizio con backup: nodi invariati, copia offline identica e campi delle otto frecce presenti. E07 riguarda B09 ancora da compilare. Testi documentali da rivedere, nessun nuovo esperimento o scelta scientifica. Persistono richieste di completamento in B04–B07.

## Schede della mappa aggiornate manualmente — 14 novembre

Alla lettura corrente risultano modificate B01–B07 ed E01–E03; B08–B19 ed E04–E34 sono ancora segnaposto. B04–B07 contengono richieste di completamento; B07 ha cinque campi vuoti. Le modifiche manuali sono da preservare e non equivalgono ad approvazione scientifica. Prossimo: completare e verificare i campi richiesti, poi proseguire progressivamente con le schede.

Pubblicazione del riordino completata e main remoto verificato al commit 0865949eab4d916bad6626fcdfc786a9032b7d7b. Controllo strutturale: 394 collegamenti locali, 34 sorgenti Python, 140 hash, zero errori; servizio mappa verificato in sola lettura. Suite: 70 passati e due skip. Nessuna nuova inferenza.

## Riordino GitHub richiesto da Marco — 14 novembre 2026

README unico ingresso della repository; rimosso START_HERE e segnaposto Integration, nove vecchi piloti esclusi dalla versione pubblicata ma preservati localmente e nella storia Git. Memoria operativa corrente distinta dai resoconti in context/archive, collegamenti riparati e asset esterni dichiarati. Sorgente test configurabile con WHAREFORMER_SRC; suite riordinata: 72 casi, 70 passati e due skip motmetrics. Codice del collega, risultati e mappa manuale preservati; nessun nuovo esperimento né modifica ai filtri. Worktree pubblicabile: shared_exports/handoff_ai_20261114. Controllo ripetibile: tools/check_repository.py in quel worktree. La struttura GitHub usa context/memory e context/archive; la cartella locale mantiene anche i materiali storici originali.

## Passaggio a un altro provider AI — 14 novembre 2026

Marco richiede memoria e contesto autosufficienti nella cartella e su GitHub. Guida corrente: [LEGGIMI_PASSAGGIO_AI.md](../../evidence/ASSET_ESTERNI.md#asset-c4e1bdd7c3c4), che distingue implementato/verificato/pendente, decisioni, dipendenze e prossimi passi. Pubblicazione selettiva preparata dalla main del collega fc5aa30: codice integrazione, memoria, mappa corrente ed evidenze leggere; dati grandi, pesi e accessi esclusi. Nessun nuovo esperimento, filtro invariato. Gli stati storici di attesa frontend, output collega mancanti e job 763531 attivo sono superati dalle verifiche successive. Consegna pubblicata su main, riferimento remoto verificato al commit 6d7a8b7; dettagli in docs/CONDIVISIONE.md e inventario in context/evidence/publication_inventory.json. Nessun job nuovo.

## Cartella mappa e ripresa — 14 novembre

Mappa nella cartella dedicata mappa_interattiva/ della repository locale, con README.md canonico, inventario, avvio e istruzioni di ripresa in altra chat. LEGGIMI rimanda al README; backup esclusi da Git. Nessuno spostamento dei file applicativi, nessun commit/push. contenuti.json invariato per hash; preservare le schede manuali B01/B02/B03 ed E01/E02/E03.


## Salvataggio revisione mappa verificato — 14 novembre

Verificata persistenza della revisione manuale di B01/B02/B03 ed E01/E02/E03: JSON valido, copia JS offline e servizio identici; 12 backup, nessun temporaneo residuo. Browser con conferma Salva e nessun modulo aperto. Verifica del salvataggio, non approvazione scientifica; contenuti invariati.


## Frontend approvato e percorso cache verificato — 14 novembre

Ok di Marco ricevuto. Implementati contratto e import cache verificato, ingresso --frontend-manifest nel comando unico; dieci detection nei tre frame con intera storia di 3398 frame, quattro file dati byte-identici. 72 casi locali (70 passati, due skip motmetrics). Rigenerazione da RGB ancora non eseguita: pesi/revisione DINOv2, provenienza PCA e scala/ambiente scena da verificare, inventario circoscritto senza prova di assenza globale. [Avanzamento e limiti](../FRONTEND_AVANZAMENTO_20261114.md). Piano parzialmente eseguito, non dichiarato completo; filtri invariati. 763531 concluso 0:0 in 23m24s, nove varianti zero completate e valutate; nessun nuovo job del frontend. Le note di attesa dell’ok e job ancora attivo sono storiche.

Completati i tre segnaposto di B01/B02 nella mappa: EPIC-KITCHENS, provenienza VISOR e modulo di segmentazione (SAM 2 come esempio da valutare, con inizializzazione esplicita). Resto dei campi preservato. Marco chiarisce che le parentesi quadre nei suoi testi sono richieste di completamento da parte dell’assistente. Nessuna adozione o implementazione di un segmentatore. Fonte primaria consultata: https://github.com/facebookresearch/sam2.


## Piano frontend preparato, attesa dell’ok — 14 novembre

Marco richiede pianificazione prima dell’esecuzione. Proposto collegamento preprocessing → runner: inventario dipendenze, manifest unico, import/rigenerazione con cache, comando unico e piccolo pilota P01_01 mantenendo la storia del tracker. [PIANO_FRONTEND_UNIFICATO_20261114.md](../PIANO_FRONTEND_UNIFICATO_20261114.md). Piano non ancora approvato: nessuna implementazione o nuovo job per questo step prima dell’ok. Filtri ancora rinviati; job precedentemente autorizzati invariati, senza nuovo controllo di stato in questa fase.

## Schede più comprensibili e collegamenti modificabili — 14 novembre

Marco estende la modifica alle descrizioni dei collegamenti e richiede testi comprensibili anche alla giuria. Implementati editor/salvataggio frecce con backup e conflitti, menu Collegamenti per selezionarle. Titoli: Possibili miglioramenti, Coerenza dei dati, Possible points of failure. Riscritti solo funzione/evidenze/coerenza di Maschere 2D · VISOR; contenuti manuali di RGB e altri campi della maschera preservati e confrontati. Verificati salvataggio freccia su copia isolata e modulo/conferma nel browser senza alterare testo della freccia reale. Regola editoriale: funzione concreta e termini spiegati, senza formule telegrafiche comprensibili solo a chi ha sviluppato il codice. Nessun esperimento o modifica al metodo scientifico.


## Valutatore e comando unico collegati — 14 novembre

Implementati export delle osservazioni/assegnazioni con hash, IDF1/mPCL originali con scope esplicito e comando input preparati → varianti → valutazione → tabella. 763498 COMPLETED/0:0 (33 s), otto test; 763530 COMPLETED/0:0 (45 s), 69 test tutti eseguiti, riprodotti IDF1 73.269735% e mPCL 70.465504% su predizioni registrate train. 763531 RUNNING a 10m50s nell’ultima osservazione: nove configurazioni zero, CPU e cache esistente; esito ancora da acquisire. [COMPLETAMENTO_PIPELINE_20261114.md](../COMPLETAMENTO_PIPELINE_20261114.md).

**GPU concluso:** 763324 COMPLETED/0:0 (43m30s), sei ricostruzioni reali ready e controllo zero esatto, ma nessuna fusione multivista ammessa. Filtri invariati e revisione ancora rinviata. Mancano unificazione del frontend dati, copertura sufficiente e calibrazione/test; il comando attuale parte da input preparati. Le precedenti note di metriche non collegate e GPU ancora attivo sono storiche.

## Descrizioni della mappa salvabili nei file — 14 novembre

Scelte esplicite di Marco: servizio locale, sole descrizioni dei riquadri, campi separati con Modifica/Salva. Implementati server.cjs e Avvia mappa.cmd; contenuti.json è la sorgente, contenuti.js la copia offline aggiornata. Backup prima di ogni modifica effettiva e protezione da aggiornamenti concorrenti; titoli/fonti/collegamenti non modificabili dall’editor. Verificati persistenza/backup e rifiuto conflitti/campi vietati su copia isolata; nel browser osservati modulo e conferma Salva senza alterare il testo originale. Guida aggiornata in [mappa_interattiva/LEGGIMI.md](../../../mappa_interattiva/LEGGIMI.md). Non modifica i Markdown scientifici; disposizione e revisione dei filtri rimangono rinviate.


## UX/UI mappa aggiornata — 14 novembre

Pannello sinistro richiudibile e chiuso inizialmente, zoom con rotella/pulsanti, pan dello sfondo, vista completa e 100%, disposizione orizzontale e stile aggiornato. Verificati visivamente nel browser apertura/chiusura, zoom (100→165%), pan e ritorno alla vista completa. Layout salvati preservati: Ripristina disposizione applica quello nuovo. Contenuti scientifici invariati. Guida: [mappa_interattiva/LEGGIMI.md](../../../mappa_interattiva/LEGGIMI.md).


## Revisione filtri di fusione rinviata — 14 novembre

Marco conferma che i filtri di ammissione delle nuvole vanno rivisti, ma non ora. Attività pendente esplicita in TODO.md: riesaminare soprattutto simmetrie/ambiguità e parzialità/supporto bidirezionale. Criteri numerici scelti dall’assistente come diagnostica provvisoria, non imposti dai paper o calibrati. Non avviare la revisione né cambiare soglie/codice in questa fase; resto del lavoro invariato.

## Prima mappa HTML interattiva — 14 novembre

Su richiesta di Marco creata [mappa_interattiva/index.html](../../../mappa_interattiva/index.html): 19 nodi trascinabili, 34 collegamenti selezionabili, pannello laterale, modifica delle schede, salvataggio nel browser e import/export JSON. Prime proposte di contenuto per RGB, maschere, aspetto e tre collegamenti; altre schede esplicitamente da compilare. File e modalità di modifica in [LEGGIMI.md](../../../mappa_interattiva/LEGGIMI.md). Verificati sintassi, caricamento e selezione/spostamento da tastiera nel browser; nessuna sincronizzazione automatica con Markdown o collaborazione simultanea. Prossimo passo documentale: discutere le prime schede in chat, poi completare geometria e posizione. Nessun nuovo esperimento o controllo HPC.

## Causa dei rifiuti verificata — 14 novembre

Audit dei log 763323: tagliere 5099 respinto solo per ambiguità, con supporto/residuo ammessi in DA/MoGE; a 7508 tagliere e coltello falliscono supporto/residuo, con ambiguità aggiuntive salvo coltello MoGE. Gate provvisori del candidato, non imposti dai paper o calibrati. Asimmetria 99%/42.3% del tagliere MoGE compatibile anche con parzialità; simmetrie possono rendere troppo severo il gate di ambiguità. Nessuna soglia modificata; diagnosi necessaria, non prova di associazioni errate. [Audit e valori](../RIPRESA_HPC_20261114.md).

## Diagnosi dei rifiuti verificata — 14 novembre

Letti motivi e soglie reali del 763323: tagliere 5099 (DA/MoGE) supera supporto/residui ma viene rifiutato solo per posa ambigua; al 7508 i quattro allineamenti falliscono supporto/residui, tre anche ambiguità. Gate provvisori del nostro prototipo, non regole dei due modelli; nessuna soglia cambiata o incompatibilità fisica dimostrata. [Numeri e criteri](../RIPRESA_HPC_20261114.md).

## Conteggi delle inizializzazioni chiariti — 14 novembre

Verificati i log del job 763323: 12 inizializzazioni = tagliere/track 4 (2893), coltello/track 6 (5099), padella/track 9 (7508), ciascuna in quattro rappresentazioni. Tre successive osservazioni candidate alla fusione (due del tagliere, una del coltello) ripetute nelle quattro configurazioni, tutte rifiutate; padella con una sola vista, nessun suo tentativo di fusione. Track predette/categorie non nuove identità GT. Audit e dettaglio in [RIPRESA_HPC_20261114.md](../RIPRESA_HPC_20261114.md).

## Runner comune e misure implementati — 14 novembre

Disponibili W0/G0/S-separata/S-accumulo/P-accumulo, DA/MoGE, memorie e modelli indipendenti, controllo sui punti ammessi e report JSONL/JSON/CSV con copertura, fallimenti, byte di payload e costi dei replay. 58 test locali superati; esempio a peso zero, tracking metrics ancora non calcolate. Nessuna nuova run reale del runner comune né modifica dei job esistenti. [RUNNER_VARIANTI_20261114.md](../RUNNER_VARIANTI_20261114.md). Prossimo: collegare valutatore tracking e protocollo/copertura di calibrazione-test.

**HPC verificato durante il lavoro:** 763322 COMPLETED/0:0 (9m56s), 763323 COMPLETED/0:0 (12m11s), zero esatto; nel secondo solo 12 inizializzazioni e 12 rifiuti, nessuna fusione, conteggi sulle quattro rappresentazioni. 763324 RUNNING a 29m19s con almeno un risultato neurale reale ready; esito complessivo ancora da acquisire. [Dettagli HPC](../RIPRESA_HPC_20261114.md). Le indicazioni precedenti di job CPU attivi/GPU in attesa sono storiche.

## Selezione e calibrazione autonome approvate — 14 novembre

Marco approva ottimizzazione di parametri/metodo e confronto delle alternative, perseguendo qualità in ogni fase e beneficio finale nel tracking. Piano corrente e criteri nel [piano d'azione](../../evidence/ASSET_ESTERNI.md#asset-fbd7fcfeb777): esiti esistenti → geometria/calibrazione → finaliste nel ciclo → test separato. Confermati inferenza SuperFlex dopo ogni aggiornamento ammesso e nessun filone autonomo sulla contaminazione generale. Prossimo: acquisire i risultati già avviati e predisporre runner/metriche comuni e confronto geometrico; nessuna nuova calibrazione, implementazione o esecuzione in questo aggiornamento. Stati HPC sotto conservati come ultime osservazioni, non ricontrollati qui.

## HPC ripristinato, arretrati inviati — 14 novembre

SSH/accounting/coda accessibili. Recuperati 761899 (prefisso storico a peso zero esatto, 3398 frame/10264 detection, zero differenze dal collega) e 761905 (IDF1 73.2697% sulle predizioni registrate train, non test). Nuovi job: 763321 COMPLETED/0:0, 50 test ambiente passati; 763322 replica aggiornata e 763323 accumulo RUNNING nell’ultima osservazione; 763324 SuperFlex differita PENDING per dipendenza dai due CPU. Nessun nuovo esito sperimentale ancora dichiarato; prossima acquisizione dei risultati. [RIPRESA_HPC_20261114.md](../RIPRESA_HPC_20261114.md). Le note precedenti sul blocco DNS e sui due esiti ancora da leggere sono storiche.

## Parere sulla proposta del collega — 14 novembre

Approfondite su richiesta di Marco le opzioni con pro/contro: pulizia conservativa, alternative di posa/RGB/scala, ammissione compatibile con viste parziali, budget/frequenza SuperFlex e valutazione visibile con controlli tracking. Precisato che simmetrie reali possono rendere pose diverse geometricamente equivalenti; nessuna modifica automatica ai gate. Analisi nel parere collegato sotto; nessuna nuova scelta o esecuzione.

Valutata la sequenza pulizia → FPFH/RANSAC/ICP → accumulo → SuperFlex → valutazione: baseline candidata plausibile, con controlli su posa/scala, rifiuti e identità; Chamfer simmetrica contro una vista parziale insufficiente come unica misura. Il candidato attuale è PCA/multistart + ICP: 0/12 non è un test di FPFH. Raccomandato piccolo confronto diagnostico alla ripresa, non adottata una sostituzione né modificato il protocollo. [Parere e fonti](../PARERE_PROPOSTA_COLLEGA_20261114.md). Nessun nuovo esperimento o risultato; priorità software e stato HPC invariati.

## SuperFlex differita collegata — 14 novembre

Implementate richieste da nuvola/versione ammessa, worker sulla pipeline esistente, verifica/importazione e pubblicazione della forma nei soli frame successivi. Replay seriale bloccato fino agli esiti, ultima forma conservata su fallimento; completamenti esclusi dai punti osservati. 43 controlli locali passati con sostituti dichiarati, nessuna nuova inferenza reale/HPC. Runner predisposto con --accumulate --reconstruct; prossimo confronto comune delle varianti e aggregazione delle misure. [SUPERFLEX_DIFFERITA_20261114.md](../SUPERFLEX_DIFFERITA_20261114.md). Le note precedenti sul collegamento SuperFlex ancora mancante sono storiche; validazione reale 2B e risultati HPC pendenti invariati.

## Registrazione/accumulo collegati — 14 novembre

Collegato il candidato esistente al coordinatore: inizializzazione, registrazione rigida e accumulo ammesso, con isolamento delle sorgenti, versioni/provenienza e conservazione dello stato su rifiuto/errore. 35 test locali passati; input sintetici e componenti controllati, nessun replay reale o HPC. Runner predisposto con --accumulate (default disattivato), preparatore con punti camera/hash; non eseguiti in questa fase. Prossimo: SuperFlex differita dalla nuvola accettata. Il matcher usa ancora forme separate; risultato reale 2B invariato (0/12). [COLLEGAMENTO_ACCUMULO_20261114.md](../COLLEGAMENTO_ACCUMULO_20261114.md). Le indicazioni precedenti sul collegamento ancora mancante sono storiche.

## Coordinatore del frame completato — 14 novembre

Implementato e collegato al runner: confronto/associazioni prima, commit delle forme e proposte geometriche dopo; versioni distinte, stato valido preservato per mancanti/rifiuti/errori. 27 controlli locali passati (11 nuovi), con metodi originali e componenti controllati; nessuna verifica Torch o run HPC. Il runner aggiorna ancora solo forme separate: prossimo collegamento del candidato registrazione/accumulo, poi SuperFlex differita. Esiti HPC e validazione 2B invariati. Resoconto: [COORDINATORE_FRAME_20261114.md](../COORDINATORE_FRAME_20261114.md). Le indicazioni sottostanti sul coordinatore ancora da implementare sono storiche.

## Mappa del risultato atteso — 14 novembre

Marco richiede revisione della nuova mappa e annotazioni per ciascun riquadro/collegamento (stato e alternative, motivi, miglioramenti). Preparata una **proposta**, non ancora approvata: mappa essenziale con schede collegate, contratti dei collegamenti ed evidenza distinta dall'implementazione. Correzioni ed esempi in [PROPOSTA_ANNOTAZIONI_MAPPA_20261114.md](../PROPOSTA_ANNOTAZIONI_MAPPA_20261114.md). Nessuna modifica alla lavagna esterna, alla selezione scientifica o ai job; compilazione sistematica delle schede ancora da fare.

Precisata con lettura del codice originale locale la provenienza degli XYZ EPIC: profondità da RGB allineata alla scena, centro bounding box/maschera, intrinseci e posa camera. La maschera alimenta anche il ramo posizione; le feature d'aspetto non lo generano. Dettagli e limiti in [MAPPA_FLUSSO_SISTEMA.md](../MAPPA_FLUSSO_SISTEMA.md). Nessuna rigenerazione o modifica della baseline; priorità operative in apertura invariate.

Marco esplicita il flusso RGB → maschera/nuvola → SuperFlex → associazione → aggiornamento delle memorie. Preparata [MAPPA_FLUSSO_SISTEMA.md](../MAPPA_FLUSSO_SISTEMA.md), coerente con il ciclo approvato: aspetto dalla regione mascherata, posizione baseline, contributo geometrico tramite adattatore e nuova forma disponibile ai frame successivi. Distinti inizializzazione, aggiornamenti rifiutati e stato effettivo; nessuna nuova implementazione o validazione. Prossimo lavoro software invariato: punto 2 del piano senza HPC.

**Consegna collaborativa ancora aperta:** Marco chiede prima Miro, poi una slide e uno spazio di lavoro in stile Miro in ChatGPT Space. Miro richiede login, non effettuato; richiesta successiva indirizzata a Space. Creata e collegata presentazione privata vuota «Ciclo Whareformer–SuperFlex», Page ID `page_f951f11ecfbc81a48983567d55429f5d`. Inserimento della mappa bloccato: servizio di modifica slide non eseguibile nell'ambiente corrente («requires MXC»), nessun editor esposto nel browser. Nessun contenuto inserito, nessuna condivisione o lavagna creata; riusare la presentazione esistente alla ripresa, senza duplicarla. La mappa locale resta disponibile.

## Punto 1 software completato — 14 novembre

Implementato componente riutilizzabile con tre modalità, quattro rappresentazioni e delega al matcher originale; runner e preparatore aggiornati. Passati 16 controlli locali (7 adapter + 9 wrapper), con modello/tensor controllati; verifica Torch/frame reali rinviata. Nessun accesso HPC o nuovo esperimento. Prossimo lavoro: punto 2, coordinatore causale e stato geometrico versionato. Resoconto: [INTEGRAZIONE_RIUTILIZZABILE_20261114.md](../INTEGRAZIONE_RIUTILIZZABILE_20261114.md).

## Priorità corrente — sviluppo senza HPC, 14 novembre

Marco dispone di sviluppare il progetto e rimandare gli esperimenti. Sospesi i tentativi di connessione come attività prioritaria; il recupero di 761899/761905 resta pendente alla ripresa. Ordine operativo: integrazione riutilizzabile → coordinatore causale → interfaccia SuperFlex differita → runner/controlli locali → pacchetto sperimentale. Piano e criteri in [PIANO_SVILUPPO_SENZA_HPC_20261114.md](../PIANO_SVILUPPO_SENZA_HPC_20261114.md). Nessun nuovo esperimento o risultato; 2B resta non validato, parametri/protocollo finale non fissati da questa revisione.

Aggiornamento: 14 novembre 2026. Prevale sulle indicazioni operative storiche.

## Integrazione reale in corso — 13 novembre

Arrivato anche fc5aa30: configurazione/comandi/patch Windows e CSV acquisiti; checkpoint locale corrispondente verificato. Input ufficiali P01_01 recuperati autonomamente e controllati su tutte le 110590 osservazioni, zero differenze di metadati/XYZ. Job CPU 761872 COMPLETED/0:0 (28 s), 120 casi a peso zero sul modello reale superati. Tentativi prefisso 761893 FAILED/1:0 (25 s, LMDB) e 761895 FAILED/1:0 (29 s, deserializzazione CUDA su CPU), corretti nel runner isolato e conservati. **761899 RUNNING nell'ultima osservazione riuscita (9m50s, almeno 3000/3398 frame), stato attuale ed esito non acquisiti**. Metriche registrate: 761902 FAILED/1:0 (12 s, xmltodict), corretto nel pacchetto; **761905 COMPLETED/0:0 (20 s), valore IDF1 ancora da leggere**. CSV del collega verificato: mPCL 70.4655% sul singolo video train, non test separato. Percorsi, hash e limiti in [INTEGRAZIONE_BASELINE_REALE_20261113.md](../INTEGRAZIONE_BASELINE_REALE_20261113.md). Coda generale non ancora ricontrollata.

**Blocco di accesso del 14 novembre:** hostname HPC non risolto (NXDOMAIN anche al DNS Wi-Fi e tramite resolver HTTPS esterno). Marco conferma solo Wi-Fi universitario, senza VPN Bocconi. Nessuna responsabilità di Norton dimostrata; rete invariata, job non rilanciati. Prossimo passo: provare VPN Bocconi e recuperare accounting/output di 761899/761905; nessuna equivalenza su tutto il prefisso o IDF1 numerico dichiarati prima di leggerli. Le precedenti note di assenza di configurazione/checkpoint/feature sono superate; restano due alias JPEG e la validazione 2B.

## Nuova consegna Whareformer verificata — 13 novembre

Remoto main osservato a bbf0e5e; ricevuti e preservati i due manifest completi. Audit reale passato: 71/73 exact, 52 track/110590 righe; 146 nuvole verificate. I due mancanti sono alias VISOR/RGB di un indice, verificati nei record/mapping originali ma non riclassificati exact prima di controllare il JPEG delle feature. In 69/71 casi annotation_index non coincide con detection_idx; lookup esplicito necessario. Revisionate tavole delle track 4/36/9/35, segnali di contaminazione e possibile frammentazione. Report [VERIFICA_CONSEGNA_WHAREFORMER_20261113.md](../VERIFICA_CONSEGNA_WHAREFORMER_20261113.md), output `outputs/github_handoff_bbf0e5e/`, segmento registrato di tre frame/dieci detection preparato. Nessuna inferenza né job; sola lettura HPC mirata, coda non ricontrollata. Step 1 chiuso per acquisizione/audit dei manifest, aperto per provenienza temporale e feature, configurazione/versione/checkpoint della run e metriche. Prevale sulle precedenti note di assenza dei due JSON. Lo sviluppo autonomo rimane disponibile.

## Esito corrente step 2B — 13 novembre

Implementati registrazione rigida candidata e memoria limitata di punti osservati; sette nuovi test finali superati. Nei piloti DA/MoGE, 12/12 aggiornamenti reali rifiutati su nove osservazioni di tre identità visive; inizializzazioni conservate, nessuna fusione reale accettata. Prima versione del controllo corretta e preservata; nessuna soglia rilassata per le viste reali. Report [RISULTATI_REGISTRAZIONE_ACCUMULO_20261113.md](../RISULTATI_REGISTRAZIONE_ACCUMULO_20261113.md); output `outputs/registration_pilot_v1/` (storico), `registration_pilot_v2/` e `registration_close_views_v1/`. Controlli artificiali positivi non certificano la posa reale. Nessuna nuova inferenza SuperFlex, mancando un accumulo reale ammesso; nessun job o coda HPC ricontrollata. Prossima incertezza: posa ambigua e geometria/scala variabile, da diagnosticare separatamente. 2A con forme separate resta disponibile; 2B candidato implementato ma non validato. Prevale sulle note precedenti che indicano ancora accumulatore non implementato.

## Avanzamento autonomo precedente — 13 novembre

Marco richiede di avanzare sugli step indipendenti ed eventualmente replicare una baseline minima. Step 2A avviato con `integration_prototype/`: adattatore candidato, sette test superati (120 confronti a peso zero col greedy originale) e replay tecnico di tre frame/cinque osservazioni P03_04 su punti/SuperFlex DA/MoGE, 20 artefatti verificati. Evidenza `outputs/independent_adapter_pilot_v1/`. Nessuna inferenza Whareformer: logits di prova e associazioni annotate esterne; nessun beneficio tracking o accumulo validato. Resoconto e piano: [AVANZAMENTO_AUTONOMO_20261113.md](../AVANZAMENTO_AUTONOMO_20261113.md). Prossimo lavoro autonomo: registrazione/accumulo controllati su punti disponibili, poi nuova inferenza SuperFlex solo quando esiste un accumulo accettato. Lo step 1 resta dipendente dai manifest della run del collega, ma non blocca questi sviluppi. Nessun nuovo job o controllo HPC in questa fase.

## Step 1 avviato — roadmap approvata

Marco approva la roadmap e avvia lo step 1. Remoto ancora ab5a946; manifest completi e asset baseline non trovati nel workspace o nella ricerca delimitata dello spazio personale HPC. Stato e richiesta minima in [STEP1_CONTRATTO_TRACKING.md](../STEP1_CONTRATTO_TRACKING.md); evidenza `outputs/step1_tracking_contract/status.json`. Preparato controllo JSON, sei casi sintetici superati; non eseguito sui dati reali mancanti. Prossimo passo dipendente dalla disponibilità di manifest/configurazione/input del collega, senza invio automatico di messaggi. Nessuna nuova inferenza o job; nessuna verifica attuale della coda. Step 1 non concluso.

## Direzione corrente — chiarimento successivo del 13 novembre

Marco conferma il ciclo unitario: forma→associazione→aggiornamento della ricostruzione→confronti futuri. Superata la precedente lettura dell’accumulo come sola estensione esterna. Roadmap dopo rilettura dei paper in [ROADMAP_CICLO_GEOMETRICO.md](../../evidence/ASSET_ESTERNI.md#asset-fbd7fcfeb777); registro voce 31. Prossimo passo: contratto baseline/join reale, poi confronto/matcher e registrazione/accumulo, prima verificati separatamente e quindi collegati. Roadmap successivamente approvata da Marco; dettagli numerici e protocollo da calibrare/verificare secondo il piano. FIFO disponibile, accumulatore e ciclo completo non implementati. Nessun nuovo job o controllo HPC in questa fase.

## Stato corrente

**Consegna autonoma completata**, entro il mandato dell'11 novembre: pipeline portabile DA/MoGE → punti → SuperFlex, export, confronto e memoria causale configurabile. Rapporto unico: [CONSEGNA_RAMO_GEOMETRICO.md](../CONSEGNA_RAMO_GEOMETRICO.md), con risultati, costi, verifiche e limiti. Guida `shared_exports/publish_candidate/SuperFlex/PIPELINE.md`; codice sul ramo `prepare/superflex-core`. Nessun beneficio tracking o metodo definitivo dichiarato.

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

Letti integralmente i sei file dei commit del 12 novembre `31e3943` e `ab5a946`; remoto `main` osservato a `ab5a946c1f94018edad90e69bc5544306f913569`. Eseguito soltanto fetch: worktree candidato ancora alla nostra revisione `71ce4f1`, nessun merge/push. Analisi autorevole: [ANALISI_AGGIORNAMENTO_GITHUB_20261113.md](../ANALISI_AGGIORNAMENTO_GITHUB_20261113.md).

Implementati dal collega recupero ID delle osservazioni dalle predizioni e join alle nuvole compare200 per P01_01. Report: 110590 righe ricondotte esattamente alle annotazioni, 52 track; 71/73 geometrie collegate a 18 track, 9 con più osservazioni. Controllati accordo JSON/CSV e manifest originale; quattro controlli sintetici sui due script superati. Evidenza `outputs/github_review_20261113/verification.json`. Conteggi reali non riprodotti: non caricati output completi, manifest dei join, configurazione/checkpoint e metriche baseline. Track 9, 18 osservazioni di padella: coerenza visiva riferita dal collega, non ricontrollata qui. Track 4/36 con categorie miste: revisione prioritaria, non identità fisiche certificate.

**Conseguenza:** il ponte dati è avviato concretamente, il matcher geometrico resta assente dai nuovi upload. Acquisire/verificare manifest e baseline reali, diagnosticare i due mancati join e le track, quindi collegare la memoria causale e verificare peso zero. Accumulo multivista proposto nel README del collega: estensione distinta, non nuovo obiettivo adottato. Nessun job HPC avviato o coda ricontrollata in questa analisi; l'ultima osservazione HPC resta quella della consegna precedente.
