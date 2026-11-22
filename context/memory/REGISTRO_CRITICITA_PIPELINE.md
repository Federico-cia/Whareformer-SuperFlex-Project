# Registro dei punti critici della pipeline

## Compattazione verificata; limite di capacità ancora aperto — 22 novembre 2026

[Migrazione e audit conclusi](../archive/COMPATTAZIONE_HPC_20261122.md): 46080 derivati non conservati per intero ma rigenerabili esattamente su CPU; circa 3.3 GiB netti recuperati, quota 41.92/46.56 GiB, circa 440040/500000 inode. Conservazione futura abilitata senza modifiche scientifiche; campagna a 15/216 e coda vuota all'ultimo controllo. Risparmio insufficiente: proiezione corrente ordine 160 GiB e 1.85 milioni di inode. Da risolvere conservazione/consumo delle mappe dopo allineamento, contenitori e capacità persistente prima di rilanciare. I requisiti scientifici e lo stato del prototipo del punto 3 sono trattati separatamente nelle relative revisioni.

## Capacità degli output: blocco operativo verificato — 22 novembre 2026

L'ultimo [controllo HPC](../archive/CONTROLLO_HPC_20261122.md) supera gli stati storici: 15/216 blocchi, coda vuota e stop preventivo per quota, 45.30/46.56 GiB e 485960/500000 file. Circa 0.64 GiB/blocco misurati: formato corrente incompatibile con l'intera campagna nella quota personale. Ridondanze di cache e artefatti confermate da codice e campioni; [analisi e proposta di conservazione](../archive/GESTIONE_SPAZIO_HPC_20261122.md). Prossimo passo: prova compatta isolata, budget complessivo e adattamento della ripartenza. Non risolto, nessun rilancio o cambio scientifico; non equiparare parametri SuperFlex a geometria osservata.

## Audit acquisito; arricchimento fermo — 21 novembre 2026, esiti 23:01–23:06

Marco esegue gli script: **783586 COMPLETED 0:0, 16m53s**, sette hash verificati; 446 osservazioni, 438 allineamenti validi e nuvole locali finite, otto fit con alpha negativo. Confronto appaiato su 415 coppie: sovrapposizione mediana 3.27% grezza → 22.80% allineata (28.08% → 68.16% nel terzile di minore spostamento, non staticità certificata). 24 osservazioni con sole maschere del catalogo. Nessuna etichetta di fusione corretta ancora certificata: mantenere limiti di staticità, simmetrie ed errori condivisi. [Risultati, provenienza e interpretazione](../archive/RISULTATI_AUDIT_AMMISSIONE_20261121.md).

**Arricchimento:** coda vuota, 8/216 blocchi, nessun riepilogo finale; riprese 783490 e 783491 entrambe FAILED 1:0. Causa non identificata dai log disponibili. Aggiornata la diagnosi di sola lettura per questi job e per gli stadi parziali; prossimo intervento di Marco: `strumenti_hpc/esegui_diagnosi_hpc.bat`, poi leggere `esito_diagnosi.txt` prima di riprendere. Nessun accesso diretto HPC, invio o training dell'assistente. Le nuvole locali consentono di proseguire la preparazione dei dati da trasformazioni note senza attendere la run completa. Decisioni metodologiche approvate invariate.


## Punto 3: prima implementazione autorizzata ed eseguita — 21 novembre 2026

Marco autorizza di procedere secondo il piano approvato iniziando dalle parti indipendenti dall'audit. Implementati allineamento DA→scena con fallimento esplicito, memoria pesata a stati senza vista fissa, separazione forma/collocazione e percorso esplicito dopo spostamento, FPS 4096 con provenienza, contratti del verificatore, baseline regressiva addestrabile e replay/adapter del coordinatore. [Dettagli, verifiche e limiti](../archive/IMPLEMENTAZIONE_PUNTO3_20261121.md); [guida software](../../integration_prototype/SCENE_MEMORY.md).

**Verificato localmente:** 105 casi, 103 superati e 2 saltati per motmetrics, inclusi 23 nuovi test tutti passati; nessuna inferenza neurale reale. Il verificatore principale non è addestrato: senza modello non si confermano/fondono ipotesi. Mancano evidenze validate di staticità, calibrazione sullo sviluppo, collegamento FPS al worker SuperFlex e validazione reale dopo spostamento. Il runner storico resta distinto e invariato nei suoi algoritmi; la nuova memoria non è già la pipeline sperimentale completa.

