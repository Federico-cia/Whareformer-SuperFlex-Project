# Integrazione Whareformer–SuperFlex: decisioni e proposta discussa

**Specifica tecnica di input, 11 novembre:** `docs/INPUT_SUPERFLEX_PER_WHAREFORMER.md` documenta input Nx3 della singola osservazione, formato NPZ compatibile, assi camera e preprocessing SuperFlex effettivamente usato. La posizione XYZ Whareformer non descrive la superficie: serve profondità per pixel e maschera, oppure mappa punti MoGE mascherata. XYZ/feature del tracker restano invariati; accoppiamento alle detection reali da verificare.

**Indicazione di Marco, 10 novembre:** mantenere DA e MoGE nei prossimi passi finché uno risulti chiaramente più conveniente. Superata l'ipotesi di procedere comunque con DA dopo il confronto. Proposta operativa: una sola interfaccia di caricamento/confronto/memoria con sorgente configurabile, XYZ/feature originali invariati e controllo sui punti. Non duplicare lo sviluppo del matcher o attendere un vincitore prima di preparare l'interfaccia. Il test d'identità ha avviato la verifica del segnale e delle distanze, senza chiudere la fase. Rafforzare il campione e il collegamento alle detection baseline; confronto successivo su utilità, copertura/fallimenti e costo, con protocollo e budget di calibrazione confrontabili. Nessuna distanza, memoria, soglia o sorgente definitiva adottata in questo chiarimento.

**Esito verificato, 10 novembre, prevale sullo stato operativo sotto:** job 750536 concluso in 47m26s, output e metriche controllati, nessun job attivo. Su due piatti P22_01, AUC D2 SuperFlex DA 0.627 contro MoGE 0.768; campione ristretto e visivamente etichettato, nessuna superiorità generale. Punti/descrittori semplici competitivi; nessun vantaggio SuperFlex sistematico o beneficio tracking dimostrato. Risultati `RISULTATI_IDENTITA_DA_MOGE.md`. Conservare entrambi i rami come confronto, estendere le identità e verificare l'interfaccia baseline prima di fissare sorgente, distanza e memoria.

**Approfondimento successivo sulla robotica:** `RICOGNIZIONE_MEMORIA_GEOMETRICA_ROBOTICA.md`. Utilità ipotetica per ingombro/compattezza anche a identità invariate, novità della sola composizione debole soprattutto rispetto a Hickory. Posa dell'oggetto e scala coerente tra forma e XYZ non sono fornite automaticamente dai modelli. Proposto test offline contro geometrie semplici, senza fusione iniziale e con GT indipendente. Nessun cambio dell'obiettivo approvato o nuovo esperimento eseguito.

**Aggiornamento operativo, 10 novembre:** confronto diagnostico DA/MoGE preparato su richiesta di Marco, con nuvole e superfici SuperFlex esistenti, descrittore D2/controllo spettrale/registrazione multi-inizio. 8797 coppie intra-video; job CPU 750536 attivo all'ultima verifica dopo preparazione e pilota conclusi. Primo campione visivo di 37 osservazioni/sette identità documentato, con limiti e soli due piatti come negativo entro categoria. Protocollo `ESPERIMENTO_IDENTITA_DA_MOGE.md`. Nessuna scelta definitiva di distanza, memoria o sorgente per il matcher; `detection_idx` e feature/XYZ baseline non ancora associati al manifest diagnostico.

Aggiornamento: 9 novembre 2026. Questo file registra l'ultima discussione; non descrive un'integrazione già implementata. Esecuzioni e risultati in `STATO_LAVORO.md` e `DIAGNOSI_SUPERFLEX_749200.md`.

## Direzione confermata da Marco

