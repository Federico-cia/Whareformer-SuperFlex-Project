# Supervisione indipendente per l'ammissione geometrica â€” analisi del 21 novembre 2026

> **Audit acquisito:** 783586 concluso; 438 nuvole valide locali, aumento descrittivo della sovrapposizione, staticitÃ  e target reali ancora da validare. [Resoconto](RISULTATI_AUDIT_AMMISSIONE_20261121.md). Arricchimento fermo a 8/216 blocchi, riprese fallite; diagnosi in attesa di esecuzione da Marco.

> **Implementazione successiva:** nucleo a stati, contratti verificatore e replay realizzati e verificati localmente; non ancora validati su EPIC o collegati al worker FPS. Vedere [resoconto](IMPLEMENTAZIONE_PUNTO3_20261121.md). Le indicazioni di codice non implementato nelle sezioni storiche si riferiscono alla fase precedente; il piano scientifico resta valido.

> Ricognizione locale successiva: vedere [stato e limiti dellâ€™audit](RICOGNIZIONE_RIPRESA_PUNTO3_20261121.md). Piano approvato distinto dallâ€™implementazione; stati HPC storici da ricontrollare tramite Marco.

## Sintesi corrente (prevale sulle sezioni cronologiche sotto)

**Problema.** Come aggiornare la memoria 3D di una traccia quando una nuova vista le viene assegnata, con criterio appreso dai dati (non soglie fisse), conservando le viste parziali valide e senza nuove annotazioni manuali.

**Evidenze.** Pose EPIC-Fields e mesh disponibili per tutti i frame osservati di P01_01 (Whareformer le usa giÃ ). La scala di DA grezzo rispetto alla scena varia fra frame (CV 9â€“23% su compare200). In letteratura i residui di registrazione predicono male l'errore (FACT); esistono verificatori appresi, non validati sul nostro dominio. Parametri DenStream di Whareformer scelti con piccola griglia sul test.

**Decisioni di Marco.**
1. Scala: DA allineata alla scena + riferimento scena; MoGE solo confronto; nessuna fusione se l'allineamento fallisce; rischio di errori di posa condivisi accettato.
2. Memoria: niente vista fissa; decisione sul frame, poi aggiunta dei punti nuovi e fusione dei duplicati (fusione pesata per cella, filtro outlier); 4096 punti FPS per SuperFlex; decadimento che riduce il peso senza cancellare la copertura unica.
3. Struttura: DenStream adattato â€” stati della collocazione confermati nel tempo, forma separata dalla collocazione, nessuna perdita della forma dopo uno spostamento.
4. Posizione per il tracking: quella di Whareformer; orientamento nella scena rimandato al punto 4.
5. Verificatore appreso sulla coppia allineata (opzione 2); classificatore sulle diagnostiche come base; sovrapposizione per punto non scelta.
6. Piano: audit su CPU â†’ prima versione con fusione solo da fermo â†’ verificatore addestrato su viste simulate realistiche e su coppie ferme con spostamento noto applicato, valutato su coppie reali ferme â†’ preaddestrato come confronto. **Obiettivo non negoziabile: fusione dopo uno spostamento.**
7. Errore misurato come distanza fra superfici; soglia operativa e parametri scelti solo su sviluppo in base all'utilitÃ  della memoria.

**Rischi aperti.** Etichette errate se un oggetto mosso Ã¨ preso per fermo; campione sbilanciato verso oggetti grandi e fermi; differenza fra errori simulati e reali; pochi oggetti e un video; effetto a catena nel tempo.

**Prossimi passi.** Interpretare l'audit (783586); implementare la prima versione; costruire i dati del verificatore dopo la run completa; ricerche bibliografiche in corso con i prompt preparati. Rinviati: test set (prioritÃ ), due memorie matching/ricostruzione (con il compagno), punto 4, altri 55 video.

**Stato storico superato dalla Sintesi corrente e dalle decisioni successive.** Analisi iniziale: nessuna decisione metodologica presa in quella fase. Nessun training, job, soglia o codice modificato. Stato HPC non ricontrollabile live da questo ambiente (risoluzione DNS di slogin.hpc.unibocconi.it fallita); vale l'ultimo stato documentato in ARRICCHIMENTO_COMPLETO_P01_20261121.md (782990 RUNNING, 782968/782969 PENDING afterok). Nessun invio effettuato.

## Evidenze verificate in questa sessione (lettura locale)

