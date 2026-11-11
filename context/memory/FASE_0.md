# Fase 0 — perimetro e verifica di fattibilità

Aggiornamento: **4 novembre 2026**. Stato: **domanda di ricerca ed EPIC-KITCHENS approvati da Marco**. Il dataset è la base comune di sviluppo e valutazione, con test finale separato. Metodo, protocollo dettagliato e campione pilota restano da definire. Nessun modello è stato eseguito e nessun miglioramento è stato misurato.

## 1. Perimetro già concordato

- Base: Whareformer; componente geometrico principale: SuperFlex, partendo dalla variante robust preaddestrata. SuperDec opzionale.
- Verificare prima qualità degli input 3D e informazione aggiuntiva della forma rispetto ad aspetto e posizione.
- Confronti con identiche osservazioni, maschere, feature visive e posizioni 3D. IDF1 prioritario, mPCL complementare.
- Gruppo di due studenti e scadenza del 23 novembre 2026 confermati da Marco il 4 novembre; circa due ore al giorno per persona. Nessun robot o dato privato garantito.
- Fuori scope iniziale: reasoning semantico aggiuntivo, training da zero di SuperFlex e memoria geometrica complessa.

## 2. Domanda approvata e alternative considerate

**Domanda approvata da Marco il 4 novembre 2026:** «A parità di immagini, maschere, descrittori visivi e posizioni 3D, aggiungere a Whareformer un confronto tra la forma stimata con SuperFlex per ciascuna osservazione e una memoria delle forme delle track, anch'esse stimate con SuperFlex, migliora l'associazione delle osservazioni alle identità degli oggetti nel tempo?»

Entrambi i lati del confronto geometrico derivano da SuperFlex. La forma corrente viene stimata da una nuvola di punti dell'oggetto, ricavata da immagine, maschera e profondità; non si introduce qui un nuovo detector. La regola con cui conservare o aggiornare le forme delle track resta aperta. Il confronto con una geometria semplice è un controllo sperimentale distinto dalla formulazione della domanda principale.

È una domanda sperimentale: il beneficio non è assunto e l'integrazione da sola non costituisce una novità metodologica.

| Opzione | Risultato cercato | Costo e limite |
|---|---|---|
| A. Confronto controllato nel tracking, raccomandata | Misurare se la forma aiuta l'identità e se serve SuperFlex | Replica, estrazione 3D e integrazione; dipende da entrambi i gate della roadmap |
| B. Diagnosi della forma fra viste | Capire quando la forma resta stabile e corregge ambiguità dell'aspetto | Meno integrazione; non dimostra un miglioramento del tracking. Possibile riduzione dello scope da concordare |
| C. Metodo nuovo di aggiornamento della memoria | Studiare selezione delle viste o gestione dell'incertezza | Richiede ulteriori ablation e sviluppo; prematuro prima dei gate |

**Ipotesi falsificabile H1:** la variante con SuperFlex migliora IDF1 rispetto alla baseline a parità di input e procedura di selezione. Se non emerge un miglioramento coerente, H1 non è sostenuta sul campione esaminato; ciò non dimostra inutilità universale della forma.

**Ipotesi H2, distinta:** il beneficio supera quello di una geometria semplice. Se le due varianti sono equivalenti entro l'incertezza misurabile, non possiamo attribuire un vantaggio specifico alla decomposizione SuperFlex.

Soglie pratiche, unità di aggregazione e misura dell'incertezza vanno concordate prima della valutazione finale. Il pilota diagnostico non basta a stabilire superiorità o generalizzazione.

## 3. Dataset approvato e pilota proposto

**EPIC-KITCHENS è approvato come base comune degli esperimenti**, con maschere VISOR e calibrazione EPIC-Fields per costruire gli input. Serve a eseguire la baseline, verificare la geometria e valutare la variante sugli stessi dati. La scelta del dataset non implica addestrare un nuovo modello: il bisogno di training del modulo di associazione dipenderà dall'integrazione scelta; non è previsto training da zero di SuperFlex. Motivo della scelta: continuità con il benchmark e disponibilità documentata degli ingredienti. Restano da verificare accesso effettivo ai file e qualità della profondità.

Per il pilota proponiamo inizialmente dati ammessi al training di Whareformer. L'approvazione del dataset non fissa automaticamente video, numerosità, split di validazione o procedura di selezione finale.

Proposta operativa limitata: **un video, 5–10 identità quando disponibili e circa 30–50 osservazioni annotate**, includendo ripetizioni da viste diverse, oggetti simili, occlusioni e casi sottili/riflettenti. Queste quantità delimitano il lavoro diagnostico, non rappresentano una numerosità statistica sufficiente. Non selezionare il campione in base ai risultati di SuperFlex.

