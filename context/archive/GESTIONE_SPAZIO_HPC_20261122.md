# Capacità e conservazione dei file HPC — 22 novembre 2026

**Revisione successiva approvata da Marco:** implementazione e migrazione documentate in [COMPATTAZIONE_HPC_20261122.md](COMPATTAZIONE_HPC_20261122.md). Le proposte sotto restano l'analisi preliminare. La rigenerazione ordinaria di tutti e tre i derivati è ora CPU e senza perdita: si conservano le matrici originali in archivio e la palette dei PLY, perché il replay GPU non è risultato identico. **Migrazione 785105 e audit 785556 conclusi**, 46080 derivati rimossi dopo verifica, circa 3.3 GiB netti recuperati. Quota 41.92/46.56 GiB, conservazione futura abilitata; proiezione ordine 160 GiB e capacità complessiva ancora insufficiente. Nessun rilancio della campagna.

## Domanda e perimetro

Marco chiede perché lo spazio sia quasi esaurito e come completare tutti i blocchi con una gestione più efficiente. Analisi di sola lettura di metadati remoti, contenuto degli indici ZIP di pochi NPZ e codice locale. Nessuna nuova cancellazione, esportazione di geometrie, inferenza o ripresa della catena. La precedente autorizzazione all'archiviazione dei tracciati non viene estesa automaticamente ad altri dati.

## Vincoli verificati

- Quota personale: 50 GB decimali, cioè circa **46.56 GiB**, e **500000 file/inode**. Lo spazio libero complessivo del filesystem non è la disponibilità dell'utente.
- [Controllo delle 11:31:28](CONTROLLO_HPC_20261122.md): **45.30 GiB** e **485960 file** occupati; 15/216 blocchi completati, 7680 nuove osservazioni, coda vuota. Stop preventivo codice 75 nei successori, con riserva operativa di 2 GiB/12000 file. Non sono soglie scientifiche.
- La [pulizia precedente](PULIZIA_E_RIPRESA_HPC_20261121.md) ha liberato 5.47 GiB conservando e verificando i tracciati sul PC. I sette blocchi successivi hanno rioccupato circa 4.42 GiB. Non basta ripetere una pulizia occasionale.

Un blocco completo già misurato (`geometry/0004`, 512 osservazioni) occupa **686428672 byte = 0.639 GiB**:

| Contenuto | Byte allocati | MiB circa |
|---|---:|---:|
| Mappe DA | 33034240 | 31.5 |
| Mappe MoGE | 141275136 | 134.7 |
| Nuvole DA | 90191360 | 86.0 |
| Nuvole MoGE | 56602624 | 54.0 |
| Esportazioni SuperFlex DA | 185698816 | 177.1 |
| Esportazioni SuperFlex MoGE | 173280768 | 165.3 |

Le righe non includono tutti i file accessori del totale. Estrapolare questo blocco a 216 dà **circa 138 GiB soltanto di output**, prima di software, pesi e input. È una stima da un blocco, non una previsione esatta: dimensioni delle maschere, primitive attive e numero di frame unici variano. Dimostra comunque l'inadeguatezza del formato corrente per una quota di 50 GB.

## Ridondanze dimostrate dal codice e da un campione remoto

### Inventario delimitato e aggregati osservati

Inventario metadati limitato a 300.5 secondi, senza errori: 402947 file regolari/altri, 56216 directory e 8760 collegamenti di proprietà dell'utente, 36.826 GiB conteggiati, **4076 directory ancora da percorrere**. Non è una ripartizione completa dei 45.30 GiB della quota; i valori per cartella sono limiti inferiori. Esclusa `.ssh`, nessuna lettura dei payload durante la scansione; inode deduplicati. Eventuali hard link fra ambienti sono attribuiti alla prima voce incontrata, non sommabili come copie indipendenti.

Rilevati almeno **12.88 GiB in `.conda`** (quattro ambienti, incluse librerie GPU), **2.465 GiB nei pesi `hf_cache`**, **12.194 GiB nella geometria corrente**, 1.186 GiB/168625 file negli input correnti, oltre all'archivio `P01_01.tar` di 1.599 GiB. Un ambiente usato non è un insieme di file inutili; librerie CUDA/PyTorch sono fra i file maggiori. La piccola cache generica `.cache` rilevata non è il principale responsabile. Sono presenti anche campagne/archivi storici, da valutare separatamente.

Per le quattro famiglie per osservazione risultano i conteggi attesi dei 15 blocchi: 7680 `points.npz` per fonte e 7680 per ognuno dei quattro artefatti SuperFlex per fonte, oltre ai report. Aggregati allocati osservati:

| Famiglia, DA + MoGE | GiB circa |
|---|---:|
| Mappe dense, 2134 record per fonte | 3.970 |
| Nuvole oggetto | 2.934 |
| Predizioni diagnostiche SuperFlex | 2.588 |
| Input SuperFlex | 0.785 |
| Mesh PLY | 1.721 |
| Parametri SuperFlex compatti | 0.059 |

La rimozione ipotetica di diagnostiche e PLY libererebbe circa 4.31 GiB, **dopo** la verifica delle dipendenze e della rigenerazione; non autorizzata/eseguita da questa analisi. Questo risparmio, da solo, non risolve l'intera campagna. Il costo già conteggiato nei primi 15 blocchi proietterebbe circa 176 GiB a 216 a media costante, superiore ai 138 del singolo blocco precedente; entrambe sono estrapolazioni, non stime statistiche della distribuzione completa. Il problema di fattibilità resta, anche usando la stima inferiore.

Evidenze locali: `outputs/storage_inventory_20261122/inventory_parallel_v2.log` (grezzo), `inventory.json` e `inventory_summary.json` (quest'ultimo elimina gruppi per directory non pertinenti alle famiglie di file). Gli inventari iniziali sono stati interrotti sostituendo solo il proprio processo di scansione; anche la scansione delimitata è ora conclusa. Nessun processo di inferenza avviato o interrotto.

Codice: `shared_exports/handoff_ai_20261114/SuperFlex/src/shape_tools/pipeline.py`, stadi backend/clouds/superflex/export; `SuperFlex-repo/superflex/utils/predictions_handler.py`, `save_npz` e `get_mesh`.

1. I backend sono deduplicati per hash RGB **entro il singolo blocco**. La stessa immagine in blocchi diversi può quindi produrre copie delle mappe dense.
2. MoGE conserva insieme punti densi, profondità, maschera e intrinseci. Nel campione di un frame: 1617054 byte; il solo array dei punti pesa 1246325 byte compressi, la profondità 369939. Non è stata ancora verificata la ricostruzione numericamente equivalente dei punti dagli altri array: non dichiarare cancellabile l'array per sola plausibilità.
3. Le nuvole per oggetto conservano punti, colori e pixel. Colori e pixel si ripetono fra DA e MoGE nel campione; generalizzazione e politica dei pixel vanno controllate prima di deduplicare.
4. Per ogni ricostruzione SuperFlex sono salvati input normalizzato, predizione completa, parametri compatti, PLY e report. La predizione completa include di nuovo nuvola e parametri, oltre alla matrice di assegnazione punti/primitive.

Campione DA del blocco 0004 (non media della campagna):

| File | Byte effettivi |
|---|---:|
| `input.npz` | 39795 |
| `prediction.npz` | 126992 |
| `shape_parameters.npz` | 3780 |
| `reconstruction.ply` | 71638 |
| `report.json` | 1156 |

Nella predizione DA, matrice di assegnazione e nuvola pesano rispettivamente 92633 e 30111 byte compressi. I parametri geometrici sono già salvati separatamente. `get_mesh` usa i parametri geometrici e non la matrice di assegnazione o la nuvola; la possibilità di rigenerare i PLY senza nuova inferenza è quindi supportata dal codice. **Equivalenza numerica e adattamento del caricatore ancora da provare**, inclusi risoluzione, colori, trasformazioni, versione del codice e presenza delle primitive.

Evidenza dei campioni: `outputs/storage_inventory_20261122/npz_samples.jsonl`. I file NPZ sono già compressi: non trasferire agli output la forte comprimibilità dimostrata dai vecchi tracciati testuali.

## Strategia raccomandata — proposta, non ancora implementata

### Destinazione dei singoli artefatti, chiarita su richiesta di Marco

| Artefatto corrente | Funzione | Condizione per non conservarlo separatamente |
|---|---|---|
| `da/*/prediction.npz` | Profondità completa, generazione nuvole e allineamento alla scena | Dopo allineamento e conservazione verificata dei dati necessari; ricalcolarla richiede inferenza |
| `moge/*/prediction.npz` | Geometria densa, profondità, validità e intrinseci per estrarre tutte le nuvole del frame | Dopo estrazione/verifica e controlli previsti; ricalcolarla richiede inferenza |
| `clouds_{da,moge}/*/points.npz` | Punti per oggetto, colori e pixel di provenienza; dati geometrici derivati dall'immagine per memoria/verificatore/confronti | Da mantenere nel lavoro corrente, eventualmente ricollocati/deduplicati con lettori compatibili; una mesh non li sostituisce |
| `superflex_*/*/input.npz` | 4096 punti normalizzati, indici selezionati e normalizzazione | Rigenerazione verificata da nuvola, selezione e normalizzazione conservate; nessuna nuova inferenza per questo file |
| `superflex_*/*/prediction.npz` | Parametri, nuvola denormalizzata e assegnazioni punti/primitive | Candidato a conservazione solo su campione diagnostico, da approvare/verificare; le assegnazioni non sono contenute nei soli parametri e recuperarle richiede inferenza |
| `superflex_*/*/shape_parameters.npz` | Forma parametrica compatta e probabilità di esistenza delle primitive | Conservare; piccolo risultato centrale per rigenerare superfici e confrontare forme |
| `superflex_*/*/reconstruction.ply` | Superficie per visualizzazione, consegna e attuali lettori delle mesh | Dopo rigenerazione equivalente dai parametri e adeguamento dei lettori; conservare comunque le consegne già preparate |
| Report, indici, manifest, configurazioni e hash | Associazione osservazioni/fonti, esiti, riproducibilità e ripartenza | Conservare l'informazione, eventualmente consolidandola in indici; non cancellarla come log generico |

I file di input RGB/maschere, i pesi e gli ambienti sono prerequisiti, distinti dagli output sopra. L'archivio originale può essere ridondante soltanto dopo verifica del contenuto necessario e della procedura di ripristino. Le nuvole sono stime dei modelli, non ground truth o scena già fusa.

**Comportamento esatto della ripartenza:** `cached()` controlla tutti gli artefatti di un record ready e solleva `ValueError("Corrupt cached artifact")` se uno manca o ha hash diverso; è chiamata prima del blocco di gestione degli errori di `run_item`. La cancellazione manuale non è una pulizia supportata: può arrestare lo stadio. Rigenerare le diagnostiche attraverso un reset o una modifica del flusso sarebbe un intervento ulteriore, non il comportamento automatico garantito.

1. **Budget e bonifica mirata.** Distinguere software effettivamente usato, cache di installazione, pesi necessari, input, vecchie campagne e risultati correnti. Rimuovere soltanto contenuti dimostrati ridondanti/ripristinabili e nel perimetro autorizzato; non trattare indistintamente gli ambienti come cache.
2. **Cache condivisa per frame**, indicizzata anche da modello, configurazione e revisione: una sola predizione densa per immagine invece di una copia per blocco. Costo: adattare riferimenti, concorrenza e ripartenza; beneficio: nessuna modifica del modello o della copertura.
3. **Conservazione dopo i consumatori.** Tenere intermedi durante il calcolo; al termine salvare un record minimo verificato con provenienza e dati richiesti dagli esperimenti. I parametri SuperFlex possono sostituire la conservazione permanente dei PLY solo dopo una prova di rigenerazione. Conservare la predizione diagnostica completa su un campione di audit, se approvato, invece che assumerla necessaria per ogni osservazione.
4. **Contenitori per blocco e indice**, preservando accesso ai singoli record, hash e pubblicazione atomica. Riduce file/inode e migliora la gestione; da solo non elimina i byte delle grandi matrici.
5. **Calcolo, verifica, consumo e compattazione progressivi.** Limitare gli intermedi contemporanei ai blocchi attivi. Eseguire i blocchi in serie senza cambiare conservazione riduce il picco, ma non lo spazio finale cumulato.

Vincoli scientifici: la profondità DA completa serve all'allineamento alla scena con background/mesh; non eliminarla prima di avere eseguito e conservato gli esiti necessari. Le nuvole osservate e la loro provenienza servono alla memoria/verificatore: non sostituirle tacitamente con mesh ricostruite, sola forma o un campionamento ridotto. Non cambiare precisione, numero di punti, fonti DA/MoGE, copertura o protocollo per rientrare nella quota senza decisione esplicita.

**Prova minima prima della migrazione:** un blocco completo esistente in una copia isolata, senza nuova inferenza; confrontare ricostruzioni e letture degli stadi downstream, hash e provenienza conservati, capacità di ripartenza, byte e inode finali/di picco. Adeguare i contratti della cache: oggi la validità richiede tutti gli artefatti dichiarati nei report e una cancellazione manuale isolata arresta la verifica del record ready. Poi stimare il budget totale e migrare i blocchi già conclusi prima del rilancio.

**Limite:** non è ancora dimostrato che tutto il patrimonio informativo richiesto dal protocollo entri in 50 GB insieme ad ambiente e input. Se la rappresentazione minima verificata eccede il budget, serve conservazione esterna persistente o quota aggiuntiva. Non promettere completamento entro quota sulla base del solo esempio 127 KB → 3.8 KB, che riguarda un file diagnostico e non tutto il blocco.
