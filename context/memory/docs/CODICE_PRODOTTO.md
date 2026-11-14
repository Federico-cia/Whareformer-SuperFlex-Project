# Che cosa abbiamo prodotto in codice

## Passaggio a un altro provider AI — 14 novembre 2026

Marco richiede memoria e contesto autosufficienti nella cartella e su GitHub. Guida corrente: [LEGGIMI_PASSAGGIO_AI.md](../LEGGIMI_PASSAGGIO_AI.md), che distingue implementato/verificato/pendente, decisioni, dipendenze e prossimi passi. Pubblicazione selettiva preparata dalla main del collega fc5aa30: codice integrazione, memoria, mappa corrente ed evidenze leggere; dati grandi, pesi e accessi esclusi. Nessun nuovo esperimento, filtro invariato. Gli stati storici di attesa frontend, output collega mancanti e job 763531 attivo sono superati dalle verifiche successive. Esito della pubblicazione in docs/CONDIVISIONE.md e context/evidence/publication_inventory.json sul remoto.

Frontend approvato: contratto/cache e ingresso nel comando implementati e verificati; rigenerazione ancora pendente per asset/provenienza/ambiente. [Stato e limiti](../FRONTEND_AVANZAMENTO_20261114.md). Pacchetto locale common_runner_20261114_v3, nessun dato/peso incluso.

## Valutatore e comando unico collegati — 14 novembre

Implementati export delle osservazioni/assegnazioni con hash, IDF1/mPCL originali con scope esplicito e comando input preparati → varianti → valutazione → tabella. 763498 COMPLETED/0:0 (33 s), otto test; 763530 COMPLETED/0:0 (45 s), 69 test tutti eseguiti, riprodotti IDF1 73.269735% e mPCL 70.465504% su predizioni registrate train. 763531 RUNNING a 10m50s nell’ultima osservazione: nove configurazioni zero, CPU e cache esistente; esito ancora da acquisire. [COMPLETAMENTO_PIPELINE_20261114.md](../COMPLETAMENTO_PIPELINE_20261114.md).

**GPU concluso:** 763324 COMPLETED/0:0 (43m30s), sei ricostruzioni reali ready e controllo zero esatto, ma nessuna fusione multivista ammessa. Filtri invariati e revisione ancora rinviata. Mancano unificazione del frontend dati, copertura sufficiente e calibrazione/test; il comando attuale parte da input preparati. Le precedenti note di metriche non collegate e GPU ancora attivo sono storiche.

## Runner comune e misure implementati — 14 novembre

Disponibili W0/G0/S-separata/S-accumulo/P-accumulo, DA/MoGE, memorie e modelli indipendenti, controllo sui punti ammessi e report JSONL/JSON/CSV con copertura, fallimenti, byte di payload e costi dei replay. 58 test locali superati; esempio a peso zero, tracking metrics ancora non calcolate. Nessuna nuova run reale del runner comune né modifica dei job esistenti. [RUNNER_VARIANTI_20261114.md](../RUNNER_VARIANTI_20261114.md). Prossimo: collegare valutatore tracking e protocollo/copertura di calibrazione-test.

**HPC verificato durante il lavoro:** 763322 COMPLETED/0:0 (9m56s), 763323 COMPLETED/0:0 (12m11s), zero esatto; nel secondo solo 12 inizializzazioni e 12 rifiuti, nessuna fusione, conteggi sulle quattro rappresentazioni. 763324 RUNNING a 29m19s con almeno un risultato neurale reale ready; esito complessivo ancora da acquisire. [Dettagli HPC](../RIPRESA_HPC_20261114.md). Le indicazioni precedenti di job CPU attivi/GPU in attesa sono storiche.

## HPC ripristinato, arretrati inviati — 14 novembre