**Discussione più recente, ancora aperta:** ridondanza della geometria dall'RGB, opzioni di confronto e ruolo di SuperFlex rispetto ai punti; Marco propone inoltre una memoria geometrica per applicazioni robotiche. Pro/contro e distinzione fra obiettivo d'identità e obiettivo geometrico in `OPZIONI_FORMA_E_MEMORIA_ROBOTICA.md`. Nessun cambio definitivo di domanda/metodo o nuova implementazione approvata.
**Chiarimento del 9 novembre per la prossima sessione:** obiettivo invariato; sintesi del percorso di comprensione di Marco in `COMPRENSIONE_DA_MOGE_SUPERFLEX.md`. DA e MoGE costruiscono entrambi geometria per pixel dall'RGB completo, poi VISOR seleziona l'oggetto e SuperFlex riceve la nuvola. Nel confronto DA usa intrinseci forniti, MoGE li recupera dalla previsione: non è una misura isolata della qualità della profondità. Riprendere da corrispondenze e identità; nessun nuovo esperimento deciso nel dialogo.
**Ultimo esito:** confronto su 200 immagini approvato da Marco e concluso: 299 osservazioni, cinque video, 890 mesh. DA grezzo ha un vantaggio appaiato modesto di compatibilità 2D (IoU 0.4697 contro 0.4481 per MoGE, stessa direzione nei cinque video); non è accuratezza 3D o tracking. È il candidato raccomandato per il ramo forma, non una scelta definitiva approvata. XYZ e feature Whareformer invariati. Risultati in `RISULTATI_CONFRONTO_200.md`; seguono identità/corrispondenze, memoria e valutazione nel tracker.

**Ulteriore controllo richiesto da Marco, concluso:** confronto DA grezzo/allineato e MoGE su 16 nuovi frame disponibili; 27 osservazioni in 11 frame, 81 output controllati e tutti ispezionati. Qualità variabile per oggetto/vista, nessun vantaggio sistematico MoGE e nessuna sorgente finale adottata. Resoconto `CONFRONTO_GEOMETRIA_ESTESO.md`; segue verifica del segnale su identità fisiche annotate.

**Revisione successiva del 9 novembre, prevale sulla priorità di replica sotto:** dopo il riesame dei codici, Marco approva il to-do centrato sulla verifica dell'integrazione. Usare VISOR per le stesse osservazioni di Whareformer; SAM3 è opzionale e il suo accesso non blocca il lavoro. Prossimo controllo diagnostico MoGE-2 + VISOR → robust sugli input esistenti, mantenendo XYZ/feature della baseline. Poi osservazioni con identità verificate, stabilità/discriminatività delle forme, confronto/memoria e prototipo nel matcher; baseline/interfaccia preparabili in parallelo. Checklist autorevole in `TODO.md`. Le proposte di distanza, memoria e fusione restano da validare.

- Obiettivo finale: unire Whareformer e SuperFlex, confrontando la forma corrente con una memoria delle forme delle track. Entrambe devono essere stimate con SuperFlex.
- Prima riprodurre la pipeline RGB descritta dagli autori (SAM3 → MoGE → SuperFlex robust), poi cercare come integrarla in Whareformer. La replica RGB non è ancora stata eseguita. Le prove EPIC con VISOR/Depth Anything erano una combinazione con geometria Whareformer, non quella replica.
- La forma è informazione aggiuntiva rispetto ad aspetto e posizione; non modifica il descrittore dell'immagine. Nessun beneficio di tracking assunto.

## Proposta spiegata e compresa, ancora da validare e fissare

Per il primo prototipo è stata raccomandata una fusione dei punteggi prima della softmax, lasciando inizialmente congelata la rete Whareformer. Non è ancora una scelta metodologica definitiva o implementata.

Per osservazione n e track k:

`dS(n,k) = min_{S in memoria_forme(k)} D(forma_corrente, S)`

`z(n,k) = zW(n,k) + lambda * m(n,k) * (tau - dS(n,k))`

- zW è il logit originale Whareformer, che combina già aspetto e posizione.
- D è una distanza fra forme da scegliere e validare. Chamfer su superfici normalizzate/allineate è stata citata come possibilità, non fissata come soluzione. Non confrontare direttamente vettori grezzi delle primitive.
- m vale 0 quando mancano forme tecnicamente valide; altrimenti 1. Validità tecnica non certifica fedeltà geometrica.
- tau è la distanza neutra: sotto aumenta il punteggio, sopra lo diminuisce.
- lambda regola il contributo della forma al punteggio complessivo, non a quello dell'immagine.
- Il logit New Track resterebbe inizialmente originale; softmax ricalcolata su tutte le opzioni, quindi anche probabilità di nuova track e frammentazione possono cambiare.