**Audit/HPC:** nessun accesso diretto o job in questa fase; stato live ignoto. Marco deve avviare `strumenti_hpc/esegui_controllo_hpc.bat` e `esegui_scarica_audit.bat`; scarico aggiornato per il job 783586, con accounting, hash e log anche parziali, nuova cartella a ogni tentativo. Poi interpretare gli esiti prima di training/ripresa. Nessun nuovo metodo principale, parametro calibrato, modifica della mappa o pubblicazione. Log e ricevuta in `outputs/point3_implementation_20261121/`.


## Ricognizione di ripresa — 21 novembre 2026

Confrontati riassunto dell'altra chat, documenti correnti, codice, ricevute locali e schede della mappa. [Stato consolidato, differenze e limiti dell'audit](../archive/RICOGNIZIONE_RIPRESA_PUNTO3_20261121.md). Nessuna nuova scelta o esecuzione: piano approvato del verificatore/memoria ancora da implementare nei moduli correnti, che conservano gate fissi e prima vista. Scala 9–23% = variabilità del rapporto allineata/grezza, non errore vero certificato. Audit: staticità non certificata; errore denominato di superficie è spostamento punto a punto, non invariante alle simmetrie; non esporta tutte le pose candidate. Tenerne conto prima di costruire target.

Stato HPC corrente NON verificato: ultima verifica documentata squeue vuota, senza accounting/esiti successori; RUNNING storici non attuali. Prossimo passo: controllo e scarico audit avviati da Marco con gli script predisposti; assistente senza accesso diretto HPC. Preservate tutte le decisioni approvate e la storia; nessun training, job o pubblicazione in questa ricognizione.


## Criteri di ammissione appresi — indicazione di Marco, 21 novembre 2026

Marco richiede che le soglie di accettazione siano apprese dai dati anziché imposte manualmente; obiettivo esplicito conservare viste parziali valide. Richiede spiegazione di parzialità, ambiguità, regole correnti e alternative di validazione con pro/contro. Direzione approvata: apprendimento del criterio; modello, target, loss e protocollo non ancora scelti. Nessun training, codice, soglia o job modificati.

Verificato cloud_memory.py/cloud_updater.py: trasformazione rigida senza stima scala; supporto in entrambe le direzioni almeno 0.65 entro 0.08R; q90 dell'80% più vicino non oltre 0.15R; alternative entro 5% dello score più epsilon rifiutate se differiscono oltre 15 gradi o spostano il centroide oltre 0.08R. Basta un gate fallito. R è il raggio RMS del riferimento fit; rapporto dei raggi registrato, non gate autonomo. Query separate dal fit, non viste indipendenti. Inizializzazione senza confronto con memoria precedente, con soli controlli di validità dell'input.

Proposte da discutere: classificatore leggero sulle diagnostiche, criterio condizionato alla sovrapposizione/affidabilità dei punti, oppure apprendimento dell'utilità della fusione. Evitare target ricavati dai gate stessi: replicherebbero le euristiche. Identità oracle non certifica posa o scala. Possibile supervisione automatica con trasformazioni note su dati sintetici/crop, verifiche RGB multivista e viste reali escluse; limiti rispettivi: domain gap, dipendenza da pose/visibilità/movimento, validazione geometrica reale non ancora disponibile. Vincolo precedente di nessuna nuova annotazione manuale preservato. Separare dati per oggetto/sequenza e valutare errori di ammissione/rifiuto e qualità della memoria; nessuna opzione già adottata. Fonti primarie consultate per fattibilità concettuale, non compatibilità EPIC verificata: PREDATOR (CVPR 2021, overlap appreso) e Deep Global Registration (CVPR 2020, affidabilità delle corrispondenze appresa).


## Priorità e divisione del lavoro aggiornate — 21 novembre 2026

Marco comunica che il compagno segue il punto 2 (integrazione della forma nel matcher), mentre Marco prende in carico il punto 3 (ammissione dei punti nella memoria geometrica). Punti 1 (confronto delle forme) e 4 (collocazione/aggiornamento nella scena) dopo la risoluzione di entrambi. Richiede di procedere sul punto 3 iniziando dal recap di stato e criticità: superato il precedente rinvio della revisione dei gate, conservato sotto come storia. Nessuna nuova soglia, alternativa o protocollo già adottati; nessuna modifica del codice o nuovo job in questo passaggio. Nessun metodo o risultato del compagno comunicato.

