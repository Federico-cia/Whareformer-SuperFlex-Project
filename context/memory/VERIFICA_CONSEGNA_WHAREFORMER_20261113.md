# Verifica dei manifest Whareformer appena condivisi

13 novembre 2026. Marco segnala il nuovo upload; ripreso lo step 1. Letti i due nuovi file dei commit `0b62e1b` e `bbf0e5e`, remoto osservato a `bbf0e5e`. Nessun merge/push o inferenza. Copia immutata e hash in `outputs/github_handoff_bbf0e5e/snapshot_manifest.json`.

## Che cosa è arrivato e che cosa è verificato

Caricati `tracks_by_id.json` (47.75 MB, 52 track, 110590 righe) e `compare200_joined_observations.json` (73 osservazioni, percorsi portabili). Non aggiunti configurazione effettiva, comando/ambiente/versione del tracker, identificazione verificabile del checkpoint, feature visive/XYZ originali, pickle di inferenza o metriche dell'evaluator.

Eseguito sui dati reali `scripts/audit_tracking_contract.py`, confrontando il nostro riferimento originale con track e manifest completo: **passato senza errori**. Join ricalcolato per frame/ID, colonne e campi coerenti: 71 exact, due mancanti conservati. Non è stata rieseguita l'inferenza o la ricostruzione di tracks_by_id dal pickle sorgente, ancora assente.

Controlli aggiuntivi:

- 33310 frame con osservazioni; track ordinate temporalmente, nessuna ripetizione del frame nella stessa track, indici detection contigui per frame; 110590 XYZ finiti a tre componenti. Sono proprietà dei dati esportati, non prova del contenuto/ordine delle feature originali.
- Su tutte le 71 osservazioni collegate, ID/categoria e bounding box coincidono con il poligono VISOR del nostro input selezionato, usando minimi e massimi+1. I box sono nel riferimento maschere 854×480; RGB e maschere del nostro ramo geometrico sono 456×256. Non sovrapporre i box ai nostri RGB senza ridimensionarli. Nessuna modifica delle nuvole o degli intrinseci.
- Verificati i byte e SHA-256 di tutte le 146 nuvole DA/MoGE referenziate dalle 73 osservazioni, inclusi i due casi non collegati.
- **69/71 annotation_index differiscono da detection_idx.** Usare gli ID e il mapping esportato; non riutilizzare l'indice della lista VISOR come riga delle feature.

Evidenze: `contract_audit.json`, `extended_audit.json`, nella cartella dell'upload. Preparato `three_frame_baseline_observations.json`: P01_01, frame 2893/5099/7508, dieci detection esportate complessive con associazioni effettive, lookup delle geometrie disponibili e track baseline nate prima del frame. È un segmento di dati registrati: non contiene feature di aspetto o logits e non rappresenta una nuova esecuzione del matcher.

## Diagnosi dei due mancanti: differenza VISOR/RGB

Gli ID non sono assenti dalle track: compaiono al nome-frame VISOR, un indice prima del nome RGB del nostro ramo.

| Osservazione RGB | Frame nelle track | Track | Mapping originale verificato |
|---|---|---:|---|
| frame_0000022584, pan | frame_0000022583 | 9 | P01_01_frame_0000022583.jpg → frame_0000022584.jpg |
| frame_0000040874, kettle | frame_0000040873 | 21 | P01_01_frame_0000040873.jpg → frame_0000040874.jpg |

Sono esattamente i due casi, fra le 73 osservazioni, in cui la mappa VISOR→RGB cambia indice. Verificati i record originali e il mapping già presenti sullo spazio personale HPC, con lettura mirata di un solo archivio e senza nuovi job. La prima interrogazione usava il nome RGB come nome VISOR e chiavi incomplete per il mapping: conservata come diagnostica preliminare e superata dal controllo corretto `source_frames_corrected_diagnosis.json`.

I record sorgenti sono identificati per ID, non per nome o sola box. L'ID della padella osservata al nome RGB 22584 esiste anche fra le righe al nome 22583; il pan già presente al nome 22584 ha un altro ID, pur avendo la stessa box. Non sostituire un ID solo perché le box coincidono.

**Interpretazione verificata:** disallineamento dei nomi-frame nel collegamento. **Ancora da verificare:** quale JPEG abbia generato le feature e le posizioni della run. La copia locale del loader cerca una chiave di mapping e ripiega sul nome VISOR quando non la trova; senza versione/configurazione effettive non è accertato se nella run ci sia solo una convenzione di nomi differente o uno spostamento reale degli input. I due alias sono registrati separatamente in `temporal_aliases.json`, non promossi a exact. Il join verificato resta 71/73.

## Revisione delle track

Nel file completo 20/52 track contengono più categorie; è un segnale da esaminare, non una metrica di errore d'identità o GT. Nuove tavole RGB/maschera per tutte le osservazioni geometriche delle track 4, 36, 9 e 35, ispezionate in questa verifica.

- **Track 4:** sette osservazioni di tagliere e due di grattugia nel nostro sottoinsieme; la tavola mostra oggetti fisicamente differenti. È un caso concreto di memoria che verrebbe contaminata seguendo l'intera track senza controlli.
- **Track 36:** categorie saucepan/sieve; la tavola mostra contenuti diversi da revisionare, non una forma omogenea garantita dall'ID.
- **Track 9:** le 18 geometrie disponibili sono compatibili visivamente con la padella rossa riferita dal collega, ma il file completo include anche 284 righe container oltre alle 12813 pan. Queste 284 osservazioni non sono certificate dalle sole immagini compare200.
- **Track 35:** le 13 geometrie pan appaiono compatibili con la padella rossa in una parte intermedia della sequenza; il completo include anche 557 saucepan oltre alle 6994 pan. Le tavole 9/35 suggeriscono possibile frammentazione della stessa padella, non nuova identità GT certificata o diagnosi completa delle due track.

Tavole in `outputs/github_handoff_bbf0e5e/track_{4,36,9,35}_review.png`. Nessuna modifica alle etichette visive storiche delle 37 osservazioni e nessuna trasformazione delle associazioni predette in ground truth.

## Conseguenza sulla roadmap

Acquisizione dei due manifest e verifica interna/geometrica del join completate. È disponibile il collegamento alle associazioni reali, utile per il ramo che aggiorna la memoria dopo il tracking e per costruire segmenti diagnostici senza inventare track.

Lo step 1 completo resta aperto per allineamento temporale delle feature, configurazione/versione/checkpoint, accesso agli input e metriche baseline. Riprodurre la run specifica o verificare peso zero del matcher reale richiede questi elementi. Il nuovo upload non risolve automaticamente i problemi di registrazione/scala emersi nello step 2B: una track corretta non fornisce una posa d'oggetto.

Priorità: verificare i due alias e la provenienza dei frame/feature; usare il mapping esplicito sui 71 exact e i casi di contaminazione come diagnostica. Richiesta dati residui ora mirata alla run, senza richiedere nuovamente i due JSON già acquisiti. Nessun nuovo esperimento neurale, job HPC, controllo coda o messaggio al collega in questa verifica.
