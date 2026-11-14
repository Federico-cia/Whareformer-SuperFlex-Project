# Sviluppo del ciclo geometrico Whareformer–SuperFlex

## Frontend approvato e percorso cache verificato — 14 novembre

Ok di Marco ricevuto. Implementati contratto e import cache verificato, ingresso --frontend-manifest nel comando unico; dieci detection nei tre frame con intera storia di 3398 frame, quattro file dati byte-identici. 72 casi locali (70 passati, due skip motmetrics). Rigenerazione da RGB ancora non eseguita: pesi/revisione DINOv2, provenienza PCA e scala/ambiente scena da verificare, inventario circoscritto senza prova di assenza globale. [Avanzamento e limiti](FRONTEND_AVANZAMENTO_20261114.md). Piano parzialmente eseguito, non dichiarato completo; filtri invariati. 763531 concluso 0:0 in 23m24s, nove varianti zero completate e valutate; nessun nuovo job del frontend. Le note di attesa dell’ok e job ancora attivo sono storiche.

## Piano frontend preparato, attesa dell’ok — 14 novembre

Marco richiede pianificazione prima dell’esecuzione. Proposto collegamento preprocessing → runner: inventario dipendenze, manifest unico, import/rigenerazione con cache, comando unico e piccolo pilota P01_01 mantenendo la storia del tracker. [PIANO_FRONTEND_UNIFICATO_20261114.md](PIANO_FRONTEND_UNIFICATO_20261114.md). Piano non ancora approvato: nessuna implementazione o nuovo job per questo step prima dell’ok. Filtri ancora rinviati; job precedentemente autorizzati invariati, senza nuovo controllo di stato in questa fase.

## Valutatore e comando unico collegati — 14 novembre

Implementati export delle osservazioni/assegnazioni con hash, IDF1/mPCL originali con scope esplicito e comando input preparati → varianti → valutazione → tabella. 763498 COMPLETED/0:0 (33 s), otto test; 763530 COMPLETED/0:0 (45 s), 69 test tutti eseguiti, riprodotti IDF1 73.269735% e mPCL 70.465504% su predizioni registrate train. 763531 RUNNING a 10m50s nell’ultima osservazione: nove configurazioni zero, CPU e cache esistente; esito ancora da acquisire. [COMPLETAMENTO_PIPELINE_20261114.md](COMPLETAMENTO_PIPELINE_20261114.md).

**GPU concluso:** 763324 COMPLETED/0:0 (43m30s), sei ricostruzioni reali ready e controllo zero esatto, ma nessuna fusione multivista ammessa. Filtri invariati e revisione ancora rinviata. Mancano unificazione del frontend dati, copertura sufficiente e calibrazione/test; il comando attuale parte da input preparati. Le precedenti note di metriche non collegate e GPU ancora attivo sono storiche.

**Revisione esplicita del 14 novembre:** Marco richiede di rivedere i filtri provvisori di fusione, ma rimanda il lavoro. Attività pendente in [TODO.md](TODO.md); nessuna revisione delle soglie o del codice da avviare in questa fase.

## Runner comune e misure implementati — 14 novembre

Disponibili W0/G0/S-separata/S-accumulo/P-accumulo, DA/MoGE, memorie e modelli indipendenti, controllo sui punti ammessi e report JSONL/JSON/CSV con copertura, fallimenti, byte di payload e costi dei replay. 58 test locali superati; esempio a peso zero, tracking metrics ancora non calcolate. Nessuna nuova run reale del runner comune né modifica dei job esistenti. [RUNNER_VARIANTI_20261114.md](RUNNER_VARIANTI_20261114.md). Prossimo: collegare valutatore tracking e protocollo/copertura di calibrazione-test.

**HPC verificato durante il lavoro:** 763322 COMPLETED/0:0 (9m56s), 763323 COMPLETED/0:0 (12m11s), zero esatto; nel secondo solo 12 inizializzazioni e 12 rifiuti, nessuna fusione, conteggi sulle quattro rappresentazioni. 763324 RUNNING a 29m19s con almeno un risultato neurale reale ready; esito complessivo ancora da acquisire. [Dettagli HPC](RIPRESA_HPC_20261114.md). Le indicazioni precedenti di job CPU attivi/GPU in attesa sono storiche.

