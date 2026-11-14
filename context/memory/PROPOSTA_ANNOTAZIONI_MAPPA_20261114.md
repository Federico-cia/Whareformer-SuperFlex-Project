# Proposta di annotazione della mappa — 14 novembre 2026

**Sviluppo successivo richiesto da Marco:** prima versione HTML in [mappa_interattiva/index.html](mappa_interattiva/index.html), con schede modificabili ed export/import. Prime sei schede proposte; compilazione completa ancora aperta. [Guida](mappa_interattiva/LEGGIMI.md). Le indicazioni sotto sul supporto sono ora tradotte in un prototipo, i contenuti restano da revisionare.

Richiesta di Marco: revisionare le due immagini aggiornate della mappa e organizzare, per ogni riquadro e collegamento, stato, alternative, motivazioni e miglioramenti. Questa è una proposta di documentazione; non adotta nuove varianti scientifiche, non modifica il diagramma esterno e non certifica risultati ulteriori.

## Correzioni e leggibilità

1. Aggiungere «Immagine RGB - frame t» → «Feature d'aspetto»: la maschera seleziona i pixel RGB usati dall'estrattore.
2. Dal blocco «Intrinseci posa camera e ricostruzione scena» aggiungere il contributo degli intrinseci al ramo DA che costruisce «Nuvola di punti dell'oggetto». MoGE può produrre direttamente punti; non rendere la posa camera una dipendenza obbligatoria della nuvola camera-frame.
3. Precisare «Profondità derivata dall'RGB» come «Profondità baseline allineata alla scena». L'allineamento dipende anche dalla ricostruzione scena: esplicitarlo con freccia dal blocco camera/scena alla profondità, oppure nella scheda del ramo se si mantiene una sola freccia aggregata verso posizione. Nel secondo caso dichiarare che la freccia riassume il preprocessing baseline. Modello/configurazione nella scheda, senza appesantire il nome.
4. «Insieme di superquadriche» → «Forma 3D»: unire in «Forma 3D: insieme di superquadriche» se la seconda casella è solo un nome riassuntivo; se rappresenta il descrittore realmente confrontato, chiamarla «Descrittore di forma 3D» e documentare superficie campionata, normalizzazione e D2/spettro effettivamente usati. La CLI del bundle corrente ammette D2, non automaticamente tutti i descrittori supportati dall'API.
5. Mostrare che «Inizializza posizione aspetto e geometria» riceve i dati dell'osservazione corrente e la nuvola corrente, oltre all'ID creato da «Crea una nuova traccia». Il segnale di creazione da solo non contiene quei dati. Analogamente «Aggiorna posizione e aspetto» legge feature/posizione correnti e memoria precedente. Per evitare molte frecce lunghe usare richiami ripetuti etichettati con lo stesso nome della sorgente, spiegati nella legenda.
6. Accorciare «Aggiorna geometria allineamento e accumulo dei punti → nuova inferenza SuperFlex» in «Aggiorna geometria e ricostruisci forma», mantenendo nella scheda registrazione, ammissione, accumulo e SuperFlex dopo ogni aggiornamento ammesso. Conservare nella mappa una nota su rifiuti/errori e ultima forma valida.
7. Spostare «Frame successivo» sulla freccia «Memoria aggiornata» → «Memoria precedente delle tracce». La lettura della memoria precedente alimenta il matching del frame corrente. Nota globale: tutte le associazioni del frame prima degli aggiornamenti.
8. «Maschere 2D»: annotare VISOR nelle prove attuali; il collegamento dall'RGB è concettuale, non certifica un segmentatore eseguito. Una legenda «input forniti/precalcolati» evita di presentare l'intero sistema come inferenza RGB strettamente online.

## Organizzazione proposta

Mappa principale con nomi brevi, frecce leggibili, SÌ/NO e poche regole essenziali. Schede associate ai riquadri e alle frecce tramite titolo/identificativo stabile. Commenti o note servono a navigare; la fonte completa deve essere un documento aggiornabile e collegato alle evidenze. Non duplicare tutta la storia scientifica sul diagramma.

Distinguere flussi di dati e segnali di controllo tramite tratto/etichetta; riservare una rappresentazione riconoscibile al passaggio temporale della memoria. Il colore da solo non basta. Identificare per sorgente/destinazione i collegamenti, anche se non si mostrano tutti gli ID nel diagramma.

## Scheda per ogni riquadro

- **Funzione e contratto:** cosa riceve, cosa produce, unità/riferimento e perimetro per frame/oggetto/track.
- **Stato attuale:** implementazione disponibile/parziale/assente separata dall'evidenza (controlli locali, dati reali, efficacia finale). Precisare provenienza: baseline degli autori, nostro contributo o dato fornito.
- **Scelte e alternative:** per ciascuna distinguere discussa teoricamente, approvata per confronto, implementata, eseguita e risultato. Includere proposte da valutare e opzioni superate con motivo documentato, senza inventare motivazioni retrospettive.
- **Motivazione:** problema affrontato, ragione documentata della scelta e compromessi. Se è una raccomandazione corrente anziché il motivo storico, dichiararlo.
- **Miglioramento e criterio:** prossimo confronto utile, misura di qualità e risultato che giustificherebbe il cambiamento. Nessuna promessa di superiorità.
- **Evidenza, limiti e dipendenze:** report/codice/configurazione, data dell'ultima verifica, fallimenti/mancanti e prossimo elemento necessario. Tempi/memoria solo quando misurati.