Alternativa distinta: introdurre dS direttamente nell'embedding `g'([dA,dL,dS])`, modificando e adattando l'addestramento dell'associatore. Non confondere questa alternativa con la fusione esterna e non promettere che basti concatenare un terzo input al checkpoint originale.

Peso della forma: nessuna percentuale a priori rispetto a immagine/posizione. Fissare prima distanza, normalizzazione e memoria; valutare pochi pesi crescenti, includendo lambda=0, sui dati di sviluppo separati dal test. Calibrare anche tau e verificare la scala rispetto ai logits. Valutare IDF1, fusioni errate e frammentazione; congelare i parametri prima del test. Lambda=0 migliore è un esito possibile e non va escluso. Nessun valore, insieme di calibrazione o soglia è ancora stato fissato.

## Osservazione e memoria della forma — chiarimento del 9 novembre

Marco chiede quando definire la memoria e quale rappresentazione confrontare con il nuovo frame. La definizione preliminare va discussa ora per guidare i test di stabilità/discriminatività; distanza, capacità e aggiornamento si fissano prima del prototipo, sulla base dei controlli di sviluppo. Non attendere la fine delle prove geometriche per iniziare a progettare l'interfaccia.

L'unità è **l'osservazione di un oggetto**, identificata da video, frame e maschera/detection, non l'intera immagine. Da RGB e maschera otteniamo una nuvola parziale; SuperFlex predice una decomposizione in superquadriche. La forma memorizzabile è questa geometria predetta, conservabile come parametri e confrontabile tramite punti campionati sulle superfici. Anche la nuova osservazione deve passare per SuperFlex: il confronto geometrico è forma nuova contro forme passate.

Proposta da validare: una memoria piccola per ciascuna track, contenente una o poche ricostruzioni di osservazioni precedentemente associate. Conservare più forme può rappresentare variazioni di vista/completamento; può anche aumentare falsi abbinamenti. Il minimo delle distanze già proposto è un candidato, non una regola approvata. Non mediare direttamente parametri di primitive non corrispondenti. Capacità, ammissione/sostituzione e soglie restano aperte.

Prima del confronto occorre rendere compatibili riferimenti e convenzioni: distinguere forma da posizione globale e trattare esplicitamente rotazione e scala. Normalizzare la scala elimina anche informazione sulla dimensione; conservarla richiede unità sufficientemente affidabili. L'allineamento delle superfici non elimina automaticamente la sensibilità del predittore alla vista.

La memoria esistente viene letta prima dell'associazione; aspetto, posizione e forma contribuiscono alla decisione. Solo dopo l'assegnazione predetta si aggiorna la memoria della track, secondo una regola da validare. Una nuova track inizializza la propria memoria; forme mancanti usano il comportamento della baseline. Nessuna osservazione futura o identità ground truth per aggiornare la memoria nel tracking misurato. Un errore di associazione può contaminarla. Non è ancora una rappresentazione unica e certificata dell'oggetto reale.

## Proposta di Marco: fusione delle nuvole e ricostruzione della memoria — 9 novembre

**Proposta, non ancora adottata.** Per ogni osservazione, confrontare la decomposizione SuperFlex con le forme delle track; combinare il punteggio con aspetto e posizione, assegnare la track e solo dopo aggiornare la memoria. Aggiornamento proposto: unire la nuvola nuova alla nuvola conservata della track e applicare di nuovo SuperFlex per ottenere una decomposizione aggregata. L'output è un insieme di superquadriche, non necessariamente una primitiva unica. Marco chiede una valutazione critica su viste parziali e costo; non autorizza con questo una nuova esecuzione o un cambio definitivo del piano.

**Precisazione sulla baseline.** Whareformer confronta descrittori dell'aspetto estratti dall'RGB isolato con maschera e posizioni 3D; non confronta direttamente la sola sagoma delle maschere. Per un confronto con track esistenti resta necessaria anche l'opzione New Track; la forma non forza un'associazione.

**Valutazione scientifica.** Aggregare osservazioni complementari può migliorare la copertura, ma non è una semplice concatenazione: serve allineare le nuvole in un riferimento solidale all'oggetto e verificare scala, sovrapposizione e coerenza. Le pose della camera compensano il movimento della camera, non una padella spostata o ruotata dalla persona. Centratura/normalizzazione separate non risolvono questa registrazione. Con viste parziali, oggetti simmetrici e profondità monoculari incoerenti, l'allineamento può fallire. ICP è un possibile componente, non una soluzione garantita; richiede una inizializzazione adeguata e non è stato provato qui.

Conservare, se si prova la fusione, i punti ottenuti dall'RGB con la relativa provenienza: già stimati, ma distinti dalle superfici completate da SuperFlex. Ricampionare la vecchia decomposizione non recupera la nuvola originale e può trasformare completamenti errati in apparenti osservazioni ripetute. Anche le nuvole originali vanno bilanciate per evitare che viste ridondanti o più dense dominino la memoria. Una ricostruzione aggregata non è garantita monotonicamente migliore; una associazione errata può contaminarla e rinforzare errori successivi.

**Vista parziale.** Anche l'aspetto RGB è incompleto; la forma aggiunge però errori di profondità, camera e completamento, perciò non è automaticamente più robusta né indipendente dall'aspetto. Nelle osservazioni poco affidabili valutare un contributo geometrico neutro/ridotto e la possibilità di non aggiornare la memoria. Indicatori, soglie e capacità di rilevare qualità restano da validare; nessun controllo garantisce assenza di contaminazione.

**Costo.** Il nostro forward SuperFlex usa 4096 punti. La riapplicazione dopo la fusione è inferenza, non riaddestramento; ricampionare a dimensione fissa evita la crescita del suo input. Restano i costi di registrazione, filtraggio, confronto e archivio dei punti, da misurare separatamente. Se ogni osservazione assegnata produce anche un aggiornamento, serve circa un forward aggiuntivo per oggetto aggiornato: può raddoppiare la sola componente di inferenza SuperFlex, non necessariamente l'intera pipeline. La profondità si calcola una volta per frame e serve tutti gli oggetti; non occorre elaborare frame esclusi dal protocollo baseline. Nuove track possono inizializzare la memoria con la forma già calcolata. Aggiornamenti selettivi e memoria limitata sono possibilità da validare, non regole già fissate.

**Raccomandazione dell'assistente.** Mantenere un primo riferimento senza fusione, con memoria limitata di forme/nuvole di osservazioni selezionate, poi valutare la fusione come variante separata. Primo controllo della fusione su poche sequenze con identità fisiche verificate, senza usare tali identità nel matcher finale: accertare allineamento, stabilità e costo prima dell'integrazione completa. Confrontare forma singola, memoria senza fusione e memoria fusa a parità di dati; non assumere che l'ultima sia migliore. La raccomandazione non modifica ancora il to-do approvato né sostituisce i test d'identità.

Fonti verificate: [Whareformer, §3.2](https://arxiv.org/html/2607.08537); [SuperFlex](https://arxiv.org/html/2607.01015); [registrazione ICP](https://www.open3d.org/docs/latest/tutorial/pipelines/icp_registration.html), [registrazione globale](https://www.open3d.org/docs/release/tutorial/pipelines/global_registration.html). Codice effettivo: `scripts/superflex_batch_probe.py` e `Whareformer-repo/src/models/whareformer.py`.

## Rischi e organizzazione raccomandata

- La stessa identità può generare forme diverse per vista/occlusione; rotazione e diverso completamento sono problemi distinti. Una ricostruzione plausibile non garantisce stabilità o capacità di distinguere istanze simili.
- I tre frame pan finora usati non hanno identità fisica comune verificata. Servono identità annotate per i controlli temporali; non dedurle dal nome della categoria.
- Un'associazione errata può contaminare la memoria. Rappresentazione, distanza e aggiornamento restano aperti; mantenere il regime online, senza osservazioni future o trasformazioni canoniche ground truth indisponibili.
- Separare replica SAM3/MoGE e confronto finale a osservazioni/maschere/feature/XYZ comuni. È stata discussa la possibilità di conservare XYZ Whareformer e ricavare la sola forma da MoGE: da verificare, non ancora adottata.
- Per evitare di lasciare l'integrazione alla fine, l'assistente ha raccomandato che il collega prepari in parallelo interfaccia, memoria e baseline mentre Marco segue la replica. Prima esecuzione completa entro 14–15 novembre proposta come obiettivo interno, non scadenza concordata né previsione garantita. Consegna confermata: 23 novembre.

Aggiornamento operativo successivo: MoGE-2 + VISOR → robust completato (749539), controllato (749582) e ispezionato, senza miglioramento visivo sistematico. Resoconto `VERIFICA_MOGE2_749539.md`. Nessuna adozione di MoGE come geometria finale e nessun beneficio tracking dimostrato. Prossimo lavoro: corrispondenze e campione con identità verificate (`TODO.md`). Non ripetere prove concluse. Nella nuova chat leggere prima le revisioni correnti e `STATO_LAVORO.md`.
