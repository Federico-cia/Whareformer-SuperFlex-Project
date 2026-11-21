# Commenti mancanti — proposta del 21 novembre 2026

Bozza da revisionare in chat, non applicata alla mappa. Solo nove nodi e tredici collegamenti mancanti, più il campo segnaposto di E10. Si descrive l'implementazione attuale; le alternative restano proposte. I testi già compilati saranno revisionati in una fase successiva.

## Riquadri

### B08 · Profondità baseline allineata alla scena

- **In una frase:** Stima la profondità dal frame RGB e la rende coerente con la ricostruzione della scena.
- **Funzione e dati scambiati:** Depth Anything V2 stima la profondità dell'immagine. La pipeline originale ne adatta scala e scostamento alla profondità ricavata dalla scena 3D, usando regioni valide esterne agli oggetti mascherati. Il risultato serve a stimare la posizione degli oggetti.
- **Stato attuale:** Processo previsto da Whareformer. Nelle prove riutilizziamo le posizioni ufficiali già calcolate; questa fase non viene rieseguita.
- **Evidenze e limiti:** Procedura verificata nel codice originale. La rigenerazione completa delle posizioni dalle immagini resta da verificare.
- **Perché questa scelta:** Manteniamo il procedimento originale per distinguere il contributo della forma da eventuali cambiamenti della posizione.
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** Completare la rigenerazione e verificarne la compatibilità con le posizioni ufficiali.
- **Coerenza dei dati:** Immagine, maschere, camera e profondità della scena devono corrispondere allo stesso frame e avere coordinate compatibili.
- **Possible points of failure:** Ricostruzione incompleta, posa errata o pochi punti validi possono rendere inaffidabile l'allineamento della profondità.

### B09 · Intrinseci, posa camera e ricostruzione scena

- **In una frase:** Fornisce i parametri della camera e il riferimento 3D necessari a interpretare immagini e profondità.
- **Funzione e dati scambiati:** Gli intrinseci descrivono la proiezione tra punti 3D e pixel. La posa colloca la camera nella scena; la ricostruzione permette di calcolare la profondità della scena dalla vista corrente. Ogni ramo usa soltanto le informazioni necessarie.
- **Stato attuale:** Sono risorse esterne richieste dal percorso originale. Nel ramo forma, Depth Anything usa gli intrinseci per ottenere i punti; MoGE produce direttamente una geometria stimata.
- **Evidenze e limiti:** Ruoli verificati nel codice. La disponibilità di questi dati non certifica la scala fisica né la corretta collocazione delle forme nella scena.
- **Perché questa scelta:** Permettono di collegare le coordinate dell'immagine alle coordinate 3D e di confrontare posizioni espresse nello stesso riferimento.
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** Verificare la catena di trasformazioni e la compatibilità di scala tra geometria dell'oggetto e scena.
- **Coerenza dei dati:** Convenzioni di proiezione, risoluzione, verso delle trasformazioni e scala devono essere espliciti e compatibili.
- **Possible points of failure:** Parametri o riferimenti incoerenti producono punti e posizioni errati anche con immagini e maschere corrette.

### B10 · Posizione 3D · pipeline Whareformer

- **In una frase:** Stima un punto 3D rappresentativo della posizione dell'oggetto nella scena.
- **Funzione e dati scambiati:** Combina il centro del rettangolo che racchiude l'oggetto con la profondità mediana nella maschera. Gli intrinseci permettono di ottenere un punto nel riferimento della camera; la posa lo trasforma nel riferimento della scena.
- **Stato attuale:** Nelle prove utilizziamo le posizioni ufficiali di Whareformer, identiche in tutte le varianti.
- **Evidenze e limiti:** Calcolo verificato nel codice originale. Il risultato è una posizione stimata, non il centro geometrico certificato né l'orientamento dell'oggetto.
- **Perché questa scelta:** Conserviamo il segnale spaziale della baseline per valutare separatamente l'aggiunta della forma.
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** Verificare la rigenerazione delle posizioni dalle immagini e dagli asset originali.
- **Coerenza dei dati:** Rettangolo, maschera, profondità e camera devono riferirsi alla stessa osservazione; le posizioni devono condividere il riferimento della scena.
- **Possible points of failure:** Maschere contaminate, profondità errata o posa imprecisa possono spostare la posizione stimata.

