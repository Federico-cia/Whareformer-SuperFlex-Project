# Commenti per la struttura approvata — proposta da revisionare

Nessun testo è stato applicato alla mappa. I riferimenti R e C identificano solo questa bozza.

## Criteri di compilazione

Tutti i nove campi sono compilati. Per le nuove schede, Perché questa scelta, Evidenze e limiti, Alternative e loro stato e Possibili miglioramenti valgono «-» se non riportati diversamente. I testi di riquadri e collegamenti rimasti equivalenti sono preservati; la loro revisione resta una fase successiva. Le nuove formulazioni non certificano nuovi risultati.

## Riquadri conservati o già proposti

- R01 · Frame RGB: scheda manuale B01 conservata.
- R02 · Maschere VISOR: scheda manuale B02 conservata.
- R03 · Camera e scena 3D: bozza B09 già presentata, ancora da confermare.
- R12 · Geometria stimata da RGB: scheda manuale B04 conservata.
- R13 · Punti visibili dell’oggetto: scheda manuale B05 conservata.
- R14 · Ricostruzione SuperFlex: scheda manuale B06 conservata.
- R15 · Descrittore di forma: scheda manuale B07 conservata.
- R16 · Osservazione corrente: bozza B11 già presentata, ancora da confermare.
- R23 · Traccia esistente?: scheda manuale B14 conservata.
- R25 · Aggiorna la traccia: bozza B15 già presentata, ancora da confermare.
- R39 · Memoria aggiornata per il frame successivo: bozza B19 già presentata, ancora da confermare.

## Nuovi riquadri e contenuti ridistribuiti

### R04 · Ritaglio dell’oggetto

- **In una frase:** Prepara l’immagine dell’oggetto per l’estrazione visiva.
- **Funzione e dati scambiati:** Usa rettangolo e maschera per ritagliare l’oggetto dal frame e preparare l’ingresso dell’estrattore.
- **Stato attuale:** Procedura originale di Whareformer; nelle prove sono riusate le feature ufficiali.
- **Evidenze e limiti:** -
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** Frame, maschera e rettangolo devono descrivere la stessa osservazione.
- **Possibili errori:** Un ritaglio errato può escludere parti dell’oggetto o includere elementi estranei.

### R05 · Estrazione visiva

- **In una frase:** Trasforma il ritaglio dell’oggetto in caratteristiche numeriche.
- **Funzione e dati scambiati:** DINOv2 preaddestrato produce un vettore che descrive l’aspetto visivo dell’oggetto.
- **Stato attuale:** Procedura originale di Whareformer; nelle prove sono riusate le feature ufficiali.
- **Evidenze e limiti:** -
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** Pesi e preparazione dell’immagine devono essere compatibili con la baseline.
- **Possibili errori:** Occlusioni e cambi di vista possono alterare la rappresentazione; oggetti diversi possono apparire simili.

### R06 · Riduzione dimensionale

- **In una frase:** Riduce la dimensione del vettore visivo.
- **Funzione e dati scambiati:** Normalizza il vettore, applica la riduzione lineare PCA già prevista e normalizza il risultato. La trasformazione non viene stimata sul frame corrente.
- **Stato attuale:** Procedura originale di Whareformer; nelle prove sono riusate le feature ufficiali.
- **Evidenze e limiti:** Il codice originale applica una PCA stimata sui dati di training; la provenienza dell’asset ufficiale da riusare resta da verificare.
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** Trasformazione e dimensione finale devono corrispondere a quelle attese da Whareformer.
- **Possibili errori:** Una trasformazione diversa da quella della baseline rende incompatibili i descrittori.

### R07 · Descrittore d’aspetto

- **In una frase:** Rende disponibile il descrittore d’aspetto dell’osservazione.
- **Funzione e dati scambiati:** Collega il vettore finale al corretto oggetto e frame, così da poterlo confrontare con la memoria visiva delle tracce.
- **Stato attuale:** Procedura originale di Whareformer; nelle prove sono riusate le feature ufficiali.
- **Evidenze e limiti:** -
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** Identificativo e ordine del vettore devono coincidere con quelli dell’osservazione.
- **Possibili errori:** Un vettore attribuito all’oggetto sbagliato altera il confronto visivo.

### R08 · Stima della profondità

- **In una frase:** Stima la profondità dei pixel a partire dall’immagine.
- **Funzione e dati scambiati:** Il modello di profondità della baseline riceve il frame RGB e produce una mappa di profondità, prima dell’allineamento alla scena.
- **Stato attuale:** Procedura originale di Whareformer; nelle prove sono riusate le posizioni ufficiali.
- **Evidenze e limiti:** -
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** Mappa e immagine devono avere coordinate compatibili.
- **Possibili errori:** Errori di profondità si propagano alla successiva stima della posizione.

### R09 · Allineamento alla scena

- **In una frase:** Rende la profondità predetta coerente con la ricostruzione della scena.
- **Funzione e dati scambiati:** Adatta scala e scostamento della profondità alla vista della scena ricostruita, usando regioni valide esterne agli oggetti mascherati.
- **Stato attuale:** Procedura originale di Whareformer; nelle prove sono riusate le posizioni ufficiali.
- **Evidenze e limiti:** -
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** Vista della scena, posa, maschere e profondità devono riferirsi allo stesso frame.
- **Possibili errori:** Una scena incompleta, una posa errata o pochi punti validi possono rendere inaffidabile l’allineamento.

### R10 · Calcolo della posizione