1. **Pose camera EPIC-Fields disponibili per tutti i frame osservati.** `data/compare200_transfer/P01_01/fields.json`: 96468 frame con posa; tutti i 33310 frame del ledger oracle P01_01 hanno posa (confronto per indice di frame; alias VISOR/RGB giÃ  noti restano un limite). Il catalogo del campione contiene `camera_pose` (quaternione + traslazione COLMAP) e intrinseci per 446/446 osservazioni geometriche.
2. **Mesh statica della scena P01_01 disponibile** (`data/compare200_transfer/P01_01/mesh.ply`, `data/epic_pilot/EPIC-Reconstructions/P01_01/`). Il codice di riferimento Whareformer usato in `scripts/expanded_geometry.py` allinea la profonditÃ  DA alla profonditÃ  renderizzata della mesh sui pixel statici (fuori dalle maschere), producendo `da_aligned`.
3. **La memoria attuale non usa pose nÃ© scala di scena.** `cloud_updater.py` accetta `da_raw_points`/`moge_points` in coordinate camera; convenzione dichiarata nei bundle: Â«as exported depth units; inter-view scale unverifiedÂ». La registrazione rigida stima quindi insieme moto della camera e moto dell'oggetto, senza correzione di scala; la memoria Ã¨ nel riferimento della prima camera ammessa.
4. **Annotazioni dense.** Ledger oracle: osservazioni per frame consecutivi (VISOR interpolato), 47 tracce, un solo track oracle per nome in P01_01. Nel campione geometrico: 17 identitÃ , 429 coppie consecutive della stessa identitÃ  (pan 190 osservazioni, chopping board 59, saucepan 44, spatula 41, knife 23, ...).
5. **Indizio preliminare di staticitÃ ** (XYZ ufficiali Whareformer delle 446 osservazioni, riferimento scena, scala EPIC-Fields arbitraria): spostamento del centroide fra osservazioni consecutive della stessa identitÃ , normalizzato sulla diagonale dell'estensione degli XYZ: mediana 0.84%, 236/429 coppie sotto 1%, 318 sotto 2%. Ãˆ solo traslazione di un centroide bbox/mediana profonditÃ : **non** prova staticitÃ  nÃ© esclude rotazioni sul posto.
6. Le annotazioni VISOR preparate localmente (`compare200/.../annotations.json`) non contengono il campo di contatto mano-oggetto; presenza nell'archivio VISOR completo sull'HPC **da verificare**.

## Tre target da tenere separati

| Target | Domanda | Fonte automatica | Indipendenza | Limiti |
|---|---|---|---|---|
| IdentitÃ  | Nuova vista e memoria sono lo stesso oggetto? | Ledger oracle (nomi benchmark) | Dalle annotazioni originali, non dal tracker | IdentitÃ  per nome; non certifica posa; ammissione avviene solo dopo associazione predetta |
| Posa | La trasformazione stimata Ã¨ corretta? | (a) trasformazioni note su viste parziali simulate; (b) posa relativa dalle camere EPIC-Fields quando l'oggetto Ã¨ statico | (b) pose da SfM sull'RGB dell'intero video, indipendenti dal nostro registratore | (a) domain gap; (b) vale solo per oggetti fermi: la staticitÃ  va stabilita senza i nostri gate; traslazione dipende dalla scala della profonditÃ  |
| UtilitÃ  | La fusione migliora la memoria? | Viste reali escluse: riproiezione della memoria nella vista esclusa (maschera VISOR, profonditÃ  allineata) prima/dopo la fusione | Vista esclusa non usata nÃ© per fit nÃ© per decisione | Richiede posa nota della vista esclusa (staticitÃ  o oggetto ancorato); errori di profonditÃ  condivisi fra viste DA |

Conseguenza: la posa relativa delle camere fornisce un riferimento di posa **senza** usare i gate e **senza** nuove annotazioni, ma solo nel sottoinsieme statico. La definizione del sottoinsieme statico Ã¨ il punto critico: se la si ricava dalla stessa registrazione da valutare, il target diventa circolare.

## Criteri di staticitÃ  candidati (nessuno scelto)