### B11 · Osservazione corrente · forma, aspetto, posizione

- **In una frase:** Riunisce le informazioni disponibili sullo stesso oggetto osservato nel frame corrente.
- **Funzione e dati scambiati:** Collega descrittore d'aspetto, posizione 3D e descrittore di forma mediante l'identificativo dell'osservazione. Segnala esplicitamente l'eventuale assenza della geometria e prepara i dati per il confronto con le tracce.
- **Stato attuale:** Aspetto e posizione alimentano Whareformer; la forma viene usata dal nostro adattatore esterno. Non viene costruito un nuovo ingresso congiunto della rete.
- **Evidenze e limiti:** Corrispondenze e ordine delle osservazioni sono stati controllati nei manifest delle prove. La geometria è disponibile soltanto per un sottoinsieme delle osservazioni.
- **Perché questa scelta:** L'associazione richiede che tutti i segnali descrivano lo stesso oggetto nello stesso istante.
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** Ampliare la disponibilità della geometria e verificarne la provenienza nel percorso dalle immagini.
- **Coerenza dei dati:** Video, frame, identificativo e ordine dell'osservazione devono coincidere tra i diversi segnali.
- **Possible points of failure:** Una corrispondenza errata può combinare aspetto, posizione e forma di oggetti diversi.

### B13 · Memoria precedente delle tracce

- **In una frase:** Conserva ciò che il sistema conosce delle tracce prima di elaborare il frame corrente.
- **Funzione e dati scambiati:** Per ogni traccia mantiene la memoria originale di aspetto e posizione e, quando disponibili, i punti osservati ammessi e l'ultima forma ricostruita con successo. Fornisce lo stato con cui confrontare le nuove osservazioni e tentare gli aggiornamenti geometrici.
- **Stato attuale:** Nel ciclo con accumulo, tutte le osservazioni del frame leggono lo stesso stato geometrico precedente. È disponibile anche una variante di confronto con forme separate.
- **Evidenze e limiti:** Ordine degli aggiornamenti e provenienza degli stati sono verificati nel coordinatore e negli output delle prove. Una memoria coerente nel software non garantisce identità o geometria fisicamente corrette.
- **Perché questa scelta:** Il confronto deve usare conoscenze precedenti, senza includere l'osservazione che sta per essere associata.
- **Alternative e loro stato:** Le forme separate senza fusione sono un confronto implementato; non costituiscono una scelta definitiva alternativa all'accumulo.
- **Possibili miglioramenti:** Valutare quanto associazioni errate e fusioni inaffidabili deteriorino la memoria.
- **Coerenza dei dati:** Ogni stato deve conservare ID della traccia, sorgente, riferimento, versione e provenienza temporale.
- **Possible points of failure:** Memorie contaminate o aggiornate troppo presto possono favorire associazioni scorrette nei frame successivi.

### B15 · Aggiorna posizione e aspetto

- **In una frase:** Aggiorna la memoria visiva e spaziale della traccia associata.
- **Funzione e dati scambiati:** Aggiunge aspetto e posizione della nuova osservazione alle rispettive memorie, secondo le regole configurate nella baseline, e aggiorna ultima posizione, istante e storia delle associazioni.
- **Stato attuale:** Utilizza il procedimento originale di Whareformer. L'aggiornamento avviene anche se la successiva fusione geometrica viene respinta.
- **Evidenze e limiti:** Procedura verificata nel codice e usata nelle prove integrate. L'aggiornamento non certifica che l'associazione sia corretta.
- **Perché questa scelta:** La traccia deve incorporare le nuove informazioni visive e spaziali mantenendo il comportamento della baseline.
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** Osservazione e memoria precedente devono appartenere alla traccia indicata dall'assegnazione, con ordine temporale corretto.
- **Possible points of failure:** Un'associazione errata inserisce nella traccia caratteristiche di un altro oggetto.

### B17 · Crea una nuova traccia