- **In una frase:** Calcola un punto rappresentativo della posizione dell’oggetto nella scena.
- **Funzione e dati scambiati:** Combina centro del rettangolo e profondità mediana nella maschera; usa gli intrinseci per passare al riferimento camera e la posa per passare alla scena.
- **Stato attuale:** Procedura originale di Whareformer; nelle prove sono riusate le posizioni ufficiali.
- **Evidenze e limiti:** -
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** Rettangolo, maschera, profondità e camera devono essere coerenti per osservazione e risoluzione.
- **Possibili errori:** Profondità o posa errate spostano la posizione stimata.

### R11 · Posizione 3D nella scena

- **In una frase:** Rende disponibili le tre coordinate spaziali dell’oggetto.
- **Funzione e dati scambiati:** Collega la posizione stimata alla corretta osservazione, nello stesso riferimento usato dalle tracce.
- **Stato attuale:** Procedura originale di Whareformer; nelle prove sono riusate le posizioni ufficiali.
- **Evidenze e limiti:** -
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** Le posizioni confrontate devono condividere riferimento e scala.
- **Possibili errori:** Il punto stimato non fornisce orientamento, dimensioni o centro geometrico certificato dell’oggetto.

### R17 · Memoria precedente

- **In una frase:** Conserva l’aspetto e la posizione delle tracce prima del frame corrente.
- **Funzione e dati scambiati:** Mantiene le rappresentazioni e la storia previste da Whareformer per confrontare le osservazioni con gli oggetti già ricordati.
- **Stato attuale:** Passaggio implementato nel ciclo corrente; le reti restano congelate.
- **Evidenze e limiti:** -
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** Ogni memoria deve restare associata al proprio ID di traccia.
- **Possibili errori:** Associazioni errate precedenti possono contaminare i confronti futuri.

### R18 · Memoria precedente

- **In una frase:** Conserva la geometria disponibile delle tracce prima del frame corrente.
- **Funzione e dati scambiati:** Mantiene punti ammessi e ultima ricostruzione riuscita. Le forme delle singole osservazioni costituiscono una memoria distinta, usata come riserva se manca una ricostruzione dell’accumulo utilizzabile.
- **Stato attuale:** Passaggio implementato nel ciclo corrente; le reti restano congelate.
- **Evidenze e limiti:** -
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** Traccia, sorgente, riferimento e versioni devono essere espliciti; tutti i confronti del frame leggono lo stato geometrico precedente.
- **Possibili errori:** Una memoria contaminata o una forma precedente non più rappresentativa possono rendere fuorviante il confronto.

### R19 · Punteggi di Whareformer

- **In una frase:** Assegna un punteggio alle possibili associazioni usando aspetto e posizione.
- **Funzione e dati scambiati:** Whareformer confronta l’osservazione con le tracce candidate e produce i punteggi originali, compresa l’opzione “nuova traccia”.
- **Stato attuale:** Passaggio implementato nel ciclo corrente; le reti restano congelate.
- **Evidenze e limiti:** -
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** L’ordine dei punteggi deve corrispondere agli ID delle tracce; la forma non è un ingresso nativo di questa rete.
- **Possibili errori:** Aspetto simile o posizione imprecisa possono favorire la traccia sbagliata.

### R20 · Distanza tra le forme

- **In una frase:** Misura quanto la forma osservata assomigli alle forme ricordate.
- **Funzione e dati scambiati:** Confronta i descrittori D2 validi: distanze minori indicano forme più simili. Usa la ricostruzione accumulata quando disponibile, altrimenti le forme singole previste dalla memoria.
- **Stato attuale:** Passaggio implementato nel ciclo corrente; le reti restano congelate.
- **Evidenze e limiti:** -
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** Verificare se la distanza aggiunge informazione utile rispetto ad aspetto e posizione.
- **Coerenza dei dati:** Sorgente, normalizzazione e definizione del descrittore devono essere compatibili. Un confronto mancante deve restare esplicitamente assente.
- **Possibili errori:** Forme simili, viste parziali o ricostruzioni instabili possono produrre distanze poco informative.

### R21 · Correzione esterna dei punteggi

- **In una frase:** Modifica dall’esterno i punteggi di Whareformer usando la distanza di forma.
- **Funzione e dati scambiati:** Applica: punteggio corretto = punteggio originale + peso × (distanza neutra − distanza di forma). Corregge soltanto i confronti geometrici validi con tracce esistenti.
- **Stato attuale:** Passaggio implementato nel ciclo corrente; le reti restano congelate.
- **Evidenze e limiti:** I controlli a contributo geometrico nullo hanno preservato la baseline; nelle configurazioni della campagna conclusa le assegnazioni non sono cambiate.
- **Perché questa scelta:** Permette di sperimentare il contributo della forma mantenendo congelata la rete originale.
- **Alternative e loro stato:** Fusione con parametri appresi e adattamento di Whareformer sono percorsi da confrontare; non sono componenti eseguiti in questa mappa.
- **Possibili miglioramenti:** Definire distanza e calibrazione su dati di sviluppo; analizzare perché le correzioni non abbiano cambiato le associazioni.
- **Coerenza dei dati:** L’opzione “nuova traccia” e i confronti mancanti non ricevono una correzione diretta; le loro probabilità possono comunque cambiare.
- **Possibili errori:** Parametri non calibrati o geometria disponibile solo per alcune tracce possono sbilanciare la decisione.

### R22 · Assegnazione originale

- **In una frase:** Converte i punteggi in associazioni tra osservazioni e tracce.
- **Funzione e dati scambiati:** Trasforma i punteggi corretti in probabilità e applica l’assegnazione originale: ogni osservazione riceve una traccia esistente oppure l’esito “nuova traccia”. Una traccia esistente può ricevere al massimo un’osservazione del frame.
- **Stato attuale:** Passaggio implementato nel ciclo corrente; le reti restano congelate.
- **Evidenze e limiti:** -
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** Righe e colonne devono corrispondere alle osservazioni e agli ID effettivi.
- **Possibili errori:** L’esito è una predizione e può frammentare un’identità o unire oggetti diversi.