## Piano d'azione approvato: selezione e calibrazione autonome — 14 novembre

Marco approva l'ottimizzazione autonoma di parametri e scelta del metodo, il confronto finito delle alternative e la selezione in due fasi. Ogni fase deve perseguire la propria qualità, verificando poi il beneficio del sistema completo. Questa sezione prevale sulle precedenti note di sola proposta o di calibrazione non adottata; motivazioni e alternative restano nel [parere](PARERE_PROPOSTA_COLLEGA_20261114.md). Approvazione del piano, non esecuzione o risultato.

### Sequenza operativa

1. **Consolidare il punto di partenza.** Acquisire gli esiti dei job già avviati senza duplicarli; completare runner comune, controllo sui punti e aggregazione. Separare equivalenza a peso zero, inizializzazioni, fusioni reali e inferenze SuperFlex. Stato HPC nel resoconto sotto, non ricontrollato da questo aggiornamento.
2. **Predisporre il confronto geometrico.** Stessi casi rappresentativi di sviluppo e viste escluse per tutte le alternative, con controlli a trasformazione nota. Verificare pixel→punto e texture per il ramo RGB; dichiarare casi non utilizzabili e fallimenti. Fissare gruppi/split, criteri, intervalli di ricerca e budget prima della selezione; tenere separato il test e rispettare la dipendenza temporale dei frame.
3. **Calibrare automaticamente geometria e accumulo.** Griglia iniziale: pulizia assente/leggera/moderata × inizializzazione RGB/FPFH × trasformazione rigida/similarità limitata × DA/MoGE: 24 combinazioni nominali, più PCA/multistart esistente come riferimento. Il conteggio non include ricerca dei parametri o repliche necessarie. Priorità tecnica RGB→3D/RANSAC/ICP robusto quando fattibile; FPFH/RANSAC/ICP come confronto. Ricerca finita sui parametri essenziali di pulizia, voxel e registrazione, registrando configurazioni, seed, risultati e costi. Reti pretrained congelate; nessuna registrazione non rigida o normalizzazione indipendente delle viste per forzare la fusione.
4. **Confrontare le finaliste nel ciclo completo.** Conservare anche configurazioni prossime alle migliori, evitando di selezionare dal solo residuo geometrico. SuperFlex dopo ogni aggiornamento ammesso, 4096 punti e preprocessing/inversa esistenti, forma disponibile ai confronti successivi. Calibrare sullo sviluppo anche peso/soglia geometrica del matcher. Confrontare baseline, accumulo diagnostico senza influenza, forme separate, SuperFlex accumulato e punti accumulati con input/budget/regole comparabili.
5. **Congelare e valutare.** Scegliere configurazione e metodo sullo sviluppo, quindi test separato senza ulteriore tuning; riportare anche copertura, rifiuti, fallimenti, variabilità rilevante e costi. Non scegliere DA o MoGE a priori né escludere dal risultato finale i casi geometrici falliti.

### Qualità perseguita in ogni fase

| Fase | Criterio di qualità | Controllo essenziale |
|---|---|---|
| Pulizia | Ridurre contaminazioni preservando dettagli e copertura | Casi controllati/revisione dei punti rimossi e verifica fuori dal fitting; il solo residuo ridotto non basta |
| Registrazione | Posa coerente e buon accordo nella regione condivisa | Errore su trasformazioni note e osservazioni/query escluse; distinguere ambiguità e scala, senza premiare il solo tasso di ammissione |
| Accumulo | Nuova copertura utile con dettaglio conservato e budget limitato | Distinguere viste tentate/accettate e ridondanza; una vista parziale non deve coprire tutta la memoria |
| SuperFlex | Spiegare nuove osservazioni con una rappresentazione utile al confronto | Distanza vista esclusa→superficie, proiezioni dove camera/posa affidabili e confronto con punti; nessuna accuratezza GT implicita |
| Associazione e sistema | Migliorare tracking secondo l'evaluator dichiarato | IDF1/mPCL, controllo a peso zero, ablation e sviluppo/test separati |

Costi e semplicità sono criteri secondari a qualità comparabile, entro risorse e scadenza. Ottimizzare le fasi non significa fissare separatamente ogni minimo locale: le interazioni si verificano sulle finaliste nel sistema completo. Query escluse dal fitting non equivalgono a osservazioni indipendenti; posa di valutazione comune e indipendente dalla forma quando disponibile, altrimenti dichiarare la misura congiunta posa/forma.

