# Roadmap operativa — ciclo Whareformer–SuperFlex

## Passaggio a un altro provider AI — 14 novembre 2026

Marco richiede memoria e contesto autosufficienti nella cartella e su GitHub. Guida corrente: [LEGGIMI_PASSAGGIO_AI.md](LEGGIMI_PASSAGGIO_AI.md), che distingue implementato/verificato/pendente, decisioni, dipendenze e prossimi passi. Pubblicazione selettiva preparata dalla main del collega fc5aa30: codice integrazione, memoria, mappa corrente ed evidenze leggere; dati grandi, pesi e accessi esclusi. Nessun nuovo esperimento, filtro invariato. Gli stati storici di attesa frontend, output collega mancanti e job 763531 attivo sono superati dalle verifiche successive. Esito della pubblicazione in docs/CONDIVISIONE.md e context/evidence/publication_inventory.json sul remoto.

Frontend approvato: contratto/cache e ingresso nel comando implementati e verificati; rigenerazione ancora pendente per asset/provenienza/ambiente. [Stato e limiti](FRONTEND_AVANZAMENTO_20261114.md). Pacchetto locale common_runner_20261114_v3, nessun dato/peso incluso.

## Valutatore e comando unico collegati — 14 novembre

Implementati export delle osservazioni/assegnazioni con hash, IDF1/mPCL originali con scope esplicito e comando input preparati → varianti → valutazione → tabella. 763498 COMPLETED/0:0 (33 s), otto test; 763530 COMPLETED/0:0 (45 s), 69 test tutti eseguiti, riprodotti IDF1 73.269735% e mPCL 70.465504% su predizioni registrate train. 763531 RUNNING a 10m50s nell’ultima osservazione: nove configurazioni zero, CPU e cache esistente; esito ancora da acquisire. [COMPLETAMENTO_PIPELINE_20261114.md](COMPLETAMENTO_PIPELINE_20261114.md).

**GPU concluso:** 763324 COMPLETED/0:0 (43m30s), sei ricostruzioni reali ready e controllo zero esatto, ma nessuna fusione multivista ammessa. Filtri invariati e revisione ancora rinviata. Mancano unificazione del frontend dati, copertura sufficiente e calibrazione/test; il comando attuale parte da input preparati. Le precedenti note di metriche non collegate e GPU ancora attivo sono storiche.

## Runner comune e misure implementati — 14 novembre

Disponibili W0/G0/S-separata/S-accumulo/P-accumulo, DA/MoGE, memorie e modelli indipendenti, controllo sui punti ammessi e report JSONL/JSON/CSV con copertura, fallimenti, byte di payload e costi dei replay. 58 test locali superati; esempio a peso zero, tracking metrics ancora non calcolate. Nessuna nuova run reale del runner comune né modifica dei job esistenti. [RUNNER_VARIANTI_20261114.md](RUNNER_VARIANTI_20261114.md). Prossimo: collegare valutatore tracking e protocollo/copertura di calibrazione-test.

**HPC verificato durante il lavoro:** 763322 COMPLETED/0:0 (9m56s), 763323 COMPLETED/0:0 (12m11s), zero esatto; nel secondo solo 12 inizializzazioni e 12 rifiuti, nessuna fusione, conteggi sulle quattro rappresentazioni. 763324 RUNNING a 29m19s con almeno un risultato neurale reale ready; esito complessivo ancora da acquisire. [Dettagli HPC](RIPRESA_HPC_20261114.md). Le indicazioni precedenti di job CPU attivi/GPU in attesa sono storiche.

## Piano corrente approvato — 14 novembre