### R24 · Crea e inizializza la traccia

- **In una frase:** Crea una traccia e inizializza la sua memoria visiva e spaziale.
- **Funzione e dati scambiati:** Assegna un nuovo ID e inserisce aspetto, posizione e prima osservazione secondo la procedura originale. La geometria viene gestita separatamente.
- **Stato attuale:** Passaggio implementato nel ciclo corrente; le reti restano congelate.
- **Evidenze e limiti:** -
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** L’ID deve essere univoco e collegato all’osservazione che lo ha generato.
- **Possibili errori:** Una nuova traccia può corrispondere a un oggetto già visto ma non riconosciuto.

### R26 · Osservazione associata

- **In una frase:** Collega l’osservazione all’ID realmente assegnato dal tracker.
- **Funzione e dati scambiati:** Raccoglie l’esito definitivo dopo la creazione o l’aggiornamento della traccia e identifica la memoria destinataria dell’eventuale aggiornamento geometrico.
- **Stato attuale:** Passaggio implementato nel ciclo corrente; le reti restano congelate.
- **Evidenze e limiti:** -
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** Il collegamento deve usare l’ID effettivo, non il solo indice della colonna dei punteggi.
- **Possibili errori:** Un ID errato invia la geometria alla traccia sbagliata.

### R27 · Stato baseline aggiornato

- **In una frase:** Conserva lo stato visivo e spaziale già aggiornato.
- **Funzione e dati scambiati:** Mantiene memorie, ultima posizione e storia prodotte dal tracker, indipendentemente dall’esito del successivo aggiornamento geometrico.
- **Stato attuale:** Passaggio implementato nel ciclo corrente; le reti restano congelate.
- **Evidenze e limiti:** -
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** Stato e aggiornamento devono riferirsi alla stessa traccia e allo stesso frame.
- **Possibili errori:** Il rifiuto geometrico non corregge un’associazione baseline eventualmente errata.

### R28 · Nuvola corrente valida?

- **In una frase:** Verifica che sia disponibile una nuvola utilizzabile per l’osservazione associata.
- **Funzione e dati scambiati:** Controlla disponibilità, validità dei punti e coerenza della provenienza. Se manca un input utilizzabile non viene aggiornata la memoria dei punti.
- **Stato attuale:** Passaggio implementato nel percorso con accumulo; i criteri di ammissione restano provvisori.
- **Evidenze e limiti:** -
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** Nuvola, sorgente e osservazione devono corrispondere; i punti devono provenire dalle superfici visibili stimate.
- **Possibili errori:** Validità dei dati e correttezza geometrica sono diverse: punti formalmente validi possono essere inaccurati.

### R29 · Punti già in memoria?

- **In una frase:** Distingue la prima geometria valida da un aggiornamento tra viste.
- **Funzione e dati scambiati:** Controlla se la traccia possiede già una memoria di punti: in assenza la inizializza, altrimenti tenta l’allineamento della nuova nuvola.
- **Stato attuale:** Passaggio implementato nel percorso con accumulo; i criteri di ammissione restano provvisori.
- **Evidenze e limiti:** -
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** La verifica riguarda la memoria dei punti della traccia assegnata, non la sola esistenza dell’ID.
- **Possibili errori:** Una traccia può esistere da più frame senza avere ancora una nuvola valida.

### R30 · Inizializza i punti

- **In una frase:** Crea la memoria geometrica dalla prima nuvola valida della traccia.
- **Funzione e dati scambiati:** Conserva un campione dei punti osservati, la loro provenienza e il riferimento della prima vista ammessa. Questa operazione non fonde viste diverse.
- **Stato attuale:** Passaggio implementato nel percorso con accumulo; i criteri di ammissione restano provvisori.
- **Evidenze e limiti:** -
- **Perché questa scelta:** Consente di inizializzare la geometria anche dopo la creazione della traccia.
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** Riferimento, sorgente e scala vengono registrati per gli aggiornamenti successivi.
- **Possibili errori:** Una prima nuvola contaminata o di scala inaccurata può compromettere gli aggiornamenti futuri.

### R31 · Allinea la nuova nuvola

- **In una frase:** Cerca come portare la nuova nuvola nel riferimento dei punti già ricordati.
- **Funzione e dati scambiati:** Prova diversi allineamenti iniziali e li affina stimando rotazione e traslazione. La scala non viene modificata.
- **Stato attuale:** Passaggio implementato nel percorso con accumulo; i criteri di ammissione restano provvisori.
- **Evidenze e limiti:** -
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** Discutere e validare il metodo di allineamento su fusioni corrette ed errate.
- **Coerenza dei dati:** Le due nuvole devono avere scala compatibile e appartenere alla stessa traccia.
- **Possibili errori:** Viste parziali, simmetrie e differenze di scala possono rendere l’allineamento errato o ambiguo.

### R32 · Fusione ammessa?

- **In una frase:** Decide se l’allineamento è abbastanza affidabile per ammettere i nuovi punti.
- **Funzione e dati scambiati:** Controlla supporto, residui e ambiguità della trasformazione. Supporto e residui sono valutati su punti separati da quelli usati per stimare l’allineamento.
- **Stato attuale:** Passaggio implementato nel percorso con accumulo; i criteri di ammissione restano provvisori.
- **Evidenze e limiti:** Nelle prove sono avvenute fusioni ammesse e rifiuti; l’accuratezza fisica delle fusioni non è certificata.
- **Perché questa scelta:** -
- **Alternative e loro stato:** Rivedere criteri e soglie oppure conservare forme separate sono alternative discusse, non una politica definitiva già scelta.
- **Possibili miglioramenti:** Concordare i criteri con il compagno e verificare sia fusioni errate ammesse sia fusioni utili respinte.
- **Coerenza dei dati:** La decisione riguarda la fusione geometrica; non annulla l’associazione alla traccia.
- **Possibili errori:** Controlli permissivi possono contaminare la memoria; controlli severi possono respingere viste utili.

