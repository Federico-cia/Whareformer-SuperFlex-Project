# Prime nuvole EPIC — verifica del 9 novembre 2026

Accesso diretto SSH con chiave verificato dall'assistente. Job 747518 COMPLETED, ExitCode 0:0, 13m11s. Run e log recuperati in `outputs/epic_geometry_cpu_747518/`; nessun modello eseguito localmente.

Rendering OSMesa/llvmpipe, Mesa 25.0.5. Box di controllo: profondità attesa 1.5, ottenuta 1.4999907. Fork PyOpenGL al commit `76d1261adee2d3fd99b418e75b0416bb7d2865e6`; ambienti e pacchetti archiviati nel run.

| Frame | Punti | RMSE del fit in unità scena | Rendering + fit + export |
|---|---:|---:|---:|
| 19834 | 1916 | 0.408 | 0.434 s |
| 43735 | 6330 | 0.301 | 0.278 s |
| 95971 | 19203 | 0.569 | 0.376 s |

I tempi per frame escludono installazione, caricamento mesh e rete neurale: non sono il costo della pipeline completa. I 13m11s includono il setup.

Controlli locali su file salvati: checksum coerenti; punti/depth finiti e positivi sull'oggetto; corrispondenza esatta pixel/maschera/colori; riproiezione entro 3e-14 pixel e trasformazione camera/mondo coerente. Queste identità numeriche verificano l'implementazione, non l'accuratezza della stima di profondità.

Figura `outputs/epic_geometry_cpu_747518/controllo_nuvole.png` ispezionata: prima vista fortemente troncata, seconda soprattutto bordo della padella, terza superficie più estesa; punti dispersi e profili di profondità irregolari ai bordi. Ogni riga è centrata/ingrandita separatamente; non dedurre uguale dimensione o identità dell'oggetto dal grafico.

RMSE relativo alla mediana della profondità di scena dei pixel usati nel fit: circa 17%, 10%, 18%. È un residuo di accordo con la mesh, non errore rispetto alla vera superficie della padella. Un fit valido numericamente non elimina gli errori della profondità.

Le maschere effettive sono rasterizzate con OpenCV come Whareformer; rispetto alle anteprime Pillow precedenti cambiano rispettivamente 203/433/311 pixel (differenza simmetrica), principalmente contorni. Le nuvole usano quelle OpenCV, salvate nel run.

Scala esplicitamente 1 in unità della ricostruzione, non metri. Restano da verificare scala, clipping e osservazioni rispetto alla baseline. Nessuna inferenza SuperFlex su EPIC ancora eseguita. Prossimo passo: usare queste nuvole per una prima prova diagnostica SuperFlex robust, mantenendo visibili i limiti dell'input e senza dedurre un beneficio per il tracking.