- Spostamento degli XYZ ufficiali nel riferimento scena: indipendente dal registratore; insensibile a rotazioni sul posto, rumoroso per viste parziali.
- Coerenza delle silhouette: punti della vista A portati nel mondo con posa/profonditÃ  allineata e riproiettati nella vista B devono cadere nella maschera VISOR di B dove visibili. Usa maschere originali e pose; condivide l'errore di profonditÃ .
- Contatto mano-oggetto VISOR, se disponibile: assenza di contatto non garantisce assenza di moto fra frame annotati.
- Politica conservativa proposta: etichettare Â«staticoÂ» solo con accordo dei criteri; i casi incerti esclusi dal training ma riportati nella valutazione.

## Punto metodologico: cosa si puÃ² apprendere

Apprendere il criterio sposta la scelta manuale ma non la elimina. Serve comunque (i) una definizione di Â«posa correttaÂ» (tolleranza di errore, oppure target continuo: errore di posa o guadagno di utilitÃ ) e (ii) un costo relativo di falsa ammissione e falso rifiuto per fissare il punto operativo. Proposta: target continui e punto operativo scelto su validazione da un costo dichiarato, invece di soglie sulle diagnostiche. Decisione di Marco.

## Percorso minimo proposto (non approvato)

0. **Audit di fattibilitÃ , CPU, nessun training.** Sulle 429 coppie consecutive del campione: posa relativa dalle camere, indicatori di staticitÃ , confronto con le 24 soluzioni candidate del registratore (errore di ciascuna rispetto al riferimento). Verifica anche se `da_aligned` riduce l'incoerenza di scala. Output: quante coppie hanno riferimento affidabile; se il registratore trova la posa giusta fra i candidati ma la scarta (ambiguitÃ ) o non la trova; quanta parzialitÃ  reale. Le decisioni dei gate attuali servono solo come confronto, mai come etichetta.
1. **Dataset di coppie memoriaâ†’nuova vista** con: identitÃ  oracle; errore di posa rispetto al riferimento (coppie statiche) e rispetto a trasformazioni note (viste parziali simulate dalle stesse nuvole reali, con rumore di profonditÃ /maschera); negativi difficili = soluzioni alternative del registratore con errore noto, simmetrie, altre identitÃ  di forma simile.
2. **Modello piccolo** (logistico/gradient boosting) su diagnostiche esistenti + misure di sovrapposizione stimate; uscita: probabilitÃ  di posa corretta o errore atteso, eventualmente selezione fra candidati. Baseline: gate attuali valutati sugli stessi target.
3. **Valutazione** separata per identitÃ  e blocchi temporali (P01_01 unico video completo: nessuna generalizzazione fra video dimostrabile; compare200 con 40 frame su cinque video come controllo esterno limitato). Metriche: false ammissioni a tasso di falsi rifiuti fissato, errore di posa delle ammissioni, utilitÃ  su viste escluse; non il numero di fusioni.

## Questioni aperte che cambiano il disegno

- Usare pose EPIC-Fields e mesh solo come **riferimento di supervisione/validazione**, oppure anche come **ingresso a runtime** (registrazione nel riferimento scena con prior sulla posa)? La seconda cambia il punto 3 e si sovrappone al punto 4; aumenta la dipendenza da asset non disponibili per video arbitrari.
- Rapporto di costo fra falsa ammissione e falso rifiuto.
- Oggetti manipolati: senza riferimento di posa reale, il loro comportamento si valuta solo su dati simulati e sull'utilitÃ  indiretta; limite da dichiarare.

## Discussione successiva con Marco â€” 21 novembre 2026

Proposte di Marco, da discutere (non decisioni): (a) sostituire la memoria Â«prima vista + 3 recentiÂ» con pesi che decrescono con l'etÃ  e premiano le viste che completano l'oggetto, penalizzando le ridondanti; (b) replicare per la geometria i meccanismi di aggiornamento della memoria d'aspetto (DenStream). Richiede limiti appresi dai dati e non numeri fissi.

Risposte dell'assistente: la politica attuale Ã¨ una scelta di budget del prototipo, senza giustificazione scientifica; per la geometria il criterio naturale Ã¨ la copertura della superficie, la recenza conta soprattutto se l'oggetto si muove o cambia forma; proposta di pesi per punto/voxel (confidenza, etÃ , copertura) usati come probabilitÃ  di campionamento per SuperFlex. Scala inter-vista non garantita oggi (DA grezzo, MoGE con scala propria, registrazione senza scala; rapporto dei raggi solo registrato): `da_aligned` Ã¨ la via principale da verificare; la stima di scala per registrazione Ã¨ rischiosa con viste parziali.

