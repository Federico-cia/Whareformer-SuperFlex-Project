# Esperimento appaiato DA/MoGE: stabilità e discriminatività delle forme

**Esecuzione conclusa e verificata il 10 novembre:** job 750536 COMPLETED/0:0 in 47m26s, tutte le 8797 coppie e analisi scaricate e controllate. Risultati e limiti in `RISULTATI_IDENTITA_DA_MOGE.md`. Nessun job ancora attivo; le indicazioni di lancio sotto documentano il protocollo e non richiedono una ripetizione.

Preparazione iniziata il 9 novembre e aggiornata il 10 novembre 2026, richiesta da Marco. Esperimento diagnostico sui dati di sviluppo già acquisiti; non valutazione finale del tracking e non adozione definitiva di una sorgente. La procedura seguente definisce il precalcolo esplorativo, non il futuro metodo nel matcher.

## Domanda e confronti

Le forme SuperFlex della stessa istanza restano simili fra osservazioni? Sono separabili da istanze diverse, anche della stessa categoria? DA e MoGE differiscono su queste proprietà? SuperFlex aggiunge informazione rispetto alla nuvola parziale di partenza?

Quattro rappresentazioni, senza nuove inferenze: punti DA grezzo, superfici SuperFlex da DA grezzo, punti MoGE e superfici SuperFlex da MoGE. Escludere DA allineato da questa fase per limitare i fattori; mantenerne gli output storici. XYZ e descrittori Whareformer non vengono modificati. Nessuna memoria fusa o addestramento aggiuntivo.

## Dati, corrispondenze e identità

Riutilizzare le 299 osservazioni del confronto 200 nei cinque video di sviluppo. Conservare tutti i casi e i fallimenti. Collegamento verificato dal programma: video, nome VISOR, mapping ufficiale, RGB, indice nell'array annotazioni, categoria, maschera e percorsi di geometria/ricostruzione. Hash delle annotazioni, riepiloghi e input geometrici conservati.

**Limite dell'interfaccia:** `annotation_index` non è ancora certificato come `detection_idx` Whareformer. Il nuovo manifest lascia quest'ultimo vuoto e registra feature/XYZ non ancora associati. Non dichiarare risolta l'equivalenza della baseline; il problema del loader resta aperto.

Conservare UUID, categoria e intervallo di interpolazione soltanto come indizi di revisione. Nessuno di questi campi genera automaticamente etichette di identità. `identity_review.csv`, `pair_review.csv`, gruppi candidati per UUID e tavole RGB/maschera/crop permettono la verifica documentata. Stato iniziale: identità non verificate. Registrare identità fisica, stato ed evidenza; casi ambigui esclusi dall'analisi etichettata e rendicontati. Verificare corrispondenze usando annotazioni/provenienza e contesto visivo prima di consultare le distanze di forma, per non costruire etichette favorevoli al metodo.

Tutte le coppie non ordinate nello stesso video, da RGB diversi, vengono precalcolate senza etichette. Coppie fra video escluse: non assumere che istanze in video diversi siano necessariamente diverse. Coppie fra frame non sono unità statistiche indipendenti. Il precalcolo resta utile anche se soltanto una parte riceverà etichette affidabili.

## Campionamento e distanze prefissati per il diagnostico

