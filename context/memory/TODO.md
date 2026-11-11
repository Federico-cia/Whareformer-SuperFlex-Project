# To-do corrente — integrazione SuperFlex in Whareformer

**Preparazione della condivisione e controllo riservatezza, 11 novembre:** Marco autorizza il caricamento del nucleo verificato e della memoria scientifica separata in `context/memory`, previo controllo di credenziali e informazioni personali. Copie dei documenti ripulite dai dettagli di accesso; originali conservati localmente. Ramo dedicato `prepare/superflex-core`, basato sul remoto, senza importare la cronologia dell’archivio locale. Corretto il solo metadato autore del commit non pubblicato: `cbd6ca1` sostituisce `eac7002`, contenuto del codice invariato. Push ancora da verificare; nessun nuovo esperimento o controllo HPC.

Aggiornato il 9 novembre 2026 dopo il riesame dei due codici e l'approvazione di Marco. Questo file prevale sulle sequenze operative precedenti. Scadenza: 23 novembre 2026; nessuna nuova data intermedia concordata.

## Obiettivo e perimetro

**Direzione aggiornata da Marco, 10 novembre:** mantenere DA e MoGE come alternative del ramo forma nei prossimi passi, fino a evidenza di convenienza chiara; non procedere automaticamente con DA. Confronti sulle stesse osservazioni, controllo sui punti e una sola interfaccia configurabile. Proseguire verifica delle identità e collegamento alla baseline; la scelta della sorgente non deve ritardare la preparazione dell'interfaccia. Valutare utilità, copertura/fallimenti e costo; nessuna soglia di scelta definitiva o nuova esecuzione fissata in questa discussione. Questa direzione prevale sulle raccomandazioni storiche di DA come ramo principale.

Verificare se le forme SuperFlex migliorano l'associazione delle identità di Whareformer. Collegamento tecnico, qualità del segnale e beneficio nel tracking sono tre verifiche distinte. SAM3 e la replica RGB completa degli autori sono opzionali, non prerequisiti; l'accesso ai pesi SAM3 non blocca il lavoro corrente.

Conservare le osservazioni e le maschere VISOR della baseline, i descrittori visivi e le posizioni XYZ. MoGE-2 è inizialmente un controllo diagnostico per il solo ramo forma, non una sostituzione delle posizioni del tracker. Nessun beneficio assunto; distanza, memoria e fusione restano da validare.

## Già completato — non ripetere

- [x] Dialogo di comprensione DA/MoGE/SuperFlex documentato per l'esposizione alla docente in `COMPRENSIONE_DA_MOGE_SUPERFLEX.md`: geometria per pixel, ruolo della maschera, camera fornita/stimata, propagazione degli errori e limite del confronto attuale. Nessun nuovo esperimento implicato.
- [x] Accesso SSH autonomo, trasferimenti e gestione job HPC operativi.
- [x] Installazione SuperFlex robust e inferenza sull'esempio degli autori, con controllo visivo.
- [x] Tre osservazioni pilota P01_01 con RGB, maschere, profondità, nuvole e primi output SuperFlex verificati.
- [x] Diagnostica orientamento/profondità/checkpoint, job 749200 e 84 casi: nessuna soluzione semplice dimostrata.
- [x] MoGE-2 + VISOR → robust, job 749539 e verifica 749582 completati; file e hash verificati, figure ispezionate. Nessun miglioramento visivo sistematico; MoGE non adottato come soluzione finale. Vedere `VERIFICA_MOGE2_749539.md`.
- [x] Sorgenti MoGE e SAM3 versionati e scaricati sull'HPC; manifest `manifests/rgb_sources.json`. Nessun nuovo ambiente o job RGB eseguito.

## Da fare, in ordine di dipendenza

**Priorità consolidate per la ripresa:** verificare prima la baseline e le corrispondenze reali su una sequenza di sviluppo; rafforzare in parallelo le identità entro categoria; poi validare distanza/memoria e un prototipo comune DA/MoGE, con controllo sui punti e recupero della baseline a contributo zero. Il test 750536 avvia la verifica del segnale ma non la chiude. Nessuna nuova inferenza geometrica necessaria prima della ricognizione degli asset; la conversazione informale non introduce compiti o cambi di metodo.

**Preparazione della collaborazione, 10 novembre:** prima dello scambio con il collega, repository documentata e codice inventariato; guida `docs/CODICE_PRODOTTO.md`, modalità `docs/CONDIVISIONE.md`, risultati selezionati in `results/`.
- [x] Distinguere codice nostro, dipendenze degli autori, diagnostici storici e integrazione ancora mancante; predisporre esclusioni e snapshot numerici con hash.
- [x] Primo commit locale e pacchetto di condivisione creati; cinque archivi con hash, codice documentato, risultati essenziali e geometrie complete separate. Percorso in `STATO_LAVORO.md`.
- [x] Collegato `origin` alla repository comune e recuperato `main`; accesso in lettura verificato. Nessun merge o push.
- [x] Revisione prima del caricamento: candidata essenziale di dieci file su `prepare/superflex-core`, separata dall'archivio storico; test, lint e regressione numerica superati. Dettagli `REVISIONE_CODICE_REPOSITORY.md`.
- [ ] Eventuale pubblicazione del solo ramo candidato nella struttura `SuperFlex/`; non importare in blocco lo storico locale. Inferenza neurale e runner di acquisizione da rendere portabili/verificare separatamente; dati pesanti fuori da Git.
- [ ] Acquisire nella struttura comune asset/configurazioni e stato effettivo della baseline del collega, evitando duplicazioni.
- [ ] Concordare export per osservazione secondo `docs/INPUT_SUPERFLEX_PER_WHAREFORMER.md` e verificare collegamento alle detection reali. La specifica chiarisce il ramo già eseguito; non certifica un'integrazione Whareformer completata.