### R33 · Conserva punti e forma

- **In una frase:** Mantiene invariati i punti accumulati e la loro ultima ricostruzione riuscita.
- **Funzione e dati scambiati:** Quando manca una nuvola utilizzabile o l’allineamento è respinto, conserva lo stato geometrico precedente senza annullare il tracking.
- **Stato attuale:** Passaggio implementato nel percorso con accumulo; i criteri di ammissione restano provvisori.
- **Evidenze e limiti:** -
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** La conservazione riguarda l’accumulo e la sua ricostruzione; la memoria distinta delle forme singole segue il proprio aggiornamento.
- **Possibili errori:** Rifiuti ripetuti possono lasciare la geometria poco rappresentativa delle nuove viste.

### R34 · Unisci i punti osservati

- **In una frase:** Integra nella memoria i punti delle viste ammesse.
- **Funzione e dati scambiati:** Trasforma i nuovi punti nel riferimento della memoria e ne conserva campioni insieme alle viste ammesse precedenti, rispettando i limiti di memoria configurati.
- **Stato attuale:** Passaggio implementato nel percorso con accumulo; i criteri di ammissione restano provvisori.
- **Evidenze e limiti:** -
- **Perché questa scelta:** Conservare viste complementari può aumentare la copertura delle superfici dell’oggetto.
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** Si aggiungono soltanto punti osservati stimati, mai le superfici completate da SuperFlex.
- **Possibili errori:** Una trasformazione scorretta può deformare la memoria anche quando supera i controlli.

### R35 · Ricostruisci con SuperFlex

- **In una frase:** Ricostruisce la forma dai punti inizializzati o aggiornati.
- **Funzione e dati scambiati:** Prepara la nuvola, applica SuperFlex preaddestrato e conserva la ricostruzione con i dati necessari a ricondurla alla versione dei punti di origine.
- **Stato attuale:** Passaggio implementato nel percorso con accumulo; i criteri di ammissione restano provvisori.
- **Evidenze e limiti:** -
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** Richiesta, traccia e versione della nuvola devono corrispondere; il completamento non rientra nei punti osservati.
- **Possibili errori:** La ricostruzione può fallire o produrre una forma inaccurata, soprattutto con nuvole parziali o contaminate.

### R36 · Ricostruzione riuscita?

- **In una frase:** Verifica se la ricostruzione ha restituito un risultato utilizzabile.
- **Funzione e dati scambiati:** Distingue un risultato riuscito da un fallimento dichiarato e controlla che appartenga alla richiesta e alla versione di punti previste.
- **Stato attuale:** Passaggio implementato nel percorso con accumulo; i criteri di ammissione restano provvisori.
- **Evidenze e limiti:** -
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** Un esito tecnico positivo non certifica la correttezza fisica della forma.
- **Possibili errori:** Risultati mancanti o incoerenti possono bloccare il replay; non equivalgono a un normale fallimento dichiarato.

### R37 · Aggiorna forma e descrittore

- **In una frase:** Rende disponibili la nuova forma e il suo descrittore per i confronti futuri.
- **Funzione e dati scambiati:** Associa alla traccia la ricostruzione riuscita e il descrittore ricavato dalla superficie, registrando la versione dei punti che li ha generati.
- **Stato attuale:** Passaggio implementato nel percorso con accumulo; i criteri di ammissione restano provvisori.
- **Evidenze e limiti:** -
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** La nuova forma viene pubblicata dopo l’associazione corrente e non ne modifica retroattivamente l’esito.
- **Possibili errori:** Una ricostruzione riuscita ma inaccurata può rendere fuorvianti i successivi confronti.

### R38 · Mantieni l’ultima forma valida

- **In una frase:** Conserva l’ultima forma riuscita quando la nuova ricostruzione fallisce.
- **Funzione e dati scambiati:** Mantiene la forma precedente, se presente, insieme ai punti appena ammessi. Se non esiste una forma precedente, la ricostruzione dell’accumulo resta indisponibile.
- **Stato attuale:** Passaggio implementato nel percorso con accumulo; i criteri di ammissione restano provvisori.
- **Evidenze e limiti:** -
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** Versione dei punti aggiornati e versione della forma precedente devono restare distinte.
- **Possibili errori:** La forma conservata può non rappresentare tutte le superfici presenti nella nuova memoria di punti.

## Collegamenti conservati o già proposti

- C10 · Geometria stimata da RGB → Punti visibili dell’oggetto: E05 (testi manuali conservati).
- C11 · Punti visibili dell’oggetto → Ricostruzione SuperFlex: E08 (testi manuali conservati).
- C12 · Ricostruzione SuperFlex → Descrittore di forma: E09 (testi manuali conservati).
- C13 · Descrittore d’aspetto → Osservazione corrente: E11 (testi manuali conservati).
- C14 · Posizione 3D nella scena → Osservazione corrente: E17 (bozza già presentata).
- C15 · Descrittore di forma → Osservazione corrente: E10 (testi conservati; completamento del solo segnaposto nelle alternative).
- C23 · Assegnazione originale → Traccia esistente?: E20 (testi manuali conservati).
- C24 · Traccia esistente? → Crea e inizializza la traccia: E23 (testi manuali conservati).
- C25 · Traccia esistente? → Aggiorna la traccia: E21 (testi manuali conservati).
- C44 · Stato baseline aggiornato → Memoria aggiornata per il frame successivo: E31 (bozza già presentata).