- 1024 punti per rappresentazione, seed 20261109. Nuvole: campionamento uniforme degli indici, con ripetizione solo se necessario. SuperFlex: campionamento uniforme per area dei triangoli delle mesh già esportate, risoluzione 30. Questo usa la superficie triangolata esportata, senza ricostruire nuovamente le primitive. Superfici sovrapposte possono essere pesate più volte; il limite va conservato.
- Centratura e divisione per raggio RMS indipendenti per rappresentazione: confronto di **forma senza dimensione assoluta**. Centro/raggio conservati per provenienza, non usati come posizione/scala fisica certificata. Le parti visibili e i completamenti possono cambiare centro e raggio; la normalizzazione non corregge la parzialità.
- **Descrittore primario D2:** 16384 distanze fra punti estratti, senza autocoppie; distanza fra distribuzioni tramite media delle differenze assolute dei valori ordinati (Wasserstein 1D empirica). Invariante a rotazioni/traslazioni a parità di campione; non rende invarianti predizioni diverse e può confondere forme differenti.
- **Controllo molto semplice:** distanza L2 fra radici dei tre autovalori della covarianza, ordinati, sulle stesse rappresentazioni. Nessun parametro di primitiva grezzo confrontato.
- **Diagnostica di registrazione:** Chamfer simmetrica non quadratica, media delle distanze nearest-neighbour nelle due direzioni, su 512 punti. Allineamento rigido con PCA e 24 permutazioni orientate degli assi; ICP massimo 12 iterazioni per inizializzazione, entrambe le direzioni di fitting e minimo finale. Nessuna riflessione o ulteriore ottimizzazione di scala. Minimo su entrambi i versi per simmetria del punteggio. È una ricerca locale multi-inizio, non una soluzione globale garantita; instabile con parzialità/simmetrie e potenzialmente troppo permissiva verso oggetti differenti.

Le scelte sono fissate prima di leggere le distanze sulle identità. Le tre misure sono riportate distintamente: nessuna selezione della metrica migliore sul test. Il diagnostico ICP misura anche se un confronto più costoso offre indicazioni oltre al descrittore economico; il suo costo non è presupposto accettabile online.

## Analisi dopo la verifica delle identità

Separare distanze della stessa istanza, istanze diverse della stessa categoria e categorie diverse. Il confronto decisivo di discriminatività è entro categoria; separare cucchiaio e tagliere non basta a dimostrare informazione sull'identità.

Riportare copertura per rappresentazione, numero di identità effettive, osservazioni/ripetizioni per identità e coppie disponibili; includere fallimenti. Confronti DA/MoGE sul medesimo insieme di coppie utilizzabili, affiancando la copertura complessiva. Distribuzioni intra/inter-identità e recupero del vicino più simile fra frame distinti; dichiarare numero di candidati e categorie. Nessun numero prestazionale finché non esistono etichette affidabili. Valutare la dipendenza per identità/video, senza intervalli di confidenza ottenuti trattando tutte le coppie come indipendenti. Se il campione verificabile è insufficiente, richiedere nuove osservazioni mirate prima delle conclusioni.

Non usare annotazioni per associazione/aggiornamento nel tracker misurato. Questo esperimento non produce IDF1, mPCL, beneficio causale nel tracker o accuratezza geometrica ground truth. Futuro confronto con aspetto/posizione dipende dal collegamento alle osservazioni reali della baseline.

## HPC e ripresa

Script: `scripts/shape_identity_experiment.py`, `scripts/shape_identity.sbatch`. Ambiente esistente `cv-superflex`, CPU senza GPU, quattro processi con librerie numeriche a un thread, 8 GB richiesti. Nessuna nuova installazione/download dei dati o modello. Directory isolata remota `~/cv_project/runs/shape_identity_v1/`; input `~/cv_project/runs/compare200_749968/` e `~/cv_project/data_compare200/`.

1. `sbatch shape_identity.sbatch prepare`: controlli sintetici delle proprietà geometriche, manifest, descrittori e tavole. Limite 30 minuti. Preparazione completata non sovrascrivibile nello stesso output; i CSV di revisione non vengono sovrascritti.
2. `sbatch shape_identity.sbatch pilot`: dieci coppie deterministiche, una della stessa categoria e una di categorie diverse per video, selezionate prima dei punteggi. Risultati conservati e riusati. Misura del costo effettivo; proiezione di durata esplicitamente approssimativa e separata dall'attesa in coda.
3. Dopo lettura del pilota, fissare il limite temporale del job completo e lanciarlo con `sbatch --time=HH:MM:SS shape_identity.sbatch run`. Non impegnare molte ore prima di misurarne il costo. Un eventuale limite raggiunto non perde le coppie già completate: ripetere `run` nella stessa directory riusa risultati con firma coerente di configurazione/codice/metadati.

