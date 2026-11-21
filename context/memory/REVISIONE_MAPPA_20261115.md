# Revisione guidata della mappa — 15 novembre 2026

## Mappa corrente — 21 novembre 2026

Struttura Rami paralleli e nuovi commenti confermati da Marco e applicati: 39 riquadri, 49 collegamenti. La sorgente corrente è [la mappa interattiva](../../mappa_interattiva/README.md). Superata la riserva storica della scrittura al solo Marco: l’assistente può applicare i testi dopo conferma esplicita. Vecchi commenti conservati, revisione scientifica successiva ancora aperta. Nessun cambiamento del metodo o nuovo esperimento.

## Revisione del mandato — 21 novembre 2026

**Applicazione successiva completata:** Marco conferma i testi e chiede di aprire l'HTML. Struttura Rami paralleli e commenti applicati alla mappa corrente, con 39 riquadri/49 collegamenti e riferimenti R/C effettivi. Verificate corrispondenza dei testi, copia offline, schede ed editor; HTML aperto nella chat. [Ricevuta dell'applicazione](../evidence/map_20261121/APPLICAZIONE_MAPPA.json). Le successive note di attesa e di mancata applicazione riportate sotto descrivono fasi storiche superate; resta distinta la revisione scientifica dei vecchi testi.

**Testi della struttura confermata:** preparate proposte per 28 riquadri e 39 frecce nuovi/ridistribuiti, [versione da revisionare](../evidence/map_20261121/COMMENTI_PER_REVISIONE_CHAT.md). I restanti elementi conservano schede manuali o bozze già presentate; nove campi per ogni elemento nella specifica separata. Riferimenti R/C limitati alla proposta, nessuna modifica alla mappa. I testi vanno confermati prima dell'inserimento; i vecchi commenti non sono oggetto di una nuova revisione in questa fase.

**Conferma successiva dell'insieme:** Marco approva l'anteprima completa («Va bene questa mappa»). La struttura 39 nodi/49 connessioni è confermata; resta da proporre e revisionare la distribuzione dei commenti nelle nuove schede. Nessuna applicazione alla mappa eseguita in questa fase di chiarimento.

**Scelta visiva successiva:** Marco sceglie «Rami paralleli», chiedendo prima dell'applicazione di vedere l'intero processo. [Anteprima completa separata](../evidence/map_20261121/mappa-completa-rami-paralleli.png) e [specifica delle suddivisioni](../evidence/map_20261121/ANTEPRIMA_COMPLETA.md) preparate; stile scelto, struttura complessiva e testi ancora da confermare. Nessuna modifica ai commenti o all'applicazione della mappa.

**Chiarimenti approvati successivamente:** tutti i campi mancanti, «-» se non sostanziale; esistenti rinviati. Una sola mappa interattiva dell'implementazione attuale; libertà di aggiungere/rimuovere nodi e frecce, con processi/decisioni e provenienza distinguibili. Diverse proposte grafiche prima della scelta di Marco, poi applicazione globale. [Bozze dei commenti](../evidence/map_20261121/TESTI_PROPOSTI.md) e tre anteprime sul ciclo critico preparate separatamente, nessuna modifica della mappa. Layout e testi restano da approvare; eventuali nuove schede dipendono dalla struttura scelta. Questi chiarimenti risolvono le domande indicate nel paragrafo storico seguente.

Le indicazioni seguenti conservano valore storico e tecnico, ma il nuovo mandato consente all'assistente di preparare i testi mancanti in chat e applicarli soltanto dopo conferma esplicita di Marco. Richiesta anche revisione visiva con flusso dall'alto al basso, minori intrecci, processi e decisioni distinguibili e attribuzione Whareformer/SuperFlex/progetto. Superati la modifica esclusivamente manuale e il rinvio grafico; campi da completare, versione rappresentata, libertà strutturale e modalità di revisione grafica ancora da chiarire. Nessuna modifica alla mappa eseguita in questa ricognizione. Restano validi i criteri di chiarezza, sintesi e distinzione fra funzione dei nodi e dipendenza spiegata dalle frecce.

## Mandato e perimetro

Marco richiede di ricostruire il contesto e assisterlo nella revisione dei commenti di nodi e collegamenti. **I testi della mappa vengono modificati da Marco.** L'assistente analizza, spiega, segnala correzioni e verifica le formulazioni discusse; non compila né salva le schede. Questa indicazione supera, per la revisione corrente, le precedenti richieste di completamento automatico e i segnaposto tra parentesi quadre.

