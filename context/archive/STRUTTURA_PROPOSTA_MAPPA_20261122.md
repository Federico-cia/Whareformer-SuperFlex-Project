# Struttura proposta della mappa — 22 novembre 2026

**Esito successivo:** Marco conferma struttura e testi e ne richiede l'applicazione; [mappa aggiornata e verificata](../evidence/map_20261122/ESITO_APPLICAZIONE.md). I paragrafi di proposta sotto conservano la provenienza, non uno stato di attesa attuale.

**Proposta non approvata e non applicata.** Revisione concreta della proposta precedente dopo la richiesta di Marco «less is more». Mantiene i **39 riquadri**, senza aggiunte o eliminazioni di nodi; i collegamenti passano da **49 a 53** (sei nuovi, due rimossi). Gli ID esistenti sono riutilizzati; nessuna rinumerazione degli elementi invariati.

**Testi pronti per revisione:** [schede a nove campi](../evidence/map_20261122/TESTI_PER_REVISIONE.md) e [specifica dei testi](../evidence/map_20261122/TESTI_PROPOSTI.json), entrambe bozze non applicate. La verifica del coordinatore precisa il ramo C43: solo il fallimento dichiarato porta alla conservazione e avanzamento; l’attesa richiede prima di risolvere la richiesta, e gli esiti incoerenti sono errori. Non cambia la topologia proposta.

## Criterio di leggibilità

Restano i Rami paralleli. Il ramo forma usa la profondità DA già allineata, invece di mostrare una seconda stima di profondità. Nel ramo inferiore ogni riquadro risponde a una domanda diversa: stato di posizione, conferma, trasformazione, ammissione, aggiornamento della forma. Titoli brevi, un sottotitolo e una spiegazione nelle schede; niente nodo autonomo per decadimento, potatura, ritorno o dettagli del verificatore. MoGE resta confronto nella scheda: il flusso principale rappresenta DA allineata. Non si aggiungono rami di training, Drive o griglia nel ciclo per frame.

## Riquadri: cambiamenti strutturali

| ID | Attuale → proposto | Che cosa rappresenta |
|---|---|---|
| R12 | Geometria stimata da RGB → **Estrai i punti dell’oggetto** | Profondità DA allineata, maschera e intrinseci; processo del progetto, non un secondo modello esterno. |
| R13 | Punti visibili dell’oggetto → **Porta i punti nella scena** | Trasformazione camera → scena tramite posa. |
| R18 | Memoria precedente → **Memoria geometrica precedente** | Un solo riquadro; due componenti nella scheda: stati di posizione e forma persistente. |
| R29 | Punti già in memoria? → **Assegna e aggiorna lo stato** | Diventa un rettangolo: criterio C, scelta dello stato compatibile oppure creazione di uno debole, aggiornamento di supporto/storia. |
| R30 | Inizializza i punti → **Stato confermato?** | Diventa un rombo: conferma già raggiunta o maturata con la nuova osservazione. Non è un certificato di staticità. |
| R31 | Allinea la nuova nuvola → **Prepara le viste per la forma** | Inizializza il riferimento se la forma è vuota; altrimenti riusa o stima la trasformazione dello stato verso la forma. |
| R32 | Fusione ammessa? → **Vista ammessa nella forma?** | Verificatore appreso per vista; non sceglie la posizione. |
| R33 | Conserva punti e forma → **Mantieni la forma precedente** | Forma invariata; lo stato di posizione può essere cambiato. |
| R34 | Unisci i punti osservati → **Aggiorna i punti della forma** | Comprende inizializzazione e fusioni ammesse, con celle/pesi. |
| R36 | Ricostruzione riuscita? → **Ricostruzione disponibile?** | Controlla l’esito; attende richieste pendenti, segnala incoerenze, distingue riuscita e fallimento dichiarato. |
| R39 | Memoria aggiornata per il frame successivo → **Memoria per il frame successivo** | Aspetto/posizione, stati e punti/ultima forma, con versioni distinte. |

Gli altri nove aggiornamenti sono di sottotitolo/scheda: R09 (allineamento già implementato anche per geometria), R14/R35 (FPS-4096 simmetrico), R15/R20 (D2 come percorso attuale, scelta finale aperta), R21 (correzione esterna come riferimento implementato), R28 (punti allineati/camera validi), R37/R38 (completamenti versionati e conservazione sui mancanti). R01–R08, R10–R11, R16–R17, R19 e R22–R27 restano strutturalmente invariati.

## Collegamenti da aggiungere

| ID proposto | Da → a | Etichetta / dipendenza |
|---|---|---|
| C50 | R09 → R12 | Profondità allineata per estrarre i punti. |
| C51 | R03 → R13 | Posa della camera per trasformare i punti nella scena. |
| C52 | R30 → R31 | **Sì**: lo stato confermato può contribuire alla forma. |
| C53 | R30 → R33 | **No**: lo stato resta debole; nessuna fusione nella forma. |
| C54 | R31 → R34 | **Prima vista, forma vuota**: inizializzazione senza confronto con una forma inesistente. |
| C55 | R31 → R33 | **Registrazione fallita**: forma precedente conservata, viste pendenti. |

