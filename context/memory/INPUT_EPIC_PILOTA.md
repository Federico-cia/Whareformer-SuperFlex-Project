# Input del primo pilota EPIC

7 novembre 2026. SuperFlex robust funziona sull'esempio degli autori. **Marco ha scelto `P01_01` come video pilota comune**, nello split di training Whareformer, e informerà il collega. Prossimo controllo: costruire una nuvola parziale da una reale osservazione del video, verificando RGB, maschera e geometria prima di applicare SuperFlex. Accesso ai dati, frame/oggetti da includere e formato di scambio restano da verificare e coordinare; il pilota non è il test finale.

## Stato dell'acquisizione

**9 novembre — controlli orientamento/profondità/checkpoint conclusi:** job 749200, 84 casi, nessuna correzione semplice e sistematica dimostrata; vedere `DIAGNOSI_SUPERFLEX_749200.md`. Sensibilità alle rotazioni confermata, ma fedeltà non risolta; unsupervised peggiore nel fit medio dei sei confronti. Pipeline comune invariata, controllo MoGE non ancora eseguito.

**9 novembre — SuperFlex su EPIC eseguito:** job 749180 riuscito, risultati ispezionati in `outputs/sf_epic_749180/`. Inferenza valida numericamente ma ricostruzioni ancora poco fedeli, soprattutto nelle due viste più incomplete. Differenza fra riferimento camera del pilota e riferimento ABO nel loader degli autori da diagnosticare; nessuna conclusione sull'utilità per le identità. Dettagli in `VERIFICA_SUPERFLEX_EPIC_749180.md`. Le note sotto su inferenza ancora da eseguire sono storiche.

**9 novembre — prime nuvole prodotte e ispezionate:** job CPU 747518 riuscito, run/log archiviati in `outputs/epic_geometry_cpu_747518/`. Tre nuvole da 1916/6330/19203 punti, controllo numerico e visivo completato; dettagli in `VERIFICA_GEOMETRIA_747518.md`. Allineamento diagnostico in unità scena, scala metrica/equivalenza baseline ancora da verificare. SuperFlex su EPIC non ancora eseguito. Le note sotto su profondità/allineamento/punti ancora mancanti descrivono le tappe precedenti.

**8 novembre — profondità grezza verificata:** job 744902, COMPLETED/0:0 in 12m20s. Risultati scaricati in `outputs/epic_depth_744902/`: tre mappe 456×256 finite e positive, controlli di provenienza e confronto visivo completati. Dettagli in `VERIFICA_PROFONDITA_744902.md`, figura `outputs/epic_depth_744902/controllo_profondita.png`. Accuratezza metrica non misurata; allineamento/scala e nuvole di punti restano aperti. Le note sul job ancora da inviare o profondità da acquisire sotto descrivono la preparazione precedente.

Sono scaricati e verificati localmente l'archivio VISOR denso del video (164.536.221 byte, CRC corretto), il JSON EPIC-Fields (35.745.196 byte, camera OPENCV 456×256, 96.468 pose) e il mapping ufficiale fornito da Marco (100.650.035 byte, 90 video, 45.082 corrispondenze per P01_01). Esaminato in streaming l'intero JSON VISOR da 817 MB senza estrarlo interamente.

Letto via HTTP Range solo il primo MiB dell'archivio RGB originale da 1.716.787.200 byte: recuperati 60 JPEG completi, dei quali **19** hanno maschere e pose corrispondenti. Selezione tecnica basata sulla disponibilità, non sui risultati del modello; non è un campione rappresentativo di valutazione. Preparati tre frame della classe `pan` (19834, 43735, 95971), con indice VISOR/RGB invariato, in `data/epic_pilot/P01_01/diagnostic_ready/`: JPEG originali, maschere PNG, metadati e calibrazione/pose del sottoinsieme. Maschere ridimensionate 854×480 → 456×256 con nearest neighbour, controllate visivamente in `outputs/epic_pilot/controllo_rgb_maschere.png`. Nessuna identità di istanza inferita dal solo nome `pan`.

Provenienza/checksum in `manifests/epic_pilot_P01_01.json` e nei metadati del sottoinsieme; script `inspect_epic_assets.py` e `select_epic_diagnostic.py`. **Profondità e verifica delle medesime osservazioni con il collega ancora pendenti.** Nessuna nuvola EPIC o inferenza SuperFlex su EPIC ancora prodotta.

**Ricostruzione acquisita da Marco:** archivio in Download ed estrazione già presente in `data/epic_pilot/EPIC-Reconstructions/`. Mesh P01_01 da 15.314.411 byte, 206.953 vertici e 413.877 facce, copiata in `diagnostic_ready/scene/` con checksum e provenienza. Non è presente `metric_scale.json`; il config Whareformer riporta `scene_scales.P01_01 = 1.234567901`, ma l'estrattore al commit fissato calcola separatamente la scala e non legge quel campo. Non assumere l'equivalenza dei due valori. Prima dell'allineamento verificare con il collega la scala effettiva della baseline o riprodurne il calcolo; non applicare silenziosamente il valore del config come se fosse il risultato verificato dell'estrattore.