### Vincoli confermati

Contaminazione da associazioni: rischio comune a posizione/aspetto 2D/forma 3D, senza filone autonomo o memoria complessa; mantenere salvaguardie essenziali e registrazione necessaria alla fusione. Conservare ultima versione valida, causalità e provenienza; mai reinserire completamenti predetti nei punti osservati. L'autonomia approvata riguarda selezione e calibrazione della pipeline, non nuovo training o ampliamento automatico della domanda/dataset.

## HPC ripristinato, arretrati inviati — 14 novembre

SSH/accounting/coda accessibili. Recuperati 761899 (prefisso storico a peso zero esatto, 3398 frame/10264 detection, zero differenze dal collega) e 761905 (IDF1 73.2697% sulle predizioni registrate train, non test). Nuovi job: 763321 COMPLETED/0:0, 50 test ambiente passati; 763322 replica aggiornata e 763323 accumulo RUNNING nell’ultima osservazione; 763324 SuperFlex differita PENDING per dipendenza dai due CPU. Nessun nuovo esito sperimentale ancora dichiarato; prossima acquisizione dei risultati. [RIPRESA_HPC_20261114.md](RIPRESA_HPC_20261114.md). Le note precedenti sul blocco DNS e sui due esiti ancora da leggere sono storiche.

## SuperFlex differita collegata — 14 novembre

Implementate richieste da nuvola/versione ammessa, worker sulla pipeline esistente, verifica/importazione e pubblicazione della forma nei soli frame successivi. Replay seriale bloccato fino agli esiti, ultima forma conservata su fallimento; completamenti esclusi dai punti osservati. 43 controlli locali passati con sostituti dichiarati, nessuna nuova inferenza reale/HPC. Runner predisposto con --accumulate --reconstruct; prossimo confronto comune delle varianti e aggregazione delle misure. [SUPERFLEX_DIFFERITA_20261114.md](SUPERFLEX_DIFFERITA_20261114.md). Le note precedenti sul collegamento SuperFlex ancora mancante sono storiche; validazione reale 2B e risultati HPC pendenti invariati.

## Registrazione/accumulo collegati — 14 novembre

Collegato il candidato esistente al coordinatore: inizializzazione, registrazione rigida e accumulo ammesso, con isolamento delle sorgenti, versioni/provenienza e conservazione dello stato su rifiuto/errore. 35 test locali passati; input sintetici e componenti controllati, nessun replay reale o HPC. Runner predisposto con --accumulate (default disattivato), preparatore con punti camera/hash; non eseguiti in questa fase. Prossimo: SuperFlex differita dalla nuvola accettata. Il matcher usa ancora forme separate; risultato reale 2B invariato (0/12). [COLLEGAMENTO_ACCUMULO_20261114.md](COLLEGAMENTO_ACCUMULO_20261114.md). Le indicazioni precedenti sul collegamento ancora mancante sono storiche.

## Coordinatore del frame completato — 14 novembre

Implementato e collegato al runner: confronto/associazioni prima, commit delle forme e proposte geometriche dopo; versioni distinte, stato valido preservato per mancanti/rifiuti/errori. 27 controlli locali passati (11 nuovi), con metodi originali e componenti controllati; nessuna verifica Torch o run HPC. Il runner aggiorna ancora solo forme separate: prossimo collegamento del candidato registrazione/accumulo, poi SuperFlex differita. Esiti HPC e validazione 2B invariati. Resoconto: [COORDINATORE_FRAME_20261114.md](COORDINATORE_FRAME_20261114.md). Le indicazioni sottostanti sul coordinatore ancora da implementare sono storiche.

Mappa concettuale del risultato atteso richiesta da Marco il 14 novembre: [MAPPA_FLUSSO_SISTEMA.md](MAPPA_FLUSSO_SISTEMA.md). Esplicita il ciclo approvato e le memorie, senza modificare metodo, priorità o stato della validazione.

## Punto 1 software completato — 14 novembre

