# Registro delle decisioni e delle motivazioni

Aggiornato: 13 novembre 2026. Obiettivo: rendere ricostruibile il percorso scientifico per report e presentazione. Prime voci ricostruite dai documenti di progetto e dalla discussione del 9 novembre, poi aggiornamenti espliciti; non è una trascrizione completa delle conversazioni. Le date indicano le decisioni documentate, senza attribuire date precise dove mancano.

Ogni voce distingue scelta, ragione ed evidenza disponibile. Le revisioni successive non cancellano le scelte precedenti: ne spiegano il cambiamento. Stato operativo e attività in `STATO_LAVORO.md` e `TODO.md`.

## 1. Studiare la forma come informazione aggiuntiva — confermata il 4 novembre

**Scelta.** Verificare se confrontare la forma SuperFlex dell'osservazione corrente con forme SuperFlex conservate nelle track migliori l'associazione delle identità di Whareformer.

**Ragione.** Whareformer usa aspetto e posizione; una rappresentazione esplicita della superficie potrebbe fornire informazione complementare. La posizione XYZ da sola non descrive la forma.

**Limite.** È un'ipotesi sperimentale: integrazione tecnica, buona ricostruzione e miglioramento del tracking sono risultati distinti. Nessun beneficio è ancora dimostrato. Non rivendichiamo come nuova l'idea generale di usare geometria o superquadriche per l'associazione.

Fonte: `FASE_0.md`, §§2 e 5.

## 2. Usare EPIC-KITCHENS e mantenere confronti controllati — 4 novembre

**Scelta.** Usare il benchmark comune a Whareformer, con le stesse osservazioni, maschere, feature visive, XYZ, split ed evaluator nelle varianti confrontate. Sviluppo e test restano separati.

**Ragione.** Attribuire eventuali differenze al contributo della forma, evitando che dipendano da un detector, da posizioni o da dati diversi. EPIC dispone degli ingredienti documentati per collegare immagini, maschere e geometria.

**Conseguenza.** Prevedere Whareformer originale, variante SuperFlex e geometria semplice dagli stessi punti; verificare il recupero della baseline a contributo geometrico zero. IDF1 misura l'associazione, mPCL completa la valutazione; registrare anche fallimenti e costo. Il protocollo dettagliato non è ancora fissato.

Fonte: `FASE_0.md`, §§3–4.

## 3. Partire da SuperFlex robust preaddestrato — confermata entro il 4 novembre

**Scelta.** Usare il checkpoint robust per le nuvole parziali, senza training da zero; verificare prima un esempio degli autori sull'HPC.

**Ragione.** Le osservazioni monoculari mostrano solo parte dell'oggetto. La variante robust è progettata per input parziali; partire dai pesi disponibili rende il lavoro compatibile con risorse e scadenza.

**Evidenza.** L'esempio lampada ha completato inferenza ed esportazione, con controllo visivo. Questo verifica il funzionamento del componente, non la qualità sugli oggetti EPIC o il tracking.

Fonti: `FASE_0.md`; `VERIFICA_SUPERFLEX_744144.md`.

## 4. Limitare il primo pilota a P01_01 — 7 novembre

**Scelta.** Usare P01_01, presente nel train della configurazione ufficiale, per il primo controllo; preparare tre osservazioni della classe pan disponibili con RGB, maschera e posa.

**Ragione.** Verificare l'intera catena con pochi dati prima di estenderla, senza usare il test per le scelte iniziali.

**Limite.** I tre frame sono diagnostici: la categoria comune non certifica la stessa identità fisica. Non costituiscono un campione di valutazione del tracking.

Fonti: `FASE_0.md`, §3; `INPUT_EPIC_PILOTA.md`.

## 5. Usare inizialmente la profondità del percorso Whareformer — eseguito entro il 9 novembre

**Scelta.** Costruire punti degli oggetti con maschere VISOR e profondità Depth Anything V2, usando il percorso di allineamento alla scena derivato dal codice Whareformer.

**Ragione.** Verificare se la geometria già prevista dalla baseline fosse sufficiente anche per alimentare SuperFlex, limitando le componenti aggiuntive. I soli file XYZ per oggetto non contengono la superficie necessaria.

**Evidenza e limite.** Profondità e nuvole sono state prodotte e controllate. La prova è rimasta in unità scena, senza equivalenza metrica con la baseline certificata. Non era una replica della pipeline RGB SuperFlex.

Fonti: `STATO_LAVORO.md`; `VERIFICA_PROFONDITA_744902.md`; `VERIFICA_GEOMETRIA_747518.md`.

## 6. Diagnosticare le forme prima di estendere gli esperimenti — 9 novembre

**Motivo della revisione.** SuperFlex ha prodotto output numericamente validi sui tre input EPIC, ma forme poco fedeli: prime due squadrate, terza più arrotondata senza manico affidabile.

**Scelta.** Controllare orientamento, profondità grezza/allineata e checkpoint supervised/unsupervised, senza scegliere a posteriori la rotazione migliore per ogni frame.

**Evidenza.** Gli 84 casi del job 749200 mostrano forte sensibilità all'orientamento; nessuna correzione semplice risolve sistematicamente la qualità visiva. Il checkpoint unsupervised aderisce peggio ai punti osservati nei sei confronti; la profondità grezza aiuta due frame e peggiora il terzo con supervised.

**Conseguenza.** Nessuna evidenza per adottare il secondo checkpoint o una rotazione come soluzione. Le distanze dai punti osservati non misurano la correttezza delle parti nascoste né l'utilità per l'identità.

Fonti: `VERIFICA_SUPERFLEX_EPIC_749180.md`; `DIAGNOSI_SUPERFLEX_749200.md`.

## 7. Considerare MoGE-2 come controllo della sorgente geometrica — 9 novembre

**Scelta corrente.** Provare MoGE-2 sugli stessi RGB e maschere VISOR, mantenendo SuperFlex robust e lasciando invariati gli XYZ Whareformer.

**Ragione.** Dopo l'esito insoddisfacente, isolare l'effetto della sorgente geometrica. L'appendice D di SuperFlex descrive SAM3 → MoGE → robust; il riferimento bibliografico è MoGE-2. Questo motiva il candidato, senza garantirne la superiorità.

**Evidenza successiva.** Job 749539 e verifica 749582 completati, output scaricati e figure ispezionate (`VERIFICA_MOGE2_749539.md`). Tutti i pixel mantenuti, stessi indici campionati e stesso robust. Le prime due forme restano squadrate, la terza diventa una sola primitiva squadrata senza recupero convincente del manico. Residui ai rispettivi punti stimati maggiori in tutti e tre i casi; non sono accuratezza fisica.

**Conseguenza e limite.** Nessuna evidenza che sostituire la sorgente con MoGE risolva il problema; nessuna adozione finale né conclusione di non integrabilità. Il cambiamento include profondità, intrinseci stimati e assenza di allineamento alla scena, quindi non isola una causa unica. Proseguire verso la verifica del segnale d'identità; non assumere che ricostruzione tecnicamente valida significhi forma utile. Gli autori non specificano tutti i dettagli per replicare identicamente la figura RGB.

