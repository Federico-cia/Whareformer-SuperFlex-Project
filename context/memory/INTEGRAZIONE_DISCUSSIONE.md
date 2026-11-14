# Interfaccia geometrica e integrazione Whareformer

## Passaggio a un altro provider AI — 14 novembre 2026

Marco richiede memoria e contesto autosufficienti nella cartella e su GitHub. Guida corrente: [LEGGIMI_PASSAGGIO_AI.md](LEGGIMI_PASSAGGIO_AI.md), che distingue implementato/verificato/pendente, decisioni, dipendenze e prossimi passi. Pubblicazione selettiva preparata dalla main del collega fc5aa30: codice integrazione, memoria, mappa corrente ed evidenze leggere; dati grandi, pesi e accessi esclusi. Nessun nuovo esperimento, filtro invariato. Gli stati storici di attesa frontend, output collega mancanti e job 763531 attivo sono superati dalle verifiche successive. Esito della pubblicazione in docs/CONDIVISIONE.md e context/evidence/publication_inventory.json sul remoto.

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

## Revisione di Marco su accumulo e inferenza — 14 novembre

Contaminazione da associazioni: rischio comune a posizione/aspetto 2D/forma 3D, senza filone autonomo o ampliamento delle memorie; controlli essenziali preservati. Distinta dalla registrazione necessaria fra viste. Approvate inferenza SuperFlex dopo ogni aggiornamento ammesso e, successivamente, selezione/calibrazione autonome delle alternative. Qualità per fase e verifica delle finaliste nel tracking secondo il [piano corrente](ROADMAP_CICLO_GEOMETRICO.md); motivazioni nel [parere](PARERE_PROPOSTA_COLLEGA_20261114.md). Nessuna nuova esecuzione in questo aggiornamento.

## HPC ripristinato, arretrati inviati — 14 novembre

SSH/accounting/coda accessibili. Recuperati 761899 (prefisso storico a peso zero esatto, 3398 frame/10264 detection, zero differenze dal collega) e 761905 (IDF1 73.2697% sulle predizioni registrate train, non test). Nuovi job: 763321 COMPLETED/0:0, 50 test ambiente passati; 763322 replica aggiornata e 763323 accumulo RUNNING nell’ultima osservazione; 763324 SuperFlex differita PENDING per dipendenza dai due CPU. Nessun nuovo esito sperimentale ancora dichiarato; prossima acquisizione dei risultati. [RIPRESA_HPC_20261114.md](RIPRESA_HPC_20261114.md). Le note precedenti sul blocco DNS e sui due esiti ancora da leggere sono storiche.

Parere del 14 novembre sulla proposta del collega, con successivo approfondimento delle soluzioni e dei pro/contro: [pulizia, FPFH/RANSAC/ICP, accumulo e valutazione](PARERE_PROPOSTA_COLLEGA_20261114.md). Metodo candidato da confrontare; nessuna sostituzione adottata o modifica al ciclo. La Chamfer simmetrica contro una vista esclusa parziale non basta come unica misura del completamento; domanda primaria tracking invariata. Precisati supporto limitato alla regione condivisa e possibili equivalenze di posa per simmetrie reali, senza cambiare i gate del candidato.

## SuperFlex differita collegata — 14 novembre

Implementate richieste da nuvola/versione ammessa, worker sulla pipeline esistente, verifica/importazione e pubblicazione della forma nei soli frame successivi. Replay seriale bloccato fino agli esiti, ultima forma conservata su fallimento; completamenti esclusi dai punti osservati. 43 controlli locali passati con sostituti dichiarati, nessuna nuova inferenza reale/HPC. Runner predisposto con --accumulate --reconstruct; prossimo confronto comune delle varianti e aggregazione delle misure. [SUPERFLEX_DIFFERITA_20261114.md](SUPERFLEX_DIFFERITA_20261114.md). Le note precedenti sul collegamento SuperFlex ancora mancante sono storiche; validazione reale 2B e risultati HPC pendenti invariati.