Su DenStream: utile da riprendere (decadimento temporale, piÃ¹ modi per vista, stesso spirito di Whareformer) ma non risolve il punto 3: le feature d'aspetto vivono in uno spazio comune e non richiedono allineamento, i punti 3D sÃ¬; ammettere una vista significa verificare una registrazione. Anche DenStream ha iperparametri fissati a mano (0.25, 10, 1e-3 nel paper). Possibile separazione da discutere: memoria di descrittori di forma invarianti alla posa (stile DenStream, senza registrazione) per il matching; memoria di punti registrati solo per ricostruzione/collocazione (punto 4).

Letteratura individuata (abstract/pagine consultati, non letture integrali): PREDATOR (CVPR 2021) apprende overlap e matchability per punto ma non la decisione di accettazione; preprint arXiv che apprendono la verifica della registrazione: Decision PCR (2025), FACT (2025, errori sintetici, residui poco predittivi), Deep-PE (2024, confidenza della posa). Anche lÃ¬ il target di correttezza Ã¨ definito con tolleranze (es. 3DMatch RE â‰¤ 15Â°, TE â‰¤ 30 cm).

## Indicazioni di Marco e verifiche successive â€” 21 novembre 2026

**Direzione indicata da Marco:** eliminare la prima vista fissa nella memoria; interesse per i pesi per punto (recenza e copertura) purchÃ© il costo resti contenuto. Non ancora implementato nÃ© specificato.

**4096 punti:** imposto dal paper SuperFlex (N = 4096, campionamento Farthest Point Sampling per oggetto, sezione implementativa); la nostra pipeline campiona a caso come la demo disponibile. Il modello Ã¨ addestrato con quella dimensione: cambiarla introduce uno scostamento non verificato. Pesi per punto su una memoria di poche migliaia di punti (griglia di voxel, campionamento pesato) hanno costo trascurabile rispetto a DA/SuperFlex.

**Scala â€” evidenza locale (compare200, 196 frame su cinque video, nuvole DA grezze e allineate sugli stessi pixel):** il rapporto profonditÃ  allineata/grezza varia fra frame dello stesso video con CV 9â€“23% e rapporto q90/q10 1.26â€“1.72; dentro lo stesso frame gli oggetti concordano (spread mediano 1.5â€“4%). Lettura: l'allineamento agisce quasi come un fattore di scala per frame e la scala di DA grezzo rispetto alla scena cambia da frame a frame, oppure l'allineamento Ã¨ rumoroso; i due casi non sono ancora separati. Il confronto IoU a vista singola (DA allineato non migliore) non risponde alla domanda, perchÃ© SuperFlex normalizza la scala. Pratico: il ramo DA salva la profonditÃ  dell'intero frame (`prediction.npz`), quindi l'allineamento si puÃ² calcolare a posteriori senza toccare la run in corso. Verifica proposta: coerenza fra viste di posizione e dimensione di oggetti statici nel riferimento scena, grezzo contro allineato; tasso di fallimento dell'allineamento (6/299 in compare200). Rischi: dipendenza da mesh e pose (disponibili per EPIC, non per video arbitrari), fit affine globale dominato dallo sfondo, regioni dinamiche non annotate.

**DenStream in Whareformer (codice verificato, `tracking/tracker/memory/denstream.py`):** ogni osservazione entra nel microcluster piÃ¹ vicino se il raggio dopo la fusione resta â‰¤ 0.25, altrimenti ne crea uno nuovo; pesi con decadimento 2^(-Î»Î”t), cluster potenziale quando il peso supera Î¼ = 10, potatura periodica dei cluster deboli; al matcher vanno tutti i centroidi. Nessuna osservazione viene rifiutata: il supporto nel tempo sostituisce il gate. Idea trasferibile proposta: ammissione per ipotesi (vista registrata come ipotesi debole, promossa se confermata da viste successive). Non trasferibile direttamente: distanza in uno spazio comune e media dei centroidi, che per punti 3D richiedono registrazione.

## Conclusione sulla scala e DenStream adattato â€” 21 novembre 2026

**Raccomandazione sulla scala (proposta, da confermare con la verifica):** usare DA allineato alla mesh della scena e portato nel riferimento scena con le pose EPIC-Fields come sorgente della memoria geometrica; DA grezzo solo come ripiego esplicito quando l'allineamento fallisce. Motivi: unico modo disponibile per avere una scala comune fra viste, metodo originale di Whareformer, elimina la vista ancorata, calcolabile a posteriori. Criterio di conferma: su oggetti fermi, coerenza di posizione e dimensioni fra viste migliore dell'alternativa grezza.