Ricognizione conclusa sui resoconti esistenti: 31 fusioni DA/40 MoGE per variante nella campagna, senza validazione fisica indipendente; audit del prefisso con rifiuti per sola ambiguità e sovrapposizione asimmetrica compatibile con parzialità. Prossimo passo proposto, da definire: validazione indipendente di ammissioni e rifiuti, distinguendo simmetrie, parzialità, scala e identità. I controlli di scala necessari alla registrazione restano nel punto 3. Evidenze e limiti in [campagna](../archive/RISULTATI_CAMPAGNA_HPC_20261115.md) e [audit](../archive/RIPRESA_HPC_20261114.md). Nessun nuovo esito sperimentale; stato del job di arricchimento non ricontrollato.


Aggiornamento: 14 novembre 2026. Mandato esplicito di Marco: prima un round completo, poi risoluzione sistematica di dubbi e tradeoff. Massima aderenza ai due paper: mantenere l’approccio originale quando applicabile e funzionante; annotare alternative senza adottarle come ottimizzazione preventiva. Integrazione riuscita è un obiettivo da verificare, non un risultato presunto.

## C13 — Collocazione e aggiornamento della forma nella scena: discussione richiesta

Marco indica come preoccupazione principale la difficoltà di collocare la ricostruzione con dimensioni, rotazione e posizione corrette nello spazio della scena e mantenerla aggiornabile con nuove nuvole. La memoria dei punti e il confronto D2 non certificano questa capacità. Distinguere coordinate normalizzate SuperFlex, camera dell'osservazione, riferimento della memoria oggetto e scena; conservare e verificare trasformazioni e compatibilità della scala, anche con movimento dell'oggetto. Invertire la normalizzazione ripristina il riferimento dell'input, non garantisce da solo scala fisica o coerenza con gli XYZ ufficiali. Stato: tema prioritario da discutere e sottoporre a verifica di fattibilità, non errore dimostrato di tutti gli output né nuovo modulo approvato. Collegato a C05/C06/C09 e ai to-do importanti; nessun esperimento avviato.

## Regola di lavoro

Precisazione C05 durante E22: discussione con il compagno esplicitamente richiesta prima della scelta definitiva dell'ammissione. Le descrizioni proposte per E22/B16 devono distinguere assegnazione dell'identità, stima dell'allineamento e gate provvisori; richiamare alternative e decisione pendente senza attribuire alle euristiche attuali una validazione scientifica o un accordo finale del gruppo.

Priorità ribadita da Marco il 15 novembre durante la revisione della mappa: C05, ammissione geometrica, deve essere discusso approfonditamente e testato; attività in evidenza in TODO.md. La richiesta rafforza l'importanza del tema senza avviarne ora l'esecuzione o revocare implicitamente il rinvio dei filtri. Distinguere associazione, registrazione e ammissione e verificare sia false ammissioni sia falsi rifiuti.

Per ogni scostamento o problema registrare: metodo del paper/codice originale effettivamente verificato, implementazione corrente, motivo della differenza, conseguenza, evidenza disponibile e verifica pendente. Non attribuire ai paper scelte nostre. Separare errore dimostrato, dubbio da controllare e compromesso provvisorio. Dopo la prima run affrontare i punti registrati, senza rimandare silenziosamente quelli che impediscono la correttezza del risultato.