Fonti: `REPLICA_RGB_SUPERFLEX.md`; `manifests/rgb_sources.json`; [paper SuperFlex, appendice D e riferimento 33](https://arxiv.org/html/2607.01015).

## 8. Rivedere la priorità della replica completa con SAM3 — 9 novembre

**Scelta precedente.** Riprodurre prima l'intera pipeline RGB degli autori; da qui l'acquisizione dei sorgenti SAM3 e la verifica dei pesi, risultata HTTP 401 senza autenticazione.

**Revisione approvata.** SAM3 diventa opzionale. Per verificare l'integrazione usiamo le maschere VISOR già disponibili; l'accesso ai pesi SAM3 non blocca il lavoro.

**Ragione.** SAM3 serve a segmentare gli oggetti, mentre la domanda riguarda il contributo della forma all'associazione. Cambiare insieme segmentazione e geometria renderebbe meno interpretabili le differenze. La replica completa era un obiettivo distinto, non un prerequisito tecnico per integrare SuperFlex.

Fonti: `INTEGRAZIONE_DISCUSSIONE.md`; `TODO.md`; discussione del 9 novembre.

## 9. Verificare il segnale d'identità prima di attribuirgli un beneficio — piano approvato il 9 novembre

**Scelta.** Preparare osservazioni con identità fisiche verificate, ripetizioni da viste diverse e istanze diverse anche simili. Studiare stabilità e separazione delle forme, anche nei casi ambigui per aspetto/posizione.

**Ragione.** Una forma plausibile può cambiare fra viste della stessa istanza o essere simile per istanze diverse. Non occorre una ricostruzione perfetta, ma un segnale utile all'associazione.

**Conseguenza.** Le etichette d'identità servono per sviluppo e valutazione, non per decidere associazioni o aggiornare la memoria durante il tracking misurato. Questa verifica non sostituisce la valutazione completa.

Fonte: `TODO.md`, punti 3 e 6.

## 10. Preparare un'integrazione minima senza fissarla come metodo definitivo — proposta del 9 novembre

**Candidato.** Conservare i modelli congelati e correggere i logits Whareformer prima della softmax con un contributo derivato dalla distanza fra forme. Calibrare sullo sviluppo includendo peso zero.

**Ragione.** Il checkpoint Whareformer combina due segnali, aspetto e posizione. Aggiungere direttamente una terza distanza al suo embedding richiederebbe modificare e adattare il modello. La fusione esterna permette un primo confronto con minori modifiche.

**Ancora aperto.** Distanza, trattamento di scala/rotazione, capacità e aggiornamento della memoria, peso e soglia neutra. Non confrontare vettori grezzi di primitive; ordine e decomposizione possono cambiare. Tenere la memoria causale, gestire forme mancanti e misurare la contaminazione da associazioni errate. Anche lasciando invariato il logit New Track, la softmax può cambiarne la probabilità.

Fonti: `INTEGRAZIONE_DISCUSSIONE.md`; `TODO.md`, punti 4–6; codice locale `Whareformer-repo/src/models/whareformer.py` e `tracking/tracker/matcher/matcher_types.py`.

## 11. Ampliare il confronto prima di scegliere la sorgente — 9 novembre

**Scelta richiesta da Marco.** Testare nuove osservazioni con entrambe le sorgenti, senza fermarsi ai tre frame precedenti. Campione fissato: 16 nuovi frame disponibili, 27 osservazioni candidate di 11 categorie; maschere >=128 pixel, esclusioni dichiarate in `CONFRONTO_GEOMETRIA_ESTESO.md`. Includere anche Depth Anything grezzo per distinguere l'effetto dell'allineamento.

**Ragione e limite.** Tre frame non permettono un giudizio generale. L'estensione aumenta copertura e varietà, ma resta un campione dipendente di un solo video, senza geometria 3D ground truth; non produce automaticamente significatività statistica né una graduatoria di accuratezza assoluta. Registrare tutti i casi e i fallimenti prima di decidere la sorgente. Verifica dell'identità e valutazione del tracking restano necessarie.

**Evidenza successiva.** Job 749665/749728 completati: 16 nuovi RGB elaborati, 27 oggetti di 11 categorie in 11 frame, 81 output validi e tutte le dieci tavole ispezionate. Alcune forme semplici sono riconoscibili, molte padelle/piatti e completamenti restano deformati; nessun vantaggio visivo sistematico MoGE. DA ha residui medi ai rispettivi punti inferiori; non sono accuratezza fisica. Nessuna sorgente finale adottata. Resoconto `CONFRONTO_GEOMETRIA_ESTESO.md`.

## 12. Confronto su 200 immagini prima della scelta geometrica — 9 novembre

**Decisione approvata da Marco.** Confrontare le stesse immagini sui due rami, senza adottare Depth Anything per sola compatibilità con Whareformer. Obiettivo 200 nuovi frame, 40 in ciascuno di cinque video del train/partecipanti distinti, prima di vedere gli output. Maschere e SuperFlex comuni, DA grezzo/allineato come controllo; protocollo `CONFRONTO_200_IMMAGINI.md`.

**Motivazione e limiti.** I campioni precedenti di un solo video non sostengono una scelta generale. Il numero maggiore amplia copertura, ma non crea ground truth geometrica né indipendenza statistica. Nessun vincitore assunto; separare affidabilità/costo, giudizio qualitativo, fitting e successiva utilità per identità/tracking. Budget iniziale circa un'ora di calcolo da verificare sul primo blocco; acquisizione separata. Stato: acquisizione 749955 inviata, nessuna nuova inferenza ancora verificata.

**Avanzamento:** acquisizione 749966 riuscita dopo correzione del percorso RGB P08_09, senza cambiare video; 200 immagini fissate e 299 candidati, GPU 749968 inviato. Prima dell'inferenza definiti controllo della sagoma riproiettata rispetto a VISOR e aggregazione per immagine/video; non accuratezza 3D, soprattutto in presenza di occlusioni. Diagnostiche numeriche su tutti i casi; lettura qualitativa di 12 osservazioni per video scelte a quantili dell'elenco eleggibile indipendentemente dagli esiti, tutti gli output conservati. Nessun risultato del confronto ancora dichiarato.

**Gestione del fallimento osservato:** 749968 si ferma nel quarto video per zero primitive attive con MoGE. Ripresa 750019 senza cambio di soglia/checkpoint e con riuso degli output completati; registrare il fallimento, non scegliere una nuova soglia sul caso. Al riepilogo condizionale affiancare una lettura descrittiva con output mancanti come sagoma vuota, applicata a tutti i rami. Questa lettura è stata aggiunta dopo l'emergere del fallimento e va dichiarata come tale.

**Esito successivo verificato:** confronto concluso in 26 min 48 s GPU, con 299 osservazioni in 200 immagini di cinque video. Su 298 osservazioni appaiate in 199 frame, IoU DA grezzo 0.4697 contro MoGE 0.4481; differenza media concorde in tutti i cinque video. In 120 frame prevale DA, in 79 MoGE. Mesh disponibili: 299 per DA grezzo, 293 per DA allineato, 298 per MoGE; fallimenti espliciti. Le 60 osservazioni qualitative prefissate mostrano ancora molti completamenti deformati. Resoconto `RISULTATI_CONFRONTO_200.md`.

**Raccomandazione, non decisione definitiva:** DA grezzo come candidato del ramo forma, mantenendo XYZ Whareformer invariati. Motivazione ora empirica: modesto vantaggio di compatibilità 2D e copertura, oltre alla possibilità di riuso della profondità della baseline. Non dimostra accuratezza 3D superiore o beneficio d'identità; prossimo controllo stabilità/discriminatività e confronto con geometria semplice prima della valutazione nel tracker.

**Chiusura della verifica:** output completi e log scaricati, 6185 checksum e 891 provenienze delle nuvole verificati localmente; 20 tavole del sottoinsieme prefissato ispezionate. Nessun job lasciato in corso. I fallimenti rimangono nell'evidenza e non sono stati corretti abbassando soglie.

## 13. Comprensione della geometria e passaggio di sessione — 9 novembre

**Richiesta di Marco.** Conservare il dialogo su maschera, profondità, camera e forma come passaggio di comprensione personale da esporre alla docente, insieme allo stato e ai prossimi passi. Sintesi scientifica in `COMPRENSIONE_DA_MOGE_SUPERFLEX.md`; non è una trascrizione letterale o un nuovo esperimento.

**Chiarimenti consolidati.** La maschera non fornisce profondità; DA e MoGE analizzano entrambi l'intera immagine. DA stima Z e noi ricaviamo XYZ con gli intrinseci disponibili; MoGE comprende il recupero della camera e rende i punti coerenti con la proiezione. Il calcolo deterministico di XY non elimina l'incertezza di Z. Le cinque camere EPIC Fields sono disponibili e utilizzate nel ramo DA, con proiezione semplificata senza distorsione. MoGE è più autonomo in assenza di calibrazione, non necessariamente più accurato.

**Conseguenza interpretativa.** Il confronto eseguito valuta DA con camera fornita contro MoGE con camera stimata. Il risultato non isola la qualità della profondità. Un controllo MoGE con campo visivo noto è stato indicato come possibile diagnostica, non eseguito e non approvato come nuova fase necessaria. Valutazione attuale: pipeline operativa e confronto informativo, forme ancora poco convincenti, utilità d'identità non misurata; nessun confronto numerico diretto con l'IoU 3D del paper.

**Continuità del piano.** Domanda scientifica invariata. La sequenza operativa è passata dalla replica RGB completa obbligatoria a VISOR con SAM3 opzionale; la scelta della geometria è stata preceduta dai confronti appaiati richiesti da Marco. Il test 200 raccomanda DA grezzo come candidato, non adozione definitiva. Ripresa: corrispondenze e identità fisiche verificate → stabilità/discriminatività e controllo con geometria semplice → distanza/memoria e prototipo minimo → tracking con evaluator originale. Baseline del collega da verificare. Nessun nuovo job o cambio di metodo in questa chiusura di sessione.

**Chiarimento successivo sulla memoria, stessa sessione.** Marco chiede quando definirla e cosa confrontare con la nuova osservazione. Discussione preliminare ora e validazione nei test d'identità, definizione prima del prototipo. Il confronto riguarda la forma SuperFlex del singolo oggetto contro forme passate della track; non l'immagine intera contro una mesh. Memoria piccola di una/poche forme, confronto di superfici e aggiornamento dopo l'associazione sono proposte da validare; nessuna media dei parametri grezzi, nessun aggiornamento con identità oracle nel tracking. Capacità, distanza, trattamento di rotazione/scala e regola di aggiornamento restano aperti. Dettagli in `INTEGRAZIONE_DISCUSSIONE.md`; nessun nuovo job o cambio di piano.

## 14. Memoria aggregata mediante fusione delle nuvole — proposta di Marco, 9 novembre

**Proposta.** Dopo l'associazione mediante forma/aspetto/posizione, fondere la nuvola nuova con quella della track e riapplicare SuperFlex per aggiornare la decomposizione. Marco chiede di valutarne rischio con viste parziali e costo; nessuna implementazione o adozione definitiva richiesta.

**Valutazione e limite.** La fusione richiede registrazione nel riferimento dell'oggetto: pose della camera e centratura non compensano automaticamente il suo movimento. Conservare punti originariamente stimati dall'RGB, distinguendoli da completamenti ricampionati dalle primitive; registrazione errata, densità sbilanciate e associazioni sbagliate possono peggiorare la memoria. Il costo non è necessariamente proibitivo: input SuperFlex fisso di 4096 punti e un forward aggiuntivo per aggiornamento, oltre a registrazione e gestione punti. Nessun costo o miglioramento della fusione ancora misurato.

**Raccomandazione, non decisione.** Prima memoria limitata senza fusione come riferimento; fusione come variante da provare su identità verificate e poi confrontare separatamente. Primo lavoro operativo invariato: corrispondenze e campione d'identità. Dettagli e fonti in `INTEGRAZIONE_DISCUSSIONE.md`, sezione proposta di Marco.

## 15. Ridondanza del 3D, rappresentazione e possibile memoria robotica — discussione del 9 novembre

**Obiezione di Marco.** Forma e profondità provengono dall'RGB già usato per l'aspetto: il guadagno può essere ridondante. Chiede alternative per confrontare le geometrie, pro/contro e giustificazione di SuperFlex se l'evidenza viene aggiornata tramite punti. Resta interessato a verificare empiricamente il beneficio.

**Valutazione.** Nessuna nuova misura indipendente, ma possibile rappresentazione complementare al descrittore compresso del tracker; beneficio non garantito. Opzioni discusse: descrittori geometrici invarianti, superfici registrate con confronto parziale, descrittori appresi. Prima proposta raccomandata: memoria limitata senza fusione e descrittore semplice, confrontando punti e SuperFlex a condizioni dichiarate equivalenti. Non ancora una scelta approvata. La memoria senza fusione non risolve automaticamente il confronto fra viste.

**Nuova ipotesi applicativa di Marco.** Usare il tracker per identità e ultima posizione nota e SuperFlex per rappresentare forma e, con un modulo di posa, orientamento nella scena. È un possibile obiettivo geometrico distinto dal miglioramento del tracking; potrebbe essere studiato anche in assenza di guadagno IDF1. Non è ancora una revisione approvata della domanda di ricerca. Non dimostra capacità robotiche o dati pronti per Physical AI; novità specifica e valutazione restano aperte. Opzioni, limiti e fonti in `OPZIONI_FORMA_E_MEMORIA_ROBOTICA.md`.

**Conseguenza corrente.** Nessun nuovo esperimento o modifica implementativa. Avvio operativo ancora su corrispondenze e identità; preservare per la prossima chat l'ipotesi robotica come proposta da discutere, non come obiettivo implicitamente sostitutivo.

## 16. Confronto DA/MoGE per il segnale d'identità e possibile lavoro notturno — discussione del 9 novembre

**Proposta di Marco.** Proseguire DA e MoGE in parallelo per mantenere un confronto, con successiva prosecuzione DA; valutare un carico computazionale notturno.

**Raccomandazione.** Confrontare i due rami sulle stesse osservazioni e identità verificate, riutilizzando prima nuvole e ricostruzioni disponibili. DA permette il riuso della profondità prevista da Whareformer, ma il suo checkpoint di associazione riceve distanze d'aspetto e posizione, non direttamente la profondità: mantenendo XYZ/feature originali, MoGE nel solo ramo forma non è escluso dal riuso del checkpoint. Il vantaggio di sagoma DA non dimostra maggiore discriminatività.

**Evidenza e conseguenza.** Accesso HPC ricontrollato: nessun job attivo e quattro ambienti esistenti presenti. Nessun nuovo job inviato. Precalcolo di distanze fra forme e controllo con geometria semplice possibile sugli output già disponibili; corrispondenze, identità e procedura devono essere esplicitate prima di interpretare i risultati. Nessuna durata stimata come verificata, nessuna adozione definitiva DA né nuovo protocollo fissato.

## 17. Preparare il confronto appaiato del segnale di forma — richiesta esecutiva del 9 novembre

**Richiesta.** Marco chiede di preparare l'esperimento proposto. Implementato un precalcolo diagnostico sui dati di sviluppo esistenti, senza fissare il futuro metodo del tracker: punti e superfici SuperFlex per DA grezzo/MoGE, normalizzazione di forma, descrittore D2, controllo spettrale e registrazione rigida multi-inizio. Tutte le coppie intra-video da frame diversi; nessuna etichetta ricavata dai punteggi o dagli UUID.

**Motivazione e limiti.** Separare contributo della sorgente e della rappresentazione senza nuove inferenze; misurare il costo sul pilota prima di impegnare molte ore. Invarianza della distanza non corregge instabilità della ricostruzione. Identità fisiche, corrispondenza `detection_idx` e complementarità ai segnali baseline restano da verificare. Procedura, limiti e piano analitico in `ESPERIMENTO_IDENTITA_DA_MOGE.md`.

**Esecuzione osservata, aggiornamento del 10 novembre.** Preparazione 750421 e pilota 750424 COMPLETED/0:0, rispettivamente 1m14s e 43s. Mapping delle 299 osservazioni verificato, 8797 coppie; UUID tutti distinti. Controlli sintetici superati. Pilota: 26.8s su dieci coppie e quattro processi, proiezione circa 1h19m per il completo; avviato 750536 con limite tre ore e riuso, osservato RUNNING. Nessun nuovo modello/inferenza/installazione. Primo campione di 37 osservazioni/sette identità revisionate visivamente prima di consultare le distanze: evidenze e limiti nel protocollo; non ground truth persistente certificata e negativi entro categoria limitati a due piatti in un video. Nessun risultato finale di stabilità/discriminatività EPIC ancora disponibile. Stati e percorsi in `STATO_LAVORO.md`. L'implementazione esplorativa non equivale ad approvazione definitiva di distanza, memoria o sorgente.

## 18. Ricognizione critica della memoria geometrica robotica — richiesta di Marco, sessione avviata il 9 novembre

**Attività autorizzata e completata.** Analisi di fonti primarie su memoria, scena, ricostruzione e posa; resoconto `RICOGNIZIONE_MEMORIA_GEOMETRICA_ROBOTICA.md`. Nessun nuovo obiettivo o protocollo adottato.

**Valutazione motivata.** Utilità possibile per ingombro/compattezza senza guadagno IDF1, ma novità debole della sola composizione: Hickory integra già ricostruzione/posa/superquadriche per mappe e navigazione; SQ-SLAM e memorie robotiche dinamiche sono precedenti pertinenti. Separare RGB con profondità stimata/localizzazione fornita, RGB-D e RGB con supporto noto (OCC4M). EPIC attuale non dimostra forma metrica o orientamento affidabile.

**Proposta, non decisione approvata.** Test offline dell'ingombro ricordato con associazioni/posa/input comuni, OBB, singola superquadrica e punti compressi; metriche qualità–byte–latenza e fallimenti. Oracle separati come diagnostica; ADT candidato per GT indipendente, non dataset adottato. Raccomandato conservare il piano d'identità, con eventuale estensione limitata previa scelta di Marco. Accettare ridondanza di SuperFlex se le geometrie semplici lo dominano.

**Conseguenza e limiti.** Nessun job/download/controllo HPC nuovo nella ricognizione robotica. In quella fase 750421 non era stato ricontrollato; il successivo controllo operativo documentato nella voce 17 lo certifica COMPLETED, insieme al pilota, e registra il nuovo job attivo 750536. Scala tra ramo forma e XYZ, riferimento d'oggetto e posa restano prerequisiti aperti.

## 19. Esito del primo confronto di identità e mantenimento del controllo MoGE — 10 novembre

**Risultato verificato.** 750536 COMPLETED/0:0 in 47m26s, 8797 coppie, output/log scaricati e controllati; nessun job attivo. Su 37 osservazioni/sette identità visive, 158 coppie etichettate e 149 comuni. Le AUC D2 del controllo entro categoria P22_01 sono 0.612/0.627/0.701/0.768 per punti DA/SuperFlex DA/punti MoGE/SuperFlex MoGE. Tutte le AUC sono state ricalcolate indipendentemente; resoconto `RISULTATI_IDENTITA_DA_MOGE.md`.

**Interpretazione e limite.** Nel campione MoGE+SuperFlex discrimina i due piatti meglio di DA+SuperFlex con D2, mentre il controllo semplice sui punti resta competitivo e il beneficio SuperFlex dipende dalla distanza. Non è una graduatoria generale: negativi entro categoria solo in un video, due identità e annotazione visiva non persistente certificata. Nessun beneficio nel tracking o correttezza 3D dimostrati.

**Raccomandazione, non nuova scelta definitiva.** Mantenere entrambi i rami e i punti come controllo; ampliare/rafforzare identità entro categoria e collegare osservazioni baseline prima dell'integrazione. Riutilizzare le distanze disponibili. Nessun nuovo job, dataset, training, soglia o metodo adottato in questa verifica.

## 20. Mantenere DA e MoGE nei prossimi passi — indicazione di Marco, 10 novembre

**Direzione approvata.** Marco indica di proseguire con entrambe le sorgenti finché una risulti chiaramente più conveniente. Questo aggiorna la precedente ipotesi di confrontarle e poi procedere comunque con DA: nessuna sorgente ha una precedenza scientifica definitiva. Obiettivo, dataset e XYZ/feature Whareformer restano invariati.

**Motivazione ed evidenza.** Compatibilità 2D e discriminazione dell'identità non danno la stessa graduatoria; il controllo d'identità è ancora troppo ristretto per eliminare un ramo. Il job 750536 ha contribuito alla fase di verifica del segnale e al confronto delle distanze, senza chiudere la validazione delle identità, fissare la memoria o dimostrare un beneficio nel tracking.

**Conseguenza operativa.** Campione e osservazioni comuni, controllo sui punti e riuso delle distanze; mantenere le due sorgenti come opzioni della stessa interfaccia, evitando due integrazioni indipendenti. Estendere/verificare identità e collegare la baseline; sviluppare l'interfaccia senza attendere un vincitore. Confronto di utilità, copertura/fallimenti e costo, poi tracking sullo sviluppo con protocollo e budget di calibrazione confrontabili. Nessuna soglia numerica di convenienza o regola finale di selezione fissata ora, nessun nuovo training/job autorizzato implicitamente da questa discussione. Un eventuale pareggio scientifico può giustificare la scelta della sorgente meno costosa; non serve forzare una superiorità geometrica.

## 21. Rendere il lavoro comprensibile e condivisibile in repository — richiesta di Marco, 10 novembre

**Richiesta.** Prima di chiedere gli asset al collega, Marco vuole capire il codice prodotto e predisporre una repository comune; conferma che la docente richiede GitHub. Raccomandata repository privata per codice/documenti/risultati essenziali, con pacchetti esterni per i dati pesanti. Nessun lavoro del collega attribuito come già acquisito.

**Esecuzione e limite.** Inventariati gli script, distinti strumenti di esperimento e codice degli autori, documentato il matcher ancora non integrato. Primo commit locale 97b3218: 112 file, 44 script condivisibili e 17 snapshot numerici; esclusi dati/pesi/materiali del corso/accesso personale. Verifica dei byte di 61 script/risultati e creazione di cinque archivi di consegna con hash, incluso il run geometrico completo separato da Git. Guide `docs/CODICE_PRODOTTO.md` e `docs/CONDIVISIONE.md`; percorsi in `STATO_LAVORO.md`. Pubblicazione ancora dipendente dall'accesso GitHub dell'utente; nessun remoto, invito o dato inviato al collega. Nessun nuovo esperimento.

## 22. Repository comune del collega e specifica di input SuperFlex — 11 novembre

**Revisione organizzativa di Marco.** Usare la repository comune senza crearne una aggiuntiva. Il lavoro locale documentato e i pacchetti restano disponibili per l'importazione, URL/accesso ancora da acquisire.

**Chiarimento verificato per l'interfaccia.** Specificato il contratto del ramo SuperFlex già eseguito: nuvola parziale per oggetto, riferimento camera dichiarato, campionamento e normalizzazione degli autori prima del tensore. Il singolo XYZ Whareformer non basta. Dettagli, formato NPZ compatibile e limiti di orientamento in `docs/INPUT_SUPERFLEX_PER_WHAREFORMER.md`. Nessuna nuova normalizzazione del tracker, sorgente adottata o esecuzione; export e corrispondenze ancora da verificare.

## 23. Collegamento remoto e selezione del codice da pubblicare — 11 novembre

**Richiesta.** Collegare la repository comune, poi controllare prima del caricamento che il codice sia pulito, efficace ed essenziale. Configurati `origin` e fetch; nessun merge/push. Il materiale storico non verrà caricato in blocco.

**Esecuzione e motivazione.** Preparata candidata basata sul remoto, ramo locale `prepare/superflex-core` (eac7002), dieci file per geometria/confronto/analisi; eliminate dalla selezione dipendenze dai vecchi run, accessi personali, diagnostici e duplicazioni. Letture geometriche condivise in memoria e analisi per video/categoria. Regressione numerica e sette test superati; sorgenti storici e risultati invariati. Perimetro/evidenza in `REVISIONE_CODICE_REPOSITORY.md`.

**Limite e conseguenza.** Nucleo installabile e verificato, non pipeline neurale completa o integrazione Whareformer. Runner di inferenza/acquisizione richiedono ulteriore portabilità e verifiche prima di includerli. Nessun nuovo esperimento scientifico e nessun file pubblicato; usare solo il ramo candidato per la futura condivisione.

## 24. Condividere codice verificato e memoria senza dettagli personali — 11 novembre

**Direzione approvata.** Marco chiede il caricamento e colloca la memoria scientifica in `context/memory`; richiede inoltre il controllo di chiavi e informazioni non condivisibili.

**Esecuzione.** Preparazione di copie ripulite dei documenti, esclusione dei materiali del corso e dei file di accesso. Conservati gli originali e i risultati locali. Rimosso l’indirizzo email personale dai metadati del commit locale non ancora pubblicato, usando il recapito GitHub no-reply dell’account verificato. Il vecchio commit candidato eac7002 è sostituito da cbd6ca1 senza cambiamenti al codice.

**Esito verificato.** Controllati contenuti, nomi, snapshot Git raggiungibili e metadati dei nuovi commit, senza pattern di credenziali rilevati. Pubblicati codice e memoria sul solo ramo `prepare/superflex-core`, riferimento remoto verificato; `main` invariato. Rapporto locale `shared_exports/publication_security.json`. Un controllo con pattern e revisione mirata non garantisce l’assenza assoluta di segreti. Cronologia indipendente dell’archivio locale esclusa; nessun nuovo esperimento.

## 25. Completare il ramo autonomo senza micro-proposte — 11 novembre

**Direzione richiesta da Marco.** Finire nel modo più efficace tutto ciò che è possibile senza il contributo del collega, mantenendo l'obiettivo finale di integrazione.

**Raccomandazione, non esecuzione.** Coordinare portabilità della pipeline DA/MoGE→SuperFlex, verifica delle identità e del segnale, export per osservazione e componente indipendente di confronto/memoria. Riutilizzare i run conclusi; nuovi calcoli mirati soltanto dove mancano dati informativi. Non limitare il lavoro alla sola revisione di alcune immagini e non confondere più inferenze con più evidenza.

**Limite e conseguenza.** Conservare entrambi i rami e il controllo sui punti. Dettagli di nuovi campioni, distanza e memoria non fissati da questa indicazione; nessun nuovo job eseguito. Per concludere l'integrazione e misurare il tracking serviranno gli asset effettivi della baseline, non necessariamente tutto il lavoro modificato del collega. Codice pubblicato finora limitato al nucleo geometrico/confronto: runner neurali ancora da rendere portabili.

**Successiva approvazione esecutiva di Marco, 11 novembre.** Procedere nella nuova chat con Astra con tutto il codice necessario e le run HPC per completare il ramo autonomo. Piano consolidato in `PIANO_CHIUSURA_RAMO_GEOMETRICO.md`: pipeline portabile, evidenza sul segnale, export/confronto/memoria e consegna riproducibile. Restano invariati domanda, EPIC, controllo sui punti e sviluppo/test separati; dettagli metodologici non già validati vanno motivati, senza trattare il mandato come approvazione di qualsiasi nuovo protocollo.

**Verifica del passaggio.** SSH non interattivo riuscito con la chiave esistente e coda personale vuota; nessuna nuova chiave necessaria o credenziale salvata in memoria. Nessun nuovo job inviato. Consolidati i documenti di ingresso, con dettagli sperimentali nei resoconti; configurazione di accesso solo locale.

## 26. Esecuzione della chiusura autonoma — 11 novembre

**Scelta operativa entro il mandato.** Pipeline a stadi con manifest esplicito, hash di input/configurazione/codice e artefatti; DA e MoGE disponibili singolarmente o con pixel comuni. Memoria candidata FIFO (capacità configurabile, D2/spettro e riduzione minimo/media), interrogata prima e aggiornata dopo associazioni esterne. Nessuna selezione di distanza/capacità sulla base del test finale.

**Verifica prefissata.** Tre osservazioni per regressione del nuovo percorso: prima disponibile in P01_01 e P22_01, più il fallimento MoGE già noto P08_09. Non è ampliamento del campione scientifico; serve a verificare portabilità e conservazione dei fallimenti. GPU 755696, limite 15 minuti. Audit CPU 755697 dei cinque archivi originali per accertare campi e corrispondenze senza consultare distanze. Esiti successivi documentati sotto.

**Limiti.** I candidati implementati non costituiscono metodo tracking validato. La fonte ufficiale VISOR distingue ID di maschera, categoria e contesto temporale: non promuovere automaticamente UUID o nome a identità fisica persistente.

**Esito consolidato il 12 novembre.** Pipeline finale verificata con 755709 COMPLETED/0:0 (5m36s), dopo 755696 (5m37s). Audit 755697 fallito per assunzione di unicità del frame; 755699 concluso (2m14s), 200 record selezionati verificati nei cinque archivi. Nessun job attivo. Sei nuvole e cinque superfici nei tre casi prefissati; fallimento MoGE noto conservato. Undici test, export compatto, ripresa e hash verificati. Equivalenza numerica esatta al run storico non superata: differenze misurate e documentate, senza cambiare i risultati scientifici precedenti.

**Evidenza e conseguenza.** ID delle 632169 maschere unici nei cinque archivi; metadati temporali locali, nessun ID fisico globale nei campi osservati. Le 37 etichette visive restano invariate. Selezionate dai soli metadati nove coppie nello stesso intervallo/nome prima di leggerne le distanze: diagnostica locale separata, non nuove identità persistenti o negativi. Nessuna nuova inferenza scientifica aggiunta in assenza di etichette globali più forti. Costi e stabilità non sostengono superiorità sistematica SuperFlex. Consegna autonoma completata; DA/MoGE, punti e test separato invariati. Dettagli e limiti in `CONSEGNA_RAMO_GEOMETRICO.md`.

**Pubblicazione, 12 novembre.** Codice/risultati/memoria salvati localmente in `f697be8`. Il controllo automatico ha respinto il push richiedendo autorizzazione più esplicita sul contenuto/destinazione; Marco chiede prima il recap. Nessun push eseguito, nessuna approvazione presunta. Consegna locale disponibile e pubblicazione in attesa della decisione.

## 27. Rendere visibile la consegna su main — 12 novembre

**Direzione di Marco.** Portare gli upload sul ramo principale della repository comune, perché siano immediatamente visibili al collega e alla docente. Include la consegna autonoma locale già documentata, non soltanto il primo nucleo pubblicato.

**Motivazione e verifica preparatoria.** Il remoto `main` contiene solo i README iniziali; codice precedente su `prepare/superflex-core`, nuova consegna ancora locale. La storia selezionata discende da `main`, quindi può avanzarlo senza sovrascrivere modifiche del collega e senza importare la storia indipendente dell'archivio locale. Controlli di riservatezza e due grafici revisionati; dati/pesi/accessi personali esclusi.

**Esito verificato.** Pubblicazione riuscita: `main` avanzato da `78eefcc` a `7cb56da`, ramo di sviluppo allineato, riferimenti remoti coincidenti con la consegna. Nessuna forzatura o modifica alle cartelle del collega; storia indipendente del main locale esclusa. Controllo di riservatezza su 72 file e nuovi commit superato, due grafici revisionati visivamente; rapporto locale `shared_exports/publication_security_pre_main.json`. Il precedente rifiuto automatico del push è superato da questa pubblicazione. Nessun nuovo esperimento o cambiamento scientifico.

## 28. Opzioni per l’adattatore Whareformer — 12 novembre

**Richiesta di Marco.** Concentrarsi sull’adattatore e confrontare modalità di costruzione con pro e contro; nessuna variante ancora scelta o implementata in questa discussione.

**Verifica del codice originale disponibile.** `WhareformerMatcher.match` calcola logits, softmax e assegnazione greedy; `StandardTracker.update` aggiorna le track e ne crea di nuove dopo il matching. La memoria geometrica deve usare track_id effettivi, non posizioni temporanee nella lista, e azzerarsi fra video. Il contenuto del codice originale non certifica la versione effettiva del collega.

**Opzioni proposte.** (A) classi adattatrici separate, riusando input del modello e assegnazione originale, con memoria esterna; (B) punti di estensione espliciti nel matcher/tracker, mantenendo il percorso originale senza adattatore; (C) geometria incorporata in Detection/Track e nel loro ciclo di vita. Raccomandazione iniziale A per limitare interferenze col lavoro del collega; B preferibile se si concorda la modifica condivisa delle interfacce; C più invasiva, non necessaria per il primo confronto. Queste opzioni riguardano architettura software, non differenti metodi geometrici né nuovo training.

**Vincoli comuni.** Lookup esplicito delle osservazioni, controllo dell’ordine detection/track, forme mancanti senza correzione diretta, aggiornamento dopo associazione, gestione nuove track/reset; percorso a peso zero equivalente da verificare. Correzione dei logits prima della softmax ancora candidata; lasciare invariato il logit New Track non ne preserva la probabilità dopo normalizzazione. Prima modalità diagnostica senza influenza sulle associazioni, poi fusione configurabile e valutazione sulla baseline reale. Nessun nuovo job o push.

## 29. Preparare i dati per il collegamento ai track

**Richiesta riferita da Marco.** Il collega chiede RGB, maschere VISOR, nuvole, selezione e script per collegare le osservazioni a Whareformer e sperimentare l'accumulo.

**Esecuzione e motivazione.** Preparato archivio mirato locale di 73.1 MB, senza ridistribuire l'intero run geometrico: input originali, 299 maschere e 598 nuvole DA grezzo/MoGE, indice dei file per osservazione e checksum. Nuvole e maschere provengono dagli output, non dalla sola cartella `data/compare200/`. Verificati CRC, checksum di tutti i file e provenienza di RGB/maschere/nuvole. Percorsi e stato in `STATO_LAVORO.md`.

**Limite e conseguenza.** Nessun invio esterno eseguito, nessuna inferenza ripetuta. Il mapping alle detection/track resta aperto. L'accumulo è un'intenzione riferita del collega, non un metodo già verificato o adottato; occorre registrare nuvole camera-frame e gestire scala e movimento prima della fusione.

**Successiva richiesta di Marco.** Pubblicare il pacchetto su GitHub mantenendo ordine: destinazione `main`, cartella `SuperFlex/data_packages/compare200/`, README e checksum con collegamento nell’indice principale. Archivio invariato, contenuti interni verificati. **Esito:** caricamento su `main` riuscito, commit del pacchetto `ee652a2` e riferimento remoto verificato; cartella collegata dal README generale. Eccezione esplicita alla precedente esclusione generale dei dati da Git.

## 30. Analisi del nuovo ponte Whareformer–compare200 — 13 novembre

**Richiesta ed esecuzione.** Marco chiede cosa abbia caricato il collega e come cambi la roadmap. Letti tutti i sei file dei commit del 12 novembre `31e3943`/`ab5a946`, remoto main verificato a `ab5a946c1f94018edad90e69bc5544306f913569`; solo fetch, nessun merge/push. Due script collegano offline predizioni→ID osservazione→nuvole P01_01. Report del collega: 110590 righe sorgenti abbinate, 52 track, 71/73 geometrie su 18 track. Coerenza JSON/CSV, manifest del pacchetto e quattro controlli sintetici verificati; non riprodotta la run reale, mancando output completi e configurazione. Dettagli/evidenza in `ANALISI_AGGIORNAMENTO_GITHUB_20261113.md`.

**Valutazione e limite.** Avanzamento concreto del mapping, non integrazione nel matcher o beneficio tracking. Due track con categorie miste richiedono revisione; controllo visivo della track 9 riferito dal collega, non certificato qui. ID d'osservazione e track predetta non equivalgono a identità fisica persistente. L'accumulo proposto dal README richiede registrazione/scala/movimento e risponde a una domanda di ricostruzione distinta.

**Raccomandazione, non revisione scientifica adottata.** Prima manifest completi e baseline verificabile, diagnosi delle track e dei mancati join, poi memoria nel ciclo matcher/tracker, equivalenza a peso zero e confronto tracking con punti/SuperFlex, DA/MoGE e sviluppo/test separati. Accumulo eventualmente come pilota separato; sostituire la domanda approvata richiederebbe una scelta esplicita di Marco. Roadmap aggiornata nello stato delle dipendenze e nelle priorità proposte, senza fissare metodo, protocollo finale o nuove scadenze. Nessun nuovo job, training o controllo HPC.

## 31. Chiarimento del ciclo unitario e roadmap dopo rilettura — 13 novembre

**Direzione esplicita di Marco.** Il confronto SuperFlex→Whareformer e il percorso Whareformer→aggiornamento delle nuvole/SuperFlex sono due componenti dello stesso sistema: l'osservazione associata aggiorna la ricostruzione della track che alimenta i confronti futuri. Marco conferma la riformulazione e chiede la roadmap dopo rilettura dei paper. Superata la raccomandazione della voce 30 che trattava l'accumulo solo come ramo esterno. Domanda principale sul tracking e vincoli già approvati restano invariati.

**Esecuzione.** Rilette via fonti primarie le sezioni tecniche pertinenti di Whareformer e SuperFlex e confrontate con matcher/tracker, preprocessing/ottimizzazione e memoria locale. Piano in ROADMAP_CICLO_GEOMETRICO.md: contratto; sviluppo dei due collegamenti; ciclo causale; ablation e valutazione separata. La memoria FIFO esistente non implementa registrazione/fusione; i paper non forniscono direttamente il ciclo proposto.

**Raccomandazioni, non parametri adottati.** Adattatore a reti congelate, controllo a peso zero, accumulo conservativo di punti osservati in riferimento d'oggetto e nuova inferenza SuperFlex, memoria precedente comune per tutto il frame. Algoritmo/soglie/scala, distanza, capacità/frequenza e protocollo sperimentale restano da scegliere o calibrare. Confrontare aggiornamento e associazione separatamente prima di chiudere il ciclo. Nessuna implementazione, run HPC, training o pubblicazione eseguita in questa fase. Rilettura e roadmap non dimostrano beneficio o correttezza della registrazione.

## 32. Roadmap approvata e avvio dello step 1 — 13 novembre

**Approvazione di Marco.** «Questa è la nostra roadmap»; avviare lo step 1. La roadmap del ciclo unitario è ora il piano di sviluppo approvato. Valori numerici e dettagli ancora da calibrare non diventano risultati verificati.

**Esecuzione.** Remoto ricontrollato, ancora ab5a946; cercati output e input baseline nel workspace e nello spazio personale HPC cv_project, con limiti riportati in STEP1_CONTRATTO_TRACKING.md. I manifest completi non sono disponibili nei percorsi controllati. Nessuna affermazione sulla loro presenza sul computer del collega o altrove. Marco chiede cosa fare se non ancora condivisi: chiarito che occorre acquisirli per la verifica indipendente; nessuna richiesta inviata a terzi.

**Risultato e dipendenza.** Preparati riferimento P01_01 e controllo JSON riutilizzabile, sei casi sintetici superati. Controllo reale, revisione individuale delle track, diagnosi a monte dei due mancanti e riproduzione baseline restano pendenti. Pacchetto minimo e accessi necessari descritti nel resoconto; non servono nuove geometrie o training. Nessun job HPC avviato, coda non ricontrollata. Step 1 avviato, non completato.

## 33. Avanzare senza dipendere dagli output del collega — 13 novembre

**Mandato di Marco.** Cercare contributi e test immediati negli altri step; se realmente necessario, replicare autonomamente la pipeline sul minimo di frame/video utile. Non attendere gli output per attività che non li richiedono. Non modifica domanda, dataset o test finale.

**Scelta operativa ed esecuzione.** Avviato 2A con un adattatore NumPy separato, riusando memoria/forme e greedy locale originale. Sette test superati, inclusa equivalenza esatta a peso zero su 120 matrici controllate. Replay diagnostico su tre frame/cinque osservazioni P03_04, quattro rappresentazioni e 20 artefatti verificati: 12 transazioni riuscite, circa 3.72 secondi locali. Punteggi artificiali e associazioni visive esterne dichiarate: nessuna inferenza Whareformer, confronto IDF1 o equivalenza reale della baseline dimostrati. Dettagli in AVANZAMENTO_AUTONOMO_20261113.md.

**Conseguenza e limiti.** Step 1 resta aperto per la run del collega; non blocca più sviluppo/test dei componenti 2A/2B. Registrazione/accumulo controllati costituiscono il prossimo contributo autonomo; non ancora implementati. Replica indipendente minima possibile con checkpoint e feature/XYZ originali, non richiede output del collega; nuovi RGB da soli non sostituiscono gli asset mancanti. Nessun download di pesi, job HPC, training o pubblicazione in questa fase. I parametri di fusione del test sono fixture, non calibrazione scientifica.

## 34. Primo accumulatore e pilota di registrazione — 13 novembre

**Mandato ed esecuzione.** Marco approva di procedere con 2B autonomo. Implementati registrazione rigida con export della trasformazione, diagnostica e memoria limitata di punti osservati, rifiuto senza modificare lo stato valido. Sette test finali superati. Corretto un controllo confuso dalla densità dei riferimenti e dal cambio d'origine, conservando la prima versione; soglie reali non rilassate. Report RISULTATI_REGISTRAZIONE_ACCUMULO_20261113.md.

**Risultato verificato.** Pilota finale su tagliere/coltello e diagnostico temporale separato sulla bottiglia: nove osservazioni/18 nuvole DA/MoGE, tre identità visive storiche; 12/12 aggiornamenti fra viste reali rifiutati. Controlli su trasformazioni artificiali passano i gate, ma la posa del tagliere resta approssimata (errore noto circa 6–7% RMS), bottiglia circa 0.3–0.4%. Inizializzare la memoria non è una fusione riuscita. Ambiguità e differenze geometriche/estensione impediscono di dichiarare valido l'accumulo reale. Nessuna superiorità di sorgente o beneficio tracking.

**Conseguenza.** Nessuna nuova inferenza SuperFlex: manca un accumulo reale accettato, l'ancora sola ripeterebbe lavoro già disponibile. Prossima diagnosi su informazione indipendente di posa/corrispondenze RGB e scala esplicita; dettagli non ancora adottati come metodo. 2A resta disponibile con forme separate, 2B implementato come candidato ma non validato. Nessun job, controllo coda, download pesi, push o messaggio al collega.

## 35. Ricezione dei manifest e audit reale del mapping — 13 novembre

**Evento e verifica.** Marco segnala il nuovo upload. Fetch fino a bbf0e5e: arrivati tracks_by_id.json e compare200_joined_observations.json completi. Copie/hash preservati, controllo reale JSON passato: 52 track, 110590 righe, 33310 frame, 71/73 join esatti. Verificate 71 box/categorie contro VISOR e 146 nuvole con SHA-256; indici detection contigui ma 69/71 diversi da annotation_index. Non ancora verificato l'ordine delle feature sorgenti.

**Nuovi risultati.** I due mancanti esistono nelle track al nome VISOR di un indice prima, in esatta corrispondenza dei due mapping VISOR→RGB non identici. Mapping/record originali ricontrollati via lettura HPC mirata. Alias separati, non promossi a exact: manca la verifica del JPEG usato per feature/XYZ. Venti track con categorie miste nel completo; revisionate le tavole 4/36/9/35. Track 4 mostra tagliere e grattugia; track 9 ha anche container fuori dal sottoinsieme geometrico. Possibile frammentazione 9/35 solo evidenza visiva, non nuove identità GT. Dettagli in VERIFICA_CONSEGNA_WHAREFORMER_20261113.md.

**Conseguenza.** Superata la mancanza dei due manifest. Disponibili segmenti con associazioni reali per diagnostica; step 1 non completamente chiuso perché non caricati configurazione/versione/checkpoint verificabili, input/feature della run e metriche. Nessuna inferenza o job, coda non ricontrollata, nessun merge/push/messaggio. Persistono i limiti geometrici 2B; track_id non equivale a posa.

## 36. Asset originali, integrazione reale e blocco di accesso — 13–14 novembre

**Mandato ed esecuzione.** Proseguita l'integrazione autorizzata. Commit fc5aa30 acquisito senza merge/push; verificati configurazione, sorgenti e checkpoint corrispondente. Recuperati autonomamente i soli tre input ufficiali P01_01 tramite lettura in streaming dell'archivio; audit completo di ordine/metadati/XYZ su 110590 osservazioni, zero differenze. Superata la dipendenza dalla mancanza di feature/configurazione. Report e hash in INTEGRAZIONE_BASELINE_REALE_20261113.md.

**Risultati e limiti.** 761872 COMPLETED/0:0, 120 controlli a peso zero sul checkpoint reale con input controllati, non video. Preparato prefisso reale di 3398 frame/10264 detection con tracker originale e quattro adattatori causali. 761893 e 761895 falliti per import/serializzazione, corretti solo nel runner isolato. Ultima osservazione riuscita di 761899: RUNNING, 9m50s, almeno 3000 frame; esito finale ignoto. 761902 fallito per xmltodict, corretto; 761905 COMPLETED/0:0 in 20 s, valore IDF1 ancora da acquisire. CSV del collega verificato: mPCL 70.4655% secondo aggregatore originale, singolo video train. Nessun beneficio della forma dimostrato, nessun nuovo accumulo 2B accettato.

**Blocco osservato e conseguenza.** Il 14 novembre il nome HPC non risolve anche al DNS universitario e tramite resolver HTTPS esterno; hostname confermato dalle dispense. Marco riferisce solo Wi-Fi universitario, senza VPN Bocconi. Presenza di adattatori Norton non dimostra la causa. Nessuna modifica alla rete e nessun rilancio: provare VPN Bocconi, poi acquisire output/log e accounting dei job esistenti. Se persiste, verificare il servizio lato università. Non dedurre lo stato dei job dall'assenza di connessione, non dichiarare chiuso lo step 1 o passato il prefisso. Restano alias JPEG, esiti finali e validazione della registrazione.

## 37. Sviluppo prioritario senza HPC — 14 novembre

**Direzione esplicita di Marco.** Oggi HPC non disponibile: sviluppare il progetto rinviando gli esperimenti. Superata la priorità operativa della voce 36 di insistere sul ripristino dell’accesso; nessuna modifica alla domanda o al ciclo approvato.

**Piano operativo, non esecuzione.** Definita sequenza in PIANO_SVILUPPO_SENZA_HPC_20261114.md: integrare i candidati esistenti in un componente riutilizzabile, coordinare causalmente il frame, predisporre ricostruzione differita con provenienza/versioni, runner comune e controlli locali, pacchetto sperimentale. Nessun nuovo codice del ciclo o esperimento eseguito in questa fase.

**Limiti e conseguenza.** Esiti 761899/761905 da recuperare alla ripresa, 0/12 fusioni reali ammesse resta il risultato 2B. Controlli locali e sostituti di SuperFlex possono verificare il flusso software, non efficacia o validità della registrazione. Parametri, split e conclusioni non fissati automaticamente. Non importare risultati differiti retroattivamente nel replay causale.

## 38. Componente riutilizzabile del punto 1 — 14 novembre

**Mandato ed esecuzione.** Marco autorizza il punto 1. Implementati wrapper/configurazione attorno al matcher originale, con hook temporaneo prima della softmax: disabled/diagnostic/active, DA/MoGE e punti/SuperFlex. Riutilizzati adattatore e memoria esistenti; nessuna copia della rete o dell’assegnazione. Runner reale e preparatore aggiornati per i futuri bundle, archivi storici invariati.

**Evidenza e limite.** Passati 7 test adapter e 9 nuovi test wrapper; nei nuovi casi metodi originali match/greedy/validazione compilati dal sorgente con modello/tensor controllati NumPy. Diagnostica e peso zero preservano l’oggetto tensor nel percorso verificato; attivo cambia un’associazione controllata senza correggere direttamente New Track. Sintassi e JSON verificati; esiti/hash in outputs/reusable_integration_20261114/verification.json. Non è verifica Torch/checkpoint reale o beneficio tracking. Nessun peso scientifico calibrato, accesso HPC, training o push.

**Conseguenza.** Punto 1 software completato; punto 2 successivo per coordinamento causale/aggiornamento geometrico. Abort riguarda soltanto la geometria; non esiste ancora rollback del tracker. Limiti 2B ed esiti HPC pendenti invariati. Documentazione in INTEGRAZIONE_RIUTILIZZABILE_20261114.md.

## 39. Mappa del risultato atteso — 14 novembre

**Richiesta di Marco.** Rappresentare il flusso RGB → maschera 2D/nuvola 3D → SuperFlex → associazione Whareformer con posizione, maschera e forma → aggiornamento delle memorie. È una riformulazione del ciclo già approvato, non una nuova scelta di rete o registrazione.

**Esecuzione e precisazioni.** Preparata MAPPA_FLUSSO_SISTEMA.md. Esplicitati feature d'aspetto della regione mascherata, XYZ baseline, adattatore geometrico, associazione esistente/nuova track e aggiornamento della forma da punti osservati registrati, dopo tutte le associazioni del frame. Distinti stato precedente e memoria per i confronti successivi; rifiuti conservano l'ultima forma valida.

**Evidenza/limite e conseguenza.** Schema coerente con roadmap e contratto software locali; descrive l'architettura obiettivo, non un ciclo completo già verificato. Nessun segmentatore nuovo scelto, training, esperimento, accesso HPC o modifica del codice. Prossimo passo operativo invariato: coordinatore causale del punto 2; validazione della registrazione ancora aperta.

## 40. Coordinamento causale del frame — 14 novembre

**Mandato ed esecuzione.** Marco autorizza il coordinatore dopo il punto 1. Implementato FrameCoordinator e collegato al runner: valida il frame, lascia associare il tracker, estrae assegnazioni dagli incrementi di history, poi committa forme separate e valuta proposte geometriche opzionali. ID nuovi effettivi, versioni separate e copie dello stato; callback prima delle pubblicazioni delle proposte accettate. Nessuna identità GT nel metodo.

**Verifica e limite.** 27 test locali superati, 11 nuovi: metodi originali tracker/matcher con track/modello/tensor controllati. Verificati stato precedente comune, rifiuti/errori/mancanti, isolamento, frame vuoti e blocco dopo errore del nucleo. Quest’ultimo richiede ricostruzione/replay: non implementato rollback né checkpoint persistente. Aggiunto percorso esplicito per frame vuoti senza inferenza. Log/hash in outputs/frame_coordinator_20261114/. Nessun esperimento Torch/HPC, training o push.

**Conseguenza.** Coordinatore completato come software; runner attuale conserva forme separate, aggiornatore geometrico reale non ancora collegato. Prossimo collegamento del candidato registrazione/accumulo e poi SuperFlex differita. La proposta generica accettata non sostituisce automaticamente il descrittore del matcher. Validazione 2B (0/12 aggiornamenti reali ammessi) ed esiti HPC pendenti invariati. Dettagli in COORDINATORE_FRAME_20261114.md.

## 41. Supporto collaborativo per la mappa — 14 novembre

**Richiesta e revisione di Marco.** Trasferire la mappa su Miro, quindi preferire una slide in ChatGPT Space e verificare uno spazio di lavoro in stile Miro. Nessuna modifica al metodo scientifico.

**Esecuzione verificata e limite.** Miro aperto alla pagina di login, accesso non effettuato. Creata e collegata una presentazione privata vuota in Space, Page ID `page_f951f11ecfbc81a48983567d55429f5d`. Il servizio di modifica restituisce «requires MXC»; nessun editor esposto nel browser. Gli strumenti presenti creano slide e fogli, ma non nuove lavagne Canvas. Nessun diagramma inserito, nessuna condivisione configurata e nessuna lavagna creata.

**Conseguenza.** Consegna collaborativa incompleta; conservare il riferimento esistente per la ripresa senza duplicazioni. Mappa locale e priorità software invariate. Non presentare una slide collaborativa come lavagna libera equivalente a Miro.

## 42. Collegamento del candidato di accumulo — 14 novembre

**Mandato ed esecuzione.** Marco autorizza di proseguire dopo il coordinatore. Implementato aggiornamento puro osservazione associata→registratore/memoria esistenti, senza cambiare metodo o gate. Inizializzazione distinta da fusione; scope video/track/sorgente, convenzioni, punti osservati, versioni e provenienza controllati. Rifiuti/errori preservano la nuvola valida. Diagnostiche delle proposte registrate; corretto il commit per non pubblicare proposte con diagnostiche non copiabili.

**Evidenza e limite.** 35 controlli locali superati: 7 adapter, 9 wrapper, 12 coordinatore, 7 updater. Registratore effettivo su trasformazione nota e forma incompatibile sintetiche; altri casi con ammissioni controllate, nessun replay reale o Torch. Runner --accumulate e preparazione punti/hash predisposti e verificati sintatticamente, non eseguiti sul prefisso ufficiale. Default accumulo disattivato, gate/configurazione del precedente pilota invariati; scala tra viste esplicitamente non verificata. Log/hash in outputs/cloud_updater_20261114/.

**Conseguenza.** Collegamento software disponibile, non validazione dell’accumulo reale: 0/12 resta l’esito reale 2B. Matching continua con forme separate; prossima interfaccia SuperFlex differita per una versione accettata e pubblicazione causale della forma. Stato solo in memoria, non checkpoint persistente. Nessun job, accesso HPC, training, inferenza SuperFlex o push. Dettagli in COLLEGAMENTO_ACCUMULO_20261114.md.

## 43. SuperFlex differita e pubblicazione causale — 14 novembre

**Mandato ed esecuzione.** Marco autorizza di proseguire dal collegamento dell’accumulo. Implementati richieste firmate dal contenuto/provenienza/versione, input normalizzato e inversa, worker che riusa la pipeline SuperFlex esistente e importazione verificata. Coordinatore seriale: blocco prima del frame successivo, validazione di tutti gli esiti, pubblicazione delle forme pronte insieme. Memoria distinta per ultima ricostruzione valida; confronto futuro su questa, fallback precedente se assente e conservazione su fallimento. Completamenti esclusi dai punti osservati.

**Verifica e limiti.** 43 test locali passati, otto nuovi; metodi originali e componenti controllati, worker GPU simulato per verificarne il cablaggio. Nessuna vera inferenza SuperFlex/Torch o replay sul prefisso. Manifest/hash e binding di nuvola/versione/configurazione, rifiuto dei backend di test per default, cache ripercorribile, nuove forme senza effetti retroattivi. Log in outputs/deferred_superflex_20261114/. Runner/preparatore predisposti per --accumulate --reconstruct; nessun checkpoint completo, alla ripresa si ripercorre la storia usando cache esatta.

**Conseguenza.** Collegamento software del ciclo disponibile, efficacia ed equivalenza reale ancora da verificare. Parametri di preprocessing/pesi e pipeline esistenti riusati, nessun nuovo split o peso geometrico calibrato. Restano 0/12 aggiornamenti reali ammessi e recupero degli esiti HPC. Prossimi runner comune delle varianti/controllo punti e aggregazione delle misure. Nessun job, accesso HPC, training o push. Dettagli in SUPERFLEX_DIFFERITA_20261114.md.

## 44. Parere sulla proposta del collega — 14 novembre

**Richiesta e proposta riferita.** Marco chiede un giudizio su pulizia Open3D, FPFH/RANSAC/ICP, accumulo, SuperFlex pretrained e valutazione Chamfer. Non attribuita al collega alcuna esecuzione.

**Analisi e raccomandazione, non decisione adottata.** Baseline candidata plausibile; distinguere posa/scala, conservare rifiuti e provenienza e correggere la lettura della Chamfer su viste parziali. Raccomandato confronto diagnostico con il candidato attuale alla ripresa sperimentale. Il precedente 0/12 riguarda PCA/multistart + ICP, non FPFH. Evidenze e fonti in [PARERE_PROPOSTA_COLLEGA_20261114.md](PARERE_PROPOSTA_COLLEGA_20261114.md).

**Conseguenza e limite.** Nessuna sostituzione del registratore o adozione di un protocollo finale; priorità senza HPC e domanda primaria tracking invariate. Nessun nuovo esperimento, accesso HPC, inferenza o risultato.

## 45. Spiegazione delle alternative e dei compromessi — 14 novembre

**Richiesta di Marco.** Spiegare ciascun problema del parere precedente e le soluzioni sensate con pro/contro.

**Analisi, non adozione.** Approfonditi pulizia conservativa/componenti, FPFH/RGB/rifiuto, rigidità/similarità/non rigido, ammissione e budget, frequenza SuperFlex, metriche su viste parziali e controlli tracking. Precisati due limiti del controllo: pose equivalenti per simmetrie reali non implicano necessariamente fusione errata; una vista parziale non deve coprire tutta la memoria accumulata. Nessun nuovo gate fissato o spiegazione del precedente 0/12 dimostrata. Ragioni e compromessi in [PARERE_PROPOSTA_COLLEGA_20261114.md](PARERE_PROPOSTA_COLLEGA_20261114.md), approfondimento successivo.

**Conseguenza.** Raccomandato avanzamento diagnostico progressivo senza introdurre tutte le alternative insieme. Nessuna scelta decisiva, implementazione o nuova esecuzione; direzione approvata e priorità senza HPC invariate.

## 46. HPC ripristinato e job arretrati inviati — 14 novembre

**Mandato ed esecuzione.** Marco richiede controllo HPC e lancio degli arretrati se disponibile. Accesso riuscito, coda personale inizialmente vuota. Recuperati e verificati 761899 COMPLETED/0:0 (11m35s, prefisso reale storico a peso zero esatto e nessuna differenza dal collega) e 761905 COMPLETED/0:0 (20 s, IDF1 73.2697350574193% da predizioni registrate train, protocollo per nome). Non rilanciati i completati. Step 1 soddisfatto nel perimetro del prefisso, due alias JPEG fuori segmento ancora pendenti.

**Nuove esecuzioni.** Pacchetto v4 e controller isolato predisposti; hash trasferiti verificati. Controllo pesi ha fermato il percorso al checkpoint alternativo prima di sbatch; corretto verso robust/ già presente e con SHA atteso. 763321 COMPLETED/0:0, 50 regressioni ambiente passate in 30 s; 763322 replica aggiornata e 763323 accumulo RUNNING a 2m48s, almeno 1000/3398 frame ciascuno nell’ultima osservazione; 763324 GPU differito PENDING Dependency. Dipendenze afterok sui controlli e poi sui due CPU. Nessuna riscrittura di output precedenti o sostituzione del metodo/gate.

**Limiti e conseguenza.** Nuovi esperimenti non ancora conclusi: non dichiarare verifica del nuovo ciclo reale o fusioni accettate. Ramo GPU usa replay seriale/cache, richiede almeno un esito neurale reale pronto per validare l’inferenza, distingue inizializzazioni/fusioni e conserva errori. Peso geometrico zero, non confronto di efficacia. FPFH/calibrazioni non adottati non lanciati; nessun training, download pesi, push o messaggio. Prossima lettura dei tre esiti, percorsi e limiti in RIPRESA_HPC_20261114.md; risultati/ID/hash in outputs/hpc_ripresa_20261114/.

## 47. Perimetro contaminazione, frequenza SuperFlex e selezione empirica — 14 novembre

**Decisioni esplicite di Marco.** La contaminazione da associazioni riguarda tutte le componenti della track, non nasce da SuperFlex e non diventa un filone autonomo. Mantenere salvaguardie essenziali; la registrazione di viste dello stesso oggetto resta necessaria per fonderle. Approvata inferenza SuperFlex dopo ogni aggiornamento ammesso, non politica a intervalli; pubblicazione causale e punti osservati distinti dal completamento.

**Richiesta e raccomandazione.** Marco domanda se ML e confronto di tutte le opzioni possano scegliere il compromesso e chiede la strada più promettente. Raccomandata calibrazione automatica di una pipeline classica, confronto finito sullo sviluppo e reti congelate; RGB→3D/RANSAC/ICP prioritario se pixel/texture adeguati, FPFH come confronto, rigido/similarità limitata e pulizia conservativa. Esempio di 24 combinazioni geometriche, non protocollo approvato né costo misurato. Selezione finale su tracking, geometria diagnostica e test separato. Dettagli e limiti in [PARERE_PROPOSTA_COLLEGA_20261114.md](PARERE_PROPOSTA_COLLEGA_20261114.md).

**Conseguenza e limite.** Superata la discussione aperta sulla frequenza e ridimensionata la priorità della contaminazione generale. Nessun nuovo modello, variante, tuning o job eseguito; stato della ripresa HPC nella voce 46 non ricontrollato qui. Raccomandazione di probabilità di successo basata su metodo e casi disponibili, non superiorità sperimentale.

## 48. Approvazione della selezione e calibrazione autonome — 14 novembre

**Decisione esplicita di Marco.** Approvata ottimizzazione autonoma di parametri e scelta del metodo, con obiettivi di qualità distinti per fase, e approvata la proposta di confronto finito/in due passaggi della voce 47. L'approvazione supera lo stato di sola raccomandazione; non certifica esecuzioni o superiorità di una variante.

**Motivazione e metodo.** Scegliere dai dati il compromesso migliore in ogni fase e verificarne l'utilità nel tracking. Piano operativo e criteri centralizzati in [ROADMAP_CICLO_GEOMETRICO.md](ROADMAP_CICLO_GEOMETRICO.md): calibrazione geometrica, finaliste nel ciclo completo e test separato, reti congelate. Costi/semplicità secondari a qualità comparabile; non ottimizzare il solo residuo o tasso di ammissione. Confermati inferenza dopo ogni aggiornamento ammesso e nessun filone autonomo sulla contaminazione generale.

**Conseguenza e limite.** Aggiornati piano e memoria; parametri numerici, intervalli/budget e scelte vincenti da documentare durante il lavoro autorizzato. Nessuna nuova implementazione, calibrazione o run in questa fase; stati/esiti HPC precedenti preservati, non ricontrollati. Domanda, dataset e scadenza invariati.

## 49. Provenienza della posizione nel diagramma — 14 novembre

**Richiesta e verifica.** Marco chiede quali input generino la posizione 3D. Letti estrattore EPIC, dataset e funzioni originali locali: Depth Anything V2 Metric da RGB, allineamento con profondità della scena, mediana nella maschera e centro bounding box, retroproiezione con intrinseci e trasformazione tramite posa camera EPIC Fields.

**Conseguenza e limite.** Precisata MAPPA_FLUSSO_SISTEMA.md: maschera e metadati camera/scena sono ingressi anche del ramo posizione; le feature d'aspetto non ne sono la sorgente. Corregge la spiegazione precedente incompleta, senza cambiare metodo o input precalcolati. Nessuna rigenerazione, run HPC o nuova certificazione della provenienza di ogni XYZ; priorità correnti invariate.

## 50. Runner comune, misure e aggiornamento job CPU — 14 novembre

**Mandato ed esecuzione.** Marco approva sviluppo del runner delle varianti con struttura delle misure mentre i job lavorano. Implementate cinque modalità, DA/MoGE, tracker/modelli/memorie autonomi e configurazione condivisa del candidato di accumulo. Controllo sui soli punti accumulati pubblicato per i frame successivi con stessa politica dei descrittori esistente. Esempio a peso zero, non calibrazione scientifica. Frequenza SuperFlex dopo ogni aggiornamento ammesso rispettata; nessun ramo autonomo sulla contaminazione.

**Misure e verifica.** JSONL/JSON/CSV con esiti parziali/falliti, denominatori, costi annidati e ledger dei replay, payload distinto da RSS e dati GPU solo se misurati. IDF1/mPCL nulli finché non collegato il valutatore; niente predizioni usate come GT o media automatica dei video. 58 test locali passati, otto nuovi; componenti controllati/input sintetici. CLI e sintassi verificate, pacchetto locale di solo codice con hash, nessuna run reale del runner nuovo. Dettagli in RUNNER_VARIANTI_20261114.md.

**Risultati HPC distinti.** 763322 COMPLETED/0:0 (9m56s) e 763323 COMPLETED/0:0 (12m11s), controlli zero esatti e nessuna differenza dall’export. Nel secondo: 12 inizializzazioni e 12 rifiuti, zero fusioni; conteggio per quattro rappresentazioni, con due rappresentazioni per sorgente, non 12 prove indipendenti. 763324 RUNNING a 29m19s nell’ultima osservazione, worker reale con esito ready ma ciclo non ancora concluso. Controller CPU acquisiti in outputs/hpc_ripresa_20261114/; nessuna modifica ai job attivi.

**Conseguenza e limite.** Prossimi valutatore tracking, protocollo/copertura e calibrazione-test da approvare; diagnosi registrazione ancora aperta. Nessun beneficio tracking o validazione di fusioni reali dedotti dal codice o dalle inizializzazioni. Nessun nuovo job, training, tuning, push o messaggio. Ripresa sperimentale dettagliata in RIPRESA_HPC_20261114.md.

## 51. Significato delle inizializzazioni per oggetto/frame — 14 novembre

**Richiesta e verifica.** Marco chiede se le 12 inizializzazioni riguardino lo stesso oggetto. Acquisite le transazioni del 763323 e confrontate con le annotazioni/associazioni preparate: tre track (4 tagliere, 6 coltello, 9 padella) inizializzate rispettivamente a 2893/5099/7508, ciascuna nelle quattro rappresentazioni.

**Conseguenza e limite.** Sei osservazioni geometriche: tre tagliere, due coltello, una padella; tre osservazioni successive candidate alla fusione moltiplicate per quattro configurazioni, non 12 prove fisiche indipendenti. Padella senza seconda vista, non testata in fusione. Tutte le dodici proposte rifiutate. Categorie/track predette non costituiscono nuova identità GT; nessuna nuova inferenza o cambio di metodo. Audit in outputs/hpc_ripresa_20261114/initialization_breakdown.json, resoconto RIPRESA_HPC_20261114.md.

## 52. Proposta di annotazione della mappa — 14 novembre

**Richiesta di Marco.** Revisionare la mappa aggiornata e organizzare per ogni riquadro/collegamento stato, alternative valutate/da valutare, motivazioni e miglioramenti, preservando comprensibilità.

**Proposta ed esecuzione documentale.** Preparata PROPOSTA_ANNOTAZIONI_MAPPA_20261114.md: diagramma essenziale e schede collegate; nei blocchi funzione/stato/alternative/motivi/verifica futura/evidenze, nei collegamenti contenuto/temporalità/convenzioni/errori. Precisati RGB→aspetto, intrinseci nel ramo DA, profondità allineata, inizializzazione dai dati correnti e passaggio al frame successivo. Esempi sul candidato di accumulo e sul suo ingresso di punti, senza attribuire risultati a metodi solo proposti.

**Limite e conseguenza.** Formato ancora proposto, schede complete non compilate e lavagna esterna non modificata. Nessuna modifica scientifica, nuovo esperimento o controllo HPC; risultati/stati operativi riportati dai resoconti esistenti. Priorità di sviluppo/calibrazione invariate.

## 53. Audit dei criteri e delle cause di rifiuto — 14 novembre

**Richiesta e verifica.** Marco chiede perché i punti non siano stati aggiunti. Letto codice e diagnostiche effettive: supporto >=65% entro 0.08 scala RMS in entrambe le direzioni; q90 della frazione vicina 80% <=0.15; rifiuto di pose alternative quasi equivalenti entro 5% (+epsilon) ma distinte oltre 15 gradi o 0.08 di spostamento normalizzato. Soglie diagnostiche del prototipo, non regole dei due paper o calibrazione conclusa.

**Risultato e limite.** Sei allineamenti distinti per osservazione/sorgente, duplicati nelle rappresentazioni. Due casi tagliere 5099 rifiutati solo per ambiguità, non supporto/residui. Quattro al 7508 falliscono supporto/residui, tre anche ambiguità. Non prova di identità sbagliata o incompatibilità fisica: simmetrie/viste parziali da diagnosticare. Audit in outputs/hpc_ripresa_20261114/rejection_criteria_audit.json; dettagli in RIPRESA_HPC_20261114.md. Nessun cambio di metodo, soglie o nuovo esperimento.

## 54. Criteri di rifiuto dell’accumulo verificati — 14 novembre

**Richiesta ed evidenza.** Marco chiede perché le nuove nuvole non siano state aggiunte e secondo quali criteri. Letti codice e transazioni 763323: gate su supporto bidirezionale (65%, distanza 0.08R), residuo q90 troncato (0.15R), alternative di posa (circa 5% del fit, oltre 15 gradi o centro oltre 0.08R). Tagliere 5099 respinto solo per ambiguità, non per supporto/residuo; a 7508 supporto/residuo falliscono per tagliere e coltello in entrambe le sorgenti. Valori salvati in rejection_criteria_audit.json, resoconto RIPRESA_HPC_20261114.md.

**Interpretazione e limite.** Sono controlli provvisori del candidato, non prescrizioni Whareformer/SuperFlex né parametri calibrati. Supporto 99% corrente→riferimento contro 42.3% inverso (tagliere MoGE 7508) è compatibile anche con vista parziale; pose simmetriche possono rendere eccessivo il rifiuto per ambiguità. Non dimostrata la correttezza delle fusioni scartate o l’errore delle associazioni. Nessuna nuova inferenza o modifica di soglie/metodo; diagnosi indipendente pendente.

## 55. Avvio della mappa HTML interattiva — 14 novembre

**Richiesta di Marco.** Avviare una mappa HTML con elementi spostabili e informazioni di nodi/frecce in pannello verticale al passaggio del mouse, per collaborazione ed esposizione; proporre progressivamente i contenuti in chat. Chiarire fonti, modificabilità e struttura delle schede.

**Esecuzione.** Creati index.html, app.js, contenuti.js, copia iniziale contenuti.json e guida in mappa_interattiva/. Diciannove nodi, 34 collegamenti, pannello fissabile al clic, modifica locale, salvataggio browser ed export/import. Prime tre schede di nodo e prime tre di collegamento compilate come proposte da discutere; altre esplicitamente incomplete. Fonti: decisioni/stato/roadmap, report verificati e codice per dettaglio implementativo. Nessun contenuto sincronizzato automaticamente dai Markdown.

**Evidenza e limiti.** Sintassi controllata e apertura browser verificata; selezione scheda e spostamento da tastiera con persistenza osservati. Non è collaborazione simultanea né salvataggio diretto dei file dal browser. Nessun nuovo job, risultato scientifico o pubblicazione. Prossimo: revisione progressiva delle schede in chat; preferenza HTML supera la sola proposta documentale precedente quanto al supporto, non approva automaticamente i testi.

## 56. Revisione dei filtri di fusione da svolgere più avanti — 14 novembre

**Decisione esplicita di Marco.** Dopo il chiarimento che criteri/soglie di ammissione sono stati introdotti dall’assistente come diagnostica provvisoria, Marco dispone di rivederli ma non ora e chiede di segnalarlo nei to-do.

**Conseguenza.** Registrata attività pendente su ambiguità/simmetrie e supporto bidirezionale per viste parziali. Revisione esplicitamente rinviata: nessun cambiamento di soglie, codice o job e nessuna nuova esecuzione. Non interpretare i rifiuti come prova che le nuvole siano impossibili da fondere; resto del progetto invariato.

## 57. Revisione UX/UI della mappa — 14 novembre

**Richiesta:** pannello comprimibile, zoom e accessibilità di tutti gli elementi, verifica UX/UI prima della consegna. **Esecuzione:** pannello sinistro chiuso inizialmente, zoom 20–250% con ancoraggio al puntatore, pan dello sfondo, vista completa e 100%, ridisposizione orizzontale e stile rinnovato. Contenuti e import/export conservati. **Verifica:** sintassi JavaScript, osservazione visiva e interazioni browser su apertura/chiusura, zoom pulsanti/rotella, pan e ritorno alla vista completa; corretto tipo CSS del server di anteprima. Nessuna validazione su tutti i browser/dispositivi né nuovo esito scientifico. Layout salvati dal browser preservati; ripristino esplicito applica quello nuovo.

## 58. Salvataggio diretto delle descrizioni della mappa — 14 novembre

**Scelta esplicita di Marco:** servizio locale che salva nei file del progetto, sole descrizioni dei riquadri, Modifica e Salva con campi separati. Disposizione disordinata riconosciuta ma non prioritaria. **Esecuzione:** endpoint limitato ai campi descrittivi dei nodi, JSON canonico e copia JS derivata, backup, controllo revisione per nodo, lettura server autorevole rispetto alla cache browser; errore mantiene i testi nel modulo. Collegamenti/titoli/fonti esclusi. Avvio locale Windows senza finestra di servizio visibile. **Verifica:** prove su copia isolata di persistenza, Unicode, backup, conservazione titoli/frecce, conflitto 409, campi vietati, ID collegamento e origine esterna; browser modulo e conferma Salva con testo invariato. Non è sincronizzazione simultanea o modifica dei Markdown scientifici. Nessuna nuova run o scelta scientifica.

## 59. Valutazione originale e orchestrazione della pipeline — 14 novembre

**Mandato ed esecuzione.** Marco chiede di proseguire e chiarire cosa manchi alla pipeline completa, mantenendo rinviata la revisione dei filtri. Collegati export delle osservazioni indipendenti dall’ID predetto, hash dei JSONL, scope/fps/orizzonte espliciti, funzioni originali verificate per IDF1/mPCL e comando unico da input preparati a confronto. Metriche non inventate per run incomplete o prive di annotazioni. Distinta mPCL originale su 145 scale dalla diagnostica sulle sole scale supportate; prefisso non confrontato con video intero.

**Verifica e risultati.** 763498 COMPLETED/0:0 (33 s), otto casi reali di valutatore passati; 763530 COMPLETED/0:0 (45 s), 69 test tutti eseguiti senza skip e riproduzione di IDF1 73.2697350574193%, mPCL 70.46550449586454% su predizioni P01_01 train già registrate. Locale 69 casi, due motmetrics saltati e poi eseguiti su HPC. 763531 RUNNING a 10m50s nell’ultima osservazione: prima pipeline comune di nove configurazioni zero, dipendenza afterok sui test, solo CPU e copie delle sei ricostruzioni già pronte. Nessuna nuova inferenza GPU o calibrazione.

**Consolidamento e limiti.** Acquisito 763324 COMPLETED/0:0 (43m30s), sette replay, sei ricostruzioni pronte e zero esatto; ammissioni tutte inizializzazioni, zero fusioni. La struttura software non prova validità multivista o beneficio tracking. Registratore/updater invariati per hash; revisione dei filtri resta rinviata. Mancano frontend unico e copertura/validazione/calibrazione-test, senza introduzione di un segmentatore o identità GT indipendenti. Pacchetto locale v2 e dettaglio in COMPLETAMENTO_PIPELINE_20261114.md. Nessun push o messaggio a terzi.

## 60. Collegamenti modificabili e linguaggio accessibile della mappa — 14 novembre

**Richiesta di Marco:** estendere l’editor alle frecce, chiarire funzione/evidenze delle maschere, rinominare sezioni e usare linguaggio comprensibile a chi non ha lavorato al progetto. **Esecuzione:** endpoint frecce, revisione/backup e menu di selezione; titoli Possibili miglioramenti, Coerenza dei dati, Possible points of failure. Aggiornati soltanto role/evidence/contract di B02 tramite servizio; B01 e gli altri campi manuali confrontati e preservati. Descrizioni delle frecce reali non riscritte. **Verifica:** persistenza e backup su copia isolata, preservazione estremi/titolo/nodi, rifiuto conflitto; browser selezione, modulo e conferma Salva con testo invariato. Nessun nuovo esperimento; modifica dei collegamenti supera il precedente perimetro limitato ai riquadri. Conservare motivazioni documentate e distinguere stato da risultati.

## 61. Piano del frontend unificato in attesa di approvazione — 14 novembre

**Mandato esplicito.** Marco chiede di pianificare il prossimo step e di eseguirlo soltanto dopo il suo ok. Questa condizione prevale sull’autonomia precedente per l’avvio di questo specifico step; non cancella job già autorizzati o altre decisioni.

**Piano proposto, non esecuzione.** Dopo lettura degli estrattori/configurazioni originali e del nucleo portabile, definita sequenza in PIANO_FRONTEND_UNIFICATO_20261114.md: verifica asset/ambienti, contratto osservazioni, adattatore con riuso/rigenerazione, comando unico, verifiche e piccolo pilota. Distinti posizione baseline in scena e nuvole di forma, PCA preaddestrata e mapping VISOR/RGB. Tre frame noti con storia precedente del tracker mantenuta; niente ricostruzione estesa della scena implicita.

**Limiti e conseguenza.** Attesa dell’ok: nessun codice implementato, modello eseguito o nuovo job per questo piano. Rigenerazione/equivalenza dipendono da pesi, PCA e immagini compatibili; non dichiararle garantite prima delle verifiche. Revisione dei filtri resta rinviata, calibrazione/copertura estesa fuori dallo step. Aggiornati stato/to-do e riferimenti operativi; nessuna nuova conclusione scientifica.

## 62. Completamento segnaposto della mappa — 14 novembre

Completati i tre segnaposto di B01/B02 nella mappa: EPIC-KITCHENS, provenienza VISOR e modulo di segmentazione (SAM 2 come esempio da valutare, con inizializzazione esplicita). Resto dei campi preservato. Marco chiarisce che le parentesi quadre nei suoi testi sono richieste di completamento da parte dell’assistente. Nessuna adozione o implementazione di un segmentatore. Fonte primaria consultata: https://github.com/facebookresearch/sam2.

## 63. Approvazione frontend e primo percorso verificato — 14 novembre

**Approvazione ed esecuzione.** Marco risponde ok al piano. Implementati frontend_inputs.py, validazione contratto/cache e ingresso alternativo nel comando unico. Pilota di dieci detection P01_01 nei tre frame noti, storia di 3398 frame conservata e quattro file dati byte-identici. Provenienza nel nuovo bundle, originali preservati. 72 casi locali, 70 passati e due skip delle dipendenze motmetrics, non conteggiati come eseguiti.

**Limite reale.** Nei percorsi HPC controllati non individuati asset DINOv2/PCA/scala con identità sufficiente; PCA locale esiste ma legame alle feature ufficiali non certificato. Nessuna assenza globale affermata. Ramo rigenerato non implementato/verificato integralmente: resta pendente risolvere asset/ambiente e pilota, senza sostituire modelli o dichiarare parità dalla cache. Nessun filtro modificato, nuovo job, fit PCA o MVS implicito. Dettaglio e inventario in FRONTEND_AVANZAMENTO_20261114.md.

**Risultato precedente consolidato.** 763531 completato 0:0 in 23m24s, tutte le nove configurazioni zero completate/valutate ed esatte rispetto alla baseline. Copie acquisite in outputs/frontend_20261114/pipeline_763531/. Nessuna conclusione su beneficio tracking o fusioni reali; piano frontend approvato ma ancora parzialmente eseguito.

## 64. Verifica salvataggio revisione mappa — 14 novembre

Verificata persistenza della revisione manuale di B01/B02/B03 ed E01/E02/E03: JSON valido, copia JS offline e servizio identici; 12 backup, nessun temporaneo residuo. Browser con conferma Salva e nessun modulo aperto. Verifica del salvataggio, non approvazione scientifica; contenuti invariati.

## 65. Organizzazione e ripresa della mappa — 14 novembre

Mappa nella cartella dedicata mappa_interattiva/ della repository locale, con README.md canonico, inventario, avvio e istruzioni di ripresa in altra chat. LEGGIMI rimanda al README; backup esclusi da Git. Nessuno spostamento dei file applicativi, nessun commit/push. contenuti.json invariato per hash; preservare le schede manuali B01/B02/B03 ed E01/E02/E03.

## 66. Consegna del contesto a un altro provider AI — 14 novembre 2026

**Mandato e scelta.** Marco autorizza aggiornamento della cartella e di GitHub per riprendere con altro provider. Creato LEGGIMI_PASSAGGIO_AI.md come ingresso corrente, conservando memoria storica e revisioni manuali della mappa. Preparata pubblicazione selettiva su main a partire da fc5aa30, senza riscrittura della storia del collega.

**Evidenza e limite.** Guida collega codice, risultati acquisiti, dipendenze e prossimi passi. Frontend cache verificato ma rigenerazione ancora pendente; filtri esplicitamente rinviati; nessuna fusione multivista o beneficio tracking dimostrati. Non ripetuti esperimenti. Dati grandi, pesi e accessi esclusi: clone sufficiente per contesto/codice/evidenze leggere, non per inferenza senza asset esterni.

**Conseguenza.** Il prossimo provider legge la guida prima dei resoconti storici; prosegue il frontend già approvato e mantiene i vincoli. Esito pubblicazione registrato in docs/CONDIVISIONE.md; inventario delle copie pubblicate con hash. Nessuna nuova scelta scientifica.

## Vincoli organizzativi che spiegano il perimetro


Due persone, circa due ore al giorno ciascuna, consegna il 23 novembre. Ruoli confermati il 7 novembre: Marco segue geometria/SuperFlex; il collega Whareformer/integrazione/valutazione. Decisioni scientifiche e report condivisi. Modelli eseguiti sull'HPC; accesso autonomo operativo. Training da zero, reasoning semantico aggiuntivo e memoria complessa restano fuori scope iniziale per concentrare il lavoro sulla domanda misurabile.

## Regola di aggiornamento

Routine permanente richiesta da Marco il 9 novembre: aggiornamento autonomo, senza promemoria dell'utente, insieme a stato, to-do e altri file di memoria interessati. Applicarla alle novità rilevanti durante il lavoro e prima di chiudere una fase; istruzioni persistenti in `../AGENTS.md`.

Aggiungere o aggiornare una voce quando viene presa una decisione rilevante o un risultato ne cambia la motivazione. Riportare solo scelta, ragione, evidenza/limite e conseguenza; collegare i resoconti tecnici senza duplicarne i dettagli. Distinguere sempre proposta, decisione approvata, esecuzione e risultato. Non ricostruire a posteriori una scelta esplorativa come se fosse stata dimostrata o pianificata fin dall'inizio.