**Prossimo job preparato, non ancora inviato:** `scripts/setup_epic_depth.sbatch` e `scripts/epic_depth_probe.py`, da trasferire con `diagnostic_ready/` in `~/cv_project`. Ambiente personale separato `cv-epic-depth`, core delle versioni ufficiali Whareformer (Python 3.13.13, torch 2.11.0+cu126, torchvision 0.26.0+cu126, transformers 5.5.4, NumPy 2.4.3). Riutilizza i corpi invariati di `load_depth_model` e `forward_depthanything_style` estratti via AST dal sorgente originale, senza importare modelli/rendering estranei alla sola profondità. Sorgente, licenza e hash sono in `diagnostic_ready/reference/`. Un frame alla volta, output 456×256, mappe NPY e anteprime PNG, commit modello osservato e ambiente registrati. **Solo profondità grezza: allineamento, punti e equivalenza baseline non ancora verificati.** Sintassi Python e formato Linux controllati; nessuna inferenza eseguita localmente.

**Discrepanza verificata nel codice Whareformer al commit fissato:** il mapping distribuito è annidato per video, con chiavi `P01_01_frame_XXXXXXXXXX.jpg`; `EPICFrameDataset._load_object_masks` cerca invece direttamente nel dizionario principale una chiave senza video né estensione. Con questo file il lookup non trova le corrispondenze e usa il fallback. Esempio reale: VISOR 937 → RGB 938; 4 delle 19 osservazioni diagnostiche hanno indice diverso. La baseline non è stata modificata. Prima del confronto finale concordare e documentare con il collega come rendere comuni le osservazioni; i tre frame diagnostici scelti evitano per ora il disallineamento d'indice, senza dimostrare equivalenza completa della baseline.

| Risorsa per lo stesso video | Uso | Fonte |
|---|---|---|
| Frame RGB originali | Stima della profondità e controllo visivo | [Downloader ufficiale EPIC](https://github.com/epic-kitchens/epic-kitchens-download-scripts) |
| VISOR dense, JSON per video | Stesse maschere/oggetti della pipeline Whareformer | [Dataset Bristol](https://data.bris.ac.uk/data/dataset/2v6cgv1x04ol22qp9rm9x2j6a7), Interpolations-DenseAnnotations |
| Mapping dei frame densi usato da Whareformer | Corrispondenza fra numerazione VISOR e RGB originali | Link `VISOR dense frame mapping` nel README Whareformer locale |
| EPIC-Fields, JSON per video | Intrinseci e pose, con risoluzione associata | [Download ufficiale](https://epic-kitchens.github.io/epic-fields/site), JSON_DATA |
| Mesh di scena e scala della pipeline originale, oppure profondità allineata già salvata | Riprodurre l'allineamento della profondità Whareformer | Link `EPIC-Reconstructions` nel README Whareformer locale; contenuto dell'archivio ancora da verificare |
| Osservazioni Whareformer del video | Controllare che frame, oggetti e ordine coincidano con la baseline del collega | `epic_osnom.tar.gz` o copia fornita dal collega; sole annotazioni/feature non bastano per la superficie |

La mesh statica serve all'allineamento, non è la superficie degli oggetti mobili. Se non abbiamo mesh/scala o profondità allineata, il primo esperimento con profondità metrica grezza va eventualmente dichiarato come diagnostico separato: non rivendicare lo stesso preprocessing della baseline.

## Ordine della verifica

1. Accertare dove sono gli asset eventualmente già scaricati, evitando duplicati.
2. Verificare prima JSON VISOR, mapping e calibrazione dello stesso video e l'intersezione con le osservazioni della baseline. Individuare i frame RGB necessari, senza scaricare l'intero dataset.
3. Acquisire i frame e la geometria di allineamento necessari. Verificare dimensioni di maschere, profondità e intrinseci: la pipeline locale usa maschere 854×480 e profondità 456×256; bisogna applicare le trasformazioni coerenti con la calibrazione reale, non sovrapporre gli array direttamente.
4. Usare il checkpoint Depth Anything V2 Metric Indoor Large della pipeline Whareformer o recuperare le mappe equivalenti. L'ambiente per l'estrazione va preparato senza alterare l'ambiente SuperFlex funzionante.
5. Esportare per un oggetto RGB, maschera, profondità, punti e provenienza. Solo dopo il controllo visivo applicare SuperFlex robust. Ripetere su altre viste dello stesso oggetto per studiare stabilità.

Sviluppo nel train; identità annotate solo per controlli/valutazione, mai per decidere associazioni. Nessuna modifica al metodo di tracking, alla memoria o al protocollo finale è stata fissata qui.

Verifica fonti del 7 novembre: pagine ufficiali EPIC, VISOR ed EPIC-Fields consultate. Superati i timeout delle pagine Bristol usando l'indice pubblico `/datasets/`; acquisito lo ZIP del video. Individuato nel browser il singolo JSON Dropbox e scaricato tramite collegamento pubblico diretto. I download RGB e del mapping non sono ancora effettuati. Il codice locale conferma modello di profondità, allineamento su scena e file attesi.