Questo documento è una checklist di revisione, non una raccolta di testi sostitutivi. Nessun cambiamento di metodo, esperimento, filtro o conclusione scientifica è approvato dalla revisione editoriale.

Chiarimento successivo di Marco: in tutte le descrizioni di nodi e collegamenti, le parentesi quadre `[]` indicano testo da inserire e/o sistemare. L'assistente deve affrontare queste richieste nelle proposte in chat; la scrittura e il salvataggio nella mappa restano riservati a Marco. Priorità editoriali confermate: comprensibilità, brevità, accuratezza nel descrivere il lavoro svolto.

## Base effettivamente consultata

Letti istruzioni, stato, attività e decisioni; contenuti correnti delle 19 schede di nodo e dei 34 collegamenti in `mappa_interattiva/contenuti.json`; guida della mappa; roadmap del ciclo e proposta storica di annotazione; registro critico; risultati della campagna e valutazione della prima run; avanzamento del frontend e documentazione del codice. Controllati il codice dell'adattatore, descrittore/memoria/preprocessing nel pacchetto della campagna e le funzioni originali locali del ramo posizione.

Il riepilogo JSON locale conferma 29 configurazioni, tutte con zero differenze di assegnazione da W0 e gli stessi IDF1/mPCL. Non eseguiti nuovi job, inferenze o controlli remoti. Non svolta una nuova rassegna bibliografica: le alternative da ricercare restano richieste storiche da discutere, non risultati di questa revisione.

Fonti principali:

- [Decisioni e motivazioni](REGISTRO_DECISIONI.md), in particolare voci 1–20, 31–32, 47–49, 56 e 69–75.
- [Risultati finali della campagna](../evidence/campaign_20261115_v1/REPORT_FINALE.md) e [riepilogo acquisito](../evidence/campaign_20261115_v1/campaign_summary.json).
- [Prima run completa](../evidence/full_video_20261114/REPORT.md), [valutazione critica](../archive/VALUTAZIONE_PRIMA_RUN_20261114.md) e [registro delle criticità](REGISTRO_CRITICITA_PIPELINE.md).
- [Frontend e limiti della rigenerazione](FRONTEND_AVANZAMENTO_20261114.md), [piano del ciclo](ROADMAP_CICLO_GEOMETRICO.md), [confronto 200 immagini](../archive/RISULTATI_CONFRONTO_200.md) e [confronto d'identità](../archive/RISULTATI_IDENTITA_DA_MOGE.md).
- [Adattatore dei punteggi](../../integration_prototype/shape_adapter.py); [descrittori](../../SuperFlex/src/shape_tools/metrics.py), [memoria](../../SuperFlex/src/shape_tools/memory.py), [campionamento e normalizzazione](../../SuperFlex/src/shape_tools/geometry.py), [preparazione dei confronti](../../SuperFlex/src/shape_tools/comparison.py).

## Contesto da tenere comune alle schede

1. La domanda resta se la forma SuperFlex aggiunga informazione utile all'associazione di identità di Whareformer, già basato su aspetto e posizione. Integrazione, accuratezza geometrica ed efficacia del tracking sono risultati diversi.
2. Il ciclo unitario è approvato: osservazione → associazione → aggiornamento dei punti osservati ammessi → nuova SuperFlex → confronto nei frame successivi. L'accumulo non è più soltanto un'estensione esterna opzionale del progetto; le ablation possono disattivarlo per confronto.
3. La prima esecuzione completa da input preparati è conclusa. Anche l'ultima campagna ha elaborato l'intero protocollo P01_01, 33310 frame/110590 osservazioni, ma ha rigenerato geometria soltanto su 247 frame/446 osservazioni (0.4033%). Non confondere questi denominatori con tutti i frame RGB del video.
4. Ultima campagna: 29/29 configurazioni concluse, assegnazioni tutte uguali a W0, IDF1 73.269735% e mPCL 70.465504%. Nessun vincitore di tracking. La griglia include confronti attivi tra forme separate, punti accumulati e SuperFlex accumulato; la precedente indicazione che tali confronti mancavano è superata per questa matrice.
5. Per variante con accumulo: DA 23 inizializzazioni/31 fusioni/392 rifiuti; MoGE 23/40/383. Le ripetizioni tra varianti non sono prove indipendenti. Fusioni ammesse non equivalgono a pose fisicamente corrette certificate. La precedente assenza di fusioni riguarda i piloti storici.
6. Feature d'aspetto/PCA/XYZ ufficiali sono riusati e preservati. Il frontend completo rigenerato dalle immagini resta incompleto. Maschere VISOR, camera/pose e ricostruzione scena sono ingressi dichiarati; non è dimostrato un sistema autonomo per un video RGB arbitrario.
7. Mantenere entrambi DA/MoGE è una scelta approvata: il confronto di sagome favoriva modestamente DA grezzo, un piccolo controllo d'identità favoriva MoGE+SuperFlex con D2. Le misure rispondono a domande diverse e non provano superiorità 3D o di tracking.
8. Revisione di filtri e registratore ancora rinviata. Diagnosi di margini, distanze, copertura dei casi difficili e qualità delle fusioni è il prossimo lavoro indicato dai risultati, non un esito già acquisito. Calibrazione e test separato restano da completare; P01_01 è sviluppo/train.

## Come scrivere senza confondere i campi

Precisazione editoriale esplicita di Marco: le schede dei **riquadri** descrivono il processo svolto nello step; le schede dei **collegamenti** spiegano perché l'output della sorgente è utile o necessario come input della destinazione. Nelle frecce citare solo il meccanismo minimo necessario a comprendere questa dipendenza, lasciando il dettaglio del calcolo al nodo. Questa indicazione prevale sulle proposte precedenti che duplicano nelle frecce il processo della destinazione, incluso l'esempio E15.

Per ogni scheda chiarire prima funzione e dato concreto; poi stato attuale e prova disponibile; infine motivo documentato, limite e prossimo controllo. Il motivo storico non va ricostruito da una giustificazione plausibile emersa soltanto ora. Distinguere sempre alternative discusse, approvate, implementate ed eseguite.

Il campo evidenze deve contenere ciò che è stato osservato e il suo limite, non un obiettivo futuro. «Replica del paper» non sostituisce la descrizione di input/output, convenzioni e verifica. Per collegamenti semplici non occorre inventare alternative o miglioramenti: motivare la non applicabilità quando pertinente. I prossimi passi devono indicare quale incertezza risolvono, senza promettere un beneficio.

## Nodi: diagnosi e contenuto da chiarire personalmente

| Nodo | Problema attuale e guida alla revisione |
|---|---|
| B01 · RGB | Il campo evidenze contiene un auspicio futuro. In alternative DA/MoGE vengono descritti come input più complessi: sono invece modelli che ricevono RGB. Separare pixel in ingresso, metadati aggiuntivi oggi necessari e obiettivo futuro di usare video generici; quest'ultimo non è uno step già concluso o automaticamente approvato. |
| B02 · Maschere | Il contenuto è in gran parte utilizzabile. Precisare che VISOR fornisce annotazioni associate a EPIC e non maschere generate dal nostro sistema. Segmentazione automatica e sua inizializzazione restano eventuali estensioni; SAM 2 è un esempio discusso, non un componente adottato. Conservare effetti degli errori su tutti i rami. |
| B03 · Aspetto | «Replica di Whareformer» ripetuto nei campi non spiega il blocco né prova una replica dell'estrazione. Indicare ritaglio RGB mascherato → descrittore visivo della baseline; feature/PCA ufficiali riusati nelle run. La rigenerazione DINOv2/PCA e relativa provenienza restano aperte. Il motivo del riuso è isolare il contributo della forma mantenendo comune il segnale d'aspetto. |
| B04 · Geometria DA/MoGE | Separare DA che stima profondità e retroproiezione con intrinseci da MoGE che produce punti e validità. Distinguere DA grezzo del ramo forma da profondità allineata alla scena del ramo posizione. «Testing» va chiarito come diagnostica/sviluppo, non held-out. Motivare i due candidati con la storia verificata e gli esiti non univoci, non soltanto con la presenza nei paper. Le superfici nascoste non diventano osservate in questo blocco. |
| B05 · Nuvola oggetto | I segnaposto «Replica del paper [...]» non sono sufficienti, e la costruzione della nuvola è pertinente al progetto. Esplicitare selezione dei punti validi con maschera, riferimento camera, sorgente e scala dichiarati. Una nuvola osservata resta parziale e non è automaticamente allineata alle viste precedenti. Non identificare «osservato» con profondità fisicamente misurata: anche questi punti derivano da stime. |
| B06 · SuperFlex | «Risultati in linea con il paper originale» non è dimostrato da questi esperimenti e non va usato come attestazione di qualità. Distinguere funzionamento del checkpoint robust, fedeltà alle superfici visibili, completion predetta ed efficacia d'identità. Le alternative richieste nel testo non costituiscono una rassegna già eseguita; il controllo sui punti è già disponibile. Non dichiarare superiorità generale rispetto a SuperDec. |
| B07 · Forma/descrittore | Correggere l'idea di confronto tra ogni singola primitiva: il percorso corrente confronta D2 ricavato da punti campionati sulla superficie dell'insieme. Centra e normalizza la scala; le distanze tra coppie di punti non dipendono da una rotazione rigida comune. Questo non recupera posa, dimensione assoluta o corrispondenza tra primitive, né rende stabile una ricostruzione che cambia con la vista. Aggiornare lo stato con il confronto attivo concluso senza cambi di associazione, senza dedurne inutilità generale di SuperFlex. |
| B08 · Profondità baseline | Scheda vuota. Spiegare predizione della profondità da RGB e allineamento alla profondità renderizzata della scena nel codice originale. È il ramo che supporta XYZ baseline, distinto dalla scelta DA/MoGE per la forma. Nelle run correnti vengono riusati gli XYZ ufficiali: lettura del codice non equivale a nuova estrazione. |
| B09 · Camera/scena | Scheda vuota. Distinguere intrinseci per proiettare pixel/profondità, posa camera per passare alla scena e ricostruzione scena per allineamento. Non tutte queste informazioni servono a ogni freccia: la nuvola camera-frame DA richiede gli intrinseci, non necessariamente posa e scena; MoGE può stimare la camera. |
| B10 · Posizione | Scheda vuota. Il codice usa centro della bounding box, mediana della profondità nella maschera, intrinseci e posa camera per ottenere XYZ scena. Non è il centroide della nuvola di forma, una posa 6D o una misura fisica GT. XYZ invariati tra varianti per rendere interpretabile il contributo geometrico aggiunto. |
| B11 · Osservazione corrente | Scheda vuota. È il collegamento dei dati della stessa detection: aspetto/XYZ e forma eventualmente disponibile, con chiave e ordine coerenti. Un frame può contenere più osservazioni/oggetti. Non descrivere una nuova rete che concatena tre embedding. |
| B12 · Associazione/adattatore | Scheda vuota, centrale per la domanda scientifica. Whareformer resta congelato; l'adattatore aggiunge peso × (distanza neutra − distanza) ai logits delle track con confronto valido prima della softmax/assegnazione originale. New Track e confronti mancanti non ricevono correzione diretta; la competizione può comunque cambiare le probabilità. Controllo zero verificato; beneficio nullo nella griglia eseguita, causa ancora da diagnosticare. |
| B13 · Memoria precedente | Scheda vuota. Distinguere memoria baseline di aspetto/posizione, punti osservati e ultima forma geometrica valida. Tutte le detection del frame leggono stato geometrico precedente comune. Specificare la variante: forme separate in memoria limitata oppure ricostruzione da accumulo; non una memoria uniforme identica per ogni esperimento. |
| B14 · Esistente/nuova | Scheda vuota. È l'esito del matching, non un secondo test sulla bontà della fusione. Il rifiuto geometrico successivo non annulla l'associazione. Gli ID sono predetti dal tracker, non identità fisiche certificate. |
| B15 · Aggiornamento baseline | Scheda vuota. Descrivere uso di osservazione associata e memoria precedente secondo regole baseline; non mediare genericamente tutti i dati. È separato dall'ammissione geometrica: una fusione respinta non impedisce automaticamente l'aggiornamento di aspetto/posizione. |
| B16 · Geometria/ricostruzione | Scheda vuota e prioritaria. Nuvola corrente + memoria della track → registrazione candidata, gate, accumulo dei soli punti ammessi, nuova SuperFlex dopo ogni aggiornamento ammesso. Registratore PCA/multistart+ICP e soglie sono scelte nostre provvisorie, non prescrizioni dei paper; FPFH/RGB sono alternative previste, non eseguite da questa campagna. Stato aggiornato: fusioni avvenute, accuratezza indipendente da verificare; filtri ancora rinviati. |
| B17 · Nuova track | Scheda vuota. Nuovo ID dal matching e creazione secondo baseline. Non richiede una forma valida e non prova la comparsa di un oggetto fisico mai visto: può esserci frammentazione. |
| B18 · Inizializzazione | Scheda vuota. L'ID non contiene i dati: servono osservazione corrente e nuvola disponibile. Distinguere prima geometria valida e fusione tra viste. Dato geometrico mancante non significa impossibilità di mantenere la track baseline. |
| B19 · Memoria aggiornata | Scheda vuota. Spiegare stato per i frame futuri, versioni distinte di punti e ricostruzione e conservazione dell'ultima forma valida sui fallimenti. Le superfici completate non rientrano nei punti osservati. Il replay seriale con worker/cache non dimostra latenza realtime o frontend online completo. |

## Collegamenti: che cosa va spiegato

E01–E06 ed E08/E09 sono già compilati; E07 ed E10–E34 sono segnaposto. Le indicazioni sotto coprono tutti i 34 collegamenti e vanno usate per scrivere le schede, senza ripetere integralmente quelle dei nodi.

| Freccia | Contenuto e attenzione principale |
|---|---|
| E01 · RGB → maschere | Associazione del frame alle annotazioni fornite, non inferenza di segmentazione. I due alias storici non sono diventati join certificati: erano esclusi dalle run che richiedono corrispondenze esatte. |
| E02 · RGB → aspetto | Pixel per il ritaglio originale; nella prova corrente il descrittore è riusato, non estratto nuovamente. |
| E03 · maschere → aspetto | Selezione pixel/bounding box coerenti con RGB, ordine detection e ridimensionamenti; la maschera binaria non sostituisce l'immagine. |
| E04 · RGB → geometria | Frame intero a DA/MoGE, prima dell'isolamento dei singoli oggetti; aggiornare la prova con geometria rigenerata sul campione della campagna. |
| E05 · geometria → nuvola | Profondità DA da retroproiettare oppure punti MoGE; tenere distinte le convenzioni di camera, scala e validità. |
| E06 · maschere → nuvola | Selezione dei punti validi allineati ai pixel dell'oggetto; non ricostruisce parti nascoste. |
| E07 · camera/scena → nuvola | Specificare quale parte dell'input viene usata: intrinseci nel ramo DA. Non fare di posa/scena un prerequisito generale per i punti camera-frame né imporre gli intrinseci forniti a MoGE senza controllo. |
| E08 · nuvola → SuperFlex | Punti, campionamento a 4096 e normalizzazione/inversa. Il pilota con sei nuvole/cinque superfici è un risultato storico: nell'ultima campagna tutte le 446 osservazioni sono pronte per ciascuna sorgente. I fallimenti storici restano documentati senza descriverli come stato della nuova run. |
| E09 · SuperFlex → forma | Parametri, superficie e trasformazioni necessarie a produrre il descrittore. Distinguere metriche diagnostiche esplorate e D2 effettivamente usato nella campagna. |
| E10 · forma → osservazione | Descrittore disponibile o indicazione di assenza, legati alla stessa detection. Non vettore di primitive confrontato componente per componente. |
| E11 · aspetto → osservazione | Feature ufficiale con ordine e chiave coerenti. |
| E12 · RGB → profondità baseline | Ingresso dell'estrattore originale; nelle run con XYZ precalcolati questa fase non viene rigenerata. |
| E13 · camera/scena → profondità | Informazioni necessarie a renderizzare/allineare la profondità della scena; dichiarare il preprocessing e l'eventuale uso di asset già ricostruiti. |
| E14 · profondità → posizione | Valori della profondità allineata per il sollevamento 2D→3D. Non porta già l'XYZ finale. |
| E15 · maschere → posizione | Mediana di profondità nella maschera e bounding box; coerenza delle risoluzioni. |
| E16 · camera/scena → posizione | Intrinseci e posa per retroproiezione e cambio di riferimento; distinguere questi ruoli dall'allineamento già riassunto in E13. |
| E17 · posizione → osservazione | XYZ baseline nel riferimento scena. Non posa 6D o punti della superficie. |
| E18 · osservazione → matching | Dati correnti per baseline e adattatore, non terzo ingresso nativo della rete. Geometria opzionale con maschera esplicita di disponibilità. |
| E19 · memoria → matching | Stato precedente delle track candidate e loro ID effettivi; niente aggiornamenti della detection corrente nel confronto che la associa. |
| E20 · matching → decisione | Esito di associazione dopo softmax/assegnazione originale, non sola distanza geometrica. |
| E21 · decisione → aggiornamento baseline | Controllo/ID della track esistente; i dati arrivano anche da E27/E28. |
| E22 · decisione → aggiornamento geometrico | Track destinataria già predetta. Non è un'autorizzazione incondizionata a fondere: segue un controllo geometrico distinto. |
| E23 · decisione → nuova track | Esito New Track, non fallimento SuperFlex né rifiuto del gate di fusione. |
| E24 · nuova track → inizializzazione | ID effettivo/segnale di creazione; non contiene da solo punti, aspetto e posizione. |
| E25 · osservazione → inizializzazione | Aspetto, XYZ e forma eventualmente disponibile della stessa detection. |
| E26 · nuvola → inizializzazione | Punti stimati osservati e provenienza, non superficie completata da SuperFlex. |
| E27 · osservazione → aggiornamento baseline | Feature/XYZ correnti per la track associata, con ordine e tempo espliciti. |
| E28 · memoria → aggiornamento baseline | Stato precedente e regole baseline; non sostituire con una media inventata. |
| E29 · nuvola → aggiornamento geometrico | Punti correnti camera-frame, sorgente e osservazione. La registrazione li deve portare nel riferimento della memoria; XYZ della track da solo non fornisce tale trasformazione. |
| E30 · memoria → aggiornamento geometrico | Nuvola osservata/versione valida precedente e provenienza; non solo mesh predetta. |
| E31 · aggiornamento baseline → memoria | Nuovo stato di aspetto/posizione, indipendente dal successo dell'ammissione geometrica. |
| E32 · aggiornamento geometrico → memoria | Punti/versione ammessi e ricostruzione validata quando disponibile. Su rifiuto/fallimento conservare lo stato valido pertinente; distinguere versione della nuvola e ultima forma riuscita. |
| E33 · inizializzazione → memoria | Stato iniziale della track, anche con geometria indisponibile; inizializzazione non va conteggiata come fusione. |
| E34 · memoria aggiornata → precedente | Passaggio temporale ai frame successivi. Nessun effetto retroattivo sul matching corrente; causalità logica distinta da una dimostrazione di esecuzione realtime. |

## Ordine pratico proposto

1. B01–B03 con E01–E03: correggere confine degli input e riuso della baseline.
2. B08–B10 con E12–E17 ed E07: rendere chiara la differenza fra posizione e forma.
3. B04–B07 con E04–E10: sorgenti geometriche, punti, SuperFlex e confronto D2.
4. B11–B14 con E11/E18–E20: spiegare esattamente come la forma può influire sull'associazione e qual è l'esito misurato.
5. B15–B19 con E21–E34: associazione, ammissione geometrica, memoria e causalità.

Per ogni gruppo: leggere i commenti esistenti; l'assistente spiega errori/lacune e prova disponibile; Marco scrive e salva; l'assistente verifica su richiesta la nuova formulazione. Non riempire tutte le schede con la stessa storia dei job: riportare solo l'evidenza pertinente e rimandare ai resoconti.

## Stato della revisione

Snapshot successivo alla compilazione manuale, verificato nel JSON il 15 novembre: 10 nodi commentati e nove ancora segnaposto; 21 frecce commentate e 13 ancora segnaposto. Residui e ID in STATO_LAVORO.md/TODO.md. E10 contiene ancora «[da espandere]» nelle alternative; E21 ha miglioramenti vuoto, senza necessità di inventare un miglioramento. Questo snapshot supera il conteggio iniziale per lo stato di compilazione; la diagnosi iniziale rimane storica. Nessun testo della mappa modificato dall'assistente.

Durante B12 Marco precisa che integrazione della forma e intensità del contributo sono una discussione architetturale ancora da svolgere con il compagno. La correzione esterna attuale è provvisoria; calibrazione mediante ricerca, apprendimento di pochi parametri a reti congelate e adattamento della rete sono alternative discusse, non nuove scelte approvate. Proporre nota nel campo alternative e richiamare la decisione pendente nei miglioramenti, senza sovrascrivere il funzionamento implementato o confondere le varianti di memoria con le modalità di fusione dei segnali.

Durante B07 Marco richiede di approfondire perdita d'informazione di D2 e normalizzazione della dimensione assoluta, considerando due utilizzi della forma: segnale di associazione e geometria dell'oggetto ricordata nello spazio della scena accanto all'XYZ della traccia. Intento esplicito da discutere, non capacità già verificata. Nella spiegazione distinguere descrittore normalizzato e ricostruzione conservata con inversa; compatibilità della scala e trasformazione dalla forma alla scena richiedono verifica, l'XYZ da solo non determina orientamento e scala della superficie.

Ricognizione e checklist completate. Restano da svolgere la scrittura manuale e la verifica progressiva delle formulazioni nuove. I testi e la struttura della mappa non sono stati modificati dall'assistente; questa analisi non ne certifica una revisione già conclusa.
