# Replica della pipeline RGB SuperFlex

**Priorità rivista il 9 novembre:** questo documento conserva la preparazione della replica completa, ora opzionale. Il piano corrente è `TODO.md`: prima MoGE-2 con maschere VISOR comuni al tracker, poi verifica del segnale e integrazione. SAM3 e l'abilitazione ai suoi pesi non sono prerequisiti. Le istruzioni seguenti si applicano soltanto se si riprenderà la replica completa.

**Avanzamento successivo:** il controllo MoGE-2 + VISOR è stato eseguito e verificato nei job 749539/749582; non risolve la scarsa fedeltà sui tre input. Vedere `VERIFICA_MOGE2_749539.md`. La pipeline completa con SAM3 resta ineseguita; le note di preparazione sotto sono storiche.

Aggiornamento: 9 novembre 2026. Preparazione avviata; nessun nuovo job SLURM inviato, nessuna inferenza RGB eseguita.

## Evidenze e scelte operative

Riletti stato, discussione d'integrazione e istruzioni scientifiche. Ricontrollati [appendice D e bibliografia del paper](https://arxiv.org/html/2607.01015#A4): SAM3 segmenta gli oggetti, MoGE produce le point map parziali, SuperFlex robust stima le primitive per oggetto. Il riferimento [33] è **MoGe-2**, non MoGe-1 né MoGe-3.

L'appendice non specifica checkpoint esatti di SAM3/MoGE, prompt, soglie, risoluzione e trasformazioni degli input sufficienti a riprodurre esattamente la figura 13. Il repository SuperFlex consultato assume PLY degli oggetti già segmentati per l'inferenza sulle scene; non include uno script completo SAM3/MoGE. La nostra esecuzione sarà una replica dei componenti descritti, con dettagli operativi dichiarati, non una riproduzione identica della figura.

Punto di partenza: SAM3 originale (`facebook/sam3`), MoGE-2 (`Ruicheng/moge-2-vitl`), SuperFlex supervised robust già verificato. Il checkpoint specifico MoGE è una nostra scelta operativa, non un dettaglio confermato dagli autori. Nessun passaggio implicito a SAM 3.1/MoGE-3.

Sono state individuate tramite API GitHub le ultime revisioni disponibili prima del 1 luglio 2026, data della v1 del paper:

- MoGE: `07444410f1e33f402353b99d6ccd26bd31e469e8`.
- SAM3: `5dd401d1c5c1d5c3eedff06d41b77af824517619`.

Queste sono revisioni scelte per la nostra preparazione, non versioni dichiarate dagli autori SuperFlex. Archivi ufficiali **scaricati ed estratti** sull'HPC sotto `~/cv_project/external/rgb_sources/`, comando concluso con exit code 0. SHA-256 registrati in `manifests/rgb_sources.json`. Esaminati pyproject MoGE 2.0.0 e firma di `v2.infer`, oltre alla firma del builder immagini SAM3. Nessun ambiente nuovo installato.

## Dipendenza esterna ancora mancante

SSH con chiave operante, comandi remoti eseguiti. Il download anonimo ufficiale `facebook/sam3/resolve/main/sam3.pt` restituisce **HTTP 401**; nessun file token nella posizione standard `~/.cache/huggingface/token`. Non sono stati letti o stampati segreti. Marco ha confermato che deve ancora richiedere l'accesso ai pesi.

Marco deve richiedere l'accesso su [Hugging Face](https://huggingface.co/facebook/sam3), attendere l'abilitazione e autenticare l'account sull'HPC. Token solo nel terminale, mai in chat, script o repository. Dopo questo passaggio l'assistente potrà riprendere direttamente download e job; non ripetere il setup SSH né le diagnostiche concluse.

## Prossimo lavoro

1. Terminare inventario e hash dei sorgenti; scegliere dipendenze dalle revisioni fissate. Tenere SAM3/MoGE separati dall'ambiente SuperFlex funzionante, scambiando file con provenienza esplicita.
2. Preparare inferenza sui tre RGB P01_01 già disponibili, prompt diagnostico `pan`, conservando tutte le istanze prodotte e i punteggi. Scelta operativa reversibile per il primo controllo, non protocollo finale. Nessuna maschera VISOR sostituita silenziosamente a SAM3, nessuna identità comune assunta tra frame.
3. MoGE-2 sul frame RGB intero; intersezione maschera SAM3/validità MoGE/punti finiti. Salvare RGB, maschere, point map, coordinate, parametri e checksum prima di SuperFlex. Documentare risoluzione, soglie, convenzioni degli assi e ogni eventuale filtro.
4. Riutilizzare caricamento robust e normalizzazione degli autori già verificati; salvare trasformazione inversa, campionamento e mesh. Nessuna selezione della migliore rotazione o posa canonica ground truth.
5. Eseguire via SLURM, recuperare log e output, verificare visivamente segmentazione, geometria e ricostruzione. La sola correttezza numerica non dimostra qualità della forma.

L'integrazione Whareformer segue questa verifica. La replica SAM3/MoGE e il confronto finale a osservazioni/feature/XYZ comuni restano distinti. Memoria delle forme, distanza e fusione dei punteggi non sono ancora fissate.