**Iperparametri DenStream nel paper (verificato, appendice E, Tabella 10):** non casuali ma scelti con una piccola griglia un fattore alla volta (Îµ 0.1/0.25/0.5; Î¼ 5/10/20; Î» 1e-4/1e-3/1e-2), scegliendo il modello con mPCL e IDF1 migliori; Â§4.5 dichiara che le ablation, salvo indicazione, sono sul test set EPIC: possibile selezione sul test da parte degli autori, da non replicare. Îµ ha l'effetto maggiore, Î¼ e Î» poco sensibili. Ï„p â‰ˆ 106 s. Possiamo fare lo stesso su dati di sviluppo; differenza rispetto al criterio appreso: selezione per metrica a valle (costosa, rumorosa con un video) contro supervisione diretta.

**Proposta di DenStream geometrico (non approvata):** riferimento comune = scena allineata; microcluster = stato/collocazione dell'oggetto con punti accumulati in voxel pesati (non medie); nuova vista coerente con uno stato â†’ rinforzo dei voxel (copertura e recenza), altrimenti nuovo stato debole; promozione con conferme successive (equivalente di Î¼), decadimento (Î»), soglia di coerenza (Îµ) sostituibile da un verificatore appreso; registrazione solo fra stati consolidati quando l'oggetto si Ã¨ mosso; input a SuperFlex: 4096 punti FPS pesato dallo stato dominante. Memoria separata per il matching: DenStream quasi invariato su descrittori di forma. Parametri da selezionare solo su sviluppo.

## Chiarimenti successivi â€” 21 novembre 2026

Decisioni di Marco in REGISTRO_DECISIONI.md (scala allineata; posizione da Whareformer; principio di accumulo; parametri solo su sviluppo). Osservazioni dell'assistente: separare forma (riferimento dell'oggetto, accumulata nel tempo) e collocazione (posa nella scena) evita di perdere la forma quando l'oggetto viene spostato; con l'oggetto fermo la posa Ã¨ nota dal riferimento scena, dopo uno spostamento va stimata registrando la vista sulla forma accumulata. Accumulo: FPS sull'unione dei punti ammessi realizza giÃ  la distribuzione uniforme; tenere solo il primo punto vicino impedisce di correggere misure vecchie (preferibile fusione pesata per cella); i punti lontani nuovi sono anche quelli piÃ¹ esposti ad artefatti di bordo maschera, quindi serve un filtro degli outlier. Memoria per il matching = descrittori di forma per traccia usati nell'associazione di Whareformer (punto 2, compagno), gestibili come DenStream senza registrazione.

## Collocazione, oggetto spostato, memoria per il matching â€” 21 novembre 2026

Marco concorda con le osservazioni sull'accumulo (fusione pesata per cella, FPS sull'unione, filtro degli outlier). Proposta di Marco su collocazione: 4096 punti + parametri di scala e rotazione con riferimento la posizione Whareformer. Osservazione dell'assistente: corretto come struttura (forma nel riferimento dell'oggetto + trasformazione di similitudine R, t, s); l'XYZ Whareformer Ã¨ centro bbox + profonditÃ  mediana della parte visibile, non il centro dell'oggetto, quindi t = XYZ + offset stimato; con profonditÃ  allineata s deriva dalla denormalizzazione SuperFlex (centro e scala salvati), R dalla registrazione o dalla stasi. Sequenza proposta per oggetto spostato: fermo â†’ accumulo con posa nota; in mano â†’ nessuna fusione senza registrazione verificata, forma conservata, collocazione Â«in movimentoÂ»; posato â†’ nuovo stato consolidato con conferme; registrazione dello stato sulla forma â†’ nuova posa e fusione dei lati nuovi; se ambigua, ipotesi separata. Memoria per il matching (punto 2, da concordare col compagno): descrittori di forma invarianti alla posa per vista, raggruppati come DenStream, distanza minima come segnale al matcher; criticitÃ : dipendenza dal punto di vista delle viste parziali, discriminativitÃ  non dimostrata (C11), D2 perde la scala assoluta (recuperabile con scala allineata), ridondanza con l'aspetto, iperparametri, dati geometrici necessari anche per il training. Varianti da confrontare: descrittore della nuvola parziale (senza SuperFlex) contro descrittore della forma completata.