- **In una frase:** Crea un nuovo identificativo quando l'assegnazione restituisce l'esito «nuova traccia».
- **Funzione e dati scambiati:** Il tracker assegna un ID alla nuova traccia e avvia la sua inizializzazione con i dati dell'osservazione corrente.
- **Stato attuale:** Creazione gestita dalla procedura originale di Whareformer; non richiede una forma 3D valida.
- **Evidenze e limiti:** Passaggio verificato nel codice e nelle associazioni delle prove. Una nuova traccia può anche derivare dal mancato riconoscimento di un oggetto già visto.
- **Perché questa scelta:** Un'osservazione non associata deve poter essere ricordata e riconosciuta nei frame successivi.
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** L'ID deve essere univoco e collegato all'osservazione che ha generato la traccia.
- **Possible points of failure:** Creazioni superflue frammentano la storia dello stesso oggetto in più tracce.

### B18 · Inizializza posizione, aspetto e geometria

- **In una frase:** Costruisce lo stato iniziale della nuova traccia con i dati disponibili.
- **Funzione e dati scambiati:** Inizializza aspetto e posizione secondo la baseline. Se disponibile, conserva la prima nuvola valida e la relativa forma; nel percorso con accumulo, SuperFlex viene eseguito sulla memoria di punti inizializzata. Questa operazione non è una fusione tra viste.
- **Stato attuale:** La traccia può esistere anche senza geometria. La prima nuvola valida può inizializzare la memoria geometrica in un'osservazione successiva.
- **Evidenze e limiti:** Nelle prove le inizializzazioni geometriche sono conteggiate separatamente dalle fusioni. La prima vista resta parziale e la forma completata è una stima.
- **Perché questa scelta:** Il sistema deve iniziare a ricordare l'oggetto anche quando alcuni segnali non sono ancora disponibili.
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** Aspetto, posizione, punti e forma devono appartenere alla stessa osservazione e al nuovo ID; la nuvola conserva sorgente, riferimento e scala.
- **Possible points of failure:** Una prima osservazione contaminata può compromettere i confronti futuri. Un fallimento della ricostruzione lascia indisponibile la forma senza impedire la traccia baseline.

### B19 · Memoria aggiornata

- **In una frase:** Rende disponibili ai frame successivi gli stati aggiornati delle tracce.
- **Funzione e dati scambiati:** Riunisce aspetto e posizione aggiornati, punti geometrici ammessi e ultima forma riuscita. Se una fusione è respinta conserva la geometria precedente; se fallisce SuperFlex conserva l'ultima forma valida, distinguendola dalla nuova versione dei punti.
- **Stato attuale:** Il ciclo è implementato ed eseguito da input preparati. Gli aggiornamenti non modificano retroattivamente l'associazione del frame corrente.
- **Evidenze e limiti:** Versioni e provenienza sono registrate negli output. Questo verifica la gestione dello stato, non l'accuratezza fisica della memoria o l'esecuzione in tempo reale.
- **Perché questa scelta:** Le nuove informazioni devono influenzare i confronti futuri senza confondere punti aggiornati e ricostruzioni riuscite in momenti diversi.
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** Verificare la qualità geometrica degli stati conservati e il loro contributo alle associazioni future.
- **Coerenza dei dati:** Punti e forma mantengono versioni distinte, ID della traccia e istanti di aggiornamento. Le superfici completate non vengono reinserite nei punti osservati.
- **Possible points of failure:** Una forma precedente può non rappresentare tutti i punti aggiornati; una fusione errata può propagarsi ai confronti successivi.

## Collegamenti

### E07 · Camera → nuvola dell'oggetto

- **In una frase:** Gli intrinseci permettono di trasformare la profondità stimata da Depth Anything in punti 3D.
- **Funzione e dati scambiati:** Fornisce i parametri che collegano pixel e raggi della camera, necessari alla costruzione della nuvola nel ramo Depth Anything.
- **Stato attuale:** Usato nel ramo Depth Anything; MoGE fornisce direttamente punti stimati.
- **Evidenze e limiti:** Verificato nel codice geometrico. Posa e ricostruzione della scena non sono prerequisiti generali per questa nuvola nel riferimento della camera.
- **Perché questa scelta:** La profondità da sola non determina le coordinate laterali dei punti.
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** Gli intrinseci devono corrispondere alla camera e alla risoluzione della profondità.
- **Possible points of failure:** Intrinseci o ridimensionamenti errati deformano la nuvola.