## Nuovi collegamenti e contenuti ridistribuiti

### C01 · Dati d’ingresso forniti → Ritaglio dell’oggetto

- **In una frase:** Fornisce immagine e selezione dell’oggetto al ritaglio.
- **Funzione e dati scambiati:** Il frame contiene l’aspetto visivo; maschera e rettangolo indicano quale regione appartiene all’oggetto da estrarre.
- **Stato attuale:** Procedura originale di Whareformer; nelle prove sono riusate le feature ufficiali.
- **Evidenze e limiti:** -
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** RGB, maschera e rettangolo devono riferirsi allo stesso oggetto e frame.
- **Possibili errori:** Un disallineamento seleziona pixel non pertinenti.

### C02 · Dati d’ingresso forniti → Stima della profondità

- **In una frase:** Fornisce il frame da cui stimare la profondità.
- **Funzione e dati scambiati:** Il modello di profondità usa i pixel RGB per stimare la distanza delle superfici visibili; maschere e camera/scena restano disponibili ai successivi passaggi del ramo.
- **Stato attuale:** Procedura originale di Whareformer; nelle prove sono riusate le posizioni ufficiali.
- **Evidenze e limiti:** -
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** Il frame deve corrispondere agli altri dati del ramo posizione.
- **Possibili errori:** Un frame errato rende incoerenti profondità e annotazioni.

### C03 · Dati d’ingresso forniti → Geometria stimata da RGB

- **In una frase:** Fornisce il frame alla stima geometrica.
- **Funzione e dati scambiati:** Depth Anything o MoGE ricavano la geometria dai pixel RGB; gli altri dati forniti vengono usati soltanto dove richiesti, come gli intrinseci nel ramo Depth Anything.
- **Stato attuale:** Dipendenza rappresentata nella struttura approvata del metodo corrente.
- **Evidenze e limiti:** -
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** Frame e parametri eventualmente usati devono avere risoluzione e convenzioni compatibili.
- **Possibili errori:** Input incoerenti producono una geometria non riferibile all’osservazione.

### C04 · Ritaglio dell’oggetto → Estrazione visiva

- **In una frase:** Fornisce all’estrattore il ritaglio preparato dell’oggetto.
- **Funzione e dati scambiati:** Il ritaglio concentra l’informazione visiva sulla regione da descrivere ed è l’immagine effettivamente ricevuta da DINOv2.
- **Stato attuale:** Procedura originale di Whareformer; nelle prove sono riusate le feature ufficiali.
- **Evidenze e limiti:** -
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** Dimensioni e normalizzazione devono seguire la preparazione prevista dalla baseline.
- **Possibili errori:** Una preparazione incompatibile altera le caratteristiche estratte.

### C05 · Estrazione visiva → Riduzione dimensionale

- **In una frase:** Fornisce il vettore visivo da ridurre.
- **Funzione e dati scambiati:** DINOv2 produce una rappresentazione numerica sulla quale può operare la trasformazione PCA; non vengono ridotti direttamente i pixel.
- **Stato attuale:** Procedura originale di Whareformer; nelle prove sono riusate le feature ufficiali.
- **Evidenze e limiti:** -
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** Dimensione e preparazione del vettore devono corrispondere alla PCA prevista.
- **Possibili errori:** Un vettore incompatibile rende invalida la riduzione.

### C06 · Riduzione dimensionale → Descrittore d’aspetto

- **In una frase:** Fornisce il vettore finale usato come descrittore d’aspetto.
- **Funzione e dati scambiati:** La trasformazione produce la dimensione e la normalizzazione richieste per confrontare l’osservazione con la memoria visiva.
- **Stato attuale:** Procedura originale di Whareformer; nelle prove sono riusate le feature ufficiali.
- **Evidenze e limiti:** -
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** Descrittore corrente e descrittori ricordati devono essere compatibili.
- **Possibili errori:** Trasformazioni diverse rendono il confronto poco interpretabile.

### C07 · Stima della profondità → Allineamento alla scena

- **In una frase:** Fornisce la profondità predetta da adattare alla scena.
- **Funzione e dati scambiati:** La mappa stimata dall’immagine deve essere resa coerente con la profondità della scena prima di usarla per le posizioni 3D.
- **Stato attuale:** Procedura originale di Whareformer; nelle prove sono riusate le posizioni ufficiali.
- **Evidenze e limiti:** -
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** Le due profondità devono descrivere la stessa vista.
- **Possibili errori:** Una vista incoerente altera scala e scostamento stimati.

### C08 · Allineamento alla scena → Calcolo della posizione

- **In una frase:** Fornisce la profondità coerente con la scena per localizzare l’oggetto.
- **Funzione e dati scambiati:** I valori allineati permettono di ricavare la profondità pertinente alla maschera e di trasformarla in una posizione nel riferimento della scena.
- **Stato attuale:** Procedura originale di Whareformer; nelle prove sono riusate le posizioni ufficiali.
- **Evidenze e limiti:** -
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** Maschera, rettangolo, camera e profondità devono essere compatibili.
- **Possibili errori:** Valori di sfondo o riferimenti incoerenti spostano la posizione stimata.

### C09 · Calcolo della posizione → Posizione 3D nella scena

- **In una frase:** Fornisce le coordinate calcolate della posizione.
- **Funzione e dati scambiati:** Il calcolo produce il punto 3D che viene conservato come segnale spaziale dell’osservazione.
- **Stato attuale:** Procedura originale di Whareformer; nelle prove sono riusate le posizioni ufficiali.
- **Evidenze e limiti:** -
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** Le coordinate devono mantenere identificativo e riferimento della scena.
- **Possibili errori:** Uno scambio di osservazione o riferimento rende errata la posizione.

