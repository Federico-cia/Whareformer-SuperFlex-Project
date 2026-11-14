window.MAP_DATA = {
  "version": 1,
  "nodes": [
    {
      "id": "B01",
      "title": "RGB · frame t",
      "x": 40,
      "y": 280,
      "group": "input",
      "review": "Descrizione modificata · evidenze da verificare",
      "summary": "Il frame RGB è l’input visivo comune del processo.",
      "sources": [
        "INTEGRAZIONE_BASELINE_REALE_20261113.md",
        "Whareformer-repo/src/feature_extraction/datasets/epic_dataset.py",
        "Whareformer-repo/src/feature_extraction/utils/common.py"
      ],
      "verified": "14 novembre 2026 · verifica documentale, nessuna nuova run",
      "failure": "-",
      "contract": "-",
      "role": "è il punto di ingresso dei pixel che trasportano informazione sulla scena. I pixel verranno utilizzati sia come input per ricostruire la posizione 3D sia per descrivere la parvenza 2D sia per ricostruire la forma 3D",
      "state": "Al momento stiamo usando solo input già utilizzati nel paper Whareformer, appartenenti al dataset EPIC-KITCHENS.",
      "evidence": "Sarebbe ottimo generalizzare con input generici, non solo il dataset già utilizzato nei paper di riferimento. Sarà uno step che verrà fatto a pipeline verificata e funzionante.",
      "why": "Input comuni permettono confronti coerenti fra baseline, punti e SuperFlex.",
      "alternatives": "DA e MoGE sono alternative geometriche sullo stesso input. Ma si tratta di input più complessi, non il video proveniente da una semplice videocamera. La pipeline che vogliamo creare vuole partire dai video egocentrici il più \"semplici\" possibili, quindi semplici video RGB.",
      "improve": "Questo punto èl'input, non è immediatamente migliorabile. L'obiettivo è rendere l'input il più semplice e \"democratico\" possibile: il classico video RGB egocentrico.",
      "editedAt": "2026-11-14T16:27:40.026Z"
    },
    {
      "id": "B02",
      "title": "Maschere 2D · VISOR",
      "x": 310,
      "y": 280,
      "group": "input",
      "review": "Descrizione modificata · evidenze da verificare",
      "summary": "La maschera indica, nel frame di input, i pixel appartenenti all'oggetto sotto osservazione.",
      "sources": [
        "INTEGRAZIONE_BASELINE_REALE_20261113.md",
        "Whareformer-repo/src/feature_extraction/datasets/epic_dataset.py",
        "Whareformer-repo/src/feature_extraction/utils/common.py"
      ],
      "verified": "14 novembre 2026 · verifica documentale, nessuna nuova run",
      "failure": "Una maschera imprecisa può aggiungere pixel non facenti parte dell'oggetto o eliminare parti che ne fanno parte. Questo ha ripercussioni sia sull'associazione del frame alla traccia che poi sulla memoria della traccia stessa.",
      "contract": "La maschera deve riferirsi alla stessa immagine e allo stesso oggetto elaborati dagli altri rami. Se l’immagine viene ridimensionata, anche la maschera deve essere adattata in modo che i pixel restino allineati.",
      "role": "Indica quali pixel dell’immagine appartengono all’oggetto. Usiamo questa selezione per:\n• descrivere l’aspetto dell’oggetto usando i suoi pixel RGB;\n• estrarre dalla ricostruzione 3D i punti dell’oggetto;\n• stimare la sua distanza dalla camera usando la profondità dei pixel selezionati.\nDalla maschera ricaviamo anche un rettangolo che racchiude l’oggetto, utile per ritagliarne l’immagine.",
      "state": "Le annotazioni VISOR sono fornite come parte del dataset EPIC-KITCHENS, attraverso le annotazioni VISOR usato per lo sviluppo della pipeline. Nessun segmentatore nuovo è stato adottato o eseguito in questa fase, ma ne va considerata l'adozione qualora si volesse gneeralizzare la pipeline.",
      "evidence": "Le maschere che usiamo sono già fornite dalle annotazioni VISOR, associate ai video EPIC-KITCHENS: in questa fase non le generiamo con un nostro modello. Abbiamo verificato nel codice che siano usate per selezionare la regione dell’oggetto e abbiamo controllato la corrispondenza con le immagini nei casi documentati.\nLimite: questo lavoro non dimostra che un modello saprebbe produrre maschere altrettanto utilizzabili su un nuovo video senza annotazioni. Una maschera può inoltre includere sfondo o escludere parti dell’oggetto.",
      "why": "Per limitare la complessità, riutilizziamo la sorgente di maschere del protocollo corrente.",
      "alternatives": "Potremmo aggiungere un modulo di segmentazione per ottenere le maschere direttamente dai video RGB, per esempio valutando SAM 2. Questo modello può seguire nel video un oggetto indicato inizialmente tramite punti o un rettangolo: resta quindi da definire come individuare gli oggetti e inizializzarlo. È un esempio da valutare, non un componente già scelto o integrato. L’implementazione verrà valutata dopo aver verificato il funzionamento della pipeline con le maschere VISOR già fornite per EPIC-KITCHENS. Fonte: https://github.com/facebookresearch/sam2",
      "improve": "Verificare bordi e contaminazioni preservando parti sottili; confrontare la pulizia sullo sviluppo.",
      "editedAt": "2026-11-14T16:27:40.065Z"
    },
    {
      "id": "B03",
      "title": "Feature d’aspetto",
      "x": 580,
      "y": 280,
      "group": "tracking",
      "review": "Descrizione modificata · evidenze da verificare",
      "summary": "Un estrattore visivo rappresenta l’aspetto della maschera RGB dell'oggetto in questione.",
      "sources": [
        "INTEGRAZIONE_BASELINE_REALE_20261113.md",
        "Whareformer-repo/src/feature_extraction/datasets/epic_dataset.py",
        "Whareformer-repo/src/feature_extraction/utils/common.py"
      ],
      "verified": "14 novembre 2026 · verifica documentale, nessuna nuova run",
      "failure": "Oggetti diversi possono avere aspetto simile. Occlusioni e cambi di vista alterano il segnale.",
      "contract": "Replica di Whareformer. Modifiche a questo putno non sono nello scope del nsotro lavoro.",
      "role": "Produce una degli elementi di input chiave di Whareformer: l'aspetto dell'oggetto nel frame, che viene confrontato con la memoria d’aspetto delle tracce salvate.",
      "state": "Replica di Whareformer.",
      "evidence": "Replica di Whareformer. Modifiche a questo putno non sono nello scope del nsotro lavoro.",
      "why": "Replica di Whareformer. Modifiche a questo putno non sono nello scope del nsotro lavoro.",
      "alternatives": "Replica di Whareformer. Modifiche a questo putno non sono nello scope del nsotro lavoro.",
      "improve": "Replica di Whareformer. Modifiche a questo putno non sono nello scope del nsotro lavoro.",
      "editedAt": "2026-11-14T16:37:55.227Z"
    },
    {
      "id": "B04",
      "title": "Stima geometria 3D · DA / MoGE",
      "x": 310,
      "y": 50,
      "group": "shape",
      "review": "Descrizione modificata · evidenze da verificare",
      "summary": "Dal frame RGB stimiamo la posizione nello spazio delle superfici visibili. Questa stima ci permette di ricavare una nuvola di punti 3D per ogni oggetto individuato dalla maschera.\nStiamo usando sia MoGE che DA, per valutare qual è migliore.",
      "sources": [
        "ROADMAP_CICLO_GEOMETRICO.md"
      ],
      "role": "La funzione di questo step è indicare quanto ogni pixel e ogni parte della scena è distante dalla camera, aka la profondità.\n- DA produce una mappa di profondità del frame; le profondità vengono convertite in punti 3D usando i parametri della camera.\n- MoGE produce una mappa di punti 3D e una propria maschera di validità.",
      "state": "Entrambe le alternative sono state eseguite sulle immagini di testing. I risultati non hanno ancora decretato un vincitore, perciò al momento li stiamo tenendo entrambi.",
      "evidence": "[spiega quali sono i limiti di MoGE]\n[Spiega quali sono i limiti di DA]\n\nLa posizione dei punti è stimata rispetto alla camera e può contenere errori: da una singola immagine non conosciamo direttamente le superfici nascoste.",
      "why": "Perchè nel paper Whareformer viene usato [...], mentre nel paper SuperFlex viene usato [...].\nEssendo entrambe soluzioni apparentemente valide, abbiamo deciso che l'AB testing fosse l'alternativa migliore.",
      "alternatives": "-",
      "improve": "-",
      "contract": "-",
      "failure": "Le porzioni nascoste delle superfici oggetto di analisi non sono osservate direttamente e sono quindi stimate. Le stime però possono variare con la vista o avere errori di scala. Dobbiamo valutare quale sorgente produca geometrie più utili al sistema completo.",
      "editedAt": "2026-11-14T17:19:27.077Z"
    },
    {
      "id": "B05",
      "title": "Nuvola di punti dell’oggetto",
      "x": 580,
      "y": 50,
      "group": "shape",
      "review": "Descrizione modificata · evidenze da verificare",
      "summary": "Il blocco riceve la stima geometrica del frame prodotta da DA o MoGE e la maschera VISOR dell’oggetto. Usa la maschera per selezionare i punti 3D validi appartenenti all’oggetto e produce una nuvola di punti, che viene fornita a SuperFlex.",
      "sources": [
        "ROADMAP_CICLO_GEOMETRICO.md"
      ],
      "role": "DA (o MoGE) elabora il frame RGB e produce una stima di geometria 3D per i pixel. Usiamo la maschera 2D dell’oggetto per conservare solo i punti corrispondenti alla sua superficie visibile.",
      "state": "Il blocco è implementato e testato: riusciamo a estrarre la nuvola del singolo oggetto sia con DA sia con MoGE e a passarla a SuperFlex. Entrambe le sorgenti restano in valutazione. ",
      "evidence": "La qualità e la coerenza delle nuvole tra viste diverse sono ancora da verificare in modo sufficiente per la fusione e il tracking.",
      "why": "Replica del paper [...].",
      "alternatives": "Replica del paper [...].",
      "improve": "Replica del paper [...]. Out of target per il progetto corrente.",
      "contract": "Replica del paper [...].",
      "failure": "Una maschera imprecisa potrebbe non includere tutti e solo i punti dell’oggetto. Errori di profondità, occlusioni e superfici poco visibili possono produrre nuvole incomplete o deformate. Una singola vista difficilmente mostra tutto l’oggetto.\nInoltre, due nuvole dello stesso oggetto non sono automaticamente allineate tra loro.",
      "editedAt": "2026-11-14T17:27:42.483Z"
    },
    {
      "id": "B06",
      "title": "SuperFlex",
      "x": 850,
      "y": 50,
      "group": "shape",
      "review": "Descrizione modificata · evidenze da verificare",
      "summary": "SuperFlex rappresenta la forma 3D dell’oggetto partendo da una nuvola di punti usando un insieme di primitive geometriche.",
      "sources": [
        "ROADMAP_CICLO_GEOMETRICO.md"
      ],
      "role": "Riceve una nuvola di punti e stima la forma dell'oggetto 3D tramite superquadriche, che sono forme geometriche flessibili che, combinate, approssimano la superficie dell’oggetto. Per limitare il problema delle viste parziali, naturali visto l'input frame by frame della camera, il modello può anche prevedere parti non visibili dell'oggetto a partire dalla vista parziale.",
      "state": "Step implementato nella pipeline. Risultati in linea con il paper originale.",
      "evidence": "La disponibilità di una nuvola non garantisce sempre una forma utilizzabile.",
      "why": "Usare Superflex crediamo aumenti il potenzila einformativo di una immagine RGB nel contesto di Whareformer.",
      "alternatives": "Tra le alternative considerate risulta Superdec, versione precedente di questo paper e superata sulle performance da Superflex. Altre alternative, da valutare indipendentemente da risultato del nostro progetto, sono [citare alternative valide per implementare il 3D in Whareformer: fare ricerca approfondita]",
      "improve": "In caso di viste parziali, e conseguenti nuvole di punti parziali, il completamento della nuvola di punti è una previsione e può essere sbagliata. Dobbiamo verificare quanto la forma sia stabile tra viste e quanto sia effettivanemtne utile al tracking.",
      "contract": "I punti devono essere preparati e normalizzati secondo il procedimento previsto per il modello; la trasformazione va conservata per interpretare il risultato.",
      "failure": "Da completare",
      "editedAt": "2026-11-14T17:35:56.378Z"
    },
    {
      "id": "B07",
      "title": "Forma 3D · superquadriche e descrittore",
      "x": 1120,
      "y": 50,
      "group": "shape",
      "review": "Scheda da compilare",
      "summary": "Blocco dell’architettura obiettivo. Dettagli da revisionare.",
      "sources": [
        "ROADMAP_CICLO_GEOMETRICO.md"
      ]
    },
    {
      "id": "B08",
      "title": "Profondità baseline allineata alla scena",
      "x": 310,
      "y": 530,
      "group": "tracking",
      "review": "Scheda da compilare",
      "summary": "Blocco dell’architettura obiettivo. Dettagli da revisionare.",
      "sources": [
        "ROADMAP_CICLO_GEOMETRICO.md"
      ]
    },
    {
      "id": "B09",
      "title": "Intrinseci, posa camera e ricostruzione scena",
      "x": 40,
      "y": 530,
      "group": "input",
      "review": "Scheda da compilare",
      "summary": "Blocco dell’architettura obiettivo. Dettagli da revisionare.",
      "sources": [
        "ROADMAP_CICLO_GEOMETRICO.md"
      ]
    },
    {
      "id": "B10",
      "title": "Posizione 3D · pipeline Whareformer",
      "x": 580,
      "y": 530,
      "group": "tracking",
      "review": "Scheda da compilare",
      "summary": "Blocco dell’architettura obiettivo. Dettagli da revisionare.",
      "sources": [
        "ROADMAP_CICLO_GEOMETRICO.md"
      ]
    },
    {
      "id": "B11",
      "title": "Osservazione corrente · forma, aspetto, posizione",
      "x": 850,
      "y": 280,
      "group": "tracking",
      "review": "Scheda da compilare",
      "summary": "Blocco dell’architettura obiettivo. Dettagli da revisionare.",
      "sources": [
        "ROADMAP_CICLO_GEOMETRICO.md"
      ]
    },
    {
      "id": "B12",
      "title": "Whareformer + adattatore · confronto e associazione",
      "x": 1120,
      "y": 280,
      "group": "tracking",
      "review": "Scheda da compilare",
      "summary": "Blocco dell’architettura obiettivo. Dettagli da revisionare.",
      "sources": [
        "ROADMAP_CICLO_GEOMETRICO.md"
      ]
    },
    {
      "id": "B13",
      "title": "Memoria precedente delle tracce",
      "x": 1120,
      "y": 530,
      "group": "memory",
      "review": "Scheda da compilare",
      "summary": "Blocco dell’architettura obiettivo. Dettagli da revisionare.",
      "sources": [
        "ROADMAP_CICLO_GEOMETRICO.md"
      ]
    },
    {
      "id": "B14",
      "title": "Associata a una traccia esistente?",
      "x": 1390,
      "y": 280,
      "group": "tracking",
      "review": "Scheda da compilare",
      "summary": "Blocco dell’architettura obiettivo. Dettagli da revisionare.",
      "sources": [
        "ROADMAP_CICLO_GEOMETRICO.md"
      ]
    },
    {
      "id": "B15",
      "title": "Aggiorna posizione e aspetto",
      "x": 1390,
      "y": 50,
      "group": "memory",
      "review": "Scheda da compilare",
      "summary": "Blocco dell’architettura obiettivo. Dettagli da revisionare.",
      "sources": [
        "ROADMAP_CICLO_GEOMETRICO.md"
      ]
    },
    {
      "id": "B16",
      "title": "Aggiorna geometria e ricostruisci forma",
      "x": 1660,
      "y": 50,
      "group": "memory",
      "review": "Scheda da compilare",
      "summary": "Blocco dell’architettura obiettivo. Dettagli da revisionare.",
      "sources": [
        "ROADMAP_CICLO_GEOMETRICO.md"
      ]
    },
    {
      "id": "B17",
      "title": "Crea una nuova traccia",
      "x": 1660,
      "y": 490,
      "group": "tracking",
      "review": "Scheda da compilare",
      "summary": "Blocco dell’architettura obiettivo. Dettagli da revisionare.",
      "sources": [
        "ROADMAP_CICLO_GEOMETRICO.md"
      ]
    },
    {
      "id": "B18",
      "title": "Inizializza posizione, aspetto e geometria",
      "x": 1660,
      "y": 710,
      "group": "memory",
      "review": "Scheda da compilare",
      "summary": "Blocco dell’architettura obiettivo. Dettagli da revisionare.",
      "sources": [
        "ROADMAP_CICLO_GEOMETRICO.md"
      ]
    },
    {
      "id": "B19",
      "title": "Memoria aggiornata",
      "x": 1390,
      "y": 710,
      "group": "memory",
      "review": "Scheda da compilare",
      "summary": "Blocco dell’architettura obiettivo. Dettagli da revisionare.",
      "sources": [
        "ROADMAP_CICLO_GEOMETRICO.md"
      ]
    }
  ],
  "edges": [
    {
      "id": "E01",
      "from": "B01",
      "to": "B02",
      "title": "RGB · frame t → Maschere 2D · VISOR",
      "label": "input fornito",
      "type": "data",
      "review": "Descrizione modificata · evidenze da verificare",
      "summary": "Semplicemente associa l’RGB alla maschera VISOR fornita. Al momento non rappresenta un segmentatore eseguito sull’immagine.",
      "sources": [
        "INTEGRAZIONE_BASELINE_REALE_20261113.md",
        "Whareformer-repo/src/feature_extraction/datasets/epic_dataset.py",
        "Whareformer-repo/src/feature_extraction/utils/common.py"
      ],
      "verified": "14 novembre 2026 · verifica documentale, nessuna nuova run",
      "failure": "Incongruenze tra RGB e maschere.",
      "contract": "-",
      "role": "Associa l’RGB alla maschera VISOR fornita.",
      "state": "Percorso presente nel codice EPIC originale (paper: [...]) e negli input precalcolati della baseline.",
      "evidence": "Verifica documentale/codice locale; nessuna nuova estrazione per la mappa. Al momento è una semplice associazione immagine-maschera, niente di più.",
      "why": "In virtù del fatto che stiamo usando un dataset in cui le maschere degli oggetti rappresentati nelle immagini RGB sono già fornite, e non vanno estratte dall'immagine.",
      "alternatives": "Nessuna alternativa necessaria per il semplice trasferimento.",
      "improve": "Uno step successivo è rendere possibile prendere come input immagini generiche. In questo caso va implementato [un sistema per estrarre le maschere dalle immagini, e questo step non sarebbe più un semplice \"trovare le corrispondenze\", ma estrarre le maschere dall'immagine RGB grezza]",
      "editedAt": "2026-11-14T16:32:48.162Z"
    },
    {
      "id": "E02",
      "from": "B01",
      "to": "B03",
      "title": "RGB · frame t → Feature d’aspetto",
      "label": "pixel RGB",
      "type": "data",
      "review": "Descrizione modificata · evidenze da verificare",
      "summary": "Fornisce colore e texture alla feature d'aspetto. COmpleta l'input fornito dalla mascher, che invece fornisce [...].",
      "sources": [
        "INTEGRAZIONE_BASELINE_REALE_20261113.md",
        "Whareformer-repo/src/feature_extraction/datasets/epic_dataset.py",
        "Whareformer-repo/src/feature_extraction/utils/common.py"
      ],
      "verified": "14 novembre 2026 · verifica documentale, nessuna nuova run",
      "failure": "Replica di [nome paper]. Percorso presente nel codice EPIC originale e negli input precalcolati della baseline. Out of scope con il contributo di questo lavoro.",
      "contract": "Replica di [nome paper]. Percorso presente nel codice EPIC originale e negli input precalcolati della baseline. Out of scope con il contributo di questo lavoro.",
      "role": "Fornisce i pixel RGB per estrarre l’aspetto.",
      "state": "Replica di [nome paper]. Percorso presente nel codice EPIC originale e negli input precalcolati della baseline.",
      "evidence": "Replica di [nome paper]. Percorso presente nel codice EPIC originale e negli input precalcolati della baseline.",
      "why": "Arricchisce l'aspetto rispetto alla sola maschera 2D",
      "alternatives": "Replica di [nome paper]. Percorso presente nel codice EPIC originale e negli input precalcolati della baseline.",
      "improve": "Replica di [nome paper]. Percorso presente nel codice EPIC originale e negli input precalcolati della baseline. Out of scope con il contributo di questo lavoro.",
      "editedAt": "2026-11-14T16:46:22.852Z"
    },
    {
      "id": "E03",
      "from": "B02",
      "to": "B03",
      "title": "Maschere 2D · VISOR → Feature d’aspetto",
      "label": "regione oggetto",
      "type": "data",
      "review": "Descrizione modificata · evidenze da verificare",
      "summary": "Maschera e bounding box delimitano quale sezione dell'imamgine di input rappresenta l'oggetto anaizzato.",
      "sources": [
        "INTEGRAZIONE_BASELINE_REALE_20261113.md",
        "Whareformer-repo/src/feature_extraction/datasets/epic_dataset.py",
        "Whareformer-repo/src/feature_extraction/utils/common.py"
      ],
      "verified": "14 novembre 2026 · verifica documentale, nessuna nuova run",
      "failure": "Replica di Whareformer. Modifiche a questo putno non sono nello scope del nsotro lavoro.",
      "contract": "Replica di Whareformer. Modifiche a questo putno non sono nello scope del nsotro lavoro.",
      "role": "Usare la maschera estratta come componente della feature d'aspetto (uno degli elementi di confronto del modello Whareformer)",
      "state": "Replica di Whareformer. Modifiche a questo putno non sono nello scope del nsotro lavoro.",
      "evidence": "Replica di Whareformer. Modifiche a questo putno non sono nello scope del nsotro lavoro.",
      "why": "Replica di Whareformer. Modifiche a questo putno non sono nello scope del nsotro lavoro.",
      "alternatives": "Replica di Whareformer. Modifiche a questo putno non sono nello scope del nsotro lavoro.",
      "improve": "Verificare corrispondenza frame/detection e risoluzioni nei casi dubbi.",
      "editedAt": "2026-11-14T16:50:43.265Z"
    },
    {
      "id": "E04",
      "from": "B01",
      "to": "B04",
      "title": "RGB · frame t → Stima geometria 3D · DA / MoGE",
      "label": "",
      "type": "data",
      "review": "Scheda da compilare",
      "summary": "Trasferimento di dati o controllo: dettaglio da revisionare.",
      "sources": [
        "MAPPA_FLUSSO_SISTEMA.md"
      ]
    },
    {
      "id": "E05",
      "from": "B04",
      "to": "B05",
      "title": "Stima geometria 3D · DA / MoGE → Nuvola di punti dell’oggetto",
      "label": "",
      "type": "data",
      "review": "Scheda da compilare",
      "summary": "Trasferimento di dati o controllo: dettaglio da revisionare.",
      "sources": [
        "MAPPA_FLUSSO_SISTEMA.md"
      ]
    },
    {
      "id": "E06",
      "from": "B02",
      "to": "B05",
      "title": "Maschere 2D · VISOR → Nuvola di punti dell’oggetto",
      "label": "",
      "type": "data",
      "review": "Scheda da compilare",
      "summary": "Trasferimento di dati o controllo: dettaglio da revisionare.",
      "sources": [
        "MAPPA_FLUSSO_SISTEMA.md"
      ]
    },
    {
      "id": "E07",
      "from": "B09",
      "to": "B05",
      "title": "Intrinseci, posa camera e ricostruzione scena → Nuvola di punti dell’oggetto",
      "label": "intrinseci per DA",
      "type": "data",
      "review": "Scheda da compilare",
      "summary": "Trasferimento di dati o controllo: dettaglio da revisionare.",
      "sources": [
        "MAPPA_FLUSSO_SISTEMA.md"
      ]
    },
    {
      "id": "E08",
      "from": "B05",
      "to": "B06",
      "title": "Nuvola di punti dell’oggetto → SuperFlex",
      "label": "",
      "type": "data",
      "review": "Scheda da compilare",
      "summary": "Trasferimento di dati o controllo: dettaglio da revisionare.",
      "sources": [
        "MAPPA_FLUSSO_SISTEMA.md"
      ]
    },
    {
      "id": "E09",
      "from": "B06",
      "to": "B07",
      "title": "SuperFlex → Forma 3D · superquadriche e descrittore",
      "label": "",
      "type": "data",
      "review": "Scheda da compilare",
      "summary": "Trasferimento di dati o controllo: dettaglio da revisionare.",
      "sources": [
        "MAPPA_FLUSSO_SISTEMA.md"
      ]
    },
    {
      "id": "E10",
      "from": "B07",
      "to": "B11",
      "title": "Forma 3D · superquadriche e descrittore → Osservazione corrente · forma, aspetto, posizione",
      "label": "",
      "type": "data",
      "review": "Scheda da compilare",
      "summary": "Trasferimento di dati o controllo: dettaglio da revisionare.",
      "sources": [
        "MAPPA_FLUSSO_SISTEMA.md"
      ]
    },
    {
      "id": "E11",
      "from": "B03",
      "to": "B11",
      "title": "Feature d’aspetto → Osservazione corrente · forma, aspetto, posizione",
      "label": "",
      "type": "data",
      "review": "Scheda da compilare",
      "summary": "Trasferimento di dati o controllo: dettaglio da revisionare.",
      "sources": [
        "MAPPA_FLUSSO_SISTEMA.md"
      ]
    },
    {
      "id": "E12",
      "from": "B01",
      "to": "B08",
      "title": "RGB · frame t → Profondità baseline allineata alla scena",
      "label": "",
      "type": "data",
      "review": "Scheda da compilare",
      "summary": "Trasferimento di dati o controllo: dettaglio da revisionare.",
      "sources": [
        "MAPPA_FLUSSO_SISTEMA.md"
      ]
    },
    {
      "id": "E13",
      "from": "B09",
      "to": "B08",
      "title": "Intrinseci, posa camera e ricostruzione scena → Profondità baseline allineata alla scena",
      "label": "scena",
      "type": "data",
      "review": "Scheda da compilare",
      "summary": "Trasferimento di dati o controllo: dettaglio da revisionare.",
      "sources": [
        "MAPPA_FLUSSO_SISTEMA.md"
      ]
    },
    {
      "id": "E14",
      "from": "B08",
      "to": "B10",
      "title": "Profondità baseline allineata alla scena → Posizione 3D · pipeline Whareformer",
      "label": "",
      "type": "data",
      "review": "Scheda da compilare",
      "summary": "Trasferimento di dati o controllo: dettaglio da revisionare.",
      "sources": [
        "MAPPA_FLUSSO_SISTEMA.md"
      ]
    },
    {
      "id": "E15",
      "from": "B02",
      "to": "B10",
      "title": "Maschere 2D · VISOR → Posizione 3D · pipeline Whareformer",
      "label": "",
      "type": "data",
      "review": "Scheda da compilare",
      "summary": "Trasferimento di dati o controllo: dettaglio da revisionare.",
      "sources": [
        "MAPPA_FLUSSO_SISTEMA.md"
      ]
    },
    {
      "id": "E16",
      "from": "B09",
      "to": "B10",
      "title": "Intrinseci, posa camera e ricostruzione scena → Posizione 3D · pipeline Whareformer",
      "label": "",
      "type": "data",
      "review": "Scheda da compilare",
      "summary": "Trasferimento di dati o controllo: dettaglio da revisionare.",
      "sources": [
        "MAPPA_FLUSSO_SISTEMA.md"
      ]
    },
    {
      "id": "E17",
      "from": "B10",
      "to": "B11",
      "title": "Posizione 3D · pipeline Whareformer → Osservazione corrente · forma, aspetto, posizione",
      "label": "",
      "type": "data",
      "review": "Scheda da compilare",
      "summary": "Trasferimento di dati o controllo: dettaglio da revisionare.",
      "sources": [
        "MAPPA_FLUSSO_SISTEMA.md"
      ]
    },
    {
      "id": "E18",
      "from": "B11",
      "to": "B12",
      "title": "Osservazione corrente · forma, aspetto, posizione → Whareformer + adattatore · confronto e associazione",
      "label": "",
      "type": "data",
      "review": "Scheda da compilare",
      "summary": "Trasferimento di dati o controllo: dettaglio da revisionare.",
      "sources": [
        "MAPPA_FLUSSO_SISTEMA.md"
      ]
    },
    {
      "id": "E19",
      "from": "B13",
      "to": "B12",
      "title": "Memoria precedente delle tracce → Whareformer + adattatore · confronto e associazione",
      "label": "",
      "type": "data",
      "review": "Scheda da compilare",
      "summary": "Trasferimento di dati o controllo: dettaglio da revisionare.",
      "sources": [
        "MAPPA_FLUSSO_SISTEMA.md"
      ]
    },
    {
      "id": "E20",
      "from": "B12",
      "to": "B14",
      "title": "Whareformer + adattatore · confronto e associazione → Associata a una traccia esistente?",
      "label": "",
      "type": "control",
      "review": "Scheda da compilare",
      "summary": "Trasferimento di dati o controllo: dettaglio da revisionare.",
      "sources": [
        "MAPPA_FLUSSO_SISTEMA.md"
      ]
    },
    {
      "id": "E21",
      "from": "B14",
      "to": "B15",
      "title": "Associata a una traccia esistente? → Aggiorna posizione e aspetto",
      "label": "Sì",
      "type": "control",
      "review": "Scheda da compilare",
      "summary": "Trasferimento di dati o controllo: dettaglio da revisionare.",
      "sources": [
        "MAPPA_FLUSSO_SISTEMA.md"
      ]
    },
    {
      "id": "E22",
      "from": "B14",
      "to": "B16",
      "title": "Associata a una traccia esistente? → Aggiorna geometria e ricostruisci forma",
      "label": "Sì",
      "type": "control",
      "review": "Scheda da compilare",
      "summary": "Trasferimento di dati o controllo: dettaglio da revisionare.",
      "sources": [
        "MAPPA_FLUSSO_SISTEMA.md"
      ]
    },
    {
      "id": "E23",
      "from": "B14",
      "to": "B17",
      "title": "Associata a una traccia esistente? → Crea una nuova traccia",
      "label": "No",
      "type": "control",
      "review": "Scheda da compilare",
      "summary": "Trasferimento di dati o controllo: dettaglio da revisionare.",
      "sources": [
        "MAPPA_FLUSSO_SISTEMA.md"
      ]
    },
    {
      "id": "E24",
      "from": "B17",
      "to": "B18",
      "title": "Crea una nuova traccia → Inizializza posizione, aspetto e geometria",
      "label": "",
      "type": "control",
      "review": "Scheda da compilare",
      "summary": "Trasferimento di dati o controllo: dettaglio da revisionare.",
      "sources": [
        "MAPPA_FLUSSO_SISTEMA.md"
      ]
    },
    {
      "id": "E25",
      "from": "B11",
      "to": "B18",
      "title": "Osservazione corrente · forma, aspetto, posizione → Inizializza posizione, aspetto e geometria",
      "label": "",
      "type": "data",
      "review": "Scheda da compilare",
      "summary": "Trasferimento di dati o controllo: dettaglio da revisionare.",
      "sources": [
        "MAPPA_FLUSSO_SISTEMA.md"
      ]
    },
    {
      "id": "E26",
      "from": "B05",
      "to": "B18",
      "title": "Nuvola di punti dell’oggetto → Inizializza posizione, aspetto e geometria",
      "label": "",
      "type": "data",
      "review": "Scheda da compilare",
      "summary": "Trasferimento di dati o controllo: dettaglio da revisionare.",
      "sources": [
        "MAPPA_FLUSSO_SISTEMA.md"
      ]
    },
    {
      "id": "E27",
      "from": "B11",
      "to": "B15",
      "title": "Osservazione corrente · forma, aspetto, posizione → Aggiorna posizione e aspetto",
      "label": "",
      "type": "data",
      "review": "Scheda da compilare",
      "summary": "Trasferimento di dati o controllo: dettaglio da revisionare.",
      "sources": [
        "MAPPA_FLUSSO_SISTEMA.md"
      ]
    },
    {
      "id": "E28",
      "from": "B13",
      "to": "B15",
      "title": "Memoria precedente delle tracce → Aggiorna posizione e aspetto",
      "label": "",
      "type": "data",
      "review": "Scheda da compilare",
      "summary": "Trasferimento di dati o controllo: dettaglio da revisionare.",
      "sources": [
        "MAPPA_FLUSSO_SISTEMA.md"
      ]
    },
    {
      "id": "E29",
      "from": "B05",
      "to": "B16",
      "title": "Nuvola di punti dell’oggetto → Aggiorna geometria e ricostruisci forma",
      "label": "punti osservati",
      "type": "data",
      "review": "Scheda da compilare",
      "summary": "Trasferimento di dati o controllo: dettaglio da revisionare.",
      "sources": [
        "MAPPA_FLUSSO_SISTEMA.md"
      ]
    },
    {
      "id": "E30",
      "from": "B13",
      "to": "B16",
      "title": "Memoria precedente delle tracce → Aggiorna geometria e ricostruisci forma",
      "label": "",
      "type": "data",
      "review": "Scheda da compilare",
      "summary": "Trasferimento di dati o controllo: dettaglio da revisionare.",
      "sources": [
        "MAPPA_FLUSSO_SISTEMA.md"
      ]
    },
    {
      "id": "E31",
      "from": "B15",
      "to": "B19",
      "title": "Aggiorna posizione e aspetto → Memoria aggiornata",
      "label": "",
      "type": "data",
      "review": "Scheda da compilare",
      "summary": "Trasferimento di dati o controllo: dettaglio da revisionare.",
      "sources": [
        "MAPPA_FLUSSO_SISTEMA.md"
      ]
    },
    {
      "id": "E32",
      "from": "B16",
      "to": "B19",
      "title": "Aggiorna geometria e ricostruisci forma → Memoria aggiornata",
      "label": "",
      "type": "data",
      "review": "Scheda da compilare",
      "summary": "Trasferimento di dati o controllo: dettaglio da revisionare.",
      "sources": [
        "MAPPA_FLUSSO_SISTEMA.md"
      ]
    },
    {
      "id": "E33",
      "from": "B18",
      "to": "B19",
      "title": "Inizializza posizione, aspetto e geometria → Memoria aggiornata",
      "label": "",
      "type": "data",
      "review": "Scheda da compilare",
      "summary": "Trasferimento di dati o controllo: dettaglio da revisionare.",
      "sources": [
        "MAPPA_FLUSSO_SISTEMA.md"
      ]
    },
    {
      "id": "E34",
      "from": "B19",
      "to": "B13",
      "title": "Memoria aggiornata → Memoria precedente delle tracce",
      "label": "Frame successivo",
      "type": "temporal",
      "review": "Scheda da compilare",
      "summary": "Trasferimento di dati o controllo: dettaglio da revisionare.",
      "sources": [
        "MAPPA_FLUSSO_SISTEMA.md"
      ]
    }
  ]
};
