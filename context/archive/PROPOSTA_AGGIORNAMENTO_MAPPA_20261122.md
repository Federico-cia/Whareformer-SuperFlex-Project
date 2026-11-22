# Proposta di aggiornamento della mappa — 22 novembre 2026

**Esito successivo:** struttura concreta e testi confermati da Marco, [applicati alla mappa HTML](../evidence/map_20261122/ESITO_APPLICAZIONE.md). Le proposte sotto documentano la fase precedente.

**Revisione successiva, prevalente per la struttura:** dopo «less is more» di Marco, preparata una [proposta concreta con 39 riquadri e 53 collegamenti](STRUTTURA_PROPOSTA_MAPPA_20261122.md), senza nuovi nodi. La soluzione espandibile sotto rimane una possibilità grafica, non una scelta adottata. Nessuna modifica applicata.

**Stato: proposta dell'assistente, non approvata né applicata.** Confrontati HTML e dati autorevoli della mappa (39 nodi/49 collegamenti), specifica dell'opzione A, decisioni vigenti e codice position_state_memory.py. Consultazione nel browser riuscita dopo avvio del servizio locale; nessuna modifica ai contenuti della mappa. Per metodo e stato usare rispettivamente MEMORIA_OPZIONE_A_E_SELEZIONE_20261122.md e STATO_LAVORO.md.

## Giudizio e perimetro

La struttura Rami paralleli resta utilizzabile, ma il ramo inferiore rappresenta l'accumulo precedente. Non bastano correzioni nelle schede: occorre rendere visibili stati di posizione, conferma e forma persistente. La vista complessiva è già molto verticale; raccomandato un dettaglio espandibile della memoria o un riquadro di sottoprocesso, mantenendo il contesto del ciclo. Questa è una scelta grafica proposta, non nuovo metodo.

## Modifiche necessarie

| Zona attuale | Proposta | Motivo |
|---|---|---|
| R08–R14 e collegamenti della geometria | Mostrare DA → allineamento alpha/beta → estrazione punti dell'oggetto e riferimento scena → FPS-4096/normalizzazione → SuperFlex. Collegare allineamento e pose anche al ramo forma; distinguere punti camera e scena. MoGE in un percorso laterale di confronto. | DA grezza e allineata non sono ingressi equivalenti; l'allineamento è implementato, non soltanto prospettato. Non dedurre uguaglianza numerica con XYZ ufficiali riusati. |
| R18 e R39 | Distinguere stati della collocazione (viste, supporto, camere, trasformazioni) dalla forma persistente (punti ammessi e ultima SuperFlex disponibile). | Un'unica voce «punti e forma» nasconde il nuovo ciclo. Le versioni di punti e completamento restano distinte. |
| R28–R34 | Sostituire la sola biforcazione «punti già in memoria?» con assegnazione per criterio C, creazione/aggiornamento dello stato debole, conferma temporale, inizializzazione o registrazione verso la forma persistente, verifica appresa per vista e fusione dei punti ammessi. | Stato di posizione e ammissione sono decisioni diverse. |
| R33 e rami negativi | Separare nuvola invalida, stato non ancora confermato, registrazione non accettata e vista non ammessa. | Nel rifiuto di fusione la forma resta invariata, ma supporto/storia dello stato possono essere aggiornati; non scrivere «nessuna modifica alla memoria». |
| R30–R32 e schede di R34 | Eliminare prima vista fissa e gate euristici come descrizione del percorso corrente; descrivere baseline appresa, punti pesati e fusione anche dopo movimento. | Parti implementate del prototipo non sono ancora validazione fisica. La prima vista del primo stato confermato inizializza la forma senza confronto con forma vuota. |
| R14 e R35 | Rendere simmetrico il contratto FPS-4096, normalizzazione e provenienza per osservazione/memoria; mantenere solo punti osservati nell'accumulo. | La superficie completata non rientra fra i dati osservati. |
| R15/R20/R21 | Indicare D2/correzione esterna come percorso implementato di riferimento, distinguendo fusione appresa/adattamento del matcher come lavoro del punto 2 non attestato concluso. | Non presentare distanza/forza del segnale o architettura finale come già selezionate. |

## Flusso da rappresentare nel dettaglio della memoria

1. Osservazione assegnata alla traccia, punti allineati validi e camera.
2. Compatibilità per riproiezione con stati attivi: prima confermati, poi deboli. Se nessuno compatibile, nuovo stato debole; altrimenti aggiornare quello scelto.
3. Aggiornare supporto/storia e verificare conferma; applicare decadimento/potatura. Stato non confermato: nessuna fusione nella forma persistente.
4. Stato confermato: chiudere gli altri stati confermati attivi. Un ritorno a uno stato chiuso apre un nuovo stato; non è un certificato di movimento o staticità.
5. Forma assente: inizializzarla dalla prima vista dello stato confermato. Forma esistente: usare la trasformazione dello stato, oppure stimarla quando manca, anche dopo spostamento.
6. Il verificatore decide per singola vista se incorporarla. Una vista non ammessa resta associata allo stato; non apre un'altra posizione. Se la posa dello stato non è ancora accettata da alcuna vista, il codice conserva le viste pendenti per un successivo tentativo di registrazione; a posa fissata le respinte non vengono riprovate.
7. Fusione ammessa → punti pesati/celle → nuova versione → FPS/SuperFlex → pubblicazione per frame successivi; fallimento/attesa conserva l'ultima forma valida. Tutte le detection del frame leggono la stessa memoria precedente.

## Organizzazione editoriale

Conservare colori di provenienza, schede a nove campi e distinzione nodi/processi e frecce/dipendenze. Aggiornare sorgenti al codice corrente. Nelle schede usare descrizioni generali; numeri, job, copertura corrente e tempi restano nei resoconti. Se utile, prevedere una vista separata di sviluppo/valutazione: export iniziale → punto 2 → griglia del sistema completo → configurazione congelata → test indipendente. Drive/HPC restano strumenti di produzione, non nuovi passaggi del ciclo per frame.

Prima dell'applicazione: proposta della struttura e dei testi in chat, conferma esplicita di Marco, poi modifica di JSON/copia offline/disegno con backup e controlli di navigazione/collegamenti. Nessuna approvazione scientifica delle soglie o del nuovo matcher implicita nell'aggiornamento grafico.