### C16 · Osservazione corrente → Punteggi di Whareformer

- **In una frase:** Fornisce aspetto e posizione dell’oggetto al modello originale.
- **Funzione e dati scambiati:** Questi due segnali sono gli ingressi utilizzati da Whareformer per confrontare l’osservazione con le tracce; la forma segue il ramo esterno.
- **Stato attuale:** Dipendenza rappresentata nella struttura approvata del metodo corrente.
- **Evidenze e limiti:** -
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** -
- **Possibili errori:** -

### C17 · Osservazione corrente → Distanza tra le forme

- **In una frase:** Fornisce la forma corrente da confrontare.
- **Funzione e dati scambiati:** Il descrittore dell’oggetto osservato è uno dei due termini del confronto con le forme delle tracce; se assente, il confronto geometrico resta indisponibile.
- **Stato attuale:** Dipendenza rappresentata nella struttura approvata del metodo corrente.
- **Evidenze e limiti:** -
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** Descrittore e osservazione devono coincidere; l’assenza deve essere esplicita.
- **Possibili errori:** Un descrittore errato può favorire la traccia sbagliata.

### C18 · Memoria precedente → Punteggi di Whareformer

- **In una frase:** Fornisce i ricordi visivi e spaziali delle tracce candidate.
- **Funzione e dati scambiati:** Whareformer ha bisogno delle rappresentazioni già memorizzate per attribuire un punteggio al possibile collegamento con ciascuna traccia.
- **Stato attuale:** Dipendenza rappresentata nella struttura approvata del metodo corrente.
- **Evidenze e limiti:** -
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** Ordine delle memorie e colonne dei punteggi devono corrispondere agli ID effettivi.
- **Possibili errori:** -

### C19 · Memoria precedente → Distanza tra le forme

- **In una frase:** Fornisce le forme ricordate da confrontare con quella corrente.
- **Funzione e dati scambiati:** Le forme associate agli ID delle tracce costituiscono il secondo termine del confronto geometrico.
- **Stato attuale:** Dipendenza rappresentata nella struttura approvata del metodo corrente.
- **Evidenze e limiti:** -
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** Tutti i confronti del frame devono usare lo stato geometrico precedente.
- **Possibili errori:** Memorie aggiornate troppo presto o assegnate male possono falsare il confronto.

### C20 · Punteggi di Whareformer → Correzione esterna dei punteggi

- **In una frase:** Fornisce i punteggi originali su cui applicare la correzione.
- **Funzione e dati scambiati:** La geometria modifica una decisione già valutata da aspetto e posizione: i punteggi originali sono il punto di partenza della combinazione.
- **Stato attuale:** Dipendenza rappresentata nella struttura approvata del metodo corrente.
- **Evidenze e limiti:** -
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** -
- **Possibili errori:** -

### C21 · Distanza tra le forme → Correzione esterna dei punteggi

- **In una frase:** Fornisce la distanza e la disponibilità del confronto geometrico.
- **Funzione e dati scambiati:** Distanza e indicazione di validità determinano se e quanto correggere il punteggio della traccia; un confronto mancante non vale distanza zero.
- **Stato attuale:** Dipendenza rappresentata nella struttura approvata del metodo corrente.
- **Evidenze e limiti:** -
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** Ogni distanza deve corrispondere alla corretta coppia osservazione-traccia.
- **Possibili errori:** Confondere assenza e somiglianza può sbilanciare i punteggi.

### C22 · Correzione esterna dei punteggi → Assegnazione originale

- **In una frase:** Fornisce i punteggi corretti alla procedura originale di assegnazione.
- **Funzione e dati scambiati:** Le probabilità e la scelta finale devono riflettere il contributo geometrico già applicato; per questo la correzione precede l’assegnazione.
- **Stato attuale:** Dipendenza rappresentata nella struttura approvata del metodo corrente.
- **Evidenze e limiti:** -
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** Mantiene ordine delle colonne e opzione “nuova traccia”.
- **Possibili errori:** -

### C26 · Crea e inizializza la traccia → Osservazione associata

- **In una frase:** Fornisce l’ID appena creato e l’osservazione che lo inizializza.
- **Funzione e dati scambiati:** La geometria deve essere collegata all’identificativo effettivamente creato dal tracker, disponibile dopo la creazione della traccia.
- **Stato attuale:** Dipendenza rappresentata nella struttura approvata del metodo corrente.
- **Evidenze e limiti:** -
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** -
- **Possibili errori:** -

### C27 · Aggiorna la traccia → Osservazione associata

- **In una frase:** Fornisce l’ID della traccia esistente che ha ricevuto l’osservazione.
- **Funzione e dati scambiati:** L’aggiornamento identifica il destinatario effettivo del dato corrente, così da selezionare la corretta memoria geometrica.
- **Stato attuale:** Dipendenza rappresentata nella struttura approvata del metodo corrente.
- **Evidenze e limiti:** -
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** -
- **Possibili errori:** -

### C28 · Osservazione associata → Stato baseline aggiornato

- **In una frase:** Rende disponibile lo stato baseline già creato o aggiornato.
- **Funzione e dati scambiati:** L’associazione definitiva consente di conservare aspetto e posizione della traccia, indipendentemente dal risultato della geometria.
- **Stato attuale:** Dipendenza rappresentata nella struttura approvata del metodo corrente.
- **Evidenze e limiti:** -
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** -
- **Possibili errori:** -

### C29 · Osservazione associata → Nuvola corrente valida?

