# Registro dei punti critici della pipeline

Aggiornamento: 14 novembre 2026. Mandato esplicito di Marco: prima un round completo, poi risoluzione sistematica di dubbi e tradeoff. Massima aderenza ai due paper: mantenere l’approccio originale quando applicabile e funzionante; annotare alternative senza adottarle come ottimizzazione preventiva. Integrazione riuscita è un obiettivo da verificare, non un risultato presunto.

## Regola di lavoro

Per ogni scostamento o problema registrare: metodo del paper/codice originale effettivamente verificato, implementazione corrente, motivo della differenza, conseguenza, evidenza disponibile e verifica pendente. Non attribuire ai paper scelte nostre. Separare errore dimostrato, dubbio da controllare e compromesso provvisorio. Dopo la prima run affrontare i punti registrati, senza rimandare silenziosamente quelli che impediscono la correttezza del risultato.

Riferimenti locali: [Whareformer](https://arxiv.org/abs/2607.08537), [SuperFlex](https://arxiv.org/abs/2607.01015), [base scientifica](../archive/LETTURA_E_BASE_SCIENTIFICA.md), [ciclo approvato](ROADMAP_CICLO_GEOMETRICO.md). Questa prima lista riprende evidenze già acquisite e letture del codice; non certifica una nuova verifica integrale di tutte le sezioni dei paper.

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

**Evidenza verificata dopo la run:** shape_adapter.py applica peso × (distanza neutra − distanza), solo alle track con confronto valido; Nuova track invariata. Con 0.1/0, tutte le 695 correzioni sono negative (mediana assoluta 0.00629963, massimo 0.03434743). Le coppie senza geometria restano direttamente invariate. **Conseguenza:** possibile vantaggio relativo per Nuova track o track senza geometria; non è stato osservato alcun cambio di assegnazione in questa run. **Compromesso:** configurazione della prima run conservata, nessun aumento automatico del peso. **Verifica necessaria:** margini originali/corretti, discriminatività delle distanze e comportamento con geometria mancante; non basta aumentare il peso finché cambia la metrica. Analisi e alternative in [VALUTAZIONE_PRIMA_RUN_20261114.md](../archive/VALUTAZIONE_PRIMA_RUN_20261114.md).

**Precisazione dei rifiuti:** 53 tentativi di fusione successivi alle 18 inizializzazioni, sette ammessi e 46 respinti; sette rifiuti per sola ambiguità. Le sette fusioni si concentrano su due track predette. Il denominatore 71 include le inizializzazioni e non va usato come numero dei tentativi di fusione. Revisione dei gate ancora rinviata.

## Campagna estesa del 15 novembre 2026

- **C03:** campione aumentato a 247 frame/446 osservazioni selezionate prima dei modelli. Copertura pronta da misurare; disponibilità/target categorie non rappresentativi dell'intero video. Feature/XYZ riusati, geometria rigenerata solo sul campione.
- **C11:** griglia finita peso 0.1/1, distanza neutra 0/0.1 e nuova telemetria di logits/margini/probabilità per distinguere scala e disponibilità. Nessuna modifica del termine o calibrazione sul test; ranking sullo stato della run non equivale a baseline indipendente dopo divergenze.
- **C12 — limite HPC verificato:** array respinto da QoS (quattro job inviati/due attivi). Conseguenza: il primo gestore aveva inviato solo geometria/build. Ricevuta parziale conservata; recupero con gruppi seriali, 764678/764679 accettati, riepilogo inviato al termine di un gruppo. Verifica pendente: completamento catena, ID/stato del riepilogo e successo effettivo di tutti i trial; nessun risultato anticipato.
- **Vincoli:** C05 resta rinviato, nessuna revisione di filtri o registratore. Campagna di sviluppo su P01_01; niente nuova PCA, training, identità fisica inventata o interpretazione dei completamenti come osservazioni.

Dettaglio operativo in [CAMPAGNA_HPC_20261115.md](CAMPAGNA_HPC_20261115.md).

**Aggiornamento verificato della campagna:** 764674/764675 conclusi 0:0, tutte le 446 geometrie pronte per entrambe le sorgenti e feature baseline byte-identiche; gruppi 764678/764679 RUNNING. Copertura effettiva 0.4033%, ancora sparsa; nessun risultato finale delle varianti anticipato.

## Esito finale campagna — 15 novembre 2026

C12 chiuso per questa esecuzione: tutti i job, incluso riepilogo 765084, conclusi 0:0; 29/29 trial completati. C11 resta aperto: tutte le configurazioni, anche con peso 1 e distanza neutra 0.1, lasciano invariate le assegnazioni; occorre distinguere margini, copertura dei casi difficili e discriminatività, senza assumere una causa. Nessun vincitore o miglioramento rilevato. Fusioni per variante DA 31/MoGE 40, non repliche indipendenti né validazione fisica. C03 copertura 0.4033%, C05 revisione filtri ancora rinviata. Nessun job di questa campagna attivo/in attesa.