Precisazioni successive: (1) dopo uno spostamento resta un'unica forma; i punti nuovi stanno in uno stato candidato finchÃ© non sono confermati e registrati, poi entrano nella forma con filtro dei duplicati. Il decadimento deve ridurre il peso nella fusione, non cancellare celle che sono l'unica copertura di una parte dell'oggetto. (2) Due confronti distinti: ammissione/registrazione su punti osservati (i completamenti SuperFlex non sono osservazioni); matching su descrittori della forma completata SuperFlex (implementazione attuale: D2 sulla ricostruzione). Il descrittore della nuvola parziale Ã¨ un controllo (ablation) per attribuire l'effetto a SuperFlex, come giÃ  richiesto nella voce 82. Opzione da valutare: registrare la nuova vista sulla forma completata della memoria per aumentare la sovrapposizione, con rischio di adattarsi a superfici inventate.

## Ricerca Consensus â€” sintesi letta il 21 novembre 2026

Pagina condivisa da Marco letta tramite Chrome (riassunto di Consensus su 20 paper; elenco bibliografico completo non esportato; esistenza e venue dei singoli lavori non ancora verificate una per una, salvo PREDATOR, FACT, TEASER++, GeoTransformer, RIE AAAI 2022 noti). La risposta copre soprattutto la domanda 1 (verifica appresa), non politiche di memoria, scala o simmetrie.

Contenuti rilevanti: tre famiglie â€” confidenza appresa per corrispondenza (pesi nella SVD, es. CEGC 2025, RIE 2022, ICC 2024), classificazione del disallineamento della coppia (FACT 2025: errore predetto in classi, addestrato con perturbazioni sintetiche; residui ICP e Chamfer/Hausdorff poco predittivi dell'errore), stimatori certificabili (TEASER++ 2020). INENet (2022) predice la soglia di sovrapposizione dalla coppia. Lacuna dichiarata: nessun metodo validato su viste parziali di oggetti piccoli, simmetrici, con bassa sovrapposizione e profonditÃ  monoculare. Indicazione per noi: il classificatore a livello di coppia (tipo FACT) Ã¨ il componente piÃ¹ trasferibile per decidere la fusione; la confidenza per corrispondenza Ã¨ utile dentro la fusione. Rafforza l'abbandono delle soglie fisse sui residui; supervisione con perturbazioni sintetiche coerente con la proposta. Proposta: ricerche separate per memoria/fusione incrementale, scala, simmetrie.

## Verificatore e ruolo di pose/mesh â€” 21 novembre 2026

Marco propende per partire dal verificatore appreso sulla coppia allineata (opzione 2, tipo FACT/Decision PCR/Deep-PE); proposta dell'assistente: tenere l'opzione 1 (classificatore sulle diagnostiche) come confronto di base a costo trascurabile; opzione 3 (sovrapposizione per punto, tipo PREDATOR) considerata e non scelta. Il verificatore Ã¨ la componente che nel DenStream geometrico sostituisce il raggio fisso Îµ, sia per l'unione della vista a uno stato sia per la fusione di uno stato nella forma. Proposta per evitare soglie manuali: addestrarlo a predire l'errore (continuo o in classi) da trasformazioni note e coppie statiche, e scegliere il punto operativo su sviluppo massimizzando l'utilitÃ  della memoria su viste escluse. Pose e mesh sono giÃ  ingressi necessari della baseline Whareformer (XYZ da profonditÃ  allineata e pose), quindi non introducono una dipendenza nuova; resta il rischio di errori di posa condivisi fra ingresso ed etichette. Audit: calcoli leggeri (minuti su CPU), GPU non utile e in competizione con la run per il limite QoS. Testo per la scheda R32 della mappa proposto in chat, non applicato.

## Opzioni per procedere col verificatore (proposte, 21 novembre 2026)

Passo comune: audit su CPU. Opzioni: (A) dati reali di qualitÃ  a livelli + sintetico realistico, valutazione a coppie e sull'intero ciclo; (B) training solo sintetico da forme statiche pulite con corruzioni realistiche, coppie reali ferme solo per valutazione indipendente; (C) verificatore preaddestrato esistente (es. FACT) usato cosÃ¬ com'Ã¨ o rifinito; (D) fusione solo negli intervalli in cui l'oggetto Ã¨ fermo, senza registrazione fra spostamenti, stati separati altrimenti. Raccomandazione dell'assistente: D come prima versione funzionante, B per il verificatore, C come confronto rapido se il codice Ã¨ disponibile.