**Aggiornamento del 7 novembre:** Marco ha scelto `P01_01` come video pilota comune perché compare nel train della configurazione locale ufficiale. La scelta del video è approvata; non abbiamo ancora verificato che offra tutti i casi richiesti. Frame, identità e formato di scambio vanno coordinati col collega e registrati prima degli esperimenti. Se la copertura è insufficiente, discutere un'estensione del pilota basata sui dati disponibili. Il pilota non è il test finale.

Alternative: IT3DEgo è supportato da Whareformer ma richiede una verifica dedicata degli input geometrici; ADT, usato da EgoTrack3D, permetterebbe un controllo con profondità più affidabile ma comporterebbe cambiare contesto e adattare la pipeline. Non li fissiamo ora come benchmark aggiuntivi.

Il test ufficiale resta separato dallo sviluppo. Il pilota non diventa test finale. La validazione andrà ricavata dai dati ammessi al training rispettando dipendenze per scena/partecipante; il checkpoint ufficiale potrebbe aver già visto quei dati, quindi quel sottoinsieme non dimostra generalizzazione fuori training. Per l'eventuale riaddestramento, usare un vero insieme di validazione e non scegliere checkpoint o pesi sul test.

## 4. Confronti da rendere eseguibili

| Sistema | Informazione aggiunta | Che cosa permette di verificare |
|---|---|---|
| W0: Whareformer ufficiale | Nessuna | Riproduzione della baseline con checkpoint ed evaluator degli autori |
| W1: Whareformer + geometria semplice | Estensioni/box stimati dalle stesse nuvole | Se è sufficiente una descrizione grossolana |
| W2: Whareformer + SuperFlex | Forma come insieme di primitive | Utilità della rappresentazione più ricca rispetto a W0 e W1 |
| Controllo di integrazione: contributo geometrico disattivato | Nessuna distanza di forma attiva | Assicurarsi che il percorso modificato recuperi la baseline |

Per W1 e W2 mantenere comparabili fusione, budget di calibrazione e regola di aggiornamento della memoria. Rappresentazione, allineamento e distanza restano aperti fino al gate 2. Non confrontare direttamente vettori grezzi di primitive: ordine e simmetrie possono cambiare fra osservazioni.

Misure previste: IDF1 e mPCL tramite evaluator ufficiale, copertura e fallimenti della geometria, costo di estrazione/inferenza/aggiornamento e memoria. Gli errori vanno analizzati anche nei casi difficili, dichiarando la loro numerosità. Se la geometria manca, conservare e contabilizzare l'osservazione con un fallback comune; eliminarla soltanto nelle varianti geometriche altererebbe il confronto.

## 5. Letteratura vicina e limite della rivendicazione

