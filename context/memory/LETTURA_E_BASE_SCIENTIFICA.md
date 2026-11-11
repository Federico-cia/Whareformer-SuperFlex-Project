# Base scientifica per il lavoro di gruppo

Aggiornamento: 4 novembre 2026 (decisioni e vincoli organizzativi; lettura preparatoria precedente invariata). Stato: lettura preparatoria completata; Marco ha approvato la domanda riportata in `Starting_point.md` ed EPIC-KITCHENS come base comune degli esperimenti. Il confronto usa forme stimate con SuperFlex sia nell'osservazione corrente sia nella memoria delle track. Sviluppo e test finale restano separati; metodo e protocollo dettagliato sono ancora da definire. Le raccomandazioni preliminari nei paragrafi seguenti documentano la valutazione precedente; per le decisioni correnti vedere `FASE_0.md`.

## 1. Che cosa è stato effettivamente esaminato

- I due Markdown iniziali: `Starting_point.md` e `ISTRUZIONI_SUPERVISORE_SCIENTIFICO.md`.
- Il testo dei 26 PDF originariamente presenti nel workspace: 1.411 pagine complessive, comprendenti syllabus, lista progetti, dieci lezioni, dispense, esempio d'esame e dodici report. Nelle slide sono state eliminate dalla lettura soltanto le righe identiche ripetute nelle animazioni.
- Sei paper: Whareformer, SuperFlex, SuperDec, OSNOM/LMK, EgoTrack3D e Hierarchical Object Representation for Spatial Robot Perception. Sono stati letti metodo, esperimenti, limiti e appendici presenti nei PDF, oltre al testo introduttivo e ai riferimenti.
- Figure e tabelle pertinenti ai requisiti, ai metodi principali e ai risultati. Non è stata svolta un'ispezione visiva individuale di tutte le 1.411 pagine del materiale didattico.
- README, configurazioni e parti centrali del codice pubblico di Whareformer e SuperFlex. Questa è un'ispezione del codice, non una replica sperimentale.

I PDF dei sei paper sono conservati nella sottocartella `Fonti`. L'inventario dei documenti del corso è in `INDICE_MATERIALI_LETTI.md`. Il materiale di estrazione e le copie di codice consultate sono organizzati sotto `tmp/pdfs` nella radice del workspace.

Non sono stati eseguiti i modelli, scaricati i checkpoint o i dataset completi, installate dipendenze CUDA o verificati accesso e disponibilità delle GPU. Le fonti possono essere aggiornate: questa ricognizione non dimostra l'assenza di ulteriori lavori concorrenti.

## 2. Requisiti e vincoli da conservare

**Documenti ufficiali del corso:** il syllabus indica gruppi di **tre studenti**, sviluppo di un progetto con progettazione, implementazione, training, validazione e discussione critica. La valutazione comprende report (12 punti), presentazione (4), poster (4), con un possibile punto aggiuntivo per un lavoro eccezionale. L'uso di strumenti generativi è consentito come supporto. Fonte: `syllabus.pdf`, sezioni Assessment Methods e GenAI Use. L'obbligo di creare e mantenere un repository Git è indicato nella `Lecture 1_DL4CV.pdf`, sezione Project Repository (riferimento corretto dopo ricontrollo del 4 novembre 2026).

Whareformer è il progetto n. 16 della lista; SuperDec è il n. 30. È consentito proporre un proprio paper. Questo non equivale all'approvazione automatica della nostra specifica integrazione. Fonte: `20600__project_list (1) (1).pdf`.

Il calendario della Lecture 1 è dichiarato provvisorio e riporta presentazioni il **24 novembre** e poster il **1 dicembre**. La scadenza di lavoro fornita da Marco resta **23 novembre 2026**. Nei materiali letti non ho trovato una consegna definitiva con numero di pagine del report, durata dell'intervento e rubrica analitica. I dodici report passati offrono solo un'indicazione generica di come si è svolto il lavoro nel corso: non stabiliscono vincoli per il nostro progetto.