**Ricognizione robotica completata, non nuovo piano adottato:** `RICOGNIZIONE_MEMORIA_GEOMETRICA_ROBOTICA.md`. Ordine operativo invariato; nessun controllo HPC indipendente durante questo approfondimento. Per lo stato operativo aggiornato vedere `STATO_LAVORO.md`.

- [x] Ricognizione critica con fonti primarie su memoria, ricostruzione, posa e scena; distinti RGB, RGB-D e geometria nota, utilità, fattibilità e novità.
- [ ] Solo se Marco sceglie l'estensione: fissare il test proposto sull'ingombro ricordato contro OBB/singola superquadrica/punti compressi, GT indipendente, posa e scala comuni, budget e criteri qualità–memoria–costo; poi due clip pilota. ADT è candidato, non nuovo dataset adottato. Non sostituisce automaticamente l'obiettivo approvato.

**Aggiornamento operativo, 10 novembre, verifica conclusiva:** esperimento **concluso e scaricato**, job 750536 COMPLETED/0:0 in 47m26s, 8797 coppie; nessun job attivo. Integrità e metriche verificate localmente. Risultati `RISULTATI_IDENTITA_DA_MOGE.md`: nessun vincitore generale; MoGE+SuperFlex migliore con D2 sui soli due piatti P22_01, punti semplici competitivi. Restano da rafforzare/ampliare le identità e collegare l'interfaccia baseline. Nessuna metrica/sorgente definitivamente adottata.

- [x] Precalcolo appaiato preparato, mapping delle 299 osservazioni verificato, tavole di revisione e primo campione visivo documentati; pilota di costo verificato.
- [x] Controllato 750536 concluso, scaricati risultati/log, verificati SHA-256, completezza/riuso, firme e AUC; analisi appaiata letta e documentata. Non rilanciare il precalcolo completo.
- [ ] Rafforzare le etichette del primo campione con continuità/annotazioni pertinenti e più negativi entro categoria; un solo video con due identità della stessa categoria non sostiene conclusioni generali.

**Verifica operativa della ripresa, 9 novembre:** HPC raggiungibile e nessun job attivo osservato; ambienti esistenti presenti. Proposta discussa: confronto DA/MoGE sullo stesso campione per il segnale d'identità, con DA candidato del prototipo. Per un eventuale job notturno privilegiare il riuso degli output disponibili e il precalcolo delle distanze contro geometria semplice; durata da misurare e identità fisiche ancora da verificare. Nessun job nuovo inviato e nessun cambio definitivo di sorgente o protocollo.

**Prossimo lavoro:** confronto 200 concluso e ispezionato, archivio interamente scaricato e verificato. DA grezzo candidato raccomandato per il primo prototipo (vantaggio di compatibilità 2D, non accuratezza 3D); scelta definitiva non ancora approvata. Seguire punti 1 e 3 per corrispondenze/identità, misurare stabilità/discriminatività anche contro geometria semplice; stato della baseline del collega da verificare. Resoconto `RISULTATI_CONFRONTO_200.md`. Nessun job in corso o inferenza da ripetere per questa fase.

**Avvio concreto della prossima chat:** esaminare prima gli asset e le annotazioni già locali per ricostruire la corrispondenza fra RGB, maschere e osservazioni Whareformer e identificare quali identità fisiche sono effettivamente verificabili. Non assumere che categoria o UUID per frame identifichino lo stesso oggetto nel tempo. Predisporre l'elenco delle osservazioni/coppie e documentare le ambiguità prima delle nuove inferenze. Il controllo MoGE con campo visivo noto resta un'opzione diagnostica discussa, non una nuova priorità approvata.

Insieme alla preparazione di questi controlli, discutere la definizione preliminare di osservazione, rappresentazione e memoria delle forme; fissarle prima del prototipo sulla base dei test. Candidati e limiti in `INTEGRAZIONE_DISCUSSIONE.md`, sezione osservazione/memoria; nessuna regola nuova già approvata.

**Proposta successiva di Marco da discutere, non attività già approvata:** fusione delle nuvole della track e della nuova osservazione dopo l'assegnazione, poi nuova inferenza SuperFlex. Prima accertare registrazione nel riferimento dell'oggetto e distinguere punti stimati dall'RGB da completamenti del modello. Raccomandato confronto separato con memoria senza fusione; dettagli in `INTEGRAZIONE_DISCUSSIONE.md`. Nessun nuovo job o cambio dell'ordine di lavoro.