## Registrazione/accumulo collegati — 14 novembre

Collegato il candidato esistente al coordinatore: inizializzazione, registrazione rigida e accumulo ammesso, con isolamento delle sorgenti, versioni/provenienza e conservazione dello stato su rifiuto/errore. 35 test locali passati; input sintetici e componenti controllati, nessun replay reale o HPC. Runner predisposto con --accumulate (default disattivato), preparatore con punti camera/hash; non eseguiti in questa fase. Prossimo: SuperFlex differita dalla nuvola accettata. Il matcher usa ancora forme separate; risultato reale 2B invariato (0/12). [COLLEGAMENTO_ACCUMULO_20261114.md](COLLEGAMENTO_ACCUMULO_20261114.md). Le indicazioni precedenti sul collegamento ancora mancante sono storiche.

## Coordinatore del frame completato — 14 novembre

Implementato e collegato al runner: confronto/associazioni prima, commit delle forme e proposte geometriche dopo; versioni distinte, stato valido preservato per mancanti/rifiuti/errori. 27 controlli locali passati (11 nuovi), con metodi originali e componenti controllati; nessuna verifica Torch o run HPC. Il runner aggiorna ancora solo forme separate: prossimo collegamento del candidato registrazione/accumulo, poi SuperFlex differita. Esiti HPC e validazione 2B invariati. Resoconto: [COORDINATORE_FRAME_20261114.md](COORDINATORE_FRAME_20261114.md). Le indicazioni sottostanti sul coordinatore ancora da implementare sono storiche.

Mappa del sistema obiettivo, richiesta da Marco il 14 novembre: [MAPPA_FLUSSO_SISTEMA.md](MAPPA_FLUSSO_SISTEMA.md). Posizione/aspetto baseline e confronto di forma tramite adattatore precedono l'aggiornamento delle memorie; lo schema non dichiara completato il ciclo accumulativo.

## Punto 1 software completato — 14 novembre

Implementato componente riutilizzabile con tre modalità, quattro rappresentazioni e delega al matcher originale; runner e preparatore aggiornati. Passati 16 controlli locali (7 adapter + 9 wrapper), con modello/tensor controllati; verifica Torch/frame reali rinviata. Nessun accesso HPC o nuovo esperimento. Prossimo lavoro: punto 2, coordinatore causale e stato geometrico versionato. Resoconto: [INTEGRAZIONE_RIUTILIZZABILE_20261114.md](INTEGRAZIONE_RIUTILIZZABILE_20261114.md).

## Priorità corrente — sviluppo senza HPC, 14 novembre

Marco dispone di sviluppare il progetto e rimandare gli esperimenti. Sospesi i tentativi di connessione come attività prioritaria; il recupero di 761899/761905 resta pendente alla ripresa. Ordine operativo: integrazione riutilizzabile → coordinatore causale → interfaccia SuperFlex differita → runner/controlli locali → pacchetto sperimentale. Piano e criteri in [PIANO_SVILUPPO_SENZA_HPC_20261114.md](PIANO_SVILUPPO_SENZA_HPC_20261114.md). Nessun nuovo esperimento o risultato; 2B resta non validato, parametri/protocollo finale non fissati da questa revisione.

**Stato prevalente al 14 novembre 2026:** configurazione, checkpoint e input ufficiali acquisiti; ordine/metadati/XYZ verificati su tutte le 110590 osservazioni. Il candidato 2A è collegato al tracker originale nel runner isolato; 120 controlli a peso zero con modello reale e input controllati superati. Replica del prefisso reale 761899: ultima osservazione RUNNING a 3000/3398 frame, esito finale ancora da acquisire. Metriche 761905: COMPLETED, valore IDF1 non ancora letto. Recupero bloccato da DNS, prossimo tentativo con VPN Bocconi; nessun rilancio. Restano due alias JPEG e validazione 2B (0/12 fusioni reali). Le note sottostanti su asset mancanti o assenza del collegamento al tracker sono storiche; non considerare completata la replica. [Resoconto tecnico](INTEGRAZIONE_BASELINE_REALE_20261113.md).