SSH/accounting/coda accessibili. Recuperati 761899 (prefisso storico a peso zero esatto, 3398 frame/10264 detection, zero differenze dal collega) e 761905 (IDF1 73.2697% sulle predizioni registrate train, non test). Nuovi job: 763321 COMPLETED/0:0, 50 test ambiente passati; 763322 replica aggiornata e 763323 accumulo RUNNING nell’ultima osservazione; 763324 SuperFlex differita PENDING per dipendenza dai due CPU. Nessun nuovo esito sperimentale ancora dichiarato; prossima acquisizione dei risultati. [RIPRESA_HPC_20261114.md](../RIPRESA_HPC_20261114.md). Le note precedenti sul blocco DNS e sui due esiti ancora da leggere sono storiche.

## SuperFlex differita collegata — 14 novembre

Implementate richieste da nuvola/versione ammessa, worker sulla pipeline esistente, verifica/importazione e pubblicazione della forma nei soli frame successivi. Replay seriale bloccato fino agli esiti, ultima forma conservata su fallimento; completamenti esclusi dai punti osservati. 43 controlli locali passati con sostituti dichiarati, nessuna nuova inferenza reale/HPC. Runner predisposto con --accumulate --reconstruct; prossimo confronto comune delle varianti e aggregazione delle misure. [SUPERFLEX_DIFFERITA_20261114.md](../SUPERFLEX_DIFFERITA_20261114.md). Le note precedenti sul collegamento SuperFlex ancora mancante sono storiche; validazione reale 2B e risultati HPC pendenti invariati.

## Registrazione/accumulo collegati — 14 novembre

Collegato il candidato esistente al coordinatore: inizializzazione, registrazione rigida e accumulo ammesso, con isolamento delle sorgenti, versioni/provenienza e conservazione dello stato su rifiuto/errore. 35 test locali passati; input sintetici e componenti controllati, nessun replay reale o HPC. Runner predisposto con --accumulate (default disattivato), preparatore con punti camera/hash; non eseguiti in questa fase. Prossimo: SuperFlex differita dalla nuvola accettata. Il matcher usa ancora forme separate; risultato reale 2B invariato (0/12). [COLLEGAMENTO_ACCUMULO_20261114.md](../COLLEGAMENTO_ACCUMULO_20261114.md). Le indicazioni precedenti sul collegamento ancora mancante sono storiche.

## Coordinatore del frame completato — 14 novembre

Implementato e collegato al runner: confronto/associazioni prima, commit delle forme e proposte geometriche dopo; versioni distinte, stato valido preservato per mancanti/rifiuti/errori. 27 controlli locali passati (11 nuovi), con metodi originali e componenti controllati; nessuna verifica Torch o run HPC. Il runner aggiorna ancora solo forme separate: prossimo collegamento del candidato registrazione/accumulo, poi SuperFlex differita. Esiti HPC e validazione 2B invariati. Resoconto: [COORDINATORE_FRAME_20261114.md](../COORDINATORE_FRAME_20261114.md). Le indicazioni sottostanti sul coordinatore ancora da implementare sono storiche.

## Punto 1 software completato — 14 novembre

Implementato componente riutilizzabile con tre modalità, quattro rappresentazioni e delega al matcher originale; runner e preparatore aggiornati. Passati 16 controlli locali (7 adapter + 9 wrapper), con modello/tensor controllati; verifica Torch/frame reali rinviata. Nessun accesso HPC o nuovo esperimento. Prossimo lavoro: punto 2, coordinatore causale e stato geometrico versionato. Resoconto: [INTEGRAZIONE_RIUTILIZZABILE_20261114.md](../INTEGRAZIONE_RIUTILIZZABILE_20261114.md).