R31 raggruppa la preparazione delle viste di uno stato: il seme iniziale segue C54; le altre viste seguono C35 verso il verificatore. I due percorsi possono contribuire allo stesso aggiornamento della forma: non richiedono due inferenze SuperFlex separate.

## Collegamenti da togliere

| ID | Collegamento attuale | Perché |
|---|---|---|
| C34 | R29 → R31 | Non si passa alla forma solo perché esistono punti: prima serve la conferma dello stato. |
| C40 | R30 → R35 | Il nuovo R30 è una decisione sullo stato; SuperFlex riceve la nuova forma di punti da R34. |

## Collegamenti da modificare, mantenendone gli estremi

| ID | Da → a | Nuovo significato |
|---|---|---|
| C03 | G01 → R12 | Maschera/intrinseci per l’estrazione, senza seconda inferenza di profondità. |
| C10 | R12 → R13 | Punti dell’oggetto nel riferimento camera. |
| C11 | R13 → R14 | Nuvola osservata allineata da campionare per SuperFlex. |
| C19 | R18 → R20 | Ultima forma/descrittore utilizzabile nel matching. |
| C30 | R13 → R28 | Nuvola nel riferimento scena con camera/provenienza necessarie ai controlli successivi. |
| C31 | R28 → R29 | **Sì**: input valido per assegnare e aggiornare lo stato. |
| C32 | R18 → R29 | Stati attivi precedenti, viste/camere di riferimento e supporto. |
| C33 | R29 → R30 | Stato scelto/creato e aggiornato; eliminare la vecchia etichetta **No**. |
| C35 | R31 → R32 | **Viste da verificare**: punti nel riferimento della forma e trasformazione. |
| C36 | R28 → R33 | **No**: input non utilizzabile, senza nuova fusione. |
| C37 | R32 → R33 | **No**: esclusione dalla forma, senza aprire un'altra posizione. |
| C38 | R32 → R34 | **Sì**: punti ammessi per l'aggiornamento. |
| C39 | R34 → R35 | Nuova versione della nuvola, iniziale o aggiornata. |
| C43 | R36 → R38 | **Fallita**: fallimento dichiarato. L’attesa non permette ancora di avanzare; gli esiti incoerenti sono errori. |
| C45 | R33 → R39 | Forma conservata con eventuali stati aggiornati. |
| C49 | R39 → R18 | Snapshot geometrico per il frame successivo, compresi gli stati. |

Gli altri 31 collegamenti restano negli stessi percorsi. Titoli/etichette descrittive che citano un nodo rinominato andranno sincronizzati con il nuovo titolo, senza introdurre ulteriori dipendenze.

## Dettagli nelle schede, non nuovi riquadri

- Priorità agli stati confermati, poi deboli; supporto, decadimento e potatura. Alla conferma in una posizione si chiudono gli altri stati confermati; tornare a uno stato chiuso apre un nuovo stato.
- Una vista respinta rimane associata allo stato. A posa fissata non si riprova; se nessuna vista ha ancora accettato la posa candidata, le viste restano pendenti per un nuovo tentativo di registrazione.
- Il primo punto di avvio è la prima vista del primo stato confermato, non una prima vista mantenuta per sempre come riferimento privilegiato.
- La forma contiene soltanto punti osservati ammessi. SuperFlex non introduce i completamenti nei punti da fondere. Forma assente o non aggiornata non blocca il tracking baseline.
- Le detection del frame leggono lo stesso snapshot precedente; completamenti nuovi solo nel futuro. Un fallimento dichiarato conserva l'ultima forma valida e i punti ammessi aggiornati. L’attesa conserva la forma ma richiede di risolvere la richiesta prima del frame successivo.
- Verificatore e test di posizione sono implementazioni sperimentali; conferma dello stato e successo software non provano staticità, validità fisica o efficacia tracking. Nessun numero di job, campagna o risultato contingente nelle schede generali.

## Verifiche e limiti della proposta

Specifica completa e grafo astratto in [STRUTTURA_PROPOSTA.json](../evidence/map_20261122/STRUTTURA_PROPOSTA.json); [controlli](../evidence/ASSET_ESTERNI.md#asset-a495d8954cfa): conteggi 39/53, ID unici, estremi esistenti, sei percorsi rappresentativi e sei file della mappa invariati per SHA256. I testi completi sono nel documento di revisione collegato sopra; non è ancora un nuovo disegno verificato graficamente. Approvazione della struttura e revisione dei testi restano fasi distinte. Fonte esecutiva: position_state_memory.py, _update/_fuse_views; per metodo e decisioni correnti leggere [specifica](../memory/MEMORIA_OPZIONE_A_E_SELEZIONE_20261122.md) e [registro](../memory/REGISTRO_DECISIONI.md).
