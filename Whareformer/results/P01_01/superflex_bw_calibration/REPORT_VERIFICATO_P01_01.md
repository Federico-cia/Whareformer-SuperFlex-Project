# Calibrazione SuperFlex → Whareformer: risultati verificati su P01_01

**Stato dell’esperimento:** calibrazione preliminare supervisionata dei logits con Whareformer e SuperFlex congelati, non valutazione del tracking causale completo. **Data dell’esecuzione:** 22 novembre 2026 (job HPC riportato: `784681`, esito `COMPLETED 0:0`).

## Obiettivo

Stimare due parametri scalari per correggere, a valle del classificatore di Whareformer, il punteggio di associazione tra una osservazione e una traccia utilizzando la forma ricostruita da SuperFlex, senza cambiare l’architettura né riaddestrare le reti.

## Modello

\[z\prime_{ij}=z_{ij}+m_{ij}\,(b-wd_{ij}),\qquad w\geq 0.\]

- `z_ij`: logit originale di Whareformer per la candidata `j`; `m_ij`: maschera che vale 1 solo con confronto geometrico disponibile; `d_ij`: distanza geometrica D2; `b`: bonus/penalità dovuto alla **disponibilità** della geometria; `w`: peso della distanza, più alto per oggetti geometricamente differenti.
- La candidata `New Track` mantiene il proprio logit; se la geometria manca, si applica correzione zero.
- L’opzione `solo b` è un **controllo essenziale**: premia le associazioni con geometria disponibile ma non utilizza la distanza. Il miglioramento ulteriore di `b+w` rispetto a `solo b` è il segnale specifico della forma.

## Dati e procedura

1. **Etichette oracle:** manifest originale di training di Whareformer, `P01_01` (110.589 righe); 66 esempi risultano esportabili con confronti geometrici coerenti, su 35 frame.
2. **Geometria:** mesh SuperFlex per singola osservazione, ricavate da nuvole MoGE oppure Depth Anything (DA); 71 osservazioni geometriche di `P01_01` collegate alle feature. Il campione delle mesh appartiene a `compare200`.
3. **Descrittori D2:** 1.024 punti campionati sulla superficie, normalizzati rispetto a centro e raggio RMS; distribuzione ordinata di 16.384 distanze tra coppie di punti. La distanza fra forme è la differenza media assoluta fra i rispettivi descrittori D2.
4. **Memoria geometrica:** ultime due osservazioni geometriche precedenti (`FIFO=2`) per traccia oracle, confronto mediante minima distanza D2. La memoria viene aggiornata **dopo** lo scoring con l’associazione oracle, senza utilizzare osservazioni future.
5. **Logits congelati:** Whareformer eseguito sul checkpoint originale e sulle feature del LMDB; corrispondenze verificate mediante hash delle feature. Le candidate oracle non vanno identificate con le track predette dal tracker durante inferenza libera.
6. **Ottimizzazione:** negative log-likelihood/cross-entropy softmax, regolarizzazione L2 `0.001`, algoritmo SciPy `L-BFGS-B`, vincolo `w>=0`; la distanza viene scalata con una mediana calcolata sul training, poi `w` viene restituito nelle unità originali D2.
7. **Split interno:** 53 righe usate per stimare i coefficienti e 13 righe successive per la validazione **all’interno dello stesso video**. Non è una separazione indipendente fra video.

## Coefficienti ottenuti

| Sorgente forma | b | w (distanza D2 originale) | d neutra = b/w |
|---|---:|---:|---:|
| MoGE → SuperFlex | 1.282405 | 0.700344 | 1.831107 |
| Depth Anything → SuperFlex | 1.440272 | 3.456357 | 0.416702 |

I due valori di `w` **non sono direttamente confrontabili come grandezze fisiche**, perché la distribuzione delle distanze D2 dipende dalla sorgente geometrica e dal relativo preprocessing.

## Metriche dello scoring oracle

Le metriche seguenti riguardano **l’associazione riga-per-riga** del manifest oracle; non sono IDF1 né mPCL. Cross-entropy minore significa maggiore probabilità assegnata al target corretto.

| Sorgente | Split | N | CE Whareformer | CE solo b | CE b+w | Argmax corretti (tutti i metodi) | Argmax cambiati |
|---|---|---:|---:|---:|---:|---:|---:|
| MoGE | train | 53 | 0.039988 | 0.025096 | 0.025009 | 100% | 0 |
| MoGE | validation | 13 | 0.065979 | 0.041531 | 0.041273 | 100% | 0 |
| Depth Anything | train | 53 | 0.039988 | 0.025096 | 0.024097 | 100% | 0 |
| Depth Anything | validation | 13 | 0.065979 | 0.041531 | 0.039648 | 100% | 0 |

### Differenze sulla validazione interna (13 righe)

- **MoGE:** CE da `0.065979` a `0.041273` (−37.45% rispetto alla baseline); rispetto a `solo b` (`0.041531`), riduzione aggiuntiva **0.62%**.
- **Depth Anything:** CE da `0.065979` a `0.039648` (−39.91% rispetto alla baseline); rispetto a `solo b` (`0.041531`), riduzione aggiuntiva **4.53%**.

**Interpretazione:** la maggior parte del calo di CE è spiegata da `b`, cioè dalla disponibilità della geometria. L’informazione D2 aggiunge poco. Nessuna decisione argmax cambia in questo campione. Il metodo modifica la confidenza, non l’identità predetta nelle righe testate.

## Controlli indipendenti effettuati sui file HPC

