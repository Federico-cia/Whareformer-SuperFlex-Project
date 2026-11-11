# Depth Anything e MoGE: confronto su 200 nuove immagini

9 novembre 2026. **Depth Anything grezzo mostra un vantaggio modesto ma coerente nell'accordo 2D delle forme SuperFlex con VISOR.** È il candidato raccomandato per il primo prototipo del ramo forma; non è dimostrata superiorità nell'accuratezza 3D o nel tracking. Nessuna modifica a Whareformer adottata.

## Esperimento

200 RGB nuovi, 40 in ciascuno di cinque video del train: P01_01, P02_03, P03_04, P08_09, P22_01. Selezione fissata prima delle inferenze, senza riutilizzare i 19 frame P01_01 precedenti. **299 osservazioni**, 37 etichette di categoria annotate; non sono 299 identità indipendenti. Tutti i candidati superano i controlli di area e punti comuni. Stessi RGB, maschere, pixel validi, campioni e checkpoint SuperFlex robust nelle tre condizioni: DA grezzo, DA allineato alla scena, MoGE-2. Nessun training o aggiustamento delle soglie in base agli esiti.

Protocollo e provenienza in [CONFRONTO_200_IMMAGINI.md](CONFRONTO_200_IMMAGINI.md); campione locale in `data/compare200/`, selezione in `manifests/compare200_selection.json`. Metriche numeriche su tutte le osservazioni; ispezione non cieca di **60 osservazioni prefissate**, 12 per video, in due viste (20 tavole). Tutte le predizioni sono conservate.

## Misura e risultato appaiato

Riproiettare le mesh con la camera del rispettivo ramo e misurare l'IoU con la maschera VISOR. Media prima per immagine, poi per video, con peso uguale ai cinque video. L'IoU descrive la compatibilità con il supporto 2D visibile: **non misura la superficie reale completa** e può penalizzare parti corrette ma occluse.

Confronto principale sugli esatti stessi **298 oggetti osservati in 199 immagini** con entrambi gli output disponibili:

| Video | DA grezzo | MoGE-2 | Differenza DA − MoGE |
|---|---:|---:|---:|
| P01_01 | 0.4666 | 0.4406 | +0.0260 |
| P02_03 | 0.4165 | 0.3813 | +0.0352 |
| P03_04 | 0.4575 | 0.4384 | +0.0190 |
| P08_09 | 0.5528 | 0.5460 | +0.0068 |
| P22_01 | 0.4554 | 0.4343 | +0.0211 |
| **Media dei video** | **0.4697** | **0.4481** | **+0.0216** |

DA grezzo ha IoU maggiore in **120/199 immagini**, MoGE in 79/199. La differenza media è nella stessa direzione nei cinque video. Questo è un risultato descrittivo del campione, non una prova di significatività o generalizzazione all'intero dataset.

![Confronto appaiato](outputs/compare200_749968/confronto_appaiato.png)

## Disponibilità e controllo dell'allineamento

| Ramo | Mesh disponibili / 299 | Mancanti | IoU media sugli output disponibili | IoU con mancanti come sagoma vuota |
|---|---:|---:|---:|---:|
| DA grezzo | 299 | 0 | 0.4682 | 0.4682 |
| DA allineato | 293 | 6 | 0.4527 | 0.4442 |
| MoGE-2 | 298 | 1 | 0.4481 | 0.4454 |

Le medie degli output disponibili hanno denominatori diversi: non sostituiscono il confronto appaiato. In P08_09, per esempio, MoGE appare leggermente migliore nella media dei soli successi, ma il confronto sugli stessi casi favorisce DA. La lettura con output mancanti come sagoma vuota è aggiuntiva e descrittiva, introdotta dopo l'emergere di un fallimento; non è una misura confermativa preregistrata.

Sei input allineati non hanno consentito l'esportazione di una nuvola valida. Nel ramo MoGE un tagliere, `P08_09/frame_0000010781__a01`, non produce primitive sopra la soglia originale 0.5. È registrato come fallimento, senza abbassare la soglia. **890 mesh valide** complessive; sette output mancanti fra le 897 combinazioni osservazione/ramo previste.

Rispetto a MoGE, DA allineato ha un vantaggio appaiato di 0.0081 IoU, nella stessa direzione in quattro video su cinque; non emerge un motivo per preferirlo a DA grezzo per questo ramo forma. L'allineamento resta diagnostico in unità scena: scala metrica ed equivalenza con il preprocessing effettivo della baseline non sono certificate.

## Qualità osservata e limite della conclusione

Le 20 tavole confermano qualità variabile: alcune strutture rettangolari o allungate sono riconoscibili, ma padelle, piatti e tazze sono spesso squadrati, frammentati o privi di dettagli plausibili. MoGE cambia le decomposizioni e talvolta introduce primitive aggiuntive; non produce un miglioramento visivo generale nel sottoinsieme prefissato. Una maggiore IoU non garantisce un completamento corretto.

Il campione dipende dalla disponibilità dei file e contiene osservazioni temporalmente correlate. Le etichette d'identità non sono state verificate; non è stata misurata l'associazione nel tempo. Le posizioni XYZ e i descrittori Whareformer non sono stati modificati. La geometria di ciascun modello non è ground truth per giudicare l'altro: i residui di fitting restano diagnostiche secondarie.

**Raccomandazione:** usare DA grezzo come primo candidato per la forma, mantenendo gli XYZ originali del tracker; poi verificare stabilità e discriminatività su identità annotate, confrontando SuperFlex anche con geometria semplice dagli stessi punti. È una proposta motivata da questo test, non un'integrazione implementata o una scelta definitiva già approvata.

## Valutazione rispetto ai paper

