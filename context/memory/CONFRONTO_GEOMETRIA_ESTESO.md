# Confronto esteso Depth Anything / MoGE

9 novembre 2026. Richiesto da Marco per superare il limite dei tre frame già esaminati. Campione e criteri fissati prima delle nuove inferenze; selezione in `manifests/geometry_expansion_selection.json`.

## Campione

Tutti i **16 nuovi frame** con RGB, VISOR e pose già disponibili in P01_01, escludendo interamente i tre frame ispezionati. **27 osservazioni candidate, 11 categorie**: pan, chopping board, plate, knife, grater, lid, spatula, spoon, curry powder package, carrot, courgette. Includere tutte le maschere candidate con almeno 128 pixel a 456×256. Escludere mani, acqua, cibo sciolto/misto, piano cottura e tessuto per concentrare il controllo sulle forme di oggetti solidi. Registrare esclusioni e fallimenti, senza scegliere le osservazioni in base agli output.

È un campione di disponibilità di un solo video del train, non rappresentativo e con frame/oggetti dipendenti. Aumenta la copertura diagnostica; non garantisce significatività statistica o generalizzazione. Identità fisiche ancora non verificate. Il campione finale per il tracking rimane distinto.

## Confronto appaiato

- Stessi RGB, maschere e pixel validi comuni per Depth Anything grezzo e MoGE-2, stesso checkpoint robust, seed 42, campionamento 4096, normalizzazione degli autori e convenzioni camera. Nessuna canonicalizzazione o selezione della migliore rotazione.
- Aggiungere Depth Anything allineato alla scena come terza condizione, mantenendo gli stessi pixel quando la profondità allineata è valida; registrare separatamente gli allineamenti falliti. Serve a distinguere gli effetti della sorgente e dell'allineamento già presenti nel percorso precedente.
- Modelli e ambienti già verificati, senza nuove installazioni. MoGE-2 fissato alla revisione del job 749539; verificare che Depth Anything mantenga la revisione del job 744902. Nessuna modifica al tracker o ai suoi XYZ.

## Lettura dei risultati

Rendicontare frame/categorie/osservazioni effettivi, esclusioni, copertura dei pixel e fallimenti. Controllare punti, primitive, normalizzazione e mesh. Confrontare figure di tutti i casi con viste e ingrandimenti normalizzati coerenti; valutare forma generale e dettagli visibili, dichiarando che è un giudizio qualitativo. Riportare l'adesione alle rispettive nuvole stimate come diagnostica di fitting, non come accuratezza 3D. Il completamento può essere errato anche con residuo basso.

Non esiste qui una superficie 3D ground truth indipendente: non stabilire un vincitore di accuratezza fisica dalla sola distanza fra output e profondità che l'ha generato. Non usare intervalli di confidenza che trattino i frame come campioni indipendenti. Un vantaggio sistematico osservabile è un motivo per approfondire, non una prova di beneficio sul tracking.

## Stato

**Completato e ispezionato.** GPU **749665 COMPLETED/0:0**, 5m20s; verifica CPU **749728 COMPLETED/0:0**, 27s. Nessuna nuova installazione o modifica alla baseline. Output, log e dieci tavole in `outputs/geometry_expanded_749665/`; run remoto `~/cv_project/runs/geometry_expanded_749665/`. Nessun job lasciato in corso.

## Risultati

Entrambi i modelli eseguiti sui 16 nuovi frame; i 27 oggetti candidati appartengono a 11 frame, mentre gli altri cinque non contengono categorie ammesse. Tutte le 27 osservazioni superano la soglia di area e i controlli, tutte hanno 100% dei pixel della maschera validi in comune. Nessun fallimento di allineamento e nessuna osservazione esclusa dopo inferenza. **81 ricostruzioni**, 27 per sorgente. Stessi indici campionati verificati nelle tre condizioni; array, normalizzazione inversa, primitive e mesh controllati. Tutti i 572 file elencati nei checksum remoti coincidono con le copie locali.