Output completi: configurazione e provenienza, osservazioni, coppie, feature, CSV per revisione, tavole, JSON per coppia, riepilogo tempi e `distances.csv`. Firma della configurazione controllata, scritture per coppia atomiche; risultati mancanti restano espliciti. Eventuali correzioni metodologiche richiedono nuova versione/directory e aggiornamento di questo protocollo.

Per identificativi job, stati effettivi, tempi misurati ed eventuali blocchi vedere `STATO_LAVORO.md`; non confondere preparazione, avvio e completamento.

## Preparazione verificata e primo campione revisionato

Job 750421 COMPLETED/0:0 in 1m14s: 299 osservazioni, **8797 coppie**; 299 nuvole e 299 superfici DA, 299 nuvole e 298 superfici MoGE. Mapping verificato per tutte le osservazioni. I 299 UUID sono tutti distinti, anche entro video: nessuna identità temporale ricavabile automaticamente da questo campo nel campione. `detection_idx` resta non verificato.

Controlli sintetici superati su rotazione/traslazione/scala, simmetria del punteggio e separazione di due geometrie sintetiche. Non sono evidenze di stabilità/discriminatività EPIC. Job pilota 750424 COMPLETED/0:0 in 43s, calcolo misurato 26.8s su dieci coppie con quattro processi. Estrapolazione del lavoro completo circa 4768s (1h19m), esclusa coda: variabilità per coppia da circa 1.1 a 6.2s. Limite prudenziale del job completo: tre ore; job **750536**, CPU soltanto, output riavviabile. Stato osservato e successiva verifica nel file di stato.

**Campione iniziale di revisione visiva, prima della lettura delle distanze:** 37 osservazioni, sette identità proposte come `visually_verified`, quattro video. Evidenza e chiavi esatte in `outputs/shape_identity_v1/visual_identity_evidence.json` e `identity_review.csv`. Sei tavole ispezionate: P01_01_01, P02_03_01, P03_04_01, P08_09_01, P22_01_01 e P22_01_02. I casi P02_03 non sono stati assegnati in questa prima revisione.

- P01_01: tagliere verde, sei osservazioni.
- P03_04: tagliere turchese con bordo/apertura caratteristici, sei osservazioni; coltello con impugnatura arancione, quattro osservazioni.
- P08_09: bottiglia bianca del latte con tappo verde, tre osservazioni; tagliere di legno, sette osservazioni.
- P22_01: piatto bianco con bordo scanalato, sei osservazioni; piatto verde chiaro a bordo liscio, cinque osservazioni. Sono distinguibili anche quando entrambi compaiono nel contesto al frame 31321; forniscono il primo confronto fra istanze diverse della stessa categoria.

La verifica usa RGB, caratteristiche visibili e contesto della preparazione, non UUID o distanze calcolate. **Non è una certificazione da annotazioni persistenti o video continuo**: l'eventuale sostituzione con un oggetto visivamente identico fra frame non è esclusa. Campione di convenienza ristretto; i negativi entro categoria sono per ora soltanto due piatti in un video, distinguibili visivamente. Non generalizzare a istanze geometricamente molto simili. Le restanti 262 osservazioni restano non verificate. Revisione indipendente/continuità temporale e ampliamento del campione rimangono necessari prima di conclusioni centrali.

Il manifest iniziale conserva lo stato non verificato; le etichette successive sono separate e versionate nel CSV. L'archivio `preparation_review.tar.gz` è lo snapshot precedente alla revisione visiva; il CSV corrente e `visual_identity_evidence.json` documentano la revisione successiva. Il valutatore `scripts/evaluate_shape_identity.py`, eseguito dopo il precalcolo, legge soltanto righe con stato esplicito, identità ed evidenza; conserva l'hash del CSV. Confronta le quattro rappresentazioni sulle stesse coppie complete, riporta copertura distinta, distanze intra/inter, AUC descrittiva e nearest-neighbour macro per identità, con risultati per video e separati entro categoria. Nessuna stima inferenziale o soglia appresa. Il confronto retrieval è diagnostico e può usare frame futuri; non simula tracking online.
