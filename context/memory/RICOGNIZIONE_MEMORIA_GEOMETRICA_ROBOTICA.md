# Memoria geometrica persistente per robotica: ricognizione critica

Ricognizione avviata il 9 novembre 2026, su richiesta di Marco. Fonti primarie online consultate nella sessione; analisi e proposta sperimentale, non risultati sperimentali nuovi. Questo approfondimento aggiorna la valutazione preliminare in `OPZIONI_FORMA_E_MEMORIA_ROBOTICA.md`. Non modifica la domanda approvata sul tracking né adotta un nuovo dataset o protocollo.

## Giudizio principale

Whareformer + SuperFlex è un'integrazione plausibile per associare a identità persistenti una geometria compatta. Può avere utilità senza migliorare IDF1, se abilita interrogazioni sull'ingombro che la sola posizione non consente. Tuttavia la combinazione non è, di per sé, una novità scientifica convincente: memoria a oggetti, posa e primitive compatte hanno precedenti diretti, soprattutto Hickory e SQ-SLAM. Non emerge una ragione documentata per aspettarsi che questa pipeline sia superiore a sistemi RGB-D dedicati alla ricostruzione/posa o a memorie più semplici per localizzazione.

La domanda più difendibile è un confronto qualità–memoria–costo: a parità di associazioni, input geometrici e procedura di posa, SuperFlex conserva più utilità geometrica di punti compressi, box e una superquadrica semplice? È un'ipotesi verificabile, non un beneficio dimostrato. La novità eventuale richiederebbe un problema o un metodo specifico e risultati convincenti, non soltanto collegare due modelli.

## Perimetro e livello di verifica delle fonti

Ricognizione mirata, non revisione sistematica esaustiva né certificazione di assenza di concorrenti. Consultati testo dei metodi e parti pertinenti degli esperimenti/limiti per Whareformer, SuperFlex, OSNOM, EgoTrack3D, ConceptGraphs, DynaMem, DovSG, Khronos, Hickory, BundleSDF, FoundationPose, OCC4M e DGSG-Mind. Per 3D-Mem consultati formulazione e input dell'esplorazione. Per QuadricSLAM consultata la pubblicazione breve ufficiale; per OnePose++ e MonoTracker le pagine degli autori: non rivendicata lettura integrale dei relativi articoli. Il PDF MonoTracker non è stato recuperato dal browser di ricerca; le sue affermazioni prestazionali non sono usate per una graduatoria.

Whareformer è indicato ECCV 2026 nel repository degli autori; BundleSDF e FoundationPose sono CVPR 2023/2024; Khronos RSS 2024; ConceptGraphs ICRA 2024; 3D-Mem CVPR 2025; Embodied VideoAgent ICCV 2025. Hickory, EgoTrack3D, OCC4M e DGSG-Mind sono trattati qui come preprint consultati, senza attribuire loro una pubblicazione non verificata. Il giudizio dipende dai setup effettivi, non soltanto dai titoli.

## Lavori più vicini: memoria, scena e geometria compatta