Distribuzione: pan 9, chopping board 5, courgette 3, knife 2, plate 2; carrot, grater, lid, spoon e curry powder package e spatula una ciascuna. Sono occorrenze annotate, non 27 identità indipendenti.

| Diagnostica di fitting | DA grezzo | DA allineato | MoGE-2 |
|---|---:|---:|---:|
| Residuo medio sulle osservazioni misurabili | 0.0261 | 0.0278 | 0.0356 |
| Mediana dei residui per osservazione | 0.0222 | 0.0299 | 0.0318 |

Residui in unità normalizzate: distanza approssimata dai pixel non selezionati a 30000 punti campionati sulla superficie predetta. Misurabili in **24/27** casi; negli altri tre tutti i punti disponibili sono già inclusi nel campione, quindi il residuo non viene sostituito artificialmente con zero. MoGE ha residuo inferiore a DA grezzo in 9/24 casi e a DA allineato in 9/24. Sono confronti rispetto alle rispettive nuvole stimate: **non** misurano la correttezza del completamento o l'accuratezza fisica e non giustificano un test di significatività basato su frame indipendenti.

## Ispezione visiva completa

Esaminate tutte le cinque tavole frontali e tutte le cinque oblique, con punti osservati sovrapposti alle primitive. Giudizio qualitativo non cieco, senza punteggio di accuratezza inventato:

- Alcune forme semplici sono riconoscibili: tagliere nel frame 6120 e taglieri nei frame 19578/20018 conservano una struttura rettangolare con entrambe le sorgenti; carota e zucchina nel frame 3465 mantengono un andamento allungato, con decomposizioni approssimate.
- Le padelle restano spesso squadrate, frammentate o prive di manico convincente. Non emerge una correzione sistematica passando a MoGE.
- Gli oggetti sottili o parzialmente visibili hanno esiti variabili: nel coltello del frame 20018 la struttura è allungata, mentre quello del 3465 è molto meno convincente. MoGE introduce in alcuni casi primitive aggiuntive fuori dalla struttura osservata.
- Anche tagliere nel frame 43552, coperchio e piatti mostrano completamenti deformati. Un residuo relativamente basso non basta a certificare una forma completa corretta.

**Conclusione circoscritta:** la qualità dipende dall'osservazione e dalla forma, non è uniformemente scadente; tuttavia non emerge un vantaggio visivo sistematico di MoGE né una soluzione generale tramite cambio della sorgente o allineamento. Nessuna scelta definitiva della geometria adottata. Questo campione amplia l'evidenza diagnostica ma resta un solo video, senza ground truth 3D o misura d'identità/tracking. Il prossimo controllo resta la stabilità e discriminatività su identità verificate.

## Tavole complete

| Casi | Frontale | Obliqua |
|---|---|---|
| 1–6 | [Tavola 1](outputs/geometry_expanded_749665/confronto_frontale_01.png) | [Tavola 1](outputs/geometry_expanded_749665/confronto_obliqua_01.png) |
| 7–12 | [Tavola 2](outputs/geometry_expanded_749665/confronto_frontale_02.png) | [Tavola 2](outputs/geometry_expanded_749665/confronto_obliqua_02.png) |
| 13–18 | [Tavola 3](outputs/geometry_expanded_749665/confronto_frontale_03.png) | [Tavola 3](outputs/geometry_expanded_749665/confronto_obliqua_03.png) |
| 19–24 | [Tavola 4](outputs/geometry_expanded_749665/confronto_frontale_04.png) | [Tavola 4](outputs/geometry_expanded_749665/confronto_obliqua_04.png) |
| 25–27 | [Tavola 5](outputs/geometry_expanded_749665/confronto_frontale_05.png) | [Tavola 5](outputs/geometry_expanded_749665/confronto_obliqua_05.png) |
