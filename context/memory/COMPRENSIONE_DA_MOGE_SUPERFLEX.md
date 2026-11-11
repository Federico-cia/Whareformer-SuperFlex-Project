# Comprensione del percorso RGB → geometria → SuperFlex

9 novembre 2026. Nota richiesta da Marco per conservare il ragionamento discusso con l'assistente e preparare l'esposizione alla docente. È una sintesi della comprensione maturata nel dialogo, non un nuovo risultato sperimentale né una trascrizione letterale.

## Il passaggio chiarito da Marco

Marco ha ricondotto il procedimento a **maschera → nuvola di punti → superquadriche**, chiedendo perché si parlasse di geometria stimata anziché della stessa procedura di SuperFlex. Il chiarimento decisivo è che la maschera identifica i pixel dell'oggetto, ma non fornisce la loro profondità. Per ottenere una nuvola 3D serve anche una stima geometrica dall'RGB o una profondità acquisita da un sensore.

Nel dialogo è stata corretta una seconda distinzione inizialmente ipotizzata: DA e MoGE lavorano entrambi sull'intera immagine, non rispettivamente sulla scena e sul solo oggetto. La maschera seleziona successivamente i punti dell'oggetto. Le geometrie monoculari descrivono superfici visibili stimate; non osservano il retro degli oggetti o tutto il volume della scena.

## Differenza fra i due rami effettivamente eseguiti

| Passaggio | Depth Anything V2 Metric | MoGE-2 |
|---|---|---|
| Input alla rete | RGB completo | Stesso RGB completo |
| Predizione e procedura | Profondità per pixel; conversione in XYZ con camera fornita | Predizione di una mappa di punti; recupero di camera, profondità e scala |
| Camera nel confronto | Intrinseci EPIC Fields disponibili | Camera stimata da MoGE, senza fornire il campo visivo |
| Selezione dell'oggetto | Maschera VISOR e punti validi comuni | Stessa maschera e stessi pixel validi |
| Input a SuperFlex | Nuvola parziale, 4096 punti normalizzati | Nuvola parziale, stessi indici di campionamento e normalizzazione |

DA non usa gli intrinseci nella predizione della profondità. Noi li usiamo dopo, nel modello prospettico:

`X = (u − cx) Z / fx; Y = (v − cy) Z / fy; Z = profondità stimata.`

Il calcolo è deterministico, ma **XYZ restano stime**: un errore in Z si propaga anche in X e Y, perfino con camera perfettamente nota. Nel nostro MoGE, `force_projection=True` ricalcola i punti rendendoli coerenti con profondità e camera recuperate; le coordinate finali non sono tre previsioni indipendenti senza vincoli.

I file `data/compare200/<video>/ready/camera.json` contengono intrinseci, distorsione e pose per tutti e cinque i video. Il ramo DA usa i primi quattro parametri intrinseci; segue il modello prospettico di Whareformer senza applicare la distorsione. Le pose servono a collocare i punti nella scena, non a costruire la sola nuvola nel riferimento della camera. Parametri disponibili non equivalgono a calibrazione perfetta certificata da noi.

MoGE è più autonomo quando la camera non è disponibile, perché ne comprende il recupero. Questo vantaggio pratico non garantisce maggiore accuratezza. DA può comunque predire la profondità senza camera; per ottenere XYZ occorre fornirla o stimarla separatamente.

## Stessa geometria, impieghi diversi

Whareformer usa la profondità per localizzare gli oggetti in 3D e associarli nel tempo insieme all'aspetto. Nel ramo aggiuntivo conserviamo i singoli punti dell'oggetto e li passiamo a SuperFlex robust per predirne la forma, anche non osservata. I due rami differiscono nella costruzione della nuvola; SuperFlex e il suo preprocessing restano comuni.

Il ramo MoGE riprende lo schema geometrico dell'appendice D di SuperFlex, sostituendo SAM3 con VISOR e usando RGB EPIC. La differenza rispetto ai benchmark quantitativi del paper riguarda dati/profondità di partenza, dominio e riferimenti 3D, non l'assenza del passaggio nuvola → superquadriche.

## Conseguenza per l'interpretazione dei risultati

Il confronto su 200 immagini valuta **DA + camera del dataset** contro **MoGE + camera stimata**, non isola soltanto la qualità della profondità. Il vantaggio DA di 0.0216 IoU 2D riguarda questi procedimenti completi. Non dimostra accuratezza 3D superiore o beneficio sul tracking. Un controllo MoGE con campo visivo noto è una possibilità diagnostica discussa, **non eseguita né aggiunta come prerequisito alla roadmap**. Non introdurre nuovi esperimenti o ripetere il confronto per effetto del solo chiarimento concettuale.

## Sintesi per l'esposizione

La maschera stabilisce quali pixel appartengono all'oggetto; non ne determina la profondità. Abbiamo confrontato due modi di costruire la nuvola parziale: Depth Anything predice la profondità e noi usiamo gli intrinseci del dataset per ottenere XYZ; MoGE comprende anche il recupero della camera dalla geometria predetta. Entrambi analizzano l'immagine completa e usano poi la stessa maschera VISOR. Le coordinate restano stimate in entrambi i casi. SuperFlex riceve le nuvole e predice superquadriche deformabili. La domanda finale è se queste forme siano stabili e discriminative abbastanza da migliorare il tracking, non soltanto se siano visivamente plausibili.

## Riferimenti verificati nel dialogo

- Codice del confronto: `scripts/expanded_geometry.py`, `scripts/superflex_batch_probe.py`; risultati e limiti in [RISULTATI_CONFRONTO_200.md](RISULTATI_CONFRONTO_200.md).
- [MoGE-2, versione effettivamente utilizzata](https://github.com/microsoft/MoGe/blob/07444410f1e33f402353b99d6ccd26bd31e469e8/moge/model/v2.py).
- [Depth Anything V2 Metric](https://github.com/DepthAnything/Depth-Anything-V2/tree/main/metric_depth).
- [SuperFlex, §5.3 e appendice D](https://arxiv.org/html/2607.01015); [Whareformer](https://arxiv.org/html/2607.08537).
- [Calibrazione della camera, OpenCV](https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html).