- **In una frase:** Identifica la traccia destinataria dell’eventuale aggiornamento dei punti.
- **Funzione e dati scambiati:** Prima di usare una nuvola occorre collegarla all’ID realmente assegnato all’osservazione, anche quando la traccia è appena nata.
- **Stato attuale:** Dipendenza rappresentata nella struttura approvata del metodo corrente.
- **Evidenze e limiti:** -
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** -
- **Possibili errori:** -

### C30 · Punti visibili dell’oggetto → Nuvola corrente valida?

- **In una frase:** Fornisce i punti correnti da verificare per l’aggiornamento.
- **Funzione e dati scambiati:** L’accumulo richiede la nuvola delle superfici visibili dell’osservazione; il solo descrittore o la superficie completata non la sostituiscono.
- **Stato attuale:** Dipendenza rappresentata nella struttura approvata del metodo corrente.
- **Evidenze e limiti:** -
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** Sorgente, riferimento e provenienza devono essere dichiarati.
- **Possibili errori:** Usare punti completati introdurrebbe nella memoria superfici non osservate.

### C31 · Nuvola corrente valida? → Punti già in memoria? · Sì

- **In una frase:** Prosegue quando la nuvola corrente è utilizzabile.
- **Funzione e dati scambiati:** Un dato utilizzabile può inizializzare una memoria assente oppure aggiornare quella esistente; il controllo successivo distingue questi casi.
- **Stato attuale:** Dipendenza rappresentata nella struttura approvata del metodo corrente.
- **Evidenze e limiti:** -
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** -
- **Possibili errori:** -

### C32 · Memoria precedente → Punti già in memoria?

- **In una frase:** Fornisce lo stato precedente dei punti della traccia.
- **Funzione e dati scambiati:** La presenza o assenza di una nuvola già conservata determina se serve un allineamento oppure una prima inizializzazione.
- **Stato attuale:** Dipendenza rappresentata nella struttura approvata del metodo corrente.
- **Evidenze e limiti:** -
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** L’assenza di punti non va confusa con l’assenza della traccia.
- **Possibili errori:** -

### C33 · Punti già in memoria? → Inizializza i punti · No

- **In una frase:** Attiva l’inizializzazione quando mancano punti già ricordati.
- **Funzione e dati scambiati:** Senza una nuvola precedente non esiste una vista con cui fondere: la nuvola corrente diventa il primo riferimento geometrico.
- **Stato attuale:** Dipendenza rappresentata nella struttura approvata del metodo corrente.
- **Evidenze e limiti:** -
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** -
- **Possibili errori:** -

### C34 · Punti già in memoria? → Allinea la nuova nuvola · Sì

- **In una frase:** Attiva l’allineamento quando esiste una memoria di punti.
- **Funzione e dati scambiati:** Le due nuvole possono essere combinate soltanto dopo aver stimato la trasformazione che le esprime nello stesso riferimento.
- **Stato attuale:** Dipendenza rappresentata nella struttura approvata del metodo corrente.
- **Evidenze e limiti:** -
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** Il passaggio conserva sia la nuvola corrente sia quella precedente.
- **Possibili errori:** -

### C35 · Allinea la nuova nuvola → Fusione ammessa?

- **In una frase:** Fornisce la trasformazione candidata e le sue verifiche.
- **Funzione e dati scambiati:** La decisione di fusione richiede informazioni sulla sovrapposizione, sui residui e sull’ambiguità dell’allineamento, oltre alla trasformazione stessa.
- **Stato attuale:** Dipendenza rappresentata nella struttura approvata del metodo corrente.
- **Evidenze e limiti:** -
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** Verifiche e trasformazione devono riferirsi alle stesse nuvole.
- **Possibili errori:** Una trasformazione disponibile non è automaticamente una trasformazione affidabile.

### C36 · Nuvola corrente valida? → Conserva punti e forma · No

- **In una frase:** Mantiene l’accumulo precedente quando manca una nuvola utilizzabile.
- **Funzione e dati scambiati:** Senza nuovi punti affidabili non è possibile aggiornare l’accumulo; la traccia continua con lo stato geometrico già disponibile.
- **Stato attuale:** Dipendenza rappresentata nella struttura approvata del metodo corrente.
- **Evidenze e limiti:** -
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** -
- **Possibili errori:** -

### C37 · Fusione ammessa? → Conserva punti e forma · No

- **In una frase:** Mantiene l’accumulo precedente quando la fusione è respinta.
- **Funzione e dati scambiati:** Il rifiuto impedisce l’ingresso dei nuovi punti nella memoria, lasciando valida l’associazione e l’aggiornamento baseline.
- **Stato attuale:** Dipendenza rappresentata nella struttura approvata del metodo corrente.
- **Evidenze e limiti:** -
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** -
- **Possibili errori:** -

### C38 · Fusione ammessa? → Unisci i punti osservati · Sì

- **In una frase:** Autorizza l’inserimento dei punti dopo il superamento dei controlli.
- **Funzione e dati scambiati:** L’esito positivo permette di applicare la trasformazione approvata e unire campioni dei nuovi punti alla memoria.
- **Stato attuale:** Dipendenza rappresentata nella struttura approvata del metodo corrente.
- **Evidenze e limiti:** -
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** Approvazione e trasformazione devono appartenere allo stesso tentativo.
- **Possibili errori:** -

### C39 · Unisci i punti osservati → Ricostruisci con SuperFlex

- **In una frase:** Fornisce la memoria di punti aggiornata per ricostruire la forma.
- **Funzione e dati scambiati:** Le viste ammesse possono aggiungere superfici visibili: SuperFlex viene rieseguito per rappresentare la nuova versione dei punti.
- **Stato attuale:** Dipendenza rappresentata nella struttura approvata del metodo corrente.
- **Evidenze e limiti:** -
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** L’ingresso contiene punti osservati ammessi, non precedenti completamenti.
- **Possibili errori:** -