| Lavoro e fonte primaria | Input e ciò che dimostra | Limite rilevante per la proposta |
|---|---|---|
| [OSNOM / Lift, Match and Keep](https://arxiv.org/html/2404.05072v2), 2024–2025 | Video RGB con profondità stimata e ricostruzione/pose della scena; conserva identità e localizzazione oltre la visibilità. | L'ultima posizione non certifica lo stato reale fuori vista. Non è ricostruzione della forma o posa 6D; i riferimenti EPIC non sono una misura fisica indipendente. |
| [Whareformer](https://arxiv.org/html/2607.08537), 2026 | Associa aspetto e posizione 3D; mantiene track online attraverso occlusioni e ricomparse. Geometria derivata dall'RGB, con allineamento alla ricostruzione nel setup principale. | Risolve già il nucleo di permanenza dell'identità proposto. Non fornisce superficie, orientamento o accuratezza robotica metrica. Online dell'associatore non equivale a ricostruzione completa online degli input. |
| [EgoTrack3D](https://arxiv.org/html/2608.08016), preprint 2026 | Track egocentriche con punti, box e gestione del movimento. Variante densa ADT con maschere, profondità e pose GT; variante sparsa con maschere predette, geometria sparsa e BoxerNet. | Precedente diretto per memoria geometrica egocentrica. I risultati densi non dimostrano funzionamento con profondità monoculare rumorosa. La selezione del lookahead tramite traiettorie GT richiede attenzione per un confronto causale. |
| [ConceptGraphs](https://concept-graphs.github.io/assets/pdf/2023-ConceptGraphs.pdf), ICRA 2024 | Frame RGB-D con posa; associa/fonde nuvole per oggetto e descrittori, costruisce relazioni e supporta compiti robotici. | L'identità dei nodi della mappa non dimostra re-identificazione di ogni oggetto manipolato dopo lunghi intervalli. Non ricava automaticamente forma completa e posa oggetto stabile. |
| [DynaMem](https://arxiv.org/html/2411.04999), 2024–2025 | RGB-D con posa; memoria voxel dinamica, rimozione di geometria obsoleta e ricerca/localizzazione per mobile manipulation. | Aggiornamento spaziale e identità persistente della stessa istanza sono proprietà diverse. La memoria voxel gestisce implicitamente molte operazioni, senza essere un tracker universale di istanze o una ricostruzione completa. |
| [DovSG](https://arxiv.org/html/2410.11989), 2024–2025 | RGB-D, scansione della scena e rilocalizzazione; aggiorna localmente oggetti/relazioni e dimostra compiti consecutivi su robot. | Le prove di adattamento a modifiche osservabili della scena non equivalgono al tracking 6D continuo di oggetti arbitrari manipolati. Richiede un'infrastruttura geometrica e di rilocalizzazione. |
| [Khronos](https://arxiv.org/html/2402.13817), RSS 2024 | Misure geometriche/semantiche e odometria; mappa spazio-temporale con dinamiche brevi e cambiamenti di lungo periodo. | Gli autori segnalano assenza di registrazione 6D tra frammenti e associazione solo geometrica: frammenti spostati non vengono associati. È un limite specifico pertinente, non prova che Whareformer lo risolva nello stesso setup. |
| [QuadricSLAM](https://openaccess.thecvf.com/content_cvpr_2018_workshops/w9/html/Nicholson_QuadricSLAM_Dual_Quadrics_CVPR_2018_paper.html), 2018 | Box 2D multivista e camera prospettica; landmark ellissoidali con posizione, dimensioni e orientamento, ottimizzati con la camera. | Geometria grossolana e landmark statici; non memoria di oggetti mobili con forma dettagliata. Dimostra che compattezza + posa non è una nuova idea. |
| [SQ-SLAM](https://arxiv.org/html/2209.10817), 2022 | SLAM monoculare, punti sparsi e rilevamenti; superquadriche e associazione multivista. | Assume roll/pitch nulli, stima yaw; descrive correzioni manuali dell'ambiguità PCA. Non dimostra posa 6D generica o oggetti arbitrariamente mobili. |
| [Hickory / Hierarchical Object Representation](https://arxiv.org/html/2606.01545), preprint 2026 | RGB-D con pose note: oggetti → mesh SAM3D → posa FoundationPose → superquadriche Marching-Primitives → primitive inflazionate. Valuta ricostruzione, allineamento mappe e navigazione. | È il precedente più vicino alla proposta applicativa. Associazione iniziale tramite IoU di OBB e scelta di una best view: non dimostra il problema Whareformer di lunga re-identificazione di oggetti mobili. La pipeline include ricostruzione costosa; le primitive non rendono automaticamente economica l'intera costruzione. |

Hickory era già presente nella lettura preparatoria: questa sessione ne approfondisce l'effetto sul giudizio di novità, senza presentarlo come una scoperta assente dalla memoria precedente.

Altri riferimenti pertinenti:

- [3D-Mem](https://arxiv.org/html/2411.17735), CVPR 2025: snapshot multivista, memoria incrementale e frontiere per esplorazione/ragionamento; nell'esplorazione riceve RGB, depth e pose. È un'alternativa quando il compito richiede contesto visivo, senza richiedere una superficie completa per oggetto.
- [Embodied VideoAgent](https://openaccess.thecvf.com/content/ICCV2025/html/Fan_Embodied_VideoAgent_Persistent_Memory_from_Egocentric_Videos_and_Embodied_Sensors_ICCV_2025_paper.html), ICCV 2025: memoria persistente da video e sensori, aggiornata tramite azioni/eventi. La pagina ufficiale e gli estratti del metodo mostrano strumenti di interrogazione e aggiornamento; non prova una memoria monoculare di forme metriche 6D.
- [OCC4M](https://arxiv.org/html/2609.28798), preprint settembre 2026: track nel mondo, eventi e contenimento come interfaccia per manipolazione. Usa RGB calibrato e intersezione dei raggi con piani ad altezza oggetto nota; il testo lascia il depth misurato come alternativa futura. Quindi **RGB con geometria nota**, non recupero metrico libero dall'RGB. Le prove reali comprendono 20 episodi a camera fissa; i risultati non dimostrano ricostruzione di forma o generalizzazione a geometrie di supporto ignote.
- [DGSG-Mind](https://arxiv.org/html/2605.29879), preprint 2026, revisione settembre: RGB-D con posa, voxel e Gaussiane con istanze, scene graph e aggiornamenti locali. Mostra un'altra alternativa ricca per mappe dinamiche; non è un sistema monoculare RGB senza geometria fornita e richiede anche rilocalizzazione/addestramento ACE specifico della scena.

## Ricostruzione e posa: che cosa è già disponibile

| Lavoro | Capacità dimostrata e requisiti | Implicazione |
|---|---|---|
| [BundleSDF](https://arxiv.org/html/2303.14158), CVPR 2023 | Ricostruzione neurale e tracking 6D di un oggetto rigido sconosciuto, RGB-D, maschera iniziale, pose graph e memoria di frame. | Forma + posa temporale non è un problema aperto in assoluto. Non è una memoria multi-oggetto di lunga durata con re-identificazione arbitraria; i requisiti RGB-D sono più forti dei nostri. |
| [FoundationPose](https://arxiv.org/html/2312.08344), CVPR 2024 | Stima/tracking 6D RGB-D di nuovi oggetti, con CAD oppure immagini di riferimento e modellazione neurale. | Candidato serio per la posa quando si accettano profondità e modello/riferimenti. «Model-free» non significa assenza di riferimento o profondità. Una mesh SuperFlex imprecisa potrebbe peggiorarlo: innesto da validare, non compatibilità garantita. |
| [OnePose++](https://zju3dv.github.io/onepose_plus_plus/), NeurIPS 2022 | Posa RGB senza CAD, ma da sequenza di riferimento con pose note e ricostruzione SfM dell'oggetto. Verificata pagina degli autori. | Non equivale a ottenere scala e orientamento assoluti da un singolo RGB sconosciuto. |
| [MonoTracker](https://monotracker827.github.io/), BMVC 2025 | Pagina degli autori: tracking 6D RGB di oggetti sconosciuti, profondità monoculare, ottimizzazione delle pose e correzione delle incoerenze di scala. | Precedente RGB particolarmente pertinente per il modulo mancante. Non verificata integralmente la procedura di inizializzazione/scala nel paper: prima di adottarlo occorre leggerla e provare codice/licenza. Nessuna superiorità numerica assunta qui. |
| [SuperFlex](https://arxiv.org/html/2607.01015), 2026 | Decomposizione di nuvole in primitive deformabili; variante robusta per input parziali. Valutazione quantitativa parziale su ASE, esempi reali ScanNet++ e pipeline RGB illustrativa in appendice D. | Non è un tracker, non stima da solo una posa globale temporalmente stabile e non dimostra accuratezza robotica dall'RGB EPIC. Le pose delle primitive non costituiscono una posa unica dell'oggetto. |

Non confrontare numeri di questi lavori come una graduatoria unica: differiscono sensori, maschere, modelli iniziali, identità note, traiettorie, scala, causalità e metriche. «Monocular RGB-D» in BundleSDF indica una sola vista con depth, non RGB-only.

## Il problema ancora da risolvere nella combinazione

1. **Riferimento metrico.** Camera calibrata e profondità stimata non bastano a garantire scala corretta. La scala globale del mondo e quella del ramo forma devono essere coerenti. DA grezzo nel ramo forma e XYZ allineati del tracker possono vivere a scale diverse: va stimata/verificata la trasformazione comune, senza adattarla alle pose GT del test. Conservare l'inversa della normalizzazione SuperFlex.
2. **Forma e posa separate.** Per oggetto servono una geometria in un riferimento persistente e una trasformazione oggetto→mondo variabile. La relazione è `T_mondo_oggetto(t) = T_mondo_camera(t) · T_camera_oggetto(t)`. Whareformer non restituisce il secondo fattore completo. Il punto di localizzazione del tracker può inoltre non coincidere con il centro della forma: occorre modellare l'offset, non sovrapporre automaticamente i centri.
3. **Orientamento osservabile.** Registrazione rigida parziale verso un template iniziale è un candidato. PCA fornisce solo assi geometrici instabili, con segni/permutazioni ambigui. Tazze quasi cilindriche e superfici parziali possono non determinare lo yaw. Usare equivalenze di simmetria, confidenza e possibilità di astensione; non inventare un asse semantico dal numero della primitiva. Un riferimento arbitrario iniziale va bene per la persistenza, ma non coincide automaticamente con quello CAD delle annotazioni.
4. **Aggiornamento causale.** La prima prova può conservare una vista selezionata con regola prefissata; non richiede fusione. Fondere viste richiede prima la posa dell'oggetto, non soltanto quella della camera. Separare parti osservate e completate per non rinforzare allucinazioni. Associazioni errate contaminano anche una forma ottima.
5. **Memoria e verità corrente.** Fuori vista si conserva «ultima stima, tempo, incertezza». Se un umano sposta l'oggetto senza osservarlo, nessuna rappresentazione recupera da sola il nuovo stato. Distinguere unknown, occlusione e evidenza di rimozione.
6. **Collisioni.** Una superficie plausibile o una distanza radiale non certificano occupazione conservativa né distanza euclidea esatta. Per le primitive deformate verificare implementazione inside/outside; il solo test della superficie non basta se un volume contiene interamente l'altro. Inflazione calibrata riduce alcuni errori, ma non garantisce copertura delle parti invisibili.

Questi sono problemi di geometria e gestione delle stime; aggiungere un modello di linguaggio non li risolve automaticamente.

## Utilità applicativa, fattibilità e novità: tre giudizi distinti

| Dimensione | Giudizio attuale | Evidenza che potrebbe cambiarlo |
|---|---|---|
| Utilità applicativa | Plausibile per ingombro, interrogazioni spaziali e archivio compatto; debole se si chiede soltanto «dove ho visto l'oggetto?». Per quest'ultimo compito basta spesso identità + punto/box + tempo. | Beneficio sul compito geometrico rispetto a box e punti, con associazioni fissate e costo completo misurato. |
| Fattibilità | Prototipo offline ristretto plausibile: modelli già operativi. Sistema metrico online con posa 6D, oggetti mobili, fusione robusta e validazione robotica è molto più impegnativo del lavoro attuale. | Primo pilota di registrazione, misura scala/posa e costo su due brevi clip. Non c'è ora una stima verificata di tempo per l'estensione. |
| Novità scientifica | Bassa per la sola composizione Whareformer + SuperFlex + stimatore di posa. Hickory e SQ-SLAM impediscono rivendicazioni generiche. | Una soluzione specifica per stabilità/aggiornamento/incertezza e un confronto credibile con i precedenti; oppure una valutazione nuova e informativa del compromesso sotto profondità monoculare. Pubblicabilità non garantita. |

Risultati locali rilevanti: 299 osservazioni di cinque video, qualità dei completamenti ancora variabile e IoU 2D appaiata 0.4697 DA grezzo contro 0.4481 MoGE. Queste evidenze non sostengono forma 3D fedele, orientamento affidabile o utilità per collisioni. Consultare `RISULTATI_CONFRONTO_200.md`, senza ripetere gli esperimenti conclusi. SuperFlex potrebbe risultare soltanto un compressore con perdita, o essere dominato da punti sottocampionati/OBB: è un esito plausibile da ammettere fin dall'inizio.

Compattezza della sola geometria non significa compattezza dell'intera memoria: descrittori visivi, immagini, punti di supporto, storico e modelli possono dominare. Se per aggiornare SuperFlex si conservano tutte le nuvole, il risparmio va calcolato sul totale, non solo sul vettore delle primitive.

## Caso d'uso circoscritto proposto

**Interrogare l'ingombro ricordato di oggetti rigidi su un piano di lavoro dopo un cambio di inquadratura.** Esempio: indicare se un cilindro virtuale da appoggiare in una posizione candidata intersecherebbe un oggetto visto prima e ora fuori campo. È un test offline di occupazione per un futuro supporto al posizionamento; non una dimostrazione di grasping, pianificazione completa o sicurezza robotica.

Iniziare con oggetti stabili durante l'intervallo non osservato e supporto planare; gestire gli spostamenti osservati in episodi separati. Se si limita la posa a yaw/traslazione, dichiararlo: non è una validazione 6D. Per oggetti simmetrici interessa l'occupazione corretta, non un angolo arbitrario. Questo compito rende forma e orientamento utili; una demo «ricorda l'ultima posizione» favorirebbe soltanto le capacità già presenti in Whareformer.

## Esperimento minimo proposto, non ancora approvato o eseguito

### Domanda e dati

Ipotesi: mantenendo identità e stime di posa uguali, la memoria SuperFlex migliora il compromesso fra correttezza delle interrogazioni d'ingombro, byte e latenza rispetto alle geometrie semplici.

EPIC attuale permette controlli di fattibilità e qualità visiva, ma non una conclusione metrica indipendente. Un candidato più adatto è [Aria Digital Twin](https://arxiv.org/abs/2306.06362), ICCV 2023: video reali egocentrici, calibrazione, pose camera/oggetti, maschere, depth di riferimento e digital twin. Disponibilità dei singoli asset e corrispondenza dei modelli vanno controllate prima di fissare il campione; nessun download eseguito qui.

Proposta di pilota: due clip per verificare il percorso tecnico; solo se informativo, circa sei clip brevi e 10–20 episodi complessivi, con oggetti rigidi, viste parziali e intervalli fuori campo. Non sono numerosità giustificate per una prova statistica definitiva. Fissare selezione prima degli output; separare sviluppo e verifica per sequenza e, ove possibile, istanza. Più query sulla stessa clip non diventano osservazioni indipendenti. Verificare sovrapposizioni di pretraining: SuperFlex usa ASE, che non va trattato ingenuamente come test inedito; ADT reale è distinto, ma l'assenza di sovrapposizioni tra asset non è qui certificata.

Setup principale: RGB con profondità predetta; intrinseci e pose camera forniti uguali a tutti. È **RGB con localizzazione fornita**, non SLAM monoculare completo. Maschere comuni, eventualmente GT nel diagnostico, sempre dichiarate. Pose oggetto e mesh GT solo per valutare; non passate al sistema principale. Profondità GT soltanto in un controllo separato per distinguere errori della sorgente da limiti della rappresentazione. Non chiamare questo controllo RGB-D da sensore se usa depth renderizzato di riferimento.

### Confronti indispensabili

| Condizione | Ruolo |
|---|---|
| Whareformer originale | Riferimento di identità/localizzazione; non ha una forma completa. Per interrogazioni d'ingombro aggiungere esplicitamente una sfera a raggio fisso calibrato, evitando di attribuire questa estensione al paper. |
| Stesse track + OBB, e singola superquadrica semplice | Baseline molto compatte: verificano se basta una geometria grossolana. |
| Stesse track + punti voxelizzati/sottocampionati | Controllo della necessità di SuperFlex; raggio dei punti o voxel e inflazione scelti sullo sviluppo. |
| Stesse track + SuperFlex | Candidato: una forma selezionata causalmente, senza fusione nel primo confronto. |

Per box, punti e SuperFlex usare la stessa osservazione selezionata, stessa sorgente, stesso budget di viste e stessa procedura di posa, dove applicabile. Valutare più budget di punti e non soltanto una nuvola inutilmente grande. Confrontare a parità di byte e, separatamente, a parità di errore sul compito. Non scegliere manualmente per SuperFlex la sua vista migliore dopo aver visto il test.

Una prima analisi con **identità e posa oracle**, esplicitamente diagnostica, misura il limite della rappresentazione. Non conta come risultato end-to-end. Se SuperFlex non porta vantaggio neppure qui, non integrare una posa complessa per salvarlo. Se passa, ripetere con le associazioni Whareformer congelate e una posa stimata comune: riferimento iniziale scelto causalmente, registrazione rigida robusta verso quel riferimento e rifiuto degli allineamenti incerti. ICP multi-inizio è un candidato da misurare, non una garanzia. Con riferimento arbitrario, la trasformazione verso il frame CAD può essere ricavata nella sola valutazione tramite il primo frame di riferimento e va mantenuta fissa; vietato riallineare alla GT ogni frame.

La fusione, se successivamente studiata, è un'ulteriore ablation e non un vantaggio esclusivo concesso al ramo SuperFlex. Un sistema tipo ConceptGraphs con nuvole per oggetto è un confronto architetturale pertinente; la baseline controllata a punti non equivale a una replica ufficiale di ConceptGraphs. Hickory è il concorrente metodologico principale: una sua replica completa non è necessaria per il primo gate, ma senza confronto adeguato non si rivendica superiorità allo stato dell'arte.

### Metriche

- **Compito principale:** quota di query con intersezione reale dichiarate erroneamente libere (false-free), quota di query libere dichiarate occupate e quota di astensioni. Presentare curve variando margine/confidenza; non premiare il sistema che dichiara tutto occupato. Query fissate da geometria GT con casi liberi/collisione, incluse vicinanze delle superfici, senza selezionarle in base agli errori del metodo. Riportare prevalenza delle classi.
- **Geometria:** F-score di superficie con soglie metriche prefissate, errore di dimensioni/ingombro e copertura delle regioni nascoste separata da quelle viste. Campionamento/risoluzione comuni; GT per intersezioni derivata da mesh o occupazione di riferimento verificata. Non usare come verità i punti predetti che alimentano SuperFlex.
- **Posa:** errore di traslazione in cm e rotazione geodetica minimizzata sulle simmetrie pertinenti, oppure yaw nel setup planare; errori separati dalla semplice variazione della forma. Registrare fallimenti/astensioni e distinguere posa relativa al primo riferimento da orientamento semantico assoluto.
- **Persistenza:** IDF1 e corretta risposta riferita all'istanza richiesta; percentuale di track con geometria valida, memoria contaminata e ritardo di aggiornamento dopo spostamenti osservati. Se le associazioni sono congelate, IDF1 deve restare uguale: serve come controllo, non come metrica primaria del contributo.
- **Costo:** byte per oggetto e memoria totale della scena inclusi punti eventualmente conservati; latenza mediana/p95 di costruzione, aggiornamento e query; tempo della profondità, SuperFlex e registrazione separati. Misurare anche il sistema completo e indicare l'hardware. Il valore di occupazione non deriva automaticamente da un tempo di forward basso.

Aggregare prima per episodio/oggetto e riportare tutti i casi; se si stimano intervalli, ricampionare sequenze o episodi, non singoli frame/query dipendenti. Con un pilota minuscolo riportare differenze descrittive e casi d'errore, senza precisione statistica artificiale.

### Criteri di decisione e costo

Fissare sullo sviluppo una tolleranza applicativa di false-free e confrontare il richiamo dello spazio libero ai budget scelti. Nessuna soglia universale di sicurezza è giustificata da questo studio. Proseguire soltanto se SuperFlex migliora un compromesso utile: stessa qualità con meno memoria, più query corrette con stessi byte, o query più rapide senza perdita oltre la tolleranza dichiarata. Un vantaggio sulla sola mesh visualizzata non basta.

Se punti compressi/OBB dominano SuperFlex, concludere che il componente è ridondante nel setup. Se il vantaggio esiste solo con depth/pose oracle, riportare valore potenziale della rappresentazione e fallimento della pipeline monoculare. Se la forma è utile ma la posa stimata fallisce, il collo di bottiglia è dimostrato e non risolto dall'integrazione.

Primo costo ragionevole: adattatore dati e test di due clip senza training, misurando tempi prima di estendere. Non è disponibile una stima verificata di ore GPU/persona; nuovi asset, posa e validazione possono costare più della sola inferenza. Con due persone e consegna il 23 novembre, raccomandata analisi aggiuntiva circoscritta, non riscrittura implicita del progetto come sistema robotico completo.

## Raccomandazione finale per il progetto

Conservare il piano d'identità già approvato. Presentare alla docente tre opzioni: (A) chiudere il confronto sul tracking; (B) aggiungere un piccolo test qualità–memoria della geometria, raccomandato se non compromette A; (C) spostare la domanda principale sulla memoria robotica, revisione più costosa che richiede scelta esplicita di Marco e nuovi dati/protocollo. Questo documento prepara quella scelta, non la compie.

Nessun nuovo esperimento, training, installazione o job HPC eseguito per la ricognizione. Durante la sessione la memoria operativa è stata aggiornata separatamente: riporta 750421/750424 conclusi e 750536 attivo all'ultima verifica registrata. Non sono controlli effettuati da questa ricognizione; per identificativi, log, output e prossima verifica seguire `STATO_LAVORO.md`.