Implementato componente riutilizzabile con tre modalità, quattro rappresentazioni e delega al matcher originale; runner e preparatore aggiornati. Passati 16 controlli locali (7 adapter + 9 wrapper), con modello/tensor controllati; verifica Torch/frame reali rinviata. Nessun accesso HPC o nuovo esperimento. Prossimo lavoro: punto 2, coordinatore causale e stato geometrico versionato. Resoconto: [INTEGRAZIONE_RIUTILIZZABILE_20261114.md](INTEGRAZIONE_RIUTILIZZABILE_20261114.md).

## Priorità corrente — sviluppo senza HPC, 14 novembre

Marco dispone di sviluppare il progetto e rimandare gli esperimenti. Sospesi i tentativi di connessione come attività prioritaria; il recupero di 761899/761905 resta pendente alla ripresa. Ordine operativo: integrazione riutilizzabile → coordinatore causale → interfaccia SuperFlex differita → runner/controlli locali → pacchetto sperimentale. Piano e criteri in [PIANO_SVILUPPO_SENZA_HPC_20261114.md](PIANO_SVILUPPO_SENZA_HPC_20261114.md). Nessun nuovo esperimento o risultato; 2B resta non validato, parametri/protocollo finale non fissati da questa revisione.

**Stato prevalente al 14 novembre 2026:** configurazione, checkpoint e input ufficiali acquisiti; ordine/metadati/XYZ verificati su tutte le 110590 osservazioni. Il candidato 2A è collegato al tracker originale nel runner isolato; 120 controlli a peso zero con modello reale e input controllati superati. Replica del prefisso reale 761899: ultima osservazione RUNNING a 3000/3398 frame, esito finale ancora da acquisire. Metriche 761905: COMPLETED, valore IDF1 non ancora letto. Recupero bloccato da DNS, prossimo tentativo con VPN Bocconi; nessun rilancio. Restano due alias JPEG e validazione 2B (0/12 fusioni reali). Le note sottostanti su asset mancanti o assenza del collegamento al tracker sono storiche; non considerare completata la replica. [Resoconto tecnico](INTEGRAZIONE_BASELINE_REALE_20261113.md).

13 novembre 2026, dopo il chiarimento esplicito di Marco. Direzione richiesta: confronto delle forme per l'associazione e aggiornamento della ricostruzione con le osservazioni associate sono due componenti dello stesso sistema. Superata la precedente lettura dell'accumulo come sola estensione esterna alla ricerca. Domanda primaria sul tracking, EPIC, DA/MoGE, controllo sui punti e scadenza 23 novembre invariati. Roadmap successivamente approvata esplicitamente da Marco il 13 novembre, con avvio dello step 1. Il piano non registra esperimenti già eseguiti o valori numerici definitivamente calibrati. Stato dello step 1: [STEP1_CONTRATTO_TRACKING.md](STEP1_CONTRATTO_TRACKING.md).

## Revisione operativa successiva — avanzamento autonomo

Marco autorizza a iniziare componenti indipendenti e, se necessario, replicare una baseline minima. Lo step 1 certifica la run del collega e resta aperto; il suo completamento non è più prerequisito per test isolati 2A/2B. Primo candidato 2A implementato e provato su fixture e geometrie esistenti, non ancora nel tracker reale. Stato, risultati e piano della replica minima: [AVANZAMENTO_AUTONOMO_20261113.md](AVANZAMENTO_AUTONOMO_20261113.md). I riferimenti sotto al completamento del contratto riguardano l'integrazione reale; i diagnostici possono usare un contratto controllato e associazioni esterne esplicitamente dichiarate.

## Esito del primo pilota 2B

Candidato di registrazione/accumulo implementato, sette nuovi test finali; 12 aggiornamenti reali rifiutati, nessun accumulo reale ammesso. Rilevante distinzione tra implementazione e validazione: il passaggio a SuperFlex sugli accumuli resta pendente. Evidenze, correzione del controllo e incertezza successiva in [RISULTATI_REGISTRAZIONE_ACCUMULO_20261113.md](RISULTATI_REGISTRAZIONE_ACCUMULO_20261113.md). Nessuna modifica alla domanda o scelta automatica di un nuovo metodo.

## Nuova consegna del collega