**Discussione più recente da preservare:** ridondanza del 3D dall'RGB; opzioni descrittore invariante/registrazione/embedding appreso e controllo punti contro SuperFlex in `OPZIONI_FORMA_E_MEMORIA_ROBOTICA.md`. Ipotesi di Marco: memoria geometrica per robotica, anche distinta dall'aumento del tracking. Non è un nuovo obiettivo adottato né richiede ora training o nuovi modelli; primo lavoro operativo invariato.

- [x] Campione 200 fissato prima delle inferenze; confronto eseguito e verificato con fallimenti espliciti, metriche su 299 osservazioni, lettura delle 60 prefissate. GPU totali 26m48s; 890 mesh. Risultati in `RISULTATI_CONFRONTO_200.md`.

- [x] Confronto geometrico esteso appaiato concluso: 16 nuovi frame elaborati, 27 oggetti in 11 frame/11 categorie, 81 ricostruzioni, nessun fallimento, dieci tavole ispezionate. Job 749665/749728; dettagli e limiti in `CONFRONTO_GEOMETRIA_ESTESO.md`.

1. [ ] **Corrispondenza delle osservazioni — insieme.** Fissare chiave `(video, frame, detection_idx)` e corrispondenza con maschera, descrittore, XYZ e forma. Risolvere e documentare la discrepanza del mapping VISOR/RGB rispetto al loader. Non usare le identità annotate per decidere associazioni nel metodo.
2. [x] **Controllo MoGE-2 + VISOR → SuperFlex — Marco/persona B.** Eseguito sugli stessi tre RGB/maschere e stessi indici campionati, con XYZ Whareformer invariati. Metadati, log e figure conservati. Diagnostica conclusa: nessun miglioramento visivo sistematico; non misura tracking o stabilità d'identità. Resoconto `VERIFICA_MOGE2_749539.md`.
3. [ ] **Campione con identità verificate — insieme.** Preparare osservazioni ripetute della stessa istanza e di istanze diverse, anche simili, nei dati di sviluppo. I tre frame pan non hanno identità fisica comune verificata. Misurare copertura delle forme valide, variazione fra viste e separazione fra identità, includendo casi ambigui per aspetto/posizione. Non richiedere ricostruzioni perfette come condizione per preparare l'interfaccia.
4. [ ] **Confronto e memoria — insieme.** Validare una distanza fra superfici, con gestione dichiarata di scala/rotazione; non distanza sui vettori grezzi delle primitive. L'allineamento dell'output non corregge automaticamente la sensibilità del modello all'orientamento dell'input. Definire una memoria iniziale semplice e limitata, aggiornata dopo l'associazione con sole osservazioni passate; regola e capacità ancora da scegliere. Registrare forme mancanti e contaminazione da associazioni errate.
5. [ ] **Prototipo nel matcher — persona A.** Preparare caricamento della forma per osservazione e memoria per track. Primo candidato: reti congelate, correzione dei logits esistenti prima della softmax, confronto con New Track incluso nella normalizzazione. Recuperare esattamente la baseline con peso zero; forme assenti non devono bloccare il tracking e, in assenza di segnale di forma, usare la baseline. Conservare il matcher greedy originale. La fusione è un candidato da validare, non un metodo definitivo; concatenare una terza distanza nell'embedding richiederebbe adattamento del modello.
6. [ ] **Valutazione completa — persona A, analisi condivisa.** Confrontare Whareformer originale, Whareformer + SuperFlex e una geometria semplice ricavata dagli stessi punti. Stesse osservazioni/feature/XYZ/split/evaluator; calibrazione sullo sviluppo includendo peso zero e test separato. Memoria aggiornata dalle associazioni predette, senza identità oracle. Riportare IDF1, mPCL, fusioni errate, frammentazione, copertura, costo di estrazione/confronto/memoria e limiti. Un risultato negativo resta un esito valido.

## Lavoro che può procedere in parallelo

- Persona A: verificare gli asset effettivamente disponibili e rendere eseguibile la baseline Whareformer con evaluator ufficiale; preparare l'interfaccia del punto 5 e il controllo peso zero. Non presumere che il collega l'abbia già completato.
- Persona B: controllo del punto 2 concluso; contribuire al campione del punto 3, preparare forme e geometria semplice secondo la sorgente che verrà fissata per il confronto.
- Insieme: corrispondenze, campione, distanza/memoria e protocollo; mantenere aggiornati report ed evidenze.
- Aggiornare `REGISTRO_DECISIONI.md` a ogni scelta scientifica rilevante o revisione motivata dai risultati, con formulazioni concise e comprensibili.

## Opzionale e rinviato

- [ ] Replica completa SAM3 → MoGE-2 → SuperFlex, solo se utile dopo le verifiche principali. Richiede accesso ai pesi SAM3, ancora non ottenuto; non attenderlo per procedere con VISOR.

Esecuzioni dei modelli sull'HPC via SLURM, gestione autonoma dell'assistente già autorizzata. Per esecuzioni concluse e verifiche usare i resoconti collegati; il chiarimento concettuale non introduce nuovi job o risultati.
