# Stato corrente — 15 novembre 2026

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

Marco richiede analisi del contesto e assistenza alla revisione, riservando a sé la modifica dei testi della mappa. Ricognizione delle 19 schede di nodo e 34 collegamenti completata: 12 nodi e 26 frecce sono segnaposto; individuate anche affermazioni inesatte o superate nelle schede compilate. [Checklist con evidenze e ordine proposto](REVISIONE_MAPPA_20261115.md). Testi e struttura della mappa invariati; nessuna nuova inferenza o verifica HPC. Prossimo passo: scrittura manuale di Marco e verifica progressiva in chat, partendo dagli input e dal confine tra dati riusati e rigenerazione. Le precedenti richieste di compilazione automatica della mappa sono superate per questa revisione; risultati della campagna e rinvio dei filtri restano invariati.

## Campagna estesa conclusa — 15 novembre 2026

[Resoconto e output](../evidence/campaign_20261115_v1/REPORT_FINALE.md). Tutte le 29 configurazioni completate e valutate su 33310 frame/110590 osservazioni; nessuna assegnazione diversa da W0 e metriche identiche (IDF1 73.269735%, mPCL 70.465504%). Quattro controlli zero esatti, nessun timeout/errore di aggiornamento/worker fallito o richiesta pendente.

764678 COMPLETED 0:0 (4h13m00s), 764679 COMPLETED 0:0 (3h54m41s), riepilogo 765084 COMPLETED 0:0 (42s). Preflight/geometria/bundle già conclusi; nessun job della campagna attivo o in attesa. Nuvole/forme per tutte le 446 osservazioni pronte in entrambe le sorgenti. Per ogni variante con accumulo: DA 23 inizializzazioni/31 fusioni/392 rifiuti; MoGE 23/40/383. SuperFlex della memoria 54/63 pronte per variante, ripetizioni non indipendenti.

Report e accounting finali acquisiti localmente in outputs/campaign_20261115_v1/final_reports/; grandi tracce, nuvole e mesh di tutte le varianti ancora sull'HPC in ~/cv_project/campaign_20261115_v1/. Prossimo passo: analizzare margini, distanze, copertura di casi difficili e qualità delle fusioni. Nessun metodo selezionato né modifica dei filtri; revisione ancora rinviata. Non rilanciare i job conclusi.

## Avvio della campagna — stato storico superato

Marco autorizza preparazione e avvio dopo i controlli. [Specifica, limiti e ripresa](CAMPAGNA_HPC_20261115.md): 247 frame/446 osservazioni congelati prima dell'inferenza, geometria DA/MoGE rigenerata e 29 configurazioni sull'intera storia P01_01. Feature/PCA/XYZ ufficiali riusati; nessun nuovo training o filtro modificato. Campagna di sviluppo, non test held-out o beneficio assunto.

Preflight 764670 COMPLETED 0:0 (1m35s), 76 test tutti passati. 764674 COMPLETED 0:0 (11m38s), 764675 COMPLETED 0:0 (1m41s): tutte le 446 osservazioni hanno nuvole e forme pronte per DA/MoGE, feature baseline byte-identiche. 764678 e 764679 RUNNING per 19 trial CPU e dieci GPU. Riepilogo da inviare automaticamente al termine del primo gruppo, con dipendenza su entrambi. Risultati finali ancora pendenti. Ricevuta/stati remoti in ~/cv_project/campaign_20261115_v1/submitted_jobs.json e logs/; snapshot locale outputs/campaign_20261115_v1/.

Limite QoS rilevato: quattro job inviati/due attivi. Primo array respinto, nessun trial partito da quell'array; adattato il solo raggruppamento, senza duplicare i job esistenti. Concorrenza attuale un gruppo CPU/un gruppo GPU, massimo 9.5 ore GPU complessive. Non reinviare i job; acquisire prima stato e output. Revisione dei filtri ancora esplicitamente rinviata.

## Prima run completa conclusa — 14 novembre 2026

Job 764454 COMPLETED 0:0 (8m40s), audit/valutazione 764474 COMPLETED 0:0 (53s); nessun job di questa run attivo/in attesa. Tutti i 33310 frame e 110590 osservazioni del protocollo ufficiale P01_01 elaborati (937–98099; metadati video 99135). Non tutti i RGB: feature/PCA/XYZ e 71 geometrie su 38 frame riusati con hash, nuova inferenza Whareformer e 25 nuove SuperFlex sugli stati ammessi. Copertura geometrica 0.0642% delle osservazioni.

S-accumulo DA, peso 0.1 non calibrato, filtri invariati: 18 inizializzazioni, 7 fusioni ammesse, 46 rifiuti, nessun errore o richiesta pendente. 695 logits modificati; 76 confronti futuri usano forme da fusioni. Memoria finale: 18 track, 38732 punti osservati, provenienza verificata; accuratezza fisica delle fusioni non certificata. Assegnazioni identiche alla baseline: 52 track, IDF1 73.269735%, mPCL 70.465504%, nessun miglioramento.

[Resoconto verificato ed evidenze](../evidence/full_video_20261114/REPORT.md).

Percorso HPC `~/cv_project/full_video_20261114_v1/`; log `cv_full_active_764454.out/.err`, `cv_full_audit_764474.out/.err`, `tests_764454.log`; output `run_764454/`, `cache_764454/`, `final_evaluation/`, `final_comparison/`, `audit/`. Tutti gli output scaricati in `outputs/full_video_20261114/results/` nella cartella locale. La valutazione iniziale a 98099 è superata da quella finale con orizzonte originale 99135; nessuna nuova inferenza per correggerla.

Prossimo passo: discutere qualità/validazione indipendente delle fusioni e copertura prima di conclusioni di efficacia; frontend RGB rigenerato e calibrazione/test rimangono aperti. Revisione dei filtri ancora rinviata: non avviarla automaticamente. Prima esecuzione operativa chiusa; non rilanciare job conclusi. Pubblicazione verificata su main: 8694e4b (codice ed evidenze della run).

## Vincoli e ripresa

Le precedenti prove zero e i risultati dei piloti sono conservati nelle [evidenze](../evidence/README.md) e nell'[archivio](../archive/). Le note storiche di zero fusioni si riferiscono ai piloti precedenti, non alla nuova run completa.

Preservare query prima degli aggiornamenti, punti osservati distinti da completazioni e riferimenti camera/scena/normalizzazione. Reti congelate. Non presentare l'ammissione dei gate come verifica fisica indipendente; mantenere distinta efficacia tracking e funzionamento software. [Registro critico](REGISTRO_CRITICITA_PIPELINE.md).

Codice corrente nel worktree locale shared_exports/handoff_ai_20261114, branch run/hpc-campaign-20261115; documentazione corrente distinta dalla storia e README unico ingresso. Dati completi e checkpoint sono esterni al clone.