Approvate selezione autonoma di metodo/parametri e confronto delle alternative: consolidamento degli esiti esistenti → confronto/calibrazione geometrica (24 combinazioni nominali più riferimento) → finaliste nel ciclo SuperFlex/tracking → configurazione congelata e test separato. Qualità perseguita in ogni fase, costi secondari a risultati comparabili; inferenza dopo ogni aggiornamento ammesso. Sequenza, criteri e vincoli nel [piano d'azione aggiornato](ROADMAP_CICLO_GEOMETRICO.md). Le precedenti note di calibrazione solo proposta sono superate; nessun nuovo esperimento eseguito da questo aggiornamento.

## HPC ripristinato, arretrati inviati — 14 novembre

SSH/accounting/coda accessibili. Recuperati 761899 (prefisso storico a peso zero esatto, 3398 frame/10264 detection, zero differenze dal collega) e 761905 (IDF1 73.2697% sulle predizioni registrate train, non test). Nuovi job: 763321 COMPLETED/0:0, 50 test ambiente passati; 763322 replica aggiornata e 763323 accumulo RUNNING nell’ultima osservazione; 763324 SuperFlex differita PENDING per dipendenza dai due CPU. Nessun nuovo esito sperimentale ancora dichiarato; prossima acquisizione dei risultati. [RIPRESA_HPC_20261114.md](RIPRESA_HPC_20261114.md). Le note precedenti sul blocco DNS e sui due esiti ancora da leggere sono storiche.

## SuperFlex differita collegata — 14 novembre

Implementate richieste da nuvola/versione ammessa, worker sulla pipeline esistente, verifica/importazione e pubblicazione della forma nei soli frame successivi. Replay seriale bloccato fino agli esiti, ultima forma conservata su fallimento; completamenti esclusi dai punti osservati. 43 controlli locali passati con sostituti dichiarati, nessuna nuova inferenza reale/HPC. Runner predisposto con --accumulate --reconstruct; prossimo confronto comune delle varianti e aggregazione delle misure. [SUPERFLEX_DIFFERITA_20261114.md](SUPERFLEX_DIFFERITA_20261114.md). Le note precedenti sul collegamento SuperFlex ancora mancante sono storiche; validazione reale 2B e risultati HPC pendenti invariati.

## Registrazione/accumulo collegati — 14 novembre

Collegato il candidato esistente al coordinatore: inizializzazione, registrazione rigida e accumulo ammesso, con isolamento delle sorgenti, versioni/provenienza e conservazione dello stato su rifiuto/errore. 35 test locali passati; input sintetici e componenti controllati, nessun replay reale o HPC. Runner predisposto con --accumulate (default disattivato), preparatore con punti camera/hash; non eseguiti in questa fase. Prossimo: SuperFlex differita dalla nuvola accettata. Il matcher usa ancora forme separate; risultato reale 2B invariato (0/12). [COLLEGAMENTO_ACCUMULO_20261114.md](COLLEGAMENTO_ACCUMULO_20261114.md). Le indicazioni precedenti sul collegamento ancora mancante sono storiche.

## Coordinatore del frame completato — 14 novembre

Implementato e collegato al runner: confronto/associazioni prima, commit delle forme e proposte geometriche dopo; versioni distinte, stato valido preservato per mancanti/rifiuti/errori. 27 controlli locali passati (11 nuovi), con metodi originali e componenti controllati; nessuna verifica Torch o run HPC. Il runner aggiorna ancora solo forme separate: prossimo collegamento del candidato registrazione/accumulo, poi SuperFlex differita. Esiti HPC e validazione 2B invariati. Resoconto: [COORDINATORE_FRAME_20261114.md](COORDINATORE_FRAME_20261114.md). Le indicazioni sottostanti sul coordinatore ancora da implementare sono storiche.

## Punto 1 software completato — 14 novembre

Implementato componente riutilizzabile con tre modalità, quattro rappresentazioni e delega al matcher originale; runner e preparatore aggiornati. Passati 16 controlli locali (7 adapter + 9 wrapper), con modello/tensor controllati; verifica Torch/frame reali rinviata. Nessun accesso HPC o nuovo esperimento. Prossimo lavoro: punto 2, coordinatore causale e stato geometrico versionato. Resoconto: [INTEGRAZIONE_RIUTILIZZABILE_20261114.md](INTEGRAZIONE_RIUTILIZZABILE_20261114.md).

## Priorità corrente — sviluppo senza HPC, 14 novembre

Marco dispone di sviluppare il progetto e rimandare gli esperimenti. Sospesi i tentativi di connessione come attività prioritaria; il recupero di 761899/761905 resta pendente alla ripresa. Ordine operativo: integrazione riutilizzabile → coordinatore causale → interfaccia SuperFlex differita → runner/controlli locali → pacchetto sperimentale. Piano e criteri in [PIANO_SVILUPPO_SENZA_HPC_20261114.md](PIANO_SVILUPPO_SENZA_HPC_20261114.md). Nessun nuovo esperimento o risultato; 2B resta non validato, parametri/protocollo finale non fissati da questa revisione.

**Stato prevalente al 14 novembre 2026:** configurazione, checkpoint e input ufficiali acquisiti; ordine/metadati/XYZ verificati su tutte le 110590 osservazioni. Il candidato 2A è collegato al tracker originale nel runner isolato; 120 controlli a peso zero con modello reale e input controllati superati. Replica del prefisso reale 761899: ultima osservazione RUNNING a 3000/3398 frame, esito finale ancora da acquisire. Metriche 761905: COMPLETED, valore IDF1 non ancora letto. Recupero bloccato da DNS, prossimo tentativo con VPN Bocconi; nessun rilancio. Restano due alias JPEG e validazione 2B (0/12 fusioni reali). Le note sottostanti su asset mancanti o assenza del collegamento al tracker sono storiche; non considerare completata la replica. [Resoconto tecnico](INTEGRAZIONE_BASELINE_REALE_20261113.md).

Aggiornamento del 13 novembre 2026 dopo il chiarimento esplicito di Marco. Confronto della forma per associare e aggiornamento della ricostruzione dopo l'associazione sono due componenti dello stesso ciclo. È superata la precedente interpretazione dell'accumulo come sola estensione esterna. Domanda sul tracking, EPIC, DA/MoGE, punti come controllo e scadenza 23 novembre invariati.

Piano tecnico dopo rilettura dei due paper, verifiche, responsabilità e criteri di uscita: [ROADMAP_CICLO_GEOMETRICO.md](ROADMAP_CICLO_GEOMETRICO.md). Marco ha approvato questa roadmap e richiesto l’avvio dello step 1; i parametri da calibrare non sono risultati. Stato: [STEP1_CONTRATTO_TRACKING.md](STEP1_CONTRATTO_TRACKING.md), avviato ma dipendente dai manifest completi della baseline.

Avanzamento successivo autorizzato: la mancanza dei manifest del collega non blocca i test isolati 2A/2B. Primo prototipo 2A e replay tecnico già eseguiti, con limiti in [AVANZAMENTO_AUTONOMO_20261113.md](AVANZAMENTO_AUTONOMO_20261113.md). Per una nostra baseline bastano asset e configurazione originali, non la sua run; replica minima prevista se necessaria.

Esito corrente 2B: candidato implementato, sette nuovi test superati; 0/12 aggiornamenti fra viste reali accettati. Nessuna nuova inferenza SuperFlex; prossima diagnosi su posa e geometria/scala, mantenendo il controllo con forme separate. [Risultati e limiti](RISULTATI_REGISTRAZIONE_ACCUMULO_20261113.md).

Consegna successiva a bbf0e5e: manifest completi acquisiti e audit del mapping reale passato. Due alias temporali VISOR/RGB identificati; allineamento delle feature e configurazione della run ancora aperti. [Verifica della consegna](VERIFICA_CONSEGNA_WHAREFORMER_20261113.md).

| Step | Risultato atteso | Responsabilità prevalente |
|---|---|---|
| 1. Contratto e baseline | Mapping riproducibile, output/configurazione reali, diagnosi mancanti e track miste | Collega; verifica comune |
| 2A. Forma→associazione | Adattatore diagnostico e a peso zero; confronto corrente/memoria precedente | Marco confronto, collega matcher |
| 2B. Associazione→geometria | Registrazione, accumulo conservativo, nuova inferenza SuperFlex a pesi fissi | Collega accumulo, Marco SuperFlex |
| 3. Ciclo completo | Associazione predetta, aggiornamento successivo, memoria versionata per i frame futuri | Insieme |
| 4. Ablation | Baseline, accumulo senza influenza, forme separate, accumulo SuperFlex, controllo punti | Insieme |
| 5. Calibrazione e test | Copertura dichiarata, scelte congelate, test separato e costi completi | Collega valutazione; analisi comune |

2A e 2B possono avanzare in parallelo fra i due membri dopo il contratto. La memoria FIFO esistente è un controllo e un primo stadio, non l'accumulatore già implementato. Prima il pilota causale, poi eventuale ampliamento della geometria: compare200 è sparso. Riservare gli ultimi due giorni a report e riproducibilità è una proposta organizzativa, non nuova scadenza concordata.

Consegna geometrica autonoma completata; mapping offline P01_01 del collega disponibile con report 71/73, non ancora riprodotto sui suoi output completi. Evidenze storiche in CONSEGNA_RAMO_GEOMETRICO.md e ANALISI_AGGIORNAMENTO_GITHUB_20261113.md. Nessun beneficio tracking, accumulo valido o fedeltà 3D dimostrati finora. Non ripetere run conclusi. Stato e attività in STATO_LAVORO.md e TODO.md.