**Vincoli del gruppo, aggiornati da Marco il 4 novembre:** due studenti, scadenza confermata il 23 novembre, circa due ore al giorno per persona; accesso alle GPU HPC Bocconi già disponibile, con A100 da 80 GB nelle specifiche universitarie riportate dall'utente. Quote e risorse assegnabili per job restano da verificare. Nessun robot o dato privato garantito; livello iniziale introduttivo. Il syllabus prevede tre studenti: l'eventuale autorizzazione al gruppo di due va verificata. Marco creerà il repository condiviso; quello locale è stato predisposto. SuperFlex resta il componente geometrico principale; SuperDec resta secondario e opzionale.

**Integrità del materiale:** il PDF delle dispense contiene 154 pagine effettive. Dopo la pagina stampata 149, conclusione del capitolo 8 sulla segmentazione, passa alla bibliografia con numerazione stampata 194. I capitoli 9–12 annunciati nell'indice non sono presenti nel corpo di questo file. La Lecture 10 fornisce comunque materiale sui transformer. Il file d'esame ha inoltre una discrepanza fra anno nel nome e data sul frontespizio: serve come esercitazione, non come fonte delle regole attuali.

## 3. I paper e il loro ruolo

### Whareformer: la base del tracking

Associa osservazioni di oggetti a identità persistenti nei video egocentrici. Combina distanza fra descrittori visivi DINOv2 e distanza fra posizioni 3D; un transformer decide l'associazione a una traccia esistente oppure l'apertura di una nuova. La memoria visiva usa microcluster DenStream; quella spaziale conserva osservazioni recenti. Il benchmark principale impiega maschere annotate e profondità allineata alla ricostruzione della scena. Riporta mPCL 72,2 e IDF1 84,0 su EPIC-KITCHENS. I tempi del tracking escludono la preparazione completa degli input.

**Confine del contributo:** contiene già informazione geometrica sulla posizione. La nostra possibile estensione riguarda forma ed estensione dell'oggetto. Non produce una ricostruzione della sua superficie o una posa 6D.