- Verificata la corrispondenza fra i 66 esempi MoGE e DA: stessi identificativi, logits Whareformer, etichette e maschere di disponibilità geometrica.
- Ricalcolate direttamente dai file JSONL tutte le cross-entropy dei tre modelli su train e validation: coincidono con le metriche riportate nell’output HPC (precisione numerica migliore di `1e-10`).
- Confermati 505 confronti osservazione–candidata con distanza geometrica valida, 54 esempi con geometria anche sulla candidata corretta; quattro collisioni candidate escluse dal report di esportazione.
- **Nessuno dei 66 target è `New Track`.** Questa asimmetria limita fortemente l’interpretazione del coefficiente `b`, che può premiare sistematicamente una traccia esistente senza testare i veri casi di nascita.
- Dove target e rivali dispongono entrambi di geometria (53 righe dopo le esclusioni), la forma corretta ha la distanza minima solo in **18/53 (MoGE)** e **15/53 (DA)**: D2 non è sempre un buon indicatore di identità.
- Il report di esportazione registra 1 conflitto di merge della memoria e 0 candidate da frame futuri; queste anomalie/esclusioni vanno mantenute nella documentazione.

## Limiti e validità scientifica

1. **Pilot su un solo video (`P01_01`)**. Lo split temporale non dà una misura di generalizzazione a video indipendenti. Le 13 righe di validation sono poche.
2. **Campione estremamente selezionato:** 66 su 110.589 esempi del manifest (~0,060%) hanno una correzione geometrica esportabile; il resto non è incluso nei risultati sopra.
3. **Ground-truth/teacher forcing:** memoria e candidate derivate dalle associazioni oracle, non dall’evoluzione delle tracce predette. Errori di tracking e nuove track non sono simulati.
4. **Nessun miglioramento di IDF1/mPCL misurato**: per questo occorre applicare i parametri nel tracker completo, con assegnazione multi-oggetto e aggiornamento causale delle track predette.
5. **Mesh single-frame**, non SuperFlex su nuvole fuse o accumulate; questa prova riguarda soltanto l’integrazione a valle dei logits.
6. **Invarianza/normalizzazione D2:** si perdono scala fisica e dettagli spaziali; superfici simili di oggetti diversi possono generare distanze piccole.
7. **Dominanza del bias `b`:** poiché i target validati sono tutti associazioni a track esistenti, una migliore CE non prova un effetto discriminativo della forma.

## Passi necessari prima di chiamare il metodo “validato”

1. Costruire analoghi esempi supervisionati su **video disgiunti** usando nuvole e mesh già disponibili, verificando hash e candidate in ciascun video; aggiungere casi difficili e target `New Track`.
2. Stimare `b,w` su un insieme di training, scegliere la regolarizzazione/metriche geometriche su validation, e usare un **test set di video non utilizzati in alcuna scelta**.
3. Integrare `weight=w` e `bias=b` nel matcher esterno in una revisione del codice verificata, preservando il comportamento baseline quando la geometria manca.
4. Eseguire il **tracking causale completo** con tre varianti `W0`, `solo b`, `SuperFlex b+w` sulla stessa copertura; misurare IDF1/mPCL, associazioni modificate, runtime e casi falliti.
5. Documentare eventuali risultati nulli o negativi, confrontando esplicitamente effetto del bias, distanza D2, copertura e qualità delle mesh.

## Provenienza e riproducibilità

- Risultati originali: `Whareformer_SuperFlex_b_w_P01_01_RESULTS.zip` inviato il 22 novembre 2026.
- File della presente cartella: `P01_01_*_bw_DEVELOPMENT.json`, `P01_01_*_variant_config.json`, `P01_01_*_export_report.json`, `P01_01_superflex_comparison.json`, `P01_01_*_descriptor_verification.json`.
- Le configurazioni delle varianti sono **candidate per un replay futuro**, non evidenza che il replay completo sia stato eseguito.
- File contenenti checkpoint, LMDB, mesh e singole righe oracle non sono inclusi in questo pacchetto GitHub per evitare distribuzioni non autorizzate e dati voluminosi; sono conservati nel pacchetto dei risultati HPC.
- Non abbiamo modificato il repository remoto o eseguito il replay causale completo durante questa verifica.

### SHA-256 principali: moge

- Manifest oracle: `725dc2f328bdbcf9885e47eb5d4f92d528f177252747b7c917d046a34b7eb7b0`
- Checkpoint Whareformer: `5b2e6692461f837ec662d0ac75a5f8c08e4fa9778e5c1b9833598cf90a58ee1d`
- Sorgente originale Whareformer: `ead5b997ca975eb97592efa3edcc2d070818cefbc00813e3eca42dbcdbdfdf94`
- Indice descrittori: `25152c55b54eac94230d96db7d9d8ae444c99d0a7094026d0aafab96845c8609`
- File JSONL delle righe oracle: `cace7afa28d750d260f0385752369974635d12df7cc44d590208bcea0ae9acad`

### SHA-256 principali: da_raw

- Manifest oracle: `725dc2f328bdbcf9885e47eb5d4f92d528f177252747b7c917d046a34b7eb7b0`
- Checkpoint Whareformer: `5b2e6692461f837ec662d0ac75a5f8c08e4fa9778e5c1b9833598cf90a58ee1d`
- Sorgente originale Whareformer: `ead5b997ca975eb97592efa3edcc2d070818cefbc00813e3eca42dbcdbdfdf94`
- Indice descrittori: `d124358a77ce6c764816d6361b2ea9f30e48585f9c57f35f35cacbe10d581dc8`
- File JSONL delle righe oracle: `4c85dba766e7d5b3f25c8e8fbe8964baefa060a4bbf2c87f0f231f5bc7950d66`