### C40 · Inizializza i punti → Ricostruisci con SuperFlex

- **In una frase:** Fornisce la prima memoria di punti da ricostruire.
- **Funzione e dati scambiati:** Anche senza fusione tra viste, la nuvola iniziale deve essere trasformata in una forma confrontabile nei frame futuri.
- **Stato attuale:** Dipendenza rappresentata nella struttura approvata del metodo corrente.
- **Evidenze e limiti:** -
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** -
- **Possibili errori:** -

### C41 · Ricostruisci con SuperFlex → Ricostruzione riuscita?

- **In una frase:** Fornisce il risultato della richiesta di ricostruzione.
- **Funzione e dati scambiati:** Prima di pubblicare una forma occorre sapere se la richiesta è riuscita e se il risultato corrisponde ai punti previsti.
- **Stato attuale:** Dipendenza rappresentata nella struttura approvata del metodo corrente.
- **Evidenze e limiti:** -
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** Richiesta, versione e artefatti devono corrispondere.
- **Possibili errori:** Un risultato assente o incoerente non va pubblicato come riuscito.

### C42 · Ricostruzione riuscita? → Aggiorna forma e descrittore · Sì

- **In una frase:** Pubblica la nuova forma quando la ricostruzione è riuscita.
- **Funzione e dati scambiati:** Un risultato utilizzabile può sostituire la forma precedente e fornire il descrittore aggiornato per le associazioni future.
- **Stato attuale:** Dipendenza rappresentata nella struttura approvata del metodo corrente.
- **Evidenze e limiti:** -
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** -
- **Possibili errori:** -

### C43 · Ricostruzione riuscita? → Mantieni l’ultima forma valida · No

- **In una frase:** Conserva la forma precedente dopo un fallimento dichiarato.
- **Funzione e dati scambiati:** La nuova inferenza non fornisce una forma utilizzabile: si mantiene l’ultima riuscita, senza annullare i punti già ammessi.
- **Stato attuale:** Dipendenza rappresentata nella struttura approvata del metodo corrente.
- **Evidenze e limiti:** -
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** Il passaggio non copre risultati mancanti o incoerenti ancora da gestire.
- **Possibili errori:** Confondere un fallimento dichiarato con un risultato irrisolto può nascondere un errore di esecuzione.

### C45 · Conserva punti e forma → Memoria aggiornata per il frame successivo

- **In una frase:** Trasmette lo stato dell’accumulo che non è stato modificato.
- **Funzione e dati scambiati:** La memoria futura deve conservare punti precedenti e loro ultima ricostruzione riuscita anche quando l’aggiornamento corrente non è ammesso.
- **Stato attuale:** Dipendenza rappresentata nella struttura approvata del metodo corrente.
- **Evidenze e limiti:** -
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** -
- **Possibili errori:** -

### C46 · Mantieni l’ultima forma valida → Memoria aggiornata per il frame successivo

- **In una frase:** Trasmette i punti aggiornati insieme alla forma precedente.
- **Funzione e dati scambiati:** Il fallimento della ricostruzione separa le due versioni: i punti sono nuovi, mentre la forma resta l’ultima riuscita.
- **Stato attuale:** Dipendenza rappresentata nella struttura approvata del metodo corrente.
- **Evidenze e limiti:** -
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** Versioni e istanti di punti e forma devono restare distinti.
- **Possibili errori:** La forma precedente non va presentata come ricostruita dai nuovi punti.

### C47 · Aggiorna forma e descrittore → Memoria aggiornata per il frame successivo

- **In una frase:** Trasmette la nuova forma con il suo descrittore e la versione d’origine.
- **Funzione e dati scambiati:** La ricostruzione riuscita deve essere conservata nella traccia per poter influenzare i confronti dei frame successivi.
- **Stato attuale:** Dipendenza rappresentata nella struttura approvata del metodo corrente.
- **Evidenze e limiti:** -
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** -
- **Possibili errori:** -

### C48 · Memoria aggiornata per il frame successivo → Memoria precedente

- **In una frase:** Rende lo stato visivo e spaziale aggiornato disponibile al frame successivo.
- **Funzione e dati scambiati:** La memoria risultante dal tracking corrente diventa il termine di confronto delle osservazioni future.
- **Stato attuale:** Dipendenza rappresentata nella struttura approvata del metodo corrente.
- **Evidenze e limiti:** -
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** L’ordine temporale deve avanzare; gli aggiornamenti non modificano associazioni già concluse.
- **Possibili errori:** -

### C49 · Memoria aggiornata per il frame successivo → Memoria precedente

- **In una frase:** Rende lo stato geometrico aggiornato disponibile al frame successivo.
- **Funzione e dati scambiati:** Punti e ultima forma valida passano ai confronti e agli aggiornamenti futuri soltanto dopo la gestione degli esiti del frame corrente.
- **Stato attuale:** Dipendenza rappresentata nella struttura approvata del metodo corrente.
- **Evidenze e limiti:** -
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** Tutte le osservazioni del nuovo frame leggono lo stesso stato geometrico precedente.
- **Possibili errori:** Un aggiornamento anticipato può introdurre dipendenze scorrette tra osservazioni dello stesso frame.

## Verifiche e limiti

Copertura: 39 riquadri e 49 collegamenti, con nove campi ciascuno. Per le schede non riscritte sono conservati i testi manuali oppure le precedenti bozze, con stato distinto. Codice consultato: estrazione EPIC, PCA originale, matcher/track originali; shape_adapter.py, geometry_matcher.py, frame_coordinator.py, cloud_updater.py, cloud_memory.py, deferred_superflex.py; shape_tools/memory.py e metrics.py. Nessuna nuova inferenza, esecuzione o validazione scientifica. File della mappa corrente non modificati.