Manifest completi ricevuti a bbf0e5e e audit reale passato; parte dati dello step 1 sbloccata. Due alias VISOR/RGB identificati, da verificare a livello delle feature effettive; configurazione/versioni/checkpoint e metriche non aggiunti. Report [VERIFICA_CONSEGNA_WHAREFORMER_20261113.md](VERIFICA_CONSEGNA_WHAREFORMER_20261113.md). Non confondere ricezione dei JSON con riproduzione dell'inferenza baseline.

## Rilettura tecnica effettiva

Consultate nuovamente le versioni HTML integrali delle sezioni pertinenti dei due paper, il 13 novembre, e confrontate con i sorgenti locali. Non sono state rieseguite le reti.

- **Whareformer:** [§§3.2–3.7, appendici 0.D–0.E](https://arxiv.org/html/2607.08537). Confronta distanze d'aspetto/posizione, le proietta in token, include New Track e aggiorna la memoria dopo l'assegnazione. Aspetto: DenStream; posizione: buffer recente. Il paper non fornisce una memoria di superfici. L'embedding ha due ingressi: aggiungere una terza distanza richiede adattamento dei pesi. L'assegnazione effettiva va fissata alla versione eseguita: nella copia locale è greedy, mentre testo e appendice distinguono più strategie.
- **SuperFlex:** [§§4.1–4.3, 5.1–5.3 e appendice D](https://arxiv.org/html/2607.01015). Predice insiemi di primitive da punti; il ramo robust apprende il completamento da input parziali. Simmetrie e permutazioni motivano confronti geometrici, non medie dei parametri. Non fornisce registrazione temporale. Il raffinamento del paper usa anche occupazione completa: non applicarlo automaticamente a punti EPIC parziali. Il benchmark ha orientamento canonico; il nostro preprocessing non garantisce invarianza alla posa.

Sorgenti riletti: `Whareformer-repo/src/tracking/tracker/matcher/matcher_types.py`, `tracker.py`, `track.py`, `video_instance.py`; `SuperFlex-repo/superflex/data/dataloader.py`, `optimization.py`; `shared_exports/publish_candidate/SuperFlex/src/shape_tools/memory.py`. Quest'ultima è FIFO di descrittori, con transazione score/commit: utile come controllo e per la causalità, non accumulatore di punti. La versione eseguita dal collega resta da acquisire.

## Contratto del ciclo

Per ogni track k mantenere distinti: feature/XYZ Whareformer originali; archivio limitato di punti realmente osservati; trasformazioni/qualità/provenienza delle viste; forma SuperFlex derivata; ultima versione valida. La forma completata è una previsione, non nuova evidenza da reinserire nei punti osservati.

Per un frame t:

1. Congelare lo stato geometrico di tutte le track a t−1.
2. Costruire le forme delle detection correnti; confrontarle con quello stato e calcolare le associazioni Whareformer, inclusa New Track.
3. Risolvere tutti i conflitti dello stesso frame con la procedura baseline.
4. Solo dopo: per ogni associazione predetta proporre allineamento/aggiornamento della geometria; per nuove track inizializzare il riferimento dalla prima osservazione valida.
5. Accettare gli aggiornamenti geometrici che superano i controlli; altrimenti conservare la versione precedente. Le decisioni di ammissione geometrica non riscrivono retroattivamente l'associazione.
6. Ricampionare la nuvola aggiornata e rieseguire SuperFlex con pesi congelati quando previsto dalla politica di aggiornamento. La nuova forma è disponibile dai confronti successivi.

Tutte le detection dello stesso frame interrogano la stessa memoria precedente. Nessuna track/forma di fine video nel percorso online; la causalità riguarda il modulo aggiunto, mentre feature/pose della baseline possono derivare da preprocessing offline da dichiarare. Non presentare il sistema come RGB strettamente online senza verificarlo.

## Step 1 — Contratto e baseline riproducibili

**Responsabile prevalente: collega; verifica condivisa.** Acquisire `tracks_by_id.json`, `compare200_joined_observations.json`, configurazione/comando/versioni/checkpoint e risultati baseline; rendere input necessari accessibili o rigenerabili senza richiedere di committare dati/pesi. Verificare ordine detection↔feature↔XYZ, unicità e hash delle geometrie. Risolvere o spiegare i due mancati join P01_01. Revisionare track 4/36 e candidati padella 9/35 senza promuoverli a ground truth.

**Uscita:** un breve segmento comune ripercorribile in ordine temporale con mapping verificato e output baseline. Usare P01_01 come sviluppo/pilota già approvato, mai come test finale. Non rilanciare compare200 o i precalcoli.

## Step 2A — Collegare forma→matcher

**Marco: confronto/export; collega: inserimento nel matcher; interfaccia condivisa.** Adattatore separato iniziale raccomandato. Riutilizzare feature, checkpoint, New Track e assegnazione originali; correzione configurabile ai logits prima della softmax come primo candidato, non terzo ingresso non addestrato. Con forma assente correzione diretta nulla; softmax e competizione possono comunque cambiare altre probabilità, inclusa New Track.

Partire dalla memoria separata già consegnata per avere un riferimento funzionante. Confrontare superfici/descrittori, non ordine o vettori grezzi delle primitive. D2 e spettro sono candidati economici esistenti, non una distanza già validata per corrente parziale contro memoria accumulata. Registrare d'aspetto, d'posizione, d'forma, logits, ordine track e decisioni. Prima sola diagnostica, poi peso zero e piccolo contributo sullo sviluppo.

**Uscita:** stessa sequenza di associazioni e metriche baseline a peso zero, anche se la geometria è calcolata/aggiornata; assenza di dati futuri verificabile. Reti congelate. Calibrazione effettiva rinviata allo step 5.

## Step 2B — Collegare associazione→aggiornamento geometrico

**Collega: registrazione/accumulo; Marco: input e ricostruzione SuperFlex; controlli condivisi.** Procedere in parallelo a 2A dopo il contratto. Prima riprodurre causalmente le associazioni baseline fisse, isolando la qualità dell'aggiornamento dall'effetto sul matching. Identità revisionate/oracle solo come diagnostica dichiarata separata.

Costruire un riferimento d'oggetto per track e sorgente, separando DA e MoGE. Non usare XYZ dell'oggetto come posa 6D. Conservare punti camera e trasformazioni; centrare/scalare separatamente ogni vista non risolve la registrazione. Iniziare con registrazione rigida dopo una convenzione di scala verificata; se emerge variazione di scala fra viste, diagnosticare e confrontare una variante di similarità a scala limitata sullo sviluppo, senza assorbirla silenziosamente. Simmetrie, scarso overlap e oggetti manipolati richiedono rifiuto esplicito degli allineamenti non affidabili. Non assumere che ICP da solo risolva registrazione globale o identità.

Misurare supporto/overlap e residui sulla parte osservata con campioni distinti da quelli usati per stimare la trasformazione quando fattibile; controllare variazioni implausibili e ciclo sintetico con trasformazioni note. Soglie da motivare e calibrare sullo sviluppo, senza scegliere numeri ora. Non accettare una vista solo perché conferma la forma già predetta. Conservare provenienza, ultima versione valida e possibilità di annullare un aggiornamento.

Accumulare solo punti osservati ammessi, con budget limitato e riequilibrio per vista/voxel per non far dominare frame ripetitivi. Ricampionare l'accumulo e applicare il preprocessing SuperFlex, salvando centro/scala inversi. L'aggiornamento è nuova inferenza della rappresentazione con pesi fissi, non nuovo training o media delle primitive. Valutare ogni vista valida all'inizio del pilota, poi misurare se serva aggiornare solo con nuova copertura o a intervalli; contabilizzare sempre i costi. Raffinamento con occupazione completa non previsto nel primo ciclo.

**Uscita:** sequenza prima/dopo su pochi casi controllati con trasformazioni, rifiuti, geometrie e costi salvati; la nuova vista può lasciare invariata la memoria. Dimostrazione tecnica di accumulo, non ancora superiorità 3D.

## Step 3 — Chiudere il ciclo completo

Collegare 2A e 2B: forma corrente contro SuperFlex dello stato accumulato precedente; associazione predetta; aggiornamento conservativo; SuperFlex aggiornato disponibile ai frame successivi. Usare identificativi track effettivi, inizializzazione/reset per video e gestione dei mancanti. La memoria va ricostruita per ogni variante: non riutilizzare la track baseline offline come se fosse quella del metodo modificato.

Controlli minimi: peso zero; perturbazione/rimozione di frame futuri senza variazione degli output passati; tutte le detection del frame leggono la versione precedente; nessun punto/completamento futuro; mancanti non cancellano la geometria valida; aggiornamento fallito conserva lo stato; sequenza con errore di associazione per misurare contaminazione/recupero. Non servono nuove inferenze dense prima che il piccolo ciclo sia verificato.

**Uscita:** ciclo riproducibile su un segmento, log delle decisioni e memoria versionata, nessun accesso a GT nel metodo.

## Step 4 — Separare il contributo dei due componenti

Proposta di ablation minima, da fissare prima della valutazione finale:

| Variante | Forma influenza associazione | Memoria geometrica |
|---|---|---|
| W0 | No | Baseline originale |
| G0 | No | Accumulo dopo associazioni baseline, a scopo diagnostico |
| S-separata | Sì | Forme di osservazioni conservate separatamente, memoria già disponibile |
| S-accumulo | Sì | Nuvola registrata aggiornata e nuova forma SuperFlex |
| P-accumulo | Sì | Controllo sui punti con stessi input, allineamento, budget e regole di ammissione comparabili |

G0 deve preservare le associazioni W0; costa geometria ma non deve cambiarne le metriche tracking. S-separata→S-accumulo misura l'utilità della ricostruzione aggiornata nel tracker; P-accumulo controlla il valore aggiunto di SuperFlex. Nessun prodotto cartesiano di molte distanze/capacità/registrazioni: diagnostica ridotta prima, confronto DA/MoGE sullo stesso campione con budget dichiarato. Entrambe le sorgenti restano supportate; nessuna eliminata da questo piano.

Per ricostruzione senza GT 3D: controlli su osservazioni escluse dall'aggiornamento e scelte prima dei punteggi, distanze punto→superficie sulla porzione osservata, silhouette rese nella posa stimata separando errore di posa/forma, stabilità e fallimenti. Una vista futura può essere usata esclusivamente per valutare uno stato passato congelato e non per aggiornarlo o registrarlo prima della decisione. Queste sono misure di consistenza con profondità/maschere stimate, non accuratezza metrica completa né IoU volumetrica GT. Non usare Chamfer simmetrico contro una sola vista parziale come unica misura del completamento, e non validare solo sui punti già fusi.

## Step 5 — Copertura, calibrazione e test

Prima di calcoli estesi dichiarare dove è disponibile la geometria e la regola di fallback comune a tutte le varianti: compare200 ha solo 40 RGB P01_01 rispetto a 33310 frame nel report tracking. Un pilota sparso può verificare il software; non basta a concludere sull'efficacia del metodo in tutto il video. Definire dal bisogno sperimentale i segmenti/la copertura aggiuntiva e solo dopo stimare il budget HPC misurato. Non rigenerare ciò che è già disponibile.

Calibrare peso/soglia della forma, ammissione, frequenza e capacità solo su sviluppo. Congelare configurazioni e criteri prima del test separato; verificare che split e identità di valutazione siano realmente compatibili con l'evaluator, non ricavate dalle predizioni. IDF1 e mPCL ufficiali, fusioni/frammentazioni, copertura, rifiuti, tempi di ricostruzione/registrazione/matching e byte per track. Riportare metriche sui dati comuni senza escludere a posteriori i casi geometrici falliti. Se il beneficio non emerge o l'accumulo peggiora, presentare la diagnosi con il controllo S-separata; non dichiarare completato con successo il ciclo accumulativo soltanto perché esiste il controllo.

## Organizzazione e calendario proposto

Sequenza per dipendenze, non promessa di durata: prima contratto; 2A e 2B possono procedere in parallelo fra i due membri; poi chiusura del ciclo, ablation e congelamento. Nessuna delega ad agenti o messaggio al collega eseguiti.

Proposta entro il 23 novembre: concentrare la prima parte del tempo residuo su contratto e piloti dei due rami, la parte centrale sul ciclo/controlli e la successiva su calibrazione/test. Riservare gli ultimi due giorni a risultati, limiti, report e riproducibilità. Non dedicare tutto il tempo alla sola registrazione: se il pilota non è affidabile, restringere il dimostratore accumulativo dichiarandolo e mantenere il confronto S-separata. Ogni ampliamento costoso richiede prima costo misurato e valore informativo. Nessun nuovo job o training avviato per scrivere questa roadmap.