**Stato prevalente al 14 novembre 2026:** configurazione, checkpoint e input ufficiali acquisiti; ordine/metadati/XYZ verificati su tutte le 110590 osservazioni. Il candidato 2A è collegato al tracker originale nel runner isolato; 120 controlli a peso zero con modello reale e input controllati superati. Replica del prefisso reale 761899: ultima osservazione RUNNING a 3000/3398 frame, esito finale ancora da acquisire. Metriche 761905: COMPLETED, valore IDF1 non ancora letto. Recupero bloccato da DNS, prossimo tentativo con VPN Bocconi; nessun rilancio. Restano due alias JPEG e validazione 2B (0/12 fusioni reali). Le note sottostanti su asset mancanti o assenza del collegamento al tracker sono storiche; non considerare completata la replica. [Resoconto tecnico](../INTEGRAZIONE_BASELINE_REALE_20261113.md).

**Stato aggiornato al 13 novembre:** pipeline portabile, confronto/export/memoria e risultati del ramo geometrico consegnati su `main` in `SuperFlex/`; vedi `../CONSEGNA_RAMO_GEOMETRICO.md`. Il collega ha aggiunto due script per il ponte offline P01_01 e report, esaminati in `../ANALISI_AGGIORNAMENTO_GITHUB_20261113.md`. Nessun contributo di forma nel matcher ancora caricato. L'inventario del 10 novembre sotto descrive l'archivio storico locale, non i soli file condivisi né il solo percorso portabile attuale.

Inventario del 10 novembre 2026. È il codice di esperimenti e verifiche del ramo geometrico, non ancora un nuovo tracker completo. All'avvio della ricognizione erano presenti 44 script: 25 Python, 17 SLURM e due PowerShell. Il catalogo in `manifests/code_inventory.json` elenca i file correnti con funzione, stato e hash.

## Il lavoro originale del progetto

Abbiamo scritto programmi che collegano componenti preaddestrati e rendono gli esperimenti controllabili:

| Componente | Input → output | File principali | Che cosa è stato verificato |
|---|---|---|---|
| Selezione/acquisizione EPIC | RGB, VISOR, pose e mapping → campione fissato e manifest | `acquire_compare200.py`, `select_epic_diagnostic.py`, `validate_compare200.py` | Campione 200 e collegamento VISOR/RGB delle osservazioni |
| Costruzione della geometria | RGB/camera/maschera → profondità e punti per oggetto | `expanded_geometry.py`, `epic_depth_probe.py`, `epic_geometry_probe.py`, `moge2_visor_probe.py` | Rami DA grezzo/allineato e MoGE eseguiti; non accuratezza 3D certificata |
| Esecuzione SuperFlex | Punti parziali → primitive, mesh e rapporti | `superflex_batch_probe.py`, `superflex_epic_probe.py` | Robust preaddestrato, campionamento/provenienza; ripresa e fallimenti per osservazione |
| Confronto delle ricostruzioni | Mesh/punti/maschere → controlli, sagome 2D e tavole | `review_expanded_geometry.py`, `summarize_compare200.py`, `paired_compare200.py` | Confronto appaiato 200 completato; hash e figure controllati |
| Segnale di identità | Punti/mesh già disponibili → distanze e analisi su identità visive | `shape_identity_experiment.py`, `evaluate_shape_identity.py`, `verify_shape_identity_results.ps1` | 8797 coppie calcolate, controllo descrittivo su 37 osservazioni; campione ancora limitato |
| Gestione HPC | Script e percorsi → job riproducibili e log | File `.sbatch` associati | Esecuzioni registrate nei resoconti; gli ambienti esistono sull'account usato |

I nomi della tabella sono relativi a `scripts/`. La mappa completa, compresi i diagnostici storici, è in `scripts/README.md`.

## Il codice degli autori, distinto dal nostro

Non abbiamo scritto le reti DA, MoGE, SuperFlex o Whareformer e non le abbiamo addestrate da zero. Le copie locali `Whareformer-repo/`, `SuperFlex-repo/` ed `external/` sono dipendenze escluse da Git; versioni e provenienza restano nei manifest. Gli script richiamano queste implementazioni o funzioni originali con hash controllati. Conservare attribuzioni e licenze quando si ricostruiscono i pacchetti.