Riferimenti locali: [Whareformer](../evidence/ASSET_ESTERNI.md#asset-c1e0aaa7afc9), [SuperFlex](../evidence/ASSET_ESTERNI.md#asset-e907ecf17e92), [base scientifica](../archive/LETTURA_E_BASE_SCIENTIFICA.md), [ciclo approvato](ROADMAP_CICLO_GEOMETRICO.md). Questa prima lista riprende evidenze già acquisite e letture del codice; non certifica una nuova verifica integrale di tutte le sezioni dei paper.

## Punti aperti iniziali

| ID | Evidenza o dubbio | Impatto sulla prima run | Azione e stato |
|---|---|---|---|
| C01 | Il frontend attuale importa cache verificate; non rigenera l’intera sequenza da RGB. | Blocca la dichiarazione di esecuzione completa dalle immagini. | Completare l’ingresso con gli estrattori originali; tenere distinti artefatti rigenerati e riusati. Aperto. |
| C02 | I tre file ufficiali Whareformer P01_01 sono disponibili e hanno hash registrati; il vecchio preparatore locale aveva un arresto esplicito a 7508. | I dati baseline completi esistono; il limite di preparazione è nostro, non del paper. | Preparazione generica con scope completo e controllo di conteggi/copertura. Non ripubblicare il vecchio runner rigido come interfaccia corrente. Aperto. |
| C03 | La geometria già verificata è sparsa: 71/73 join esatti, non geometria disponibile per tutte le osservazioni del video. | Una run intera con fallback prevalente non dimostra integrazione geometricamente attiva su tutto il video. | Misurare e dichiarare copertura per frame/oggetto/stadio; generare gli input mancanti previsti dal protocollo. Aperto. |
| C04 | PCA locale presente, ma provenienza rispetto alle feature ufficiali non certificata; DINOv2/revisione e scala scena da verificare. | Differenze di baseline possono contaminare il confronto e impedire replica numerica. | Usare il metodo originale; distinguere replica da nuova rigenerazione. Nessun fit PCA o sostituzione modello impliciti. Aperto. |
| C05 | Gate di fusione scelti dall’assistente come diagnostica provvisoria, non prescritti dai due paper; 12 proposte respinte nel pilota a quattro rappresentazioni. | Il programma può terminare senza dimostrare accumulo multivista. | Registrare motivi e distinguere associazione/fusione. Revisione esplicitamente rinviata da Marco: nessuna modifica ora. Aperto, rinviato. |
| C06 | Descrittori di confronto, correzione dei logits, registrazione e politica di accumulo collegano modelli che i paper non integrano già in questa forma. | Non è corretto presentare ogni dettaglio del ponte come replica del paper. | Mappare componenti riusate e adattamenti del nostro contributo; mantenere semplice l’adattamento e verificarne causalità. Aperto. |
| C07 | Sei inferenze SuperFlex reali già acquisite sono da inizializzazioni singole; il checkpoint/config robust verificati non certificano automaticamente ogni variante di completamento discussa nel paper. | Non rivendicare ricostruzione multivista o specifico protocollo di completion senza verifica. | Dichiarare variante/checkpoint e input; confrontarli con la sezione pertinente del metodo prima delle nuove inferenze. Aperto. |
| C08 | IDF1/mPCL riproducono il protocollo originale per nomi e XYZ stimati; risultato corrente da P01_01 train, non test indipendente. | La run dimostra esecuzione; non dimostra da sola miglioramento o generalizzazione. | Conservare metriche originali e limiti, separare successivo sviluppo/test. Aperto. |
| C09 | Replay/cache e ricostruzione della scena non equivalgono a pipeline strettamente online; maschere/camera/asset sono ingressi dichiarati. | Non descrivere la prima prova come video arbitrario RGB-only o inferenza online completa. | Dichiarare preprocessing, provenienza, tempi inclusi/esclusi e costi dei replay. Aperto. |

## Cosa dovrà mostrare il primo resoconto

Inizio/fine e copertura della sequenza; configurazione usata; componenti originali e adattamenti; input generati/riusati/mancanti; associazioni e aggiornamenti separati; ricostruzioni riuscite/fallite; rifiuti e fallback; output finali; dubbi rimasti e loro conseguenze. Una run terminata, una fusione multivista verificata e un beneficio misurato sono evidenze distinte.
## Aggiornamento operativo: primo full-video attivo

- **C01/C04/C09 — compromesso dichiarato:** riusati feature ufficiali/PCA/XYZ e geometrie per osservazione con hash; nuova rigenerazione da RGB non eseguita. La prima run verifica il ciclo integrato da tali ingressi e non la provenienza retrospettiva dei JPEG o la parità di una nuova PCA. DINOv2/PCA/scena restano dipendenze del frontend rigenerato, non sostituite.
- **C02 — preparazione completa verificata:** rimosso il limite operativo del vecchio preparatore, mantenuto come storico locale; nuovo comando prepara 33310 frame e 110590 osservazioni, zero differenze di ordine/metadati/XYZ dal riferimento condiviso.
- **C03 — copertura misurata:** 71 osservazioni geometriche su 110590 (circa 0.0642%), 38 frame su 33310. Il fallback prevale: una run conclusa non proverà funzionamento geometrico su ogni frame né una copertura sufficiente per efficacia generale.
- **C05 — rinvio rispettato:** gate/registratore invariati; saranno registrate inizializzazioni, fusioni e rifiuti separatamente, senza allentare soglie per produrre un risultato positivo.
- **C06/C07 — fonti rilette:** PDF Whareformer §§3.2–3.7 (pp. 5–8), SuperFlex §§4.1–4.3 e 5.3 (pp. 5–8 e 12), confrontati con codice originale. Riusati matcher/softmax/assegnazione greedy originali e checkpoint robust feed-forward. Ponte D2/correzione logits/registrazione/memoria temporale sono adattamenti nostri. Il campionamento casuale a 4096 punti segue la demo originale disponibile, non il FPS del benchmark canonico; orientamento EPIC non canonico, nessuna ottimizzazione test-time con occupazione completa.
- **C10 — orizzonte video/protocollo:** CSV originale riporta 99135 frame a 59.94 fps, convertiti a 60 secondo Config; feature ufficiali fra 937 e 98099. La copertura completa riguarda tutti i frame con osservazioni del protocollo. Verificare valutazione finale con orizzonte 99135 come nell'originale; non confondere ultimo frame osservato e fine nominale del video.

Job 764454 avviato; nessuna fusione o metrica nuova ancora dichiarata. Prossima verifica: esito, causalità delle query, differenze reali dei logits e uso futuro delle ricostruzioni, memoria dei soli punti osservati, copertura e report finale.

## Esito della prima run completa — supera lo stato di attesa precedente

764454/764474 conclusi 0:0; dettagli nel resoconto della prima run completa.

- **C01/C03/C04/C09 aperti:** percorso completo da cache dichiarate, non nuova estrazione RGB; 71 geometrie/38 frame, fallback prevalente. Il limite non viene nascosto dalla chiusura software.
- **C02 risolto per questa preparazione:** intera sequenza ufficiale verificata/elaborata, 33310 frame/110590 osservazioni.
- **C05 aggiornato, revisione ancora rinviata:** sette fusioni effettivamente ammesse con gate identici; 46 rifiuti, ragioni sovrapposte (supporto 39, residui 33, ambiguità 34). Non si conferma più zero fusioni per questa nuova run. Validazione indipendente delle pose/identità ancora necessaria.
- **C06/C07 verificati operativamente nei limiti dichiarati:** 25 inferenze reali nuove, 695 correzioni non nulle, 76 confronti futuri con ricostruzioni da fusioni. Memoria finale ricostruibile dai soli dati osservati e trasformazioni. Questo non misura accuratezza 3D né certifica il dominio EPIC del checkpoint robust.
- **C08 esito nullo del tracking:** zero assegnazioni diverse dalla baseline registrata; metriche identiche, non miglioramento. Peso 0.1 provvisorio, non calibrare retrospettivamente la prima run per ottenere un beneficio.
- **C10 corretto:** la valutazione automatica iniziale usava erroneamente ultimo frame osservato 98099; quella autorevole è final_evaluation con 99135, convenzione originale. Predizioni preservate e non rigenerate.
- **Verifica numerica locale:** uguaglianza bit a bit della ricostruzione indipendente dei punti falliva per moltiplicazione matriciale Windows/Linux (massimo 2.22e-16). Limite di verifica derivato dall'aritmetica float64, non gate di fusione, ora esplicito; hash degli artefatti e uguaglianza memoria/richiesta restano esatti.

## C11 — segno e disponibilità della correzione geometrica

**Revisione successiva del 16 novembre:** Marco richiede entrambe le prove, esterna e con riaddestramento, usando esclusivamente dati già etichettati; nessuna nuova etichettatura manuale. Target oracle originali riusabili in principio; storia geometrica da collegare/rigenerare, costo e accesso completo da verificare. [Fattibilità e distanze](../archive/FATTIBILITA_DUE_INTEGRAZIONI_20261116.md), [registro storico, voce 81](../archive/prima_consolidamento_20261122/REGISTRO_DECISIONI.md#81-tentare-entrambe-le-integrazioni-senza-nuove-etichette-manuali--16-novembre-2026). Export SuperFlex concatena primitive: superfici interne possono influenzare i descrittori. D2/Chamfer candidati, nessuna nuova correzione, soglia o efficacia dimostrata.

Discussione del 16 novembre: proposta stima supervisionata di peso/riferimento neutro oppure adattamento interno del matcher; nessuna opzione adottata. Prima verificare target e join alle geometrie, senza usare track predette come verità. [Analisi e limiti](../archive/DISCUSSIONE_INTEGRAZIONE_FORMA_20261116.md); [registro storico, voce 80](../archive/prima_consolidamento_20261122/REGISTRO_DECISIONI.md#80-richiesta-di-una-stima-giustificata-del-peso-e-dei-dati--16-novembre-2026). C11 resta aperto, nessuna nuova evidenza di beneficio.

**Evidenza verificata dopo la run:** shape_adapter.py applica peso × (distanza neutra − distanza), solo alle track con confronto valido; Nuova track invariata. Con 0.1/0, tutte le 695 correzioni sono negative (mediana assoluta 0.00629963, massimo 0.03434743). Le coppie senza geometria restano direttamente invariate. **Conseguenza:** possibile vantaggio relativo per Nuova track o track senza geometria; non è stato osservato alcun cambio di assegnazione in questa run. **Compromesso:** configurazione della prima run conservata, nessun aumento automatico del peso. **Verifica necessaria:** margini originali/corretti, discriminatività delle distanze e comportamento con geometria mancante; non basta aumentare il peso finché cambia la metrica. Analisi e alternative in [VALUTAZIONE_PRIMA_RUN_20261114.md](../archive/VALUTAZIONE_PRIMA_RUN_20261114.md).

**Precisazione dei rifiuti:** 53 tentativi di fusione successivi alle 18 inizializzazioni, sette ammessi e 46 respinti; sette rifiuti per sola ambiguità. Le sette fusioni si concentrano su due track predette. Il denominatore 71 include le inizializzazioni e non va usato come numero dei tentativi di fusione. Revisione dei gate ancora rinviata.

## Campagna estesa del 15 novembre 2026

- **C03:** campione aumentato a 247 frame/446 osservazioni selezionate prima dei modelli. Copertura pronta da misurare; disponibilità/target categorie non rappresentativi dell'intero video. Feature/XYZ riusati, geometria rigenerata solo sul campione.
- **C11:** griglia finita peso 0.1/1, distanza neutra 0/0.1 e nuova telemetria di logits/margini/probabilità per distinguere scala e disponibilità. Nessuna modifica del termine o calibrazione sul test; ranking sullo stato della run non equivale a baseline indipendente dopo divergenze.
- **C12 — limite HPC verificato:** array respinto da QoS (quattro job inviati/due attivi). Conseguenza: il primo gestore aveva inviato solo geometria/build. Ricevuta parziale conservata; recupero con gruppi seriali, 764678/764679 accettati, riepilogo inviato al termine di un gruppo. Verifica pendente: completamento catena, ID/stato del riepilogo e successo effettivo di tutti i trial; nessun risultato anticipato.
- **Vincoli:** C05 resta rinviato, nessuna revisione di filtri o registratore. Campagna di sviluppo su P01_01; niente nuova PCA, training, identità fisica inventata o interpretazione dei completamenti come osservazioni.

Dettaglio operativo in [CAMPAGNA_HPC_20261115.md](../archive/CAMPAGNA_HPC_20261115.md).

**Aggiornamento verificato della campagna:** 764674/764675 conclusi 0:0, tutte le 446 geometrie pronte per entrambe le sorgenti e feature baseline byte-identiche; gruppi 764678/764679 RUNNING. Copertura effettiva 0.4033%, ancora sparsa; nessun risultato finale delle varianti anticipato.

## Esito finale campagna — 15 novembre 2026

C12 chiuso per questa esecuzione: tutti i job, incluso riepilogo 765084, conclusi 0:0; 29/29 trial completati. C11 resta aperto: tutte le configurazioni, anche con peso 1 e distanza neutra 0.1, lasciano invariate le assegnazioni; occorre distinguere margini, copertura dei casi difficili e discriminatività, senza assumere una causa. Nessun vincitore o miglioramento rilevato. Fusioni per variante DA 31/MoGE 40, non repliche indipendenti né validazione fisica. C03 copertura 0.4033%, C05 revisione filtri ancora rinviata. Nessun job di questa campagna attivo/in attesa.

## C05 — riferimento di posa disponibile, 21 novembre 2026

La registrazione attuale opera in coordinate camera senza pose e con scala DA inter-vista non verificata, sebbene pose EPIC-Fields e mesh di scena siano disponibili per P01_01. Possibile contributo ai rifiuti per supporto/residui (scala) da verificare, non dimostrato. Le pose offrono un riferimento indipendente di posa relativa solo per oggetti statici. Analisi: [SUPERVISIONE_AMMISSIONE_20261121.md](../archive/SUPERVISIONE_AMMISSIONE_20261121.md).