Fonte: [paper](https://arxiv.org/html/2607.08537), metodo, esperimenti e appendici; [progetto](https://jacobchalk.github.io/Whareformer/).

### SuperFlex: la rappresentazione geometrica principale

Trasforma una nuvola di punti di un oggetto in un insieme compatto di superquadriche deformabili, con tapering e bending. Usa PVCNN e un decoder transformer con un massimo di 16 primitive. La formulazione geometrica conta 19 gradi di libertà per primitiva, oltre all'esistenza; il numero di valori memorizzati dipende dalla codifica delle rotazioni. Distingue fitting della superficie osservata e completamento supervisionato a partire da osservazioni parziali. Le prove reali di completamento sono prevalentemente qualitative. L'appendice D mostra già una pipeline RGB con SAM3, MoGE e SuperFlex.

**Confine del contributo:** non verifica identità temporale o memoria egocentrica. L'ottimizzazione con occupazione completa non può essere trasferita automaticamente a un video con sole superfici visibili. La distanza radiale usata nel metodo non coincide generalmente con una distanza euclidea esatta dalla superficie.

Fonte: [paper](https://arxiv.org/html/2607.01015), incluse appendici C–D; [progetto](https://superflex3d.github.io/).

### SuperDec: riferimento secondario

È il predecessore basato su superquadriche rigide, con encoder di punti, query di primitive e raffinamento opzionale. La decomposizione di scene dipende dalla segmentazione preventiva dei singoli oggetti. Le dimostrazioni robotiche usano scene ricostruite e condizioni specifiche; non dimostrano memoria temporale da video egocentrico. Serve per capire la famiglia di rappresentazioni ed eventualmente costruire un confronto, se utile e sostenibile. Non è una componente obbligatoria del progetto.

Fonte: [paper, versione 2](https://arxiv.org/html/2504.00992v2).

### OSNOM / Lift, Match and Keep: task e valutazione

Introduce il problema di mantenere identità e posizione di oggetti anche fuori dall'inquadratura. LMK solleva le osservazioni 2D in coordinate 3D, le associa usando aspetto e posizione e mantiene l'ultima localizzazione. Le posizioni di riferimento derivano dallo stesso procedimento di proiezione con profondità stimata; non sono misure fisiche indipendenti. La ricostruzione statica e la retroproiezione temporale iniziale richiedono attenzione quando si parla di elaborazione causale. Lo split originale non coincide con quello successivo di Whareformer. Le appendici analizzano spostamento, rappresentazione visiva e fallimenti in scene affollate.

Fonte: [paper, versione 2](https://arxiv.org/html/2404.05072v2), [progetto OSNOM](https://dimadamen.github.io/OSNOM/).

### EgoTrack3D: confronto recente sulla geometria nel tracking

Il preprint del 2026 combina aspetto, movimento, nuvole di punti e box 3D per associare oggetti egocentrici. La variante densa è valutata in condizioni controllate con profondità affidabile; quella sparsa affronta input geometrici più limitati. La sua PCL ha definizione e aggregazione diverse da quelle di Whareformer: i numeri non sono direttamente confrontabili. Mostra che usare geometria più ricca per il tracking è una direzione già esplorata, senza risolvere automaticamente il nostro caso.

Fonte: [paper](https://arxiv.org/html/2608.08016), in particolare metodo e valutazione.

### Hierarchical Object Representation / Hickory: precedente sulle primitive come memoria

Il preprint del 2026 costruisce una rappresentazione gerarchica di oggetti da RGB-D: punti, mesh, superquadriche e primitive inflazionate per collisioni. Usa anche descrittori geometrici di superquadriche per associazione e allineamento di mappe. Le prove riguardano soprattutto percezione robotica e mappe, con componenti di ricostruzione costose. Non coincide con il benchmark OSNOM, ma impedisce di rivendicare genericamente come nuova una memoria di oggetti basata su superquadriche.

Fonte: [paper](https://arxiv.org/html/2606.01545), [repository degli autori](https://github.com/perceptica-robotics/Hickory).

## 4. Che cosa aggiunge la lettura del codice

Versioni consultate: Whareformer commit `82dd349957e1f04f92a2979b4c92c2f3fed445c5`; SuperFlex commit `15b63b23375c6a80c3ce0dec4be0c9b11055c722`. Sono istantanee consultate, non garanzie sulla versione più recente.

| Aspetto | Evidenza nell'implementazione | Conseguenza per noi |
|---|---|---|
| Input di Whareformer | Descrittori visivi e coordinate XYZ per osservazione | I descrittori già estratti non contengono la superficie dell'oggetto: occorrono RGB, maschere e profondità o point cloud |
| Associazione | Proiezione iniziale di due distanze, con parametri appresi | Aggiungere una distanza di forma richiede adattare il modello o progettare una fusione calibrata |
| SuperFlex | Campionamento di 4.096 punti; normalizzazione per oggetto | Conservare trasformazione inversa, scala metrica e posa; duplicare punti non aggiunge superficie osservata |
| Dipendenze | Operazioni point-voxel CUDA e pacchetti compilati | Installazione e compatibilità vanno provate; non è verificata un'esecuzione semplice su CPU/Windows |
| Risorse rilasciate | Link a pesi e feature nei README | Rilascio annunciato verificato; download, permessi e funzionamento dei checkpoint non verificati |

La configurazione Whareformer usa PCA a 256 dimensioni e transformer con dimensione interna 64. Il codice usa weight decay `5e-3`, coerente con l'appendice ma diverso dal valore nel testo principale: per una replica bisogna fissare versione e configurazione. L'aggregazione della metrica va ripresa dall'evaluator ufficiale, non reinventata come media arbitraria per video.

**Discrepanza da verificare per la replica:** il §3.7 descrive una risoluzione iterativa dei conflitti fra osservazioni che scelgono la stessa track; l'appendice 0.E distingue iterative, Hungarian e greedy, dichiara selezionata greedy e riporta 72,2 mPCL / 84,0 IDF1 per greedy contro 72,2 / 83,6 per iterative. Non trattare i due nomi come sinonimi: controllare nell'implementazione e nella configurazione dei risultati principali quale strategia è stata effettivamente usata.

Le configurazioni SuperFlex partono da modelli già addestrati e prevedono training lungo; alcune contengono percorsi specifici degli autori. Per i tempi del gruppo, partire dai checkpoint è la raccomandazione preliminare. Nessuna stima di VRAM o di ore GPU del nostro progetto è stata misurata.

Fonti: [codice Whareformer consultato](https://github.com/JacobChalk/Whareformer/tree/82dd349957e1f04f92a2979b4c92c2f3fed445c5), [codice SuperFlex consultato](https://github.com/GabrielTavernini/superflex/tree/15b63b23375c6a80c3ce0dec4be0c9b11055c722).

## 5. Valutazione scientifica preliminare

I punti seguenti sono **inferenze e criteri proposti per la discussione**, non risultati di nostri esperimenti.

**Direzione di ricerca concordata il 1 novembre 2026.** Studiare se una memoria della forma 3D degli oggetti, ottenuta con SuperFlex come insieme di superquadriche deformabili, migliori l'associazione delle osservazioni alle track di Whareformer nei video egocentrici. La prima verifica deve isolare il contributo della forma mantenendo comparabili maschere, feature visive e posizioni 3D. Forma e posizione svolgono ruoli diversi: non assumere che le superquadriche possano semplicemente sostituire il singolo punto 3D di Whareformer. Resta aperto come costruire le nuvole di punti degli oggetti, confrontare forme stimate da viste parziali e aggiornare la memoria senza confondere cambiamenti di vista con cambiamenti reali. Non è stato ancora scelto un metodo specifico né dimostrato un miglioramento.

**Estensione discussa ma esclusa dallo scope attuale per il poco tempo disponibile.** Usare un modello di reasoning su categoria, interazioni e stato dell'oggetto per decidere quando una variazione della forma sia compatibile con la stessa identità e quanto pesare la geometria nell'associazione. Esempi discussi: contenitori che si svuotano rispetto a oggetti strutturalmente stabili. Prima di aggiungere un tale modulo, occorre verificare la sola integrazione SuperFlex–Whareformer. Un peso adattivo semplice potrebbe diventare un'analisi successiva solo se fattibilità e tempo lo consentono; non è un requisito del progetto.

**Priorità scientifiche decisive, confermate dopo la lettura di Whareformer:** (1) verificare se maschere, profondità e pose disponibili consentono di costruire nuvole di punti degli oggetti abbastanza affidabili per SuperFlex; (2) verificare se la forma stimata aggiunge informazione per l'associazione delle identità rispetto alle feature DINOv2 e alle posizioni 3D già usate da Whareformer. Queste due domande guidano la scelta della domanda di ricerca e il primo controllo di fattibilità. Analisi di New Track, strategie avanzate di aggiornamento e test diagnostici sulle coppie non sono priorità decisive; restano dettagli eventuali solo se necessari a interpretare o migliorare i risultati principali.

**Fattibilità della nuvola di punti, da verificare empiricamente:** per ciascun pixel valido della maschera di un oggetto, usare la profondità per retroproiettarlo con gli intrinseci della camera (`p_camera = z(u,v) K^{-1}[u,v,1]^T`); applicare la posa solo se servono coordinate nel mondo. Il risultato è una superficie visibile *parziale*, non la geometria completa. VISOR fornisce maschere, EPIC-Fields pose/intrinseci e Whareformer parte da RGB e profondità monoculare allineata alla scena; i soli descrittori preestratti e la posizione 3D puntuale distribuiti per il tracker non bastano, e potrebbe essere necessario rieseguire la stima della profondità per pixel. La ricostruzione statica EPIC-Fields non è la nuvola degli oggetti mobili. SuperFlex dimostra l'uso di maschere e mappe di profondità per punti parziali (§5.3, appendice D), ma non ne valida l'utilità nel benchmark Whareformer. Rischi principali: profondità locale errata o senza scala coerente, contaminazione ai bordi della maschera, oggetti piccoli/riflettenti/sottili e forte occlusione; ricampionare a 4096 punti non aggiunge superficie non osservata. Prima dell'integrazione, controllare visivamente su un piccolo campione maschera, profondità, punti e output SuperFlex, e misurare la stabilità fra viste dello stesso oggetto rispetto alla separazione fra oggetti diversi. Ottenere i punti è tecnicamente plausibile; ottenere forme abbastanza affidabili e discriminative resta aperto.

1. **La giunzione fra i due metodi è un problema di dati.** Una posizione XYZ non basta per ricostruire la forma. Va verificata la disponibilità di osservazioni geometriche degli oggetti mobili, senza confonderle con la mesh statica dell'ambiente.
2. **Forma, identità e posizione richiedono misure distinte.** Una forma plausibile può essere identica per due oggetti diversi; una migliore ricostruzione può lasciare invariato IDF1. PCL combina associazione e localizzazione e da sola non spiega quale componente migliori.
   **Possibile ridondanza con DINOv2 da approfondire:** il descrittore visivo può già codificare indizi di forma. Prima dell'integrazione, confrontare distanze visive e geometriche su coppie di osservazioni dello stesso oggetto e di oggetti diversi, separando cambi di vista, occlusioni, oggetti di forma simile e cambiamenti d'aspetto. La domanda è se la geometria corregga errori specifici del descrittore visivo, non se distingua genericamente le categorie. Se i due segnali commettono gli stessi errori, il contributo aggiuntivo della forma potrebbe essere scarso.
3. **I parametri delle primitive non sono identificatori stabili.** Ordine, simmetrie e decomposizioni alternative rendono debole una distanza euclidea sul vettore grezzo. Serve distinguere forma, scala e posa, con confronto fra insiemi o superfici adeguatamente allineati.
4. **La geometria completata contiene ipotesi.** Le parti non viste possono essere plausibili ma errate. Una memoria dovrebbe distinguere evidenza osservata e completamento, e considerare qualità e occlusione prima di aggiornarsi.
5. **Accumulare punti di un oggetto mobile nelle coordinate del mondo può deformarlo artificialmente.** Servono allineamento coerente, selezione delle viste o aggiornamenti conservativi. Usare frame futuri cambierebbe il regime temporale del metodo.
6. **L'originalità deve essere precisa.** Unire due reti o applicare SuperFlex a RGB non basta. Gli eventuali contributi potrebbero riguardare stabilità temporale, aggiornamento della memoria o gestione dell'incertezza, ma la domanda va ancora scelta e confrontata con i lavori vicini.

Per attribuire un eventuale beneficio a SuperFlex sarebbe utile confrontarlo anche con una geometria semplice, come dimensioni o box 3D, mantenendo gli stessi input. I costi dovrebbero includere estrazione geometrica, aggiornamento, memoria e associazione; il solo tempo di forward non misura l'intera pipeline.

**Disciplina del confronto concordata con Marco:** confrontare Whareformer originale e Whareformer con memoria della forma usando le stesse osservazioni, maschere, feature visive, posizioni 3D, split e protocollo di valutazione. Aggiungere, se fattibile, una baseline geometrica semplice (per esempio dimensioni o box 3D ottenuti dagli stessi dati) per verificare se gli eventuali guadagni richiedono davvero la decomposizione in superquadriche di SuperFlex. Riportare IDF1 per l'associazione e mPCL per la localizzazione, senza attribuire alla sola forma benefici dovuti a input o preprocessing diversi.

## 6. Spunti dai report di lavori passati

I dodici report sono esempi generici del contesto del corso. Tema, metodo, struttura, lunghezza, metriche, risorse e ambizione dei lavori passati non vincolano le nostre scelte. Non costituiscono una rubrica ufficiale e i loro risultati non sono verificati indipendentemente. La tabella raccoglie soltanto osservazioni critiche che possono aiutarci a ragionare.

| Report | Osservazione metodologica possibile |
|---|---|
| Feedback-Augmented RT-DETR | Distinguere confronto interno con modifica attiva/disattiva e confronto con una baseline addestrata in condizioni equivalenti |
| Mean Square Terrific | Un obiettivo può funzionare su un benchmark e generalizzare poco quando cambia la struttura delle annotazioni |
| SuperCLIP-Recon (`report.pdf`) | Guadagni piccoli o incerti e risultati negativi sono informativi se valutati e descritti correttamente |
| BRAATHEN / CutLER | L'aumento della metrica totale può dipendere da oggetti medi e grandi, senza risolvere il problema iniziale degli oggetti piccoli |
| ASO / Temba | Un risultato sul modulo temporale non comprende necessariamente costo e causalità dell'estrattore delle feature |
| DAFT-Drive | Confrontare specialisti e modello globale richiede controllare dati, budget di ottimizzazione e disponibilità del router |
| Guidotti-Toscano | Le divisioni per video e il trasferimento della soglia fuori dominio sono essenziali per interpretare risultati elevati |
| Epipoles and Popsicles | Una migliore stima dell'orientamento non implica una migliore detection; verificare se i guadagni restano a training più lungo |
| Convolution & Co | Il recupero di watermark su prompt e trasformazioni limitati non dimostra robustezza generale; esaminare crop e visibilità |
| shape SIFTers / TembaPanoptic | STQ può crescere grazie alla segmentazione mentre la componente di associazione non migliora |
| FERT / Where to Slide | Separare cambiamento visivo, successo semantico e preservazione; dichiarare quando la stessa maschera guida e valuta il metodo |
| OMNI-4DGS | Compattezza, fedeltà e velocità hanno compromessi diversi; FPS su hardware diverso e singole esecuzioni non provano superiorità generale |

Il materiale didattico fornisce il collegamento fra formazione dell'immagine, proiezione geometrica, CNN, ottimizzazione, detection, segmentazione, attenzione e transformer. Per il nostro progetto i punti più direttamente operativi sono maschere, coordinate e trasformazioni, rappresentazioni preaddestrate, associazione temporale e validazione fuori scena.

## 7. Questioni aperte prima di fissare il progetto

- **Accesso concreto:** checkpoint funzionanti, condizioni d'uso dei dataset, maschere, profondità, pose, dimensioni dei download e risorse HPC effettive.
- **Qualità geometrica:** superfici utilizzabili degli oggetti di interesse, soprattutto piccoli, sottili, riflettenti o fortemente occlusi.
- **Utilità del segnale:** stabilità della forma fra viste dello stesso oggetto e capacità di distinguerlo da altri oggetti simili.
- **Aggiornamento della memoria della forma, da discutere prima di fissare il metodo:** confrontare almeno forma della prima osservazione, sostituzione con l'ultima e aggiornamento solo con osservazioni giudicate migliori. Possibili estensioni sono conservare poche forme rappresentative o accumulare punti dopo un allineamento dell'oggetto. Valutare viste parziali, errori di associazione, cambiamenti reali dell'oggetto, costo e stabilità. Non mediare direttamente i parametri di insiemi di superquadriche senza corrispondenza fra primitive. Whareformer non fornisce una regola per aggiornare una memoria della forma: è una decisione del nostro progetto.
- **Protocollo:** eventuale validazione ricavata dalle scene ammesse al training; test separato; nessun tuning su frame dipendenti o sul test.
- **Rivendicazione:** quale risultato misurabile vogliamo spiegare e quale differenza concreta avremmo rispetto a Whareformer, EgoTrack3D e Hickory.

La raccomandazione preliminare è discutere prima un controllo diagnostico piccolo sulla qualità e discriminatività della geometria, poi valutare il costo dell'integrazione. È una proposta da valutare insieme: nessun dataset, esperimento o metodo è stato fissato con questo documento.
