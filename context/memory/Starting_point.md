# Progetto di gruppo - Computer Vision

## Contesto e obiettivi

Siamo un gruppo di **2 studenti** del corso *Deep Learning for Computer Vision* della Bocconi (confermato da Marco il 4 novembre 2026). Vogliamo sviluppare un lavoro eccellente per la valutazione didattica, rilevante per la percezione dei robot, in particolare la robotica umanoide, e con una domanda di ricerca abbastanza solida e una metodologia eccellente tale da poter aspirare a una pubblicazione scientifica.

La direzione di ricerca è **integrare Whareformer con una memoria geometrica degli oggetti basata principalmente su SuperFlex**. Il 4 novembre 2026 Marco ha approvato la domanda riportata sotto ed EPIC-KITCHENS come base comune degli esperimenti. Architettura, aggiornamento della memoria e protocollo dettagliato restano da definire.

## Paper principali

1. **[Whareformer: Learning to Track What is Where in Long Egocentric Videos](https://arxiv.org/html/2607.08537)** — Jacob Chalk et al., 2026. È la base del progetto. Traccia nel tempo l’identità e la posizione 3D degli oggetti osservati in video egocentrici, mantenendone memoria anche quando escono dall’inquadratura.

2. **[SuperFlex: Deformable Superquadrics for Point Cloud Decomposition](https://arxiv.org/html/2607.01015)** — Gabriel Tavernini et al., 2026. È il **componente geometrico principale** che intendiamo studiare. Rappresenta oggetti 3D con un insieme compatto di primitive geometriche; la sua versione *robust* è progettata per osservazioni parziali, frequenti nei video egocentrici. [Codice e pesi](https://github.com/GabrielTavernini/superflex) sono pubblici.

**[SuperDec: 3D Scene Decomposition with Superquadric Primitives](https://arxiv.org/html/2504.00992)** — Elisabetta Fedele et al., 2025 — è **esclusivamente un riferimento secondario e opzionale**. Può servire per comprendere l’evoluzione verso SuperFlex o, se utile e fattibile, come confronto sperimentale. **Non è un paper principale, non è un componente richiesto e non è obbligatorio implementarlo.**

## Idea scientifica iniziale

**Domanda approvata:** «A parità di immagini, maschere, descrittori visivi e posizioni 3D, aggiungere a Whareformer un confronto tra la forma stimata con SuperFlex per ciascuna osservazione e una memoria delle forme delle track, anch'esse stimate con SuperFlex, migliora l'associazione delle osservazioni alle identità degli oggetti nel tempo?»

Whareformer conserva informazioni su *che cosa* sia un oggetto e *dove* si trovi. La nostra estensione studia la forma sia nell'osservazione corrente sia nella memoria. EPIC-KITCHENS è la base comune approvata per sviluppo e valutazione; il test finale resta separato. Questo non implica addestrare un nuovo modello: l'eventuale training del modulo di associazione dipenderà dalla modifica scelta. La misura dell'identità è prioritaria; confronto delle forme, aggiornamento della memoria e protocollo dettagliato restano da definire. La superquadrica non sostituisce automaticamente il punto usato da Whareformer per la posizione: forma e posizione sono segnali distinti.

**Estensione discussa, fuori dallo scope attuale per limiti di tempo:** aggiungere un modello di reasoning che riconosca tipo e stato dell'oggetto, distingua cambiamenti reali dalle differenze dovute al punto di vista e regoli quanto fidarsi della forma nell'associazione. L'idea potrebbe essere rilevante per oggetti manipolati che cambiano aspetto o contenuto pur mantenendo la stessa identità. Non la includiamo tra gli obiettivi necessari del progetto: prima va verificata la fattibilità e l'utilità della sola integrazione SuperFlex–Whareformer. Se emergessero risultati e tempo sufficienti, un semplice peso adattivo della forma potrebbe essere studiato come estensione successiva, senza impegnarsi ora a integrare un ulteriore modello.

**Due verifiche decisive prima di fissare il metodo:**

1. Gli input disponibili permettono di ottenere, per gli oggetti osservati, nuvole di punti 3D sufficientemente affidabili da usare con SuperFlex? Whareformer dispone di un punto 3D per oggetto, che da solo non basta a descriverne la superficie.
2. La forma così stimata porta informazione utile per l'associazione delle identità **oltre** a quella già presente nelle feature visive DINOv2 e nella posizione 3D di Whareformer? Un'integrazione tecnicamente riuscita non implica un contributo misurabile.

La rilevanza per la robotica riguarda la memoria degli oggetti e la percezione spaziale necessarie, per esempio, a navigazione e manipolazione. Non disponiamo di un robot per validare direttamente queste applicazioni: dovremo distinguere con rigore i risultati misurati dalle possibili applicazioni future.

## Vincoli e prossimi passi

- Ruoli confermati il **7 novembre 2026**: **Marco segue dati/geometria e SuperFlex (persona B)**; l'altro membro segue **Whareformer, integrazione e valutazione (persona A)**. Report e decisioni metodologiche restano condivisi.
- Tempo disponibile: fino al **23 novembre 2026**, circa **2 ore al giorno per persona**.
- Accesso alle GPU HPC Bocconi già confermato da Marco il 4 novembre 2026. Configurazione universitaria riportata da Marco: due nodi Dell PowerEdge R750XA, ciascuno con due Intel Xeon 5317 da 12 core, 512 GB DDR4-3200 e quattro NVIDIA A100 da 80 GB. Quote, risorse assegnabili per job e tempi di coda restano da verificare; non assumere uso esclusivo dei nodi o disponibilità contemporanea di tutte le GPU.
- Repository Git locale predisposto; Marco deve creare quello condiviso.
- Pianificare il lavoro assumendo **nessun accesso garantito a robot o dati privati**; privilegiare dati e modelli pubblici.
- Il mio livello iniziale in deep learning e computer vision è ancora introduttivo.

I file del corso presenti in questo nuovo progetto contengono syllabus e requisiti ufficiali del lavoro: consultali prima di definire il piano. Aiutaci poi a scegliere **una domanda di ricerca precisa, fattibile e difendibile**, verificando la letteratura, la disponibilità dei dati, la novità rispetto ai lavori esistenti e i confronti sperimentali necessari. Non presumere che l’integrazione migliori Whareformer: anche stabilire *quando e perché* la geometria aiuta o non aiuta deve essere oggetto della ricerca.

Dopo aver scelto la domanda di ricerca, procederemo con la stesura del piano di realizzazione del progetto e l'esecuzione scientifica di questo.