### E13 · Camera e scena → profondità baseline

- **In una frase:** La scena e la camera forniscono il riferimento con cui allineare la profondità stimata dall'immagine.
- **Funzione e dati scambiati:** Permette di calcolare la profondità della ricostruzione dalla vista corrente, usata per adattare quella predetta dal modello.
- **Stato attuale:** Collegamento previsto dalla baseline; nelle prove con posizioni ufficiali non viene rieseguito.
- **Evidenze e limiti:** Verificato nel codice originale; rigenerazione completa non ancora verificata.
- **Perché questa scelta:** Le due profondità devono essere compatibili prima di stimare posizioni nel riferimento della scena.
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** Ricostruzione, intrinseci e posa devono descrivere la stessa vista e condividere le convenzioni richieste.
- **Possible points of failure:** Una vista errata o una scena incompleta possono rendere inaffidabile il riferimento di allineamento.

### E14 · Profondità baseline → posizione 3D

- **In una frase:** La profondità allineata fornisce la distanza necessaria a collocare l'oggetto in 3D.
- **Funzione e dati scambiati:** Trasferisce la mappa da cui il ramo posizione seleziona i valori pertinenti all'oggetto mediante la maschera.
- **Stato attuale:** Previsto dalla baseline; nelle prove sono riutilizzate le posizioni finali ufficiali.
- **Evidenze e limiti:** Dipendenza verificata nel codice. La mappa non contiene già la posizione finale dell'oggetto.
- **Perché questa scelta:** La sola posizione nell'immagine non specifica la distanza dalla camera.
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** Profondità, maschera e rettangolo devono corrispondere allo stesso frame e avere coordinate compatibili.
- **Possible points of failure:** Profondità non pertinenti all'oggetto producono una posizione 3D errata.

### E16 · Camera → posizione 3D

- **In una frase:** I parametri della camera permettono di passare da pixel e profondità a una posizione nella scena.
- **Funzione e dati scambiati:** Gli intrinseci consentono la conversione nel riferimento della camera; la posa permette il passaggio al riferimento della scena.
- **Stato attuale:** Previsto dal codice originale; nelle prove sono riutilizzate le posizioni ufficiali.
- **Evidenze e limiti:** Trasformazioni verificate nel codice. La posizione ottenuta non determina l'orientamento dell'oggetto.
- **Perché questa scelta:** Le posizioni osservate da camere diverse devono essere espresse nello stesso riferimento per essere confrontabili.
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** Intrinseci, risoluzione e verso della trasformazione camera-scena devono essere coerenti.
- **Possible points of failure:** Una trasformazione invertita o una posa errata sposta l'oggetto nella scena.

### E17 · Posizione 3D → osservazione corrente

- **In una frase:** Aggiunge all'osservazione la posizione spaziale usata da Whareformer.
- **Funzione e dati scambiati:** Trasferisce le tre coordinate della posizione baseline, collegate alla stessa osservazione di aspetto e forma.
- **Stato attuale:** Collegamento attivo con posizioni ufficiali mantenute identiche tra varianti.
- **Evidenze e limiti:** Corrispondenze verificate negli input delle prove. Il dato è una posizione puntuale, non una superficie o una posa completa.
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** Coordinate, ID e ordine dell'osservazione devono coincidere con quelli degli altri segnali.
- **Possible points of failure:** Una posizione attribuita all'oggetto sbagliato altera il confronto spaziale.

### E19 · Memoria precedente → associazione

- **In una frase:** Fornisce le tracce già note con cui confrontare la nuova osservazione.
- **Funzione e dati scambiati:** Trasmette ID, memoria d'aspetto e posizione e, quando disponibile, descrizione geometrica delle tracce candidate.
- **Stato attuale:** Whareformer usa aspetto e posizione; il nostro adattatore usa la forma disponibile nello stato precedente.
- **Evidenze e limiti:** Il coordinatore separa confronto e aggiornamento geometrico. Le tracce candidate sono predizioni, non identità fisiche certificate.
- **Perché questa scelta:** L'associazione richiede un termine di confronto che rappresenti gli oggetti già ricordati.
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** Dati e ordine delle tracce devono corrispondere agli ID dei punteggi; il confronto geometrico usa uno stato comune precedente al frame.
- **Possible points of failure:** ID disallineati o uso prematuro dei nuovi dati possono falsare l'associazione.