| Fonte primaria | Vicinanza e distinzione rispetto alla proposta |
|---|---|
| [Whareformer](https://arxiv.org/html/2607.08537), metodo ed esperimenti | Memoria di aspetto e posizione; baseline diretta. Non studia la nostra memoria esplicita della superficie |
| [SuperFlex](https://arxiv.org/html/2607.01015), §5.3 e appendice D | Primitive deformabili e input parziali; già mostra RGB → geometria. Quella pipeline non è una nostra novità |
| [EgoTrack3D](https://arxiv.org/html/2608.08016), §3–4 | Usa geometria più ricca nel tracking egocentrico. Non rivendicare come nuovo l'uso generico di forma/geometria nel tracking |
| [Hickory](https://arxiv.org/html/2606.01545), §5.3 | Usa superquadriche per associazione e allineamento di mappe. Non rivendicare come nuova una memoria basata genericamente su superquadriche |
| [OSNOM / LMK](https://arxiv.org/html/2404.05072v2) | Definisce il task; confronto con lo split e l'evaluator successivi da mantenere esplicito |

Le quattro fonti principali sono state ricontrollate via web il 4 novembre; la lettura precedente di OSNOM è documentata in `LETTURA_E_BASE_SCIENTIFICA.md`. La ricerca mirata ha inoltre individuato [Collaborative Learning ... Using Superquadrics](https://arxiv.org/html/2501.07100): esaminati abstract e impostazione introduttiva, non l'intero metodo. Riguarda ricostruzione mano-oggetto e riconoscimento di azioni, ed è un ulteriore precedente da approfondire se pertinente. Questa ricognizione non prova l'assenza di altri lavori concorrenti.

La rivendicazione sostenibile, se gli esperimenti riescono, sarà circoscritta al valore aggiunto misurato della forma nella specifica pipeline e alle condizioni in cui aiuta o fallisce. Rilevanza robotica motivata, nessuna validazione robotica dimostrata.

## 6. Accesso ai dati e risorse: evidenza effettiva

| Risorsa | Verifica del 4 novembre | Che cosa resta da fare |
|---|---|---|
| Codice Whareformer / SuperFlex | Copie locali leggibili, licenze MIT presenti; README pubblici consultabili | Le copie locali non hanno metadati Git; i commit citati nella base scientifica sono riferimenti documentati, non HEAD ricontrollati. Fissare versioni nella replica |
| Feature e checkpoint Whareformer | Link nei [README ufficiali](https://github.com/JacobChalk/Whareformer/blob/main/README.md) confermati; apertura di entrambi via web reindirizza a login Microsoft | Verificare download nella sessione dell'utente; non dedurre indisponibilità generale o accesso già riuscito |
| SuperFlex robust | Link dal [README ufficiale](https://github.com/GabrielTavernini/superflex/blob/main/README.md) raggiunge una cartella Drive, senza inventario leggibile nello strumento | Scaricare e verificare checkpoint/configurazione; nessun forward eseguito |
| VISOR | [Scheda Bristol](https://data.bris.ac.uk/data/dataset/2v6cgv1x04ol22qp9rm9x2j6a7) raggiungibile; sito ufficiale documenta maschere | Verificare contenuti del video scelto, condizioni d'uso, mapping dei frame e dimensioni prima del download |
| RGB / pose / intrinseci | Elencati nel README Whareformer e nelle pagine ufficiali [VISOR](https://epic-kitchens.github.io/VISOR/) / [EPIC-Fields](https://epic-kitchens.github.io/epic-fields/) | Scaricare un sottoinsieme coerente; verificare calibrazione e condizioni delle singole risorse |
| Profondità per pixel | Nel codice EPIC locale viene stimata e allineata, ma vengono salvate posizioni per oggetto, non mappe dense | Esportare la profondità allineata per i frame pilota; controllare ridimensionamenti, intrinseci e scala |
| Computer locale | Windows, Git 2.53; circa 62 GiB liberi sul disco C al controllo. Successivamente individuato Python 3.11.9 funzionante in `AppData/Local/Python/pythoncore-3.11-64`, senza NumPy, PyYAML e PyTorch | GPU non verificata: `nvidia-smi` non trovato e interrogazione hardware negata. Il comando Python predefinito punta a un alias WindowsApps non avviabile; usare il percorso esplicito. Dipendenze Whareformer non installate |
| GPU Bocconi | Accesso già operativo confermato da Marco. Specifiche universitarie riportate da lui: due Dell PowerEdge R750XA, ciascuno con due Xeon 5317 da 12 core, 512 GB RAM e quattro A100 da 80 GB | Specifiche ricevute dall'utente, non ricontrollate indipendentemente. Verificare GPU effettivamente assegnata, quote, durata massima dei job, spazio, code e trasferimento dati; nessuna esecuzione HPC effettuata in questa chat |

Non è necessario scaricare ShapeNet completo per il primo esempio SuperFlex. Il README indica 73,4 GB per quel dataset, più dello spazio libero locale rilevato; partire dagli esempi forniti dagli autori. Licenze del codice, dati e checkpoint vanno trattate separatamente: la licenza MIT del codice non dimostra le condizioni d'uso di tutti gli asset.

**Discrepanza nei nomi dei file:** `ARCHITECTURE.md` descrive `observations.json`, mentre `BaseFeatureExtractor.save_results()` nella copia locale scrive `object_annotations.json`. Prima della replica verificare ciò che richiedono loader ed evaluator alla versione scelta.

## 7. Chiusura della fase 0

Preparato: domanda approvata, alternative considerate, ipotesi falsificabili, pilota proposto, tabella dei confronti, fonti vicine e registro degli accessi. Repository locale inizializzato nella cartella `lavoro di gruppo`; Marco creerà quello condiviso. Confermati due componenti, scadenza del 23 novembre e accesso alle GPU Bocconi. Marco ha approvato EPIC-KITCHENS come base comune per sviluppo e valutazione, mantenendo separato il test finale.

Da confermare con Marco:

1. Eventuale autorizzazione al gruppo di due, dato che il syllabus ne prevede tre. Il numero effettivo è già confermato e non va richiesto nuovamente.
2. Dettagli della consegna: report, durata presentazione, poster e approvazione del tema. La scadenza del 23 novembre è confermata; 24 novembre e 1 dicembre sono ancora provvisori nei materiali.
3. Limiti operativi HPC e URL del repository condiviso, dopo la creazione da parte di Marco. L'accesso GPU è già confermato.
4. Dettaglio del campione pilota e del protocollo. Domanda e scelta di EPIC-KITCHENS sono già approvate e non vanno richieste nuovamente.

La fase 0 resta aperta finché questi punti non sono risolti. Le prime verifiche tecniche successive sono accesso a un checkpoint/feature Whareformer, un esempio SuperFlex robust e disponibilità congiunta degli input di un video pilota. Una risorsa annunciata non equivale a una pipeline funzionante.

Preparazione della replica avviata: vedere `PRIMA_ESECUZIONE.md`. La pagina HPC ufficiale consultata successivamente indica istanze MIG per gli studenti: gli 80 GB della scheda fisica non sono una quota per job verificata. Download del checkout ufficiale non riuscito; modalità di accesso HPC richiesta a Marco. Verificati sintassi e comando di aiuto dello script di preparazione, non i controlli su asset reali o l'inferenza.