## Scheda per ogni collegamento

- **Che cosa passa:** dato concreto o segnale; da quale osservazione/versione/track deriva.
- **Quando e con quali convenzioni:** prima/dopo matching, frame di disponibilità, camera/scena/riferimento d'oggetto, scala e mapping di ID/pixel quando pertinenti.
- **Stato e verifica:** collegamento esistente, controlli effettivi e limiti; non confondere un file disponibile con correttezza del contenuto.
- **Perché serve:** relazione necessaria tra sorgente e destinazione.
- **Errori e miglioramenti:** comportamento con dato assente/incompatibile, controllo prossimo utile e alternative solo se esiste una reale scelta. Per semplici trasferimenti le alternative possono essere «non applicabile».
- **Evidenza:** riferimento al contratto o resoconto, evitando di duplicare la scheda della sorgente.

## Esempio di riquadro: aggiornamento geometrico

**Casella nelle immagini:** «Aggiorna geometria allineamento e accumulo dei punti → nuova inferenza SuperFlex».

**Funzione:** osservazione associata più stato precedente → candidata registrazione, ammissione, punti accumulati e nuova forma. I punti predetti da SuperFlex non diventano osservazioni.

**Stato:** candidato PCA/multistart + ICP e collegamento al coordinatore/SuperFlex differita implementati. Nel job CPU 763323 risultano 12 inizializzazioni (tre osservazioni iniziali ripetute in quattro rappresentazioni), 12 rifiuti e nessuna fusione; i tentativi successivi corrispondono a tre osservazioni, non dodici prove indipendenti. Non è dimostrata efficacia dell'accumulo reale.

**Perché:** viste camera-frame di oggetti mobili richiedono allineamento prima della fusione; l'ammissione e la conservazione dello stato valido evitano di sostituire la memoria con una proposta non affidabile. Questa è la motivazione del requisito, non una prova che il registratore attuale sia sufficiente.

**Alternative:** confronto RGB→3D/RANSAC/ICP e FPFH/RANSAC/ICP, pulizia e rigido/similarità limitata approvati per selezione/calibrazione; non trattare l'approvazione come esecuzione. Il risultato negativo PCA/ICP non valuta automaticamente FPFH.

**Miglioramento/criterio:** verificare posa e coerenza su controlli noti e viste escluse, quindi utilità nel tracking. Non selezionare dal solo residuo o tasso di aggiornamenti accettati.

**Fonti:** [COLLEGAMENTO_ACCUMULO_20261114.md](COLLEGAMENTO_ACCUMULO_20261114.md), [SUPERFLEX_DIFFERITA_20261114.md](SUPERFLEX_DIFFERITA_20261114.md), [RIPRESA_HPC_20261114.md](RIPRESA_HPC_20261114.md), piano corrente [ROADMAP_CICLO_GEOMETRICO.md](ROADMAP_CICLO_GEOMETRICO.md). Stati HPC quelli documentati, non ricontrollati durante questa revisione.

## Esempio di collegamento: nuvola verso aggiornamento geometrico

**Sorgente → destinazione:** «Nuvola di punti dell'oggetto» → «Aggiorna geometria allineamento e accumulo dei punti → nuova inferenza SuperFlex».

**Contenuto:** punti osservati della detection corrente, chiave dell'osservazione, sorgente DA/MoGE e provenienza. Il candidato attuale usa punti camera-frame e controlla convenzioni/versioni; colori/pixel non vanno dichiarati ingressi del registratore attuale senza verificarne l'uso.

**Momento:** la nuvola è costruita prima del matching; l'uso per aggiornare la memoria è successivo all'associazione della detection a un ID effettivo. La trasformazione candidata deve portare i punti nel riferimento della track. Posizione XYZ dell'oggetto non equivale a posa 6D.

**Motivo:** l'associazione assegna la traccia destinataria, ma non fornisce i punti da fondere.

**Fallimenti:** nuvola assente/invalida o registrazione rifiutata preservano la geometria valida; nessun punto completato reinserito nell'accumulo.

**Miglioramento:** verificare mapping pixel→punto e texture per sperimentare registrazione assistita da RGB, come da piano approvato. Il collegamento non dimostra da solo la qualità della registrazione.

## Ordine proposto di compilazione

Prima camera/maschere/RGB, aspetto e posizione della baseline; poi nuvole, SuperFlex e descrittore; infine matching, inizializzazione/aggiornamenti e memoria. Per ogni blocco compilare insieme le frecce entranti. Le schede devono essere concise, verificabili e aggiornabili; campi privi di evidenza restano esplicitamente da verificare.