### E24 · Nuova traccia → inizializzazione

- **In una frase:** Indica a quale nuovo ID assegnare lo stato iniziale dell'osservazione.
- **Funzione e dati scambiati:** Trasmette l'identificativo creato dal tracker e attiva l'inizializzazione. Aspetto, posizione e geometria arrivano dagli altri collegamenti in ingresso.
- **Stato attuale:** Collegamento implementato; la creazione non dipende dalla disponibilità della forma.
- **Evidenze e limiti:** Verificato nel codice e nel coordinamento degli ID. L'identificativo non contiene da solo i dati dell'oggetto.
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** Il nuovo ID deve corrispondere all'osservazione che ne ha causato la creazione.
- **Possible points of failure:** Un ID errato inizializza la memoria della traccia sbagliata.

### E28 · Memoria precedente → aggiornamento di aspetto e posizione

- **In una frase:** Fornisce lo stato della traccia a cui aggiungere la nuova informazione visiva e spaziale.
- **Funzione e dati scambiati:** Rende disponibili le memorie d'aspetto e posizione e la storia della traccia selezionata, aggiornate secondo le regole originali.
- **Stato attuale:** Aggiornamento baseline conservato; indipendente dal successo della fusione geometrica.
- **Evidenze e limiti:** Verificato nella classe originale della traccia. Non viene introdotta una nuova regola di media tra osservazioni.
- **Perché questa scelta:** La nuova osservazione deve aggiornare la storia corretta, preservando il funzionamento della baseline.
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** Memoria precedente e assegnazione devono riferirsi allo stesso ID.
- **Possible points of failure:** Una memoria selezionata erroneamente mescola la storia di oggetti diversi.

### E30 · Memoria precedente → aggiornamento geometrico

- **In una frase:** Fornisce i punti già ricordati rispetto ai quali allineare e valutare la nuova nuvola.
- **Funzione e dati scambiati:** Trasmette nuvola osservata precedente, riferimento, sorgente e versione della traccia associata. Se manca una nuvola valida, il nuovo dato può inizializzarla.
- **Stato attuale:** Collegamento del percorso con accumulo. La sola superficie ricostruita non sostituisce la memoria dei punti osservati.
- **Evidenze e limiti:** Gestione verificata nel codice dell'accumulatore e del coordinatore; la correttezza fisica degli allineamenti resta da validare.
- **Perché questa scelta:** Per unire viste diverse serve una geometria di riferimento; la sola posizione della traccia non basta.
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** ID, sorgente, scala e riferimento devono essere compatibili con il nuovo dato.
- **Possible points of failure:** Una memoria contaminata o di scala incompatibile può indurre un allineamento scorretto.

### E31 · Aggiornamento di aspetto e posizione → memoria aggiornata

- **In una frase:** Conserva il nuovo stato visivo e spaziale per i confronti futuri.
- **Funzione e dati scambiati:** Trasferisce memorie aggiornate, ultima posizione e storia della traccia, anche quando la geometria non cambia.
- **Stato attuale:** Passaggio baseline mantenuto nel ciclo integrato.
- **Evidenze e limiti:** Verificato nel codice della traccia e nelle prove integrate.
- **Perché questa scelta:** -
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** Lo stato deve restare collegato all'ID e all'istante dell'aggiornamento.
- **Possible points of failure:** Dati obsoleti o attribuiti male compromettono i confronti successivi.

### E32 · Aggiornamento geometrico → memoria aggiornata