Il dialogo di comprensione richiesto da Marco per l'esposizione è conservato in [COMPRENSIONE_DA_MOGE_SUPERFLEX.md](COMPRENSIONE_DA_MOGE_SUPERFLEX.md). Limite chiarito: DA usa intrinseci forniti da EPIC Fields, MoGE recupera la camera senza campo visivo fornito; il confronto riguarda quindi i due procedimenti completi, non soltanto la stima della profondità. Il controllo MoGE con campo visivo noto non è stato eseguito.

Chiarimento del percorso effettivo: entrambi i rami costruiscono una nuvola parziale dell'oggetto e la passano allo stesso SuperFlex robust. La maschera VISOR seleziona i pixel; la geometria 3D proviene dall'RGB tramite DA (profondità e intrinseci disponibili) o MoGE-2 (mappa di punti e intrinseci stimati). Nel ramo MoGE usiamo la proiezione coerente con la profondità, `force_projection=True`. Segue campionamento di 4096 punti e normalizzazione degli autori. Il ramo MoGE riprende quindi lo schema geometrico dell'appendice D, sostituendo SAM3 con maschere annotate e usando immagini EPIC; non è la replica completa della pipeline SAM3. La distinzione con i benchmark quantitativi del paper riguarda origine/qualità dei dati 3D e valutazione, non l'assenza del passaggio nuvola → superquadriche. La sola maschera 2D non determina la profondità.

Valutazione del 9 novembre: risultato soddisfacente come verifica operativa e confronto controllato; qualità delle forme ancora poco convincente per usarle come rappresentazione affidabile dell'identità. Il piccolo vantaggio DA non risolve le deformazioni osservate. L'IoU 2D, da sola, non consente un giudizio assoluto di accuratezza: manca una superficie reale di riferimento e il completamento può includere parti occluse.

Il [paper SuperFlex, §5.3](https://arxiv.org/html/2607.01015#S5.SS3) valuta quantitativamente nuvole parziali ASE estratte da profondità fornite, confrontandole con mesh 3D complete; mostra anche il beneficio dell'adattamento ad ASE. Il nostro test usa geometria monoculare stimata su EPIC e una metrica 2D: i valori non sono confrontabili con l'IoU volumetrica del paper. La pipeline RGB con SAM3/MoGE dell'[appendice D](https://arxiv.org/html/2607.01015#A4) è una dimostrazione qualitativa, senza un benchmark quantitativo corrispondente al nostro. I risultati attuali non dimostrano né una replica delle prestazioni dichiarate né una loro confutazione. Il diverso dominio è una possibile spiegazione, non una causa verificata degli errori.

Rispetto a [Whareformer](https://arxiv.org/html/2607.08537), manca ancora la misura pertinente: associazione delle identità nel tempo e tracking con/senza forma. Una ricostruzione grossolana potrebbe essere utile se stabile e discriminativa; questa proprietà resta da verificare. Nessuna modifica alla roadmap o scelta definitiva deriva da questa valutazione.

## Esecuzione e verifiche

GPU 749968 interrotto dopo 19m33s sul caso senza primitive; ripresa 750019 conclusa in 7m15s, riutilizzando i blocchi completati e registrando i fallimenti per osservazione. **26m48s GPU complessivi**, entro il budget di un'ora; acquisizione e CPU separati. Il CSV delle fasi non include il tempo parziale del tentativo fallito: per il totale usare i tempi SLURM, non la sola somma CSV.

Verifica finale 750021 conclusa in 3m09s; controlli progressivi e grafico appaiato tracciati nei log. Hash dei 200 RGB e delle cinque mesh verificati localmente. Archivio completo scaricato: **6185 checksum di file e 891 provenienze delle nuvole verificati**, oltre ai due artefatti appaiati. Campionamento, normalizzazione, predizioni e riproiezione controllati; fallimenti espliciti. Verifica in `outputs/compare200_749968/download_verification.json`, risultati grezzi in `aggregate.json`, confronto appaiato in `paired_scores.json`, note qualitative per video in `visual_review.json`. Nessun job lasciato in corso.

## Tavole del sottoinsieme prefissato

| Video | Frontali | Oblique |
|---|---|---|
| P01_01 | [1](outputs/compare200_749968/P01_01/confronto_frontale_01.png), [2](outputs/compare200_749968/P01_01/confronto_frontale_02.png) | [1](outputs/compare200_749968/P01_01/confronto_obliqua_01.png), [2](outputs/compare200_749968/P01_01/confronto_obliqua_02.png) |
| P02_03 | [1](outputs/compare200_749968/P02_03/confronto_frontale_01.png), [2](outputs/compare200_749968/P02_03/confronto_frontale_02.png) | [1](outputs/compare200_749968/P02_03/confronto_obliqua_01.png), [2](outputs/compare200_749968/P02_03/confronto_obliqua_02.png) |
| P03_04 | [1](outputs/compare200_749968/P03_04/confronto_frontale_01.png), [2](outputs/compare200_749968/P03_04/confronto_frontale_02.png) | [1](outputs/compare200_749968/P03_04/confronto_obliqua_01.png), [2](outputs/compare200_749968/P03_04/confronto_obliqua_02.png) |
| P08_09 | [1](outputs/compare200_749968/P08_09/confronto_frontale_01.png), [2](outputs/compare200_749968/P08_09/confronto_frontale_02.png) | [1](outputs/compare200_749968/P08_09/confronto_obliqua_01.png), [2](outputs/compare200_749968/P08_09/confronto_obliqua_02.png) |
| P22_01 | [1](outputs/compare200_749968/P22_01/confronto_frontale_01.png), [2](outputs/compare200_749968/P22_01/confronto_frontale_02.png) | [1](outputs/compare200_749968/P22_01/confronto_obliqua_01.png), [2](outputs/compare200_749968/P22_01/confronto_obliqua_02.png) |
