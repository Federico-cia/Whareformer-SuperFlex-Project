# Testi proposti per la mappa

**Esito successivo:** testi confermati da Marco e [applicati alla mappa](ESITO_APPLICAZIONE.md). La dicitura di bozza sotto conserva lo stato originario della proposta, ormai superato.

**Bozza non approvata e non applicata.** Venti schede di riquadro e ventidue di collegamento, comprese tutte le sei nuove frecce. Nove campi per scheda; «-» dove non occorre contenuto aggiuntivo. Schede e metadati sono separati: le date qui fuori dalle schede documentano la revisione.

## Precisazione rispetto alla proposta strutturale

Il codice del coordinatore richiede di risolvere le richieste SuperFlex pendenti prima del frame seguente. Per questo C43 propone **«Fallita»**, anziché «Non disponibile»: l’attesa mantiene la forma precedente, ma non permette ancora di avanzare. Un risultato incoerente è un errore, non un fallimento gestito da convertire silenziosamente in fallback. Nessun nodo o estremo viene cambiato. C49 mantiene il tipo temporale già usato dall’interfaccia.

## Indice

**Riquadri:** [R09](#r09) · [R12](#r12) · [R13](#r13) · [R14](#r14) · [R15](#r15) · [R18](#r18) · [R20](#r20) · [R21](#r21) · [R28](#r28) · [R29](#r29) · [R30](#r30) · [R31](#r31) · [R32](#r32) · [R33](#r33) · [R34](#r34) · [R35](#r35) · [R36](#r36) · [R37](#r37) · [R38](#r38) · [R39](#r39)

**Collegamenti:** [C03](#c03) · [C10](#c10) · [C11](#c11) · [C19](#c19) · [C30](#c30) · [C31](#c31) · [C32](#c32) · [C33](#c33) · [C35](#c35) · [C36](#c36) · [C37](#c37) · [C38](#c38) · [C39](#c39) · [C43](#c43) · [C45](#c45) · [C49](#c49) · [C50](#c50) · [C51](#c51) · [C52](#c52) · [C53](#c53) · [C54](#c54) · [C55](#c55)

## Riquadri

<a id="r09"></a>

### R09 — Allineamento alla scena

**Sottotitolo:** Profondità coerente con il riferimento della scena

**In una frase:** Adatta la profondità stimata al riferimento della scena.

**Funzione e dati scambiati:** Stima scala e scostamento confrontando la profondità predetta con quella della scena ricostruita, nelle regioni valide esterne agli oggetti mascherati.

**Stato attuale:** Allineamento derivato dal metodo Whareformer, con controlli espliciti di validità per la memoria. Le posizioni ufficiali della baseline restano un ingresso riusato.

**Evidenze e limiti:** L’allineamento è stato riprodotto rispetto al riferimento di verifica; questo non certifica l’accuratezza fisica dei punti.

**Perché questa scelta:** La memoria richiede profondità confrontabili nel riferimento della scena.

**Alternative e loro stato:** -

**Possibili miglioramenti:** -

**Coerenza dei dati:** Profondità, maschere, posa e vista della scena devono riferirsi allo stesso frame.

**Possibili errori:** Scena incompleta, pose errate o poche regioni valide possono rendere il fit inaffidabile.

<a id="r12"></a>

### R12 — Estrai i punti dell’oggetto

**Sottotitolo:** Profondità allineata · maschera · intrinseci

**In una frase:** Ricava i punti stimati dell’oggetto dalla profondità allineata.

**Funzione e dati scambiati:** Seleziona i pixel validi nella maschera e li converte in punti 3D nel riferimento della camera usando gli intrinseci.

**Stato attuale:** Percorso principale con Depth Anything allineata. La profondità arriva dal ramo condiviso: qui non viene eseguito un secondo modello.

**Evidenze e limiti:** -

**Perché questa scelta:** -

**Alternative e loro stato:** MoGE è conservato come confronto su campione; non alimenta il percorso principale della memoria rappresentato qui.

**Possibili miglioramenti:** -

**Coerenza dei dati:** Maschera, profondità e intrinseci devono avere risoluzione e convenzioni compatibili.

**Possibili errori:** Errori della maschera o della profondità producono punti estranei o superfici deformate.

<a id="r13"></a>

### R13 — Porta i punti nella scena

**Sottotitolo:** Posa della camera · punti osservati

**In una frase:** Esprime i punti dell’oggetto nel riferimento della scena.

**Funzione e dati scambiati:** Applica la posa della camera ai punti dell’osservazione, conservando camera, provenienza e allineamento della profondità.

**Stato attuale:** Nuvole allineate preparate a piena risoluzione; i punti restano stime delle sole superfici visibili.

**Evidenze e limiti:** Coerenza del passaggio di riferimento verificata; le coordinate di scena non sono automaticamente misure certificate in metri.

**Perché questa scelta:** -

**Alternative e loro stato:** -

**Possibili miglioramenti:** -

**Coerenza dei dati:** Posa, punti e camera devono appartenere allo stesso frame; conservare il verso della trasformazione.

**Possibili errori:** Una posa errata può spostare la nuvola e falsare i confronti fra stati.

<a id="r14"></a>

### R14 — Ricostruzione SuperFlex

**Sottotitolo:** FPS-4096 · normalizzazione · primitive

**In una frase:** Stima la forma della singola osservazione con SuperFlex.

**Funzione e dati scambiati:** Campiona 4096 punti con FPS, una selezione distribuita sulla nuvola, e li normalizza. Il checkpoint robust stima primitive deformabili, dette superquadriche.

**Stato attuale:** Checkpoint preaddestrato congelato; ingresso ricavato dai punti dell’osservazione allineata.

**Evidenze e limiti:** Produzione delle ricostruzioni verificata; le parti nascoste previste restano ipotesi del modello.

**Perché questa scelta:** Rendere confrontabile la forma dell’osservazione con quella ricordata dalla traccia.

**Alternative e loro stato:** Confronto diretto dei punti come controllo del contributo di SuperFlex.

**Possibili miglioramenti:** Valutare stabilità fra viste e fedeltà alle superfici osservate.

**Coerenza dei dati:** Conservare campionamento e trasformazione inversa della normalizzazione; non riusare i completamenti come punti osservati.

**Possibili errori:** Parzialità e rumore possono produrre forme instabili o completamenti errati.

<a id="r15"></a>

### R15 — Descrittore di forma

**Sottotitolo:** D2: percorso attuale

**In una frase:** Riassume la superficie ricostruita in un descrittore confrontabile.

**Funzione e dati scambiati:** D2 descrive la distribuzione delle distanze fra coppie di punti campionati dalla superficie delle primitive, dopo centratura e normalizzazione della scala.

**Stato attuale:** Descrittore implementato nel percorso di riferimento; la scelta finale del confronto resta aperta.

**Evidenze e limiti:** L’invarianza a rotazione e scala non garantisce stabilità quando la ricostruzione cambia con la vista.

**Perché questa scelta:** -

**Alternative e loro stato:** Confronto dopo allineamento dei punti, ad esempio con distanza Chamfer, ancora da concordare.

**Possibili miglioramenti:** Misurare quanto il descrittore distingua identità simili e conservi viste complementari.

**Coerenza dei dati:** Usare lo stesso campionamento e la stessa normalizzazione per osservazione e memoria.

**Possibili errori:** Superfici interne o sovrapposte delle primitive possono alterare il descrittore; dimensione assoluta e posa non sono rappresentate.

<a id="r18"></a>

### R18 — Memoria geometrica precedente

**Sottotitolo:** Stati di posizione · forma persistente

**In una frase:** Conserva stati di posizione e forma persistente prima del frame corrente.

**Funzione e dati scambiati:** Gli stati raccolgono viste, camere e supporto di ciascuna collocazione. La forma persistente conserva i punti ammessi e l’ultima ricostruzione riuscita, con versioni distinte.

**Stato attuale:** Memoria opzione A implementata. Il matcher usa la forma disponibile; gli stati guidano l’aggiornamento, non sono nuovi descrittori da confrontare.

**Evidenze e limiti:** -

**Perché questa scelta:** -

**Alternative e loro stato:** Nel matcher di riferimento le forme delle singole osservazioni costituiscono una riserva distinta quando manca una ricostruzione dell’accumulo utilizzabile.

**Possibili miglioramenti:** -

**Coerenza dei dati:** Tutte le detection del frame leggono lo stesso stato precedente; riferimenti, traccia e versioni devono essere espliciti.

**Possibili errori:** Associazioni errate, stati incompatibili o forme precedenti poco rappresentative possono rendere fuorviante la memoria.

<a id="r20"></a>

### R20 — Distanza tra le forme

**Sottotitolo:** Confronti geometrici validi

**In una frase:** Confronta la forma corrente con quelle delle tracce candidate.

**Funzione e dati scambiati:** Nel percorso D2 calcola la distanza fra descrittori compatibili e segnala quali coppie osservazione–traccia hanno geometria utilizzabile.

**Stato attuale:** Confronto D2 implementato; distanza e uso finale della geometria restano da concordare con il matcher.

**Evidenze e limiti:** -

**Perché questa scelta:** -

**Alternative e loro stato:** Distanze fra punti allineati come confronto alternativo, non come scelta finale già adottata.

**Possibili miglioramenti:** -

**Coerenza dei dati:** Descrittori compatibili e memoria precedente al frame; coppie senza geometria indicate esplicitamente.

**Possibili errori:** Una distanza bassa non certifica la stessa identità, e una distanza alta può dipendere da parzialità o ricostruzione.

<a id="r21"></a>

### R21 — Correzione esterna dei punteggi

**Sottotitolo:** Percorso implementato di riferimento

**In una frase:** Usa la distanza di forma per correggere i punteggi di Whareformer.

**Funzione e dati scambiati:** Nel percorso di riferimento aggiunge peso × (distanza neutra − distanza di forma) ai punteggi delle tracce esistenti con confronto valido, prima dell’assegnazione originale.

**Stato attuale:** Correzione esterna implementata con rete Whareformer congelata; il nuovo matcher non è presentato come componente già concluso.

**Evidenze e limiti:** Il controllo a contributo geometrico nullo preserva la baseline; ciò non dimostra un beneficio della forma.

**Perché questa scelta:** -

**Alternative e loro stato:** Fusione esterna con parametri appresi e adattamento del matcher sono percorsi richiesti, ancora da confrontare.

**Possibili miglioramenti:** Definire contributo e calibrazione su sviluppo, poi valutarli con il sistema completo.

**Coerenza dei dati:** Nessuna correzione diretta all’opzione nuova traccia o alle coppie senza geometria; la competizione può comunque cambiarne le probabilità.

**Possibili errori:** Parametri non calibrati o copertura geometrica diseguale possono sbilanciare le associazioni.

<a id="r28"></a>

### R28 — Nuvola corrente valida?

**Sottotitolo:** Punti allineati · camera · validità

**In una frase:** Controlla se la nuvola può entrare nella memoria di posizione.

**Funzione e dati scambiati:** Richiede allineamento valido, camera coerente e un insieme sufficiente di punti utilizzabili dopo il filtraggio.

**Stato attuale:** Controllo preliminare implementato; non decide né la posizione né l’ammissione nella forma.

**Evidenze e limiti:** -

**Perché questa scelta:** -

**Alternative e loro stato:** -

**Possibili miglioramenti:** -

**Coerenza dei dati:** Nuvola e metadati devono corrispondere all’osservazione e alla traccia assegnata.

**Possibili errori:** La validità numerica non certifica la correttezza della profondità o dell’identità.

<a id="r29"></a>

### R29 — Assegna e aggiorna lo stato

**Sottotitolo:** Compatibilità per riproiezione · criterio C

**In una frase:** Assegna la vista a uno stato di posizione e ne aggiorna la storia.

**Funzione e dati scambiati:** Il criterio C verifica la coerenza di riproiezione con sagoma e spazio libero, prima negli stati confermati attivi e poi nei deboli. Se nessuno è compatibile, crea uno stato debole; aggiorna viste e supporto.

**Stato attuale:** Opzione A implementata; soglia e margine restano parametri da selezionare sul sistema completo.

**Evidenze e limiti:** Il test misura compatibilità geometrica, non certifica staticità. Occlusioni ed errori di profondità possono alterare l’assegnazione.

**Perché questa scelta:** Separare la collocazione dell’oggetto dalla decisione di incorporare una vista nella forma.

**Alternative e loro stato:** -

**Possibili miglioramenti:** Valutare aperture e chiusure degli stati insieme alle metriche di tracking.

**Coerenza dei dati:** Quando uno stato confermato riceve la vista, gli altri confermati si chiudono. Il ritorno a una posizione chiusa apre un nuovo stato; supporto e potatura seguono la storia temporale.

**Possibili errori:** Un rifiuto del verificatore di forma non deve creare un nuovo stato di posizione.

<a id="r30"></a>

### R30 — Stato confermato?

**Sottotitolo:** Supporto da più osservazioni

**In una frase:** Decide se lo stato ha supporto sufficiente per contribuire alla forma.

**Funzione e dati scambiati:** Lo stato è confermato se lo era già oppure se raggiunge i requisiti di osservazioni e supporto temporale. Uno stato ancora debole non modifica la forma persistente.

**Stato attuale:** Conferma implementata; non richiede che esista già una forma SuperFlex.

**Evidenze e limiti:** Più osservazioni compatibili non sono una prova indipendente di staticità o posa corretta.

**Perché questa scelta:** -

**Alternative e loro stato:** -

**Possibili miglioramenti:** -

**Coerenza dei dati:** La decisione riguarda lo stato scelto dopo l’aggiornamento del supporto.

**Possibili errori:** Errori coerenti fra viste possono confermare uno stato scorretto; osservazioni scarse possono ritardare la conferma.

<a id="r31"></a>

### R31 — Prepara le viste per la forma

**Sottotitolo:** Riferimento iniziale o trasformazione dello stato

**In una frase:** Porta le viste dello stato confermato nel riferimento della forma.

**Funzione e dati scambiati:** Se la forma è vuota, la prima vista inizializza il riferimento. Altrimenti riusa la trasformazione dello stato, oppure ne stima rotazione e traslazione rispetto alla forma, anche dopo uno spostamento.

**Stato attuale:** Percorso implementato; la registrazione candidata deve essere verificata prima di fissare la posa dello stato.

**Evidenze e limiti:** -

**Perché questa scelta:** -

**Alternative e loro stato:** -

**Possibili miglioramenti:** -

**Coerenza dei dati:** Scala compatibile, stessa traccia e soli punti osservati. Il primo seme va direttamente all’inizializzazione; le altre viste passano al verificatore.

**Possibili errori:** Simmetrie e sovrapposizione limitata possono produrre trasformazioni ambigue. Un fallimento lascia le viste pendenti senza modificare la forma.

<a id="r32"></a>

### R32 — Vista ammessa nella forma?

**Sottotitolo:** Verificatore appreso

**In una frase:** Decide se una vista può essere incorporata nella forma persistente.

**Funzione e dati scambiati:** Una baseline appresa sulle diagnostiche della coppia stima l’errore geometrico della vista allineata rispetto alla forma. Una soglia esplicita determina l’ammissione.

**Stato attuale:** Baseline leggera addestrata su dati simulati; il verificatore diretto sulle coppie di nuvole resta una direzione distinta.

**Evidenze e limiti:** Verifiche sintetiche disponibili, ma affidabilità sulle fusioni reali non dimostrata.

**Perché questa scelta:** -

**Alternative e loro stato:** Verificatore appreso direttamente sulle nuvole, non già sostituito alla baseline.

**Possibili miglioramenti:** Usare errori prodotti dal registratore effettivo e validare ammissioni e rifiuti con evidenza indipendente.

**Coerenza dei dati:** Non sceglie lo stato di posizione. Il seme iniziale non ha una forma precedente contro cui essere verificato; un modello o esito assente non equivale ad ammissione.

**Possibili errori:** False ammissioni contaminano la forma; falsi rifiuti escludono viste utili. La soglia non è una garanzia di rischio su nuovi dati.

<a id="r33"></a>

### R33 — Mantieni la forma precedente

**Sottotitolo:** Lo stato può essere aggiornato

**In una frase:** Conserva la forma senza annullare la storia dello stato o il tracking.

**Funzione e dati scambiati:** Non aggiunge punti quando la nuvola è invalida, lo stato è debole, la registrazione fallisce o la vista non è ammessa. Conserva l’ultima ricostruzione disponibile.

**Stato attuale:** Esiti distinti gestiti nel prototipo; forma invariata non significa intera memoria invariata.

**Evidenze e limiti:** -

**Perché questa scelta:** -

**Alternative e loro stato:** -

**Possibili miglioramenti:** -

**Coerenza dei dati:** La vista respinta resta associata allo stato. A posa fissata non viene riprovata; se nessuna vista ha accettato la posa candidata, le viste restano pendenti per una nuova registrazione.

**Possibili errori:** Rifiuti ripetuti possono lasciare la forma poco rappresentativa; cancellare supporto o storia confonderebbe rifiuto di fusione e posizione.

<a id="r34"></a>

### R34 — Aggiorna i punti della forma

**Sottotitolo:** Inizializzazione o fusione · punti pesati

**In una frase:** Inizializza o aggiorna la forma con i punti osservati ammessi.

**Funzione e dati scambiati:** Inserisce il primo seme oppure fonde le viste ammesse nel riferimento della forma. Conserva punti in celle spaziali con pesi e provenienza, producendo una nuova versione.

**Stato attuale:** Accumulo pesato implementato; la prima vista non viene conservata per sempre come riferimento privilegiato.

**Evidenze e limiti:** -

**Perché questa scelta:** Conservare superfici complementari senza reintrodurre come osservazioni le parti completate dal modello.

**Alternative e loro stato:** -

**Possibili miglioramenti:** -

**Coerenza dei dati:** Si fondono soltanto punti osservati stimati. Più viste dello stesso aggiornamento producono una versione della forma, non un’inferenza separata per ogni freccia in ingresso.

**Possibili errori:** Punti contaminati o trasformazioni errate possono deformare la forma anche dopo l’ammissione.

<a id="r35"></a>

### R35 — Ricostruisci con SuperFlex

**Sottotitolo:** FPS-4096 · nuova versione dei punti

**In una frase:** Ricostruisce con SuperFlex una nuova versione dei punti della forma.

**Funzione e dati scambiati:** Seleziona 4096 punti con FPS, li normalizza e prepara una richiesta legata alla versione della forma. Il modello robust stima le primitive e restituisce il risultato con la sua provenienza.

**Stato attuale:** Collegamento al worker implementato; stesso contratto di campionamento del ramo osservazione.

**Evidenze e limiti:** -

**Perché questa scelta:** -

**Alternative e loro stato:** -

**Possibili miglioramenti:** -

**Coerenza dei dati:** La richiesta contiene soli punti osservati ammessi e conserva trasformazione inversa e versione. Nessuna nuova richiesta se i punti della forma non cambiano.

**Possibili errori:** Un’inferenza fallita o un risultato associato alla versione sbagliata non devono sostituire una forma valida.

<a id="r36"></a>

### R36 — Ricostruzione disponibile?

**Sottotitolo:** Esito della richiesta versionata

**In una frase:** Controlla l’esito e la coerenza della ricostruzione richiesta.

**Funzione e dati scambiati:** Distingue un risultato valido da un fallimento dichiarato e verifica corrispondenza fra richiesta, input e versione. I risultati incoerenti sono segnalati come errori.

**Stato attuale:** Il coordinatore richiede di risolvere le richieste pendenti prima di avanzare al frame successivo.

**Evidenze e limiti:** -

**Perché questa scelta:** -

**Alternative e loro stato:** -

**Possibili miglioramenti:** -

**Coerenza dei dati:** Durante l’attesa l’ultima forma resta conservata, ma non si percorre il ramo di avanzamento. Il ramo negativo rappresenta un fallimento risolto, non una richiesta ancora pendente.

**Possibili errori:** Scambiare attesa o artefatti di un’altra versione per un esito riuscito viola il contratto temporale.

<a id="r37"></a>

### R37 — Aggiorna forma e descrittore

**Sottotitolo:** Completamento valido della versione richiesta

**In una frase:** Rende disponibili forma e descrittore della ricostruzione valida.

**Funzione e dati scambiati:** Registra il completamento riuscito e il descrittore associato, mantenendo la corrispondenza con la versione dei punti da cui derivano.

**Stato attuale:** Pubblicazione versionata implementata nel coordinamento della memoria.

**Evidenze e limiti:** -

**Perché questa scelta:** -

**Alternative e loro stato:** -

**Possibili miglioramenti:** -

**Coerenza dei dati:** La nuova forma serve ai confronti futuri; non modifica le associazioni del frame che ha prodotto la richiesta.

**Possibili errori:** Una versione scambiata o pubblicata retroattivamente rende non causale il confronto.

<a id="r38"></a>

### R38 — Mantieni l’ultima forma valida

**Sottotitolo:** Ricostruzione assente o fallita

**In una frase:** Conserva l’ultima ricostruzione valida quando quella nuova fallisce.

**Funzione e dati scambiati:** Mantiene la forma riuscita precedente senza annullare l’aggiornamento dei punti ammessi. Se non esiste una forma precedente, la sua assenza rimane esplicita.

**Stato attuale:** Gestione del fallimento dichiarato separata dall’attesa ancora da risolvere.

**Evidenze e limiti:** -

**Perché questa scelta:** -

**Alternative e loro stato:** -

**Possibili miglioramenti:** -

**Coerenza dei dati:** Punti e ricostruzione possono avere versioni diverse; la forma precedente non viene attribuita ai nuovi punti.

**Possibili errori:** Una forma vecchia può diventare poco rappresentativa. Se manca, il matcher deve usare il fallback previsto, senza inventare geometria.

<a id="r39"></a>

### R39 — Memoria per il frame successivo

**Sottotitolo:** Aspetto/posizione · stati · punti/ultima forma

**In una frase:** Conserva le memorie aggiornate per i confronti dei frame successivi.

**Funzione e dati scambiati:** Riunisce aspetto e posizione della baseline, stati geometrici, punti della forma e ultima ricostruzione utilizzabile. Mantiene distinti versioni e riferimenti.

**Stato attuale:** Coordinamento causale implementato; richieste SuperFlex pendenti da risolvere prima del frame seguente.

**Evidenze e limiti:** -

**Perché questa scelta:** -

**Alternative e loro stato:** -

**Possibili miglioramenti:** -

**Coerenza dei dati:** Tutte le detection di un frame leggono lo stesso stato precedente. La mancata fusione non annulla l’associazione o l’aggiornamento baseline.

**Possibili errori:** Aggiornamenti visibili ad alcune detection dello stesso frame o uso di risultati futuri introducono dipendenze non ammesse.

## Collegamenti

<a id="c03"></a>

### C03 — Dati d’ingresso forniti → Estrai i punti dell’oggetto

**Da → a:** G01 → R12 · **Etichetta:** nessuna

**In una frase:** Fornisce maschera e intrinseci per estrarre i punti dell’oggetto.

**Funzione e dati scambiati:** La profondità allineata descrive il frame; maschera e intrinseci permettono di attribuirne i pixel all’oggetto e ricavarne punti 3D.

**Stato attuale:** -

**Evidenze e limiti:** -

**Perché questa scelta:** -

**Alternative e loro stato:** -

**Possibili miglioramenti:** -

**Coerenza dei dati:** Stesso frame e risoluzione compatibile con la profondità.

**Possibili errori:** -

<a id="c10"></a>

### C10 — Estrai i punti dell’oggetto → Porta i punti nella scena

**Da → a:** R12 → R13 · **Etichetta:** nessuna

**In una frase:** Fornisce i punti dell’oggetto nel riferimento della camera.

**Funzione e dati scambiati:** Per portarli nella scena serve conoscere le coordinate 3D prima della trasformazione di posa.

**Stato attuale:** -

**Evidenze e limiti:** -

**Perché questa scelta:** -

**Alternative e loro stato:** -

**Possibili miglioramenti:** -

**Coerenza dei dati:** I punti conservano la provenienza dai pixel dell’osservazione.

**Possibili errori:** -

<a id="c11"></a>

### C11 — Porta i punti nella scena → Ricostruzione SuperFlex

**Da → a:** R13 → R14 · **Etichetta:** nessuna

**In una frase:** Fornisce a SuperFlex la nuvola allineata dell’osservazione.

**Funzione e dati scambiati:** La ricostruzione deve partire dalle superfici visibili stimate dell’oggetto, prima del proprio campionamento e della normalizzazione.

**Stato attuale:** -

**Evidenze e limiti:** -

**Perché questa scelta:** -

**Alternative e loro stato:** -

**Possibili miglioramenti:** -

**Coerenza dei dati:** Soli punti osservati validi, con riferimento e scala dichiarati.

**Possibili errori:** -

<a id="c19"></a>

### C19 — Memoria geometrica precedente → Distanza tra le forme

**Da → a:** R18 → R20 · **Etichetta:** nessuna

**In una frase:** Fornisce le forme precedenti delle tracce candidate.

**Funzione e dati scambiati:** Il confronto richiede una forma ricordata utilizzabile oltre a quella dell’osservazione corrente.

**Stato attuale:** -

**Evidenze e limiti:** -

**Perché questa scelta:** -

**Alternative e loro stato:** -

**Possibili miglioramenti:** -

**Coerenza dei dati:** Usare l’ultima forma disponibile prima del frame; segnalare le candidate prive di geometria.

**Possibili errori:** -

<a id="c30"></a>

### C30 — Porta i punti nella scena → Nuvola corrente valida?

**Da → a:** R13 → R28 · **Etichetta:** nessuna

**In una frase:** Fornisce la nuvola corrente nel riferimento della scena.

**Funzione e dati scambiati:** I controlli d’ingresso richiedono punti e metadati coerenti prima di assegnare la vista a uno stato.

**Stato attuale:** -

**Evidenze e limiti:** -

**Perché questa scelta:** -

**Alternative e loro stato:** -

**Possibili miglioramenti:** -

**Coerenza dei dati:** Allineamento, camera e provenienza devono riferirsi alla stessa osservazione.

**Possibili errori:** -

<a id="c31"></a>

### C31 — Nuvola corrente valida? → Assegna e aggiorna lo stato

**Da → a:** R28 → R29 · **Etichetta:** Sì

**In una frase:** Permette di assegnare allo stato una nuvola utilizzabile.

**Funzione e dati scambiati:** Soltanto un input che supera i controlli preliminari può sostenere un’ipotesi di posizione.

**Stato attuale:** -

**Evidenze e limiti:** -

**Perché questa scelta:** -

**Alternative e loro stato:** -

**Possibili miglioramenti:** -

**Coerenza dei dati:** La validità dell’input non equivale a compatibilità con uno stato.

**Possibili errori:** -

<a id="c32"></a>

### C32 — Memoria geometrica precedente → Assegna e aggiorna lo stato

**Da → a:** R18 → R29 · **Etichetta:** nessuna

**In una frase:** Fornisce gli stati precedenti della traccia assegnata.

**Funzione e dati scambiati:** Viste, camere e supporto degli stati attivi sono il riferimento per collocare la nuova vista; in loro assenza serve un nuovo stato.

**Stato attuale:** -

**Evidenze e limiti:** -

**Perché questa scelta:** -

**Alternative e loro stato:** -

**Possibili miglioramenti:** -

**Coerenza dei dati:** Usare gli stati della traccia effettiva, precedenti al frame.

**Possibili errori:** -

<a id="c33"></a>

### C33 — Assegna e aggiorna lo stato → Stato confermato?

**Da → a:** R29 → R30 · **Etichetta:** nessuna

**In una frase:** Fornisce lo stato scelto o creato con la storia aggiornata.

**Funzione e dati scambiati:** La decisione di conferma richiede il supporto risultante dall’osservazione appena assegnata.

**Stato attuale:** -

**Evidenze e limiti:** -

**Perché questa scelta:** -

**Alternative e loro stato:** -

**Possibili miglioramenti:** -

**Coerenza dei dati:** Stato, supporto e vista devono appartenere alla stessa traccia.

**Possibili errori:** -

<a id="c35"></a>

### C35 — Prepara le viste per la forma → Vista ammessa nella forma?

**Da → a:** R31 → R32 · **Etichetta:** Viste da verificare

**In una frase:** Fornisce le viste allineate da verificare rispetto alla forma.

**Funzione e dati scambiati:** Il giudizio di ammissione richiede la coppia vista–forma nello stesso riferimento geometrico.

**Stato attuale:** -

**Evidenze e limiti:** -

**Perché questa scelta:** -

**Alternative e loro stato:** -

**Possibili miglioramenti:** -

**Coerenza dei dati:** Usare la trasformazione candidata o già fissata dello stato; escludere il primo seme della forma vuota.

**Possibili errori:** -

<a id="c36"></a>

### C36 — Nuvola corrente valida? → Mantieni la forma precedente

**Da → a:** R28 → R33 · **Etichetta:** No

**In una frase:** Mantiene la forma quando la nuvola non è utilizzabile.

**Funzione e dati scambiati:** Senza nuovi punti utilizzabili manca l’evidenza necessaria per modificare la forma.

**Stato attuale:** -

**Evidenze e limiti:** -

**Perché questa scelta:** -

**Alternative e loro stato:** -

**Possibili miglioramenti:** -

**Coerenza dei dati:** Il tracking baseline resta valido; gli eventuali aggiornamenti temporali degli stati non sono nuove fusioni.

**Possibili errori:** -

<a id="c37"></a>

### C37 — Vista ammessa nella forma? → Mantieni la forma precedente

**Da → a:** R32 → R33 · **Etichetta:** No

**In una frase:** Esclude dalla forma una vista non ammessa.

**Funzione e dati scambiati:** Il rifiuto impedisce la fusione dei punti, ma non cambia lo stato di posizione a cui la vista è stata assegnata.

**Stato attuale:** -

**Evidenze e limiti:** -

**Perché questa scelta:** -

**Alternative e loro stato:** -

**Possibili miglioramenti:** -

**Coerenza dei dati:** A posa fissata la vista non si riprova; con posa ancora non accettata può restare pendente per una nuova registrazione.

**Possibili errori:** -

<a id="c38"></a>

### C38 — Vista ammessa nella forma? → Aggiorna i punti della forma

**Da → a:** R32 → R34 · **Etichetta:** Sì

**In una frase:** Fornisce i punti della vista ammessa all’aggiornamento.

**Funzione e dati scambiati:** Solo una vista accettata può estendere la forma persistente.

**Stato attuale:** -

**Evidenze e limiti:** -

**Perché questa scelta:** -

**Alternative e loro stato:** -

**Possibili miglioramenti:** -

**Coerenza dei dati:** Esito, vista e trasformazione devono riferirsi allo stesso tentativo.

**Possibili errori:** -

<a id="c39"></a>

### C39 — Aggiorna i punti della forma → Ricostruisci con SuperFlex

**Da → a:** R34 → R35 · **Etichetta:** nessuna

**In una frase:** Fornisce la nuova versione dei punti da ricostruire.

**Funzione e dati scambiati:** Una forma inizializzata o estesa richiede una ricostruzione coerente con i suoi punti aggiornati.

**Stato attuale:** -

**Evidenze e limiti:** -

**Perché questa scelta:** -

**Alternative e loro stato:** -

**Possibili miglioramenti:** -

**Coerenza dei dati:** Soli punti osservati ammessi; richiesta legata alla versione risultante.

**Possibili errori:** -

<a id="c43"></a>

### C43 — Ricostruzione disponibile? → Mantieni l’ultima forma valida

**Da → a:** R36 → R38 · **Etichetta:** Fallita

**In una frase:** Conserva l’ultima forma valida dopo un fallimento dichiarato.

**Funzione e dati scambiati:** L’esito negativo non fornisce una ricostruzione sostitutiva, quindi resta utilizzabile quella precedente.

**Stato attuale:** -

**Evidenze e limiti:** -

**Perché questa scelta:** -

**Alternative e loro stato:** -

**Possibili miglioramenti:** -

**Coerenza dei dati:** L’attesa non percorre questa freccia; risultati incoerenti sono errori da risolvere.

**Possibili errori:** -

<a id="c45"></a>

### C45 — Mantieni la forma precedente → Memoria per il frame successivo

**Da → a:** R33 → R39 · **Etichetta:** nessuna

**In una frase:** Trasmette la forma conservata con gli stati eventualmente aggiornati.

**Funzione e dati scambiati:** Il frame seguente deve conoscere la nuova storia delle posizioni anche quando nessun punto è entrato nella forma.

**Stato attuale:** -

**Evidenze e limiti:** -

**Perché questa scelta:** -

**Alternative e loro stato:** -

**Possibili miglioramenti:** -

**Coerenza dei dati:** Distinguere aggiornamento degli stati e cambiamento della forma.

**Possibili errori:** -

<a id="c49"></a>

### C49 — Memoria per il frame successivo → Memoria geometrica precedente

**Da → a:** R39 → R18 · **Etichetta:** nessuna

**In una frase:** Rende la memoria geometrica disponibile al frame successivo.

**Funzione e dati scambiati:** I confronti futuri richiedono stati, punti e ultima forma risultanti dagli aggiornamenti già conclusi.

**Stato attuale:** -

**Evidenze e limiti:** -

**Perché questa scelta:** -

**Alternative e loro stato:** -

**Possibili miglioramenti:** -

**Coerenza dei dati:** Stesso stato precedente per tutte le detection del nuovo frame; nessun completamento futuro.

**Possibili errori:** -

<a id="c50"></a>

### C50 — Allineamento alla scena → Estrai i punti dell’oggetto

**Da → a:** R09 → R12 · **Etichetta:** nessuna · **Nuova freccia**

**In una frase:** Fornisce la profondità allineata per ricavare i punti dell’oggetto.

**Funzione e dati scambiati:** L’estrazione deve usare la profondità resa coerente con la scena, anziché una predizione grezza indipendente.

**Stato attuale:** -

**Evidenze e limiti:** -

**Perché questa scelta:** -

**Alternative e loro stato:** -

**Possibili miglioramenti:** -

**Coerenza dei dati:** Stesso frame della maschera; allineamento valido e parametri conservati.

**Possibili errori:** -

<a id="c51"></a>

### C51 — Camera e scena 3D → Porta i punti nella scena

**Da → a:** R03 → R13 · **Etichetta:** nessuna · **Nuova freccia**

**In una frase:** Fornisce la posa della camera per esprimere i punti nella scena.

**Funzione e dati scambiati:** Le coordinate nel riferimento camera non bastano a confrontare viste riprese da posizioni diverse.

**Stato attuale:** -

**Evidenze e limiti:** -

**Perché questa scelta:** -

**Alternative e loro stato:** -

**Possibili miglioramenti:** -

**Coerenza dei dati:** Posa del frame corretto e verso camera → scena.

**Possibili errori:** Invertire la trasformazione colloca i punti nel riferimento sbagliato.

<a id="c52"></a>

### C52 — Stato confermato? → Prepara le viste per la forma

**Da → a:** R30 → R31 · **Etichetta:** Sì · **Nuova freccia**

**In una frase:** Permette allo stato confermato di contribuire alla forma.

**Funzione e dati scambiati:** La conferma fornisce il supporto richiesto prima di preparare viste per la forma persistente.

**Stato attuale:** -

**Evidenze e limiti:** -

**Perché questa scelta:** -

**Alternative e loro stato:** -

**Possibili miglioramenti:** -

**Coerenza dei dati:** Riguarda lo stato scelto; non certifica la posa o la staticità.

**Possibili errori:** -

<a id="c53"></a>

### C53 — Stato confermato? → Mantieni la forma precedente

**Da → a:** R30 → R33 · **Etichetta:** No · **Nuova freccia**

**In una frase:** Conserva la forma mentre lo stato è ancora debole.

**Funzione e dati scambiati:** Il supporto non è ancora sufficiente per autorizzare un contributo alla forma persistente.

**Stato attuale:** -

**Evidenze e limiti:** -

**Perché questa scelta:** -

**Alternative e loro stato:** -

**Possibili miglioramenti:** -

**Coerenza dei dati:** La vista e la storia restano nello stato, soggette al suo ciclo temporale.

**Possibili errori:** -

<a id="c54"></a>

### C54 — Prepara le viste per la forma → Aggiorna i punti della forma

**Da → a:** R31 → R34 · **Etichetta:** Prima vista, forma vuota · **Nuova freccia**

**In una frase:** Fornisce il primo seme quando la forma è vuota.

**Funzione e dati scambiati:** Senza una forma precedente manca il termine di confronto per verificare la prima vista.

**Stato attuale:** -

**Evidenze e limiti:** -

**Perché questa scelta:** -

**Alternative e loro stato:** -

**Possibili miglioramenti:** -

**Coerenza dei dati:** Solo la prima vista del primo stato confermato segue questo percorso; le altre sono verificate.

**Possibili errori:** La validità del seme non ne certifica l’accuratezza fisica.

<a id="c55"></a>

### C55 — Prepara le viste per la forma → Mantieni la forma precedente

**Da → a:** R31 → R33 · **Etichetta:** Registrazione fallita · **Nuova freccia**

**In una frase:** Conserva la forma quando non si ottiene una registrazione utilizzabile.

**Funzione e dati scambiati:** Senza una trasformazione disponibile non si possono combinare i punti dello stato con la forma precedente.

**Stato attuale:** -

**Evidenze e limiti:** -

**Perché questa scelta:** -

**Alternative e loro stato:** -

**Possibili miglioramenti:** -

**Coerenza dei dati:** Le viste restano pendenti; non è un rifiuto definitivo del verificatore a posa fissata.

**Possibili errori:** -

## Provenienza e conservazione

Le sorgenti di ciascuna scheda sono elencate in TESTI_PROPOSTI.json, separate dal testo rivolto ai lettori. Le schede non incluse restano conservate; C34 e C40 sono soltanto proposte per la rimozione. Nessuna modifica ai file della mappa, nessuna nuova inferenza o esecuzione HPC. La conferma dei testi resta distinta dalla validazione scientifica e dall’applicazione grafica.