- **In una frase:** Conserva i punti ammessi e la forma ricostruita con successo per gli usi futuri.
- **Funzione e dati scambiati:** Pubblica la versione dei punti e, quando riuscita, la nuova ricostruzione con il descrittore. Un rifiuto mantiene la geometria precedente; un fallimento di SuperFlex mantiene l'ultima forma valida anche se i punti sono già aggiornati.
- **Stato attuale:** Implementato nel ciclo con accumulo; punti e forma hanno versioni distinte.
- **Evidenze e limiti:** Versioni e provenienza sono registrate negli output. Il salvataggio corretto non certifica la qualità della fusione.
- **Perché questa scelta:** La memoria deve conservare risultati utilizzabili senza sostituire una forma valida con una ricostruzione fallita.
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** ID e versioni devono restare espliciti; nessun punto generato dal completamento viene aggiunto ai punti osservati.
- **Possible points of failure:** Confondere la versione dei punti con quella della forma può far usare una ricostruzione precedente come se fosse aggiornata.

### E33 · Inizializzazione → memoria aggiornata

- **In una frase:** Inserisce lo stato iniziale della nuova traccia nella memoria disponibile ai frame successivi.
- **Funzione e dati scambiati:** Trasferisce ID, aspetto, posizione e geometria eventualmente disponibile; l'assenza della geometria resta esplicita.
- **Stato attuale:** Implementato anche per tracce prive di forma valida.
- **Evidenze e limiti:** Inizializzazioni e fusioni sono distinte nei log; una prima vista non dimostra accumulo multivista.
- **Perché questa scelta:** La traccia deve diventare candidata per le associazioni future.
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** Tutti i dati iniziali devono condividere ID della traccia e provenienza dell'osservazione.
- **Possible points of failure:** Un'inizializzazione contaminata può causare errori nei successivi riconoscimenti.

### E34 · Memoria aggiornata → memoria precedente

- **In una frase:** Lo stato aggiornato diventa il riferimento per elaborare il frame successivo.
- **Funzione e dati scambiati:** Trasferisce nel tempo lo stato delle tracce dopo gli aggiornamenti del frame corrente e la gestione degli esiti delle ricostruzioni.
- **Stato attuale:** Il replay procede in ordine temporale; le richieste di ricostruzione pendenti vengono risolte prima del frame successivo.
- **Evidenze e limiti:** Ordine imposto dal coordinatore e verificato nelle prove. La causalità dello stato non dimostra elaborazione in tempo reale né assenza di preprocessing sull'intero video.
- **Perché questa scelta:** Le osservazioni già elaborate devono contribuire alle decisioni future senza modificare quelle passate.
- **Alternative e loro stato:** -
- **Possibili miglioramenti:** -
- **Coerenza dei dati:** Frame e istanti devono avanzare; nessun aggiornamento geometrico del frame corrente entra nel confronto che lo ha generato.
- **Possible points of failure:** Un ordine errato può usare dati futuri o memorie obsolete.

## E10 · Solo completamento del campo «Alternative e loro stato»

Sono da confrontare l'attuale correzione esterna dei punteggi, una combinazione con pochi parametri appresi mantenendo le reti congelate e l'adattamento di Whareformer con il segnale geometrico. Marco ha richiesto di tentare fusione esterna e riaddestramento, previa verifica di dati e distanza. Nessuna soluzione è stata selezionata come definitiva; le alternative non sono rappresentate come moduli già eseguiti.

## Evidenze consultate per questa bozza

- JSON attuale della mappa e checklist REVISIONE_MAPPA_20261115.md.
- Whareformer-repo/src/feature_extraction/extractors/epic_extractor.py e utils/epic_utils.py: allineamento esterno alle maschere, scala/scostamento, mediana e proiezione.
- Whareformer-repo/src/tracking/tracker/track.py e memory/buffer.py: inizializzazione e aggiornamento originali secondo configurazione.
- integration_prototype/frame_coordinator.py, cloud_updater.py, cloud_memory.py ed experiment_runner.py: confronto precedente agli aggiornamenti, inizializzazione tardiva, versioni e gestione delle ricostruzioni.
- RISULTATI_CAMPAGNA_HPC_20261115.md, STATO_LAVORO.md e ultime decisioni: stato eseguito e limiti; nessuna nuova esecuzione sperimentale.

Le nuove eventuali schede derivanti dalla divisione dei blocchi saranno proposte dopo la scelta strutturale, senza duplicare i commenti esistenti né cambiarli in questa fase.