Revisione del 13 novembre 2026 dopo il chiarimento esplicito di Marco. Le due direzioni fanno parte dello stesso ciclo: la forma contribuisce all'associazione e l'osservazione associata aggiorna la ricostruzione usata nei confronti successivi. Superata la precedente caratterizzazione dell'accumulo come sola estensione esterna. Specifica proposta e rilettura dei paper in [ROADMAP_CICLO_GEOMETRICO.md](ROADMAP_CICLO_GEOMETRICO.md); storia nelle voci 28–31 del registro.

## Prototipo indipendente avviato

`integration_prototype/shape_adapter.py` esercita il confine logits/memoria senza checkpoint; sette test e replay di tre frame su geometrie reali, ma con punteggi controllati e associazioni annotate. Non è ancora l'adattatore Torch/Whareformer reale. Risultati e limiti in [AVANZAMENTO_AUTONOMO_20261113.md](AVANZAMENTO_AUTONOMO_20261113.md). Registrazione/accumulo successivamente implementati come candidati, con sette nuovi test ma nessun aggiornamento reale ammesso nel pilota; vedi [RISULTATI_REGISTRAZIONE_ACCUMULO_20261113.md](RISULTATI_REGISTRAZIONE_ACCUMULO_20261113.md). Nessuna nuova forma da accumulo reale disponibile.

## Mapping reale ora disponibile

A bbf0e5e sono arrivati i due manifest completi; 71/73 join verificati, indici espliciti da usare (69 differiscono dalla lista VISOR). Due alias temporali di un indice richiedono verifica delle immagini usate per feature/XYZ. Associazioni predette non sono identità GT né pose d'oggetto. Report [VERIFICA_CONSEGNA_WHAREFORMER_20261113.md](VERIFICA_CONSEGNA_WHAREFORMER_20261113.md).

## Contratto corrente

Conservare feature e XYZ originali. Per track e sorgente DA/MoGE mantenere punti osservati, riferimento d'oggetto, trasformazioni/provenienza, forma SuperFlex derivata e ultima versione valida. Il completamento predetto non diventa evidenza osservata. Confronto di superfici/descrittori, non media di parametri delle primitive.

Tutte le detection del frame leggono la memoria precedente; matching e conflitti risolti prima degli aggiornamenti. Poi ammissione geometrica, registrazione, accumulo con budget, ricampionamento e nuova inferenza a pesi congelati. La nuova rappresentazione serve ai frame successivi. Rifiuti/fallimenti conservano lo stato valido. Le track del metodo si ricostruiscono dalle sue associazioni predette, non si copiano dal tracking baseline finale.

## Candidati ancora da validare

Primo adattatore raccomandato: correzione configurabile dei logits prima della softmax con reti congelate e assegnazione originale. Peso zero equivalente; forma assente senza correzione diretta; New Track rimane in competizione e la sua probabilità può cambiare. La precedente formula lambda*(tau-dS) resta candidata, non metodo approvato. Un terzo ingresso nell'embedding richiede adattamento del modello.

FIFO di forme separate come riferimento; accumulo registrato come componente del ciclo da costruire e confrontare. Registrazione rigida dopo controllo della scala, variante di similarità soltanto se motivata dai dati; soglie/ammissione/frequenza da calibrare sullo sviluppo. Nessun accumulo camera-frame diretto di oggetti mobili, nessuna posa oracle o occupazione completa inventata. SAM3 e memoria robotica non diventano prerequisiti.

Valutazione proposta: isolare associazione e aggiornamento, poi confrontare ciclo completo, forme separate e punti con input/budget comparabili; IDF1/mPCL e costi, diagnostica di consistenza geometrica distinta da fedeltà 3D certificata. Sviluppo/test separati; nessun nuovo job avviato.