> Chiarimento successivo del 13 novembre: confronto e aggiornamento geometrico appartengono allo stesso ciclo. La memoria FIFO disponibile non è ancora registrazione/accumulo; piano in `../ROADMAP_CICLO_GEOMETRICO.md`. Nessun nuovo codice del ciclo implementato durante la pianificazione.

## Nuovi dati del collega

Ricevuti tracks_by_id e joined_observations completi a bbf0e5e; audit reale passato e segmenti registrati preparati. Non ancora configurazione/feature/logits della rete o nuova inferenza. Dettagli in `../VERIFICA_CONSEGNA_WHAREFORMER_20261113.md`. Le precedenti note di assenza dei manifest sono storiche.

## Aggiornamento 2B successivo

`integration_prototype/cloud_memory.py` e runner/test implementano registrazione rigida candidata e memoria dei punti. Sette nuovi test superati; nessun aggiornamento reale ammesso su 12 tentativi, nessuna inferenza su accumuli. Report `../RISULTATI_REGISTRAZIONE_ACCUMULO_20261113.md`. Prevale sulle indicazioni sotto secondo cui registrazione/accumulo non fossero ancora implementati; la validazione reale resta aperta.

## Prototipo locale aggiunto il 13 novembre

`integration_prototype/` contiene il candidato NumPy logits/memoria e i test indipendenti. Sette test e replay con geometrie esistenti superati; nessun matcher neurale, registrazione/fusione o ciclo reale implementato. Dettagli in `../AVANZAMENTO_AUTONOMO_20261113.md`. Non pubblicato su GitHub e distinto dal nucleo portabile condiviso.

## Componenti condivisi successivi all'inventario

Il componente portabile `SuperFlex/src/shape_tools/` contiene pipeline DA/MoGE, geometria, confronto, valutazione, export e memoria causale candidata; esempi/test e limiti nella consegna autonoma. La memoria è indipendente, non ancora collegata al ciclo Whareformer reale.

Dal collega: `Whareformer/build_tracks_by_id.py` ricostruisce gli ID d'osservazione per le track predette; `Whareformer/link_compare200_tracks.py` collega il manifest compare200 alle track. Report P01_01: 71/73 geometrie su 18 track, coerenza verificata ma run reale non ripetuta. I sorgenti sono nel remoto `main` a `ab5a946`, non ancora importati nel worktree candidato locale fermo a `71ce4f1`. Le copie locali degli autori non certificano la versione eseguita dal collega.

## Che cosa resta da implementare o verificare

- Collegamento certificato tra `annotation_index` dei nostri manifest e `detection_idx`, feature e XYZ effettivi della baseline.
- Integrazione della forma nel matcher Whareformer e prova di equivalenza con contributo geometrico zero.
- Collegamento della memoria di forme già implementata ai track reali, con aggiornamento causale dalle associazioni predette.
- Valutazione di tracking DA/MoGE/SuperFlex contro baseline e geometria semplice.

`prepare_baseline.py` controlla input e prepara una configurazione: **non esegue da solo la baseline**. Gli upload del collega sono ora analizzati; output completi e configurazione necessari per una riproduzione indipendente restano da acquisire. Accumulo/registrazione di nuvole sono proposti nel suo README, non implementati nei nuovi upload.

## Come leggere il progetto senza perdersi

1. `README.md`: obiettivo, stato e accessi ai documenti.
2. Questo file: cosa è stato sviluppato e cosa manca.
3. `RISULTATI_CONFRONTO_200.md`: confronto delle sagome/ricostruzioni.
4. `RISULTATI_IDENTITA_DA_MOGE.md`: domanda, procedimento, distanze e AUC del test più recente.
5. `docs/CONDIVISIONE.md`: file del repository e pacchetti dati separati.

Gli script sono strumenti di ricerca costruiti per gli esperimenti documentati, non un pacchetto installabile universale. Alcuni richiedono directory/cache di precedenti run e gli ambienti HPC già predisposti. Non eseguire tutti i file in sequenza: partire dal resoconto dell'esperimento e riusare i risultati conclusi.
