# Registro delle decisioni e delle motivazioni

Aggiornato: 9 novembre 2026. Obiettivo: rendere ricostruibile il percorso scientifico per report e presentazione. Ricostruito dai documenti di progetto e dalla discussione corrente; non è una trascrizione completa delle conversazioni. Le date indicano le decisioni documentate, senza attribuire date precise dove mancano.

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

**Successiva richiesta di Marco.** Pubblicare il pacchetto su GitHub mantenendo ordine: destinazione `main`, cartella `SuperFlex/data_packages/compare200/`, README e checksum con collegamento nell’indice principale. Archivio invariato, contenuti interni verificati; caricamento da verificare. Eccezione esplicita alla precedente esclusione generale dei dati da Git.

## Vincoli organizzativi che spiegano il perimetro

Due persone, circa due ore al giorno ciascuna, consegna il 23 novembre. Ruoli confermati il 7 novembre: Marco segue geometria/SuperFlex; il collega Whareformer/integrazione/valutazione. Decisioni scientifiche e report condivisi. Modelli eseguiti sull'HPC; accesso autonomo operativo. Training da zero, reasoning semantico aggiuntivo e memoria complessa restano fuori scope iniziale per concentrare il lavoro sulla domanda misurabile.

## Regola di aggiornamento

Routine permanente richiesta da Marco il 9 novembre: aggiornamento autonomo, senza promemoria dell'utente, insieme a stato, to-do e altri file di memoria interessati. Applicarla alle novità rilevanti durante il lavoro e prima di chiudere una fase; istruzioni persistenti in `../AGENTS.md`.

Aggiungere o aggiornare una voce quando viene presa una decisione rilevante o un risultato ne cambia la motivazione. Riportare solo scelta, ragione, evidenza/limite e conseguenza; collegare i resoconti tecnici senza duplicarne i dettagli. Distinguere sempre proposta, decisione approvata, esecuzione e risultato. Non ricostruire a posteriori una scelta esplorativa come se fosse stata dimostrata o pianificata fin dall'inizio.
