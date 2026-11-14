# Runner comune e struttura delle misure — 14 novembre 2026

## Risultato software

Implementati `integration_prototype/experiment_runner.py`, `run_experiments.py`, `summarize_experiments.py` e configurazione di esempio. Ogni variante riceve un tracker originale nuovo; il runner rifiuta riuso del tracker o del modello fra varianti. Ordine, detection e input sono comuni, ma associazioni e memorie vengono prodotte autonomamente da ciascuna esecuzione. Nessuna etichetta oracle o track predetta usata come GT.

| Modalità | Influenza geometrica | Aggiornamento geometrico |
|---|---|---|
| W0 | Disattivata | Nessuno |
| G0 | Solo diagnostica, peso obbligatoriamente zero | Registrazione/accumulo dopo associazione |
| S-separata | Peso configurabile | Forme delle osservazioni conservate separatamente |
| S-accumulo | Peso configurabile | Stesso accumulatore, SuperFlex dopo ogni versione ammessa e pubblicazione futura |
| P-accumulo | Peso configurabile | Stesso accumulatore, descrittore dei soli punti osservati ammessi pubblicato per i frame successivi |

DA/MoGE supportati separatamente. Un'unica configurazione di registrazione/budget per il confronto; nessuna modifica dei gate. Il controllo P-accumulo è ora collegato al matcher: campiona 1024 punti dalla nuvola accettata, normalizza e calcola D2/spettro secondo la stessa politica del caricatore esistente. Le forme SuperFlex usano 1024 campioni di superficie: il confronto controlla l'input accumulato e il budget di descrizione, non rende uguale il costo di inferenza. L'evidenza distingue `accumulated_points/...` da `reconstruction/...`.

`variants_zero.example.json` contiene una baseline e quattro modalità per ciascuna sorgente: nove esecuzioni, tutte a **peso zero**, per verifica del collegamento. Valori preesistenti riusati; nessuna calibrazione, nuovo split o protocollo finale fissati. Pesi non nulli sono un parametro esplicito, non una scelta sperimentalmente approvata dal file di esempio.

## Misure ed export

- JSONL per frame/variante: associazioni effettive, disponibilità delle feature/nuvole, coppie confrontabili e relativi denominatori, aggiornamenti con diagnostiche, fallimenti, richieste SuperFlex e stato pubblicato.
- Riepilogo JSON: completato/in attesa/fallito, frame di errore, inizializzazioni distinte dalle fusioni, mancanti/rifiuti/errori, esiti dei worker. Una variante fallita non impedisce il resoconto delle altre.
- Tempi: setup, esecuzione corrente, coordinamento, registrazione/accumulo, descrittori dei punti, risoluzione differita e worker. Alcune fasi sono annidate, quindi non vanno sommate. Durata per variante fissata alla sua conclusione, senza includere l'attesa delle varianti successive.
- Registro append-only dei tentativi nella cache, separato per firma di input/provenienza/configurazione: conserva anche costi di setup e replay incompleti. Il collegamento dei tentativi richiede provenienza degli input e scope esatto dei frame; senza identificativo degli input ogni tentativo resta separato, senza cumulare costi di dati non confrontabili. Il costo forward delle ricostruzioni in cache è distinto dal costo appena sostenuto; mancanti rimangono nulli.
- Byte dei punti osservati e dei descrittori persistenti come indicatori di payload, non RSS complessiva/Python/GPU. Picco GPU allocato riportato solo quando misurato dal worker reale, con provenienza della cache.
- CSV/JSON di confronto senza media automatica tra video o scelta del metodo vincente. Provenienze diverse o risultati controllati vengono separati; report senza identificativo degli input non vengono raggruppati automaticamente.

IDF1 e mPCL rimangono **null/not_scored**, celle CSV vuote: il valutatore tracking dei nuovi export non è ancora collegato. Associazioni esatte rispetto alla baseline sono un controllo software a peso zero, non accuracy. Non confrontare ID numerici divergenti tra metodi come una misura di identità fisica. I due job CPU precedenti sono diagnostici con più copie del tracker e uno schema diverso: non vengono trasformati automaticamente in risultati delle cinque ablation o confrontati direttamente per costo.

## Uso e limiti

`run_experiments.py --root <bundle_verificato> --config variants_zero.example.json --output <nuovo_report> --cache <cache_dedicata>` verifica gli hash degli input, riusa il checkpoint Whareformer con copia CPU a tensori identici e crea i tracker originali. Il bundle corrente contiene descrittori D2: la CLI rifiuta spectrum, senza fabbricare valori sostitutivi. L'API accetta tuple complete reali per altre metriche già supportate.

Senza `--superflex-runtime <pipeline_config.json>`, i risultati differiti mancanti lasciano la variante in attesa e generano report parziale (exit 2). Con runtime esplicito, il worker usa la pipeline esistente; esecuzioni fallite o controllo zero non superato danno exit 1. Si ripete dalla prima osservazione con nuovi tracker e cache esatta; nessun checkpoint completo aggiunto. Cartelle di output esistenti non sovrascritte. Nessun costo di replay nascosto mediante sostituzione dei tentativi precedenti.

`summarize_experiments.py --reports <summary.json> ... --output <nuova_tabella>` esporta comparison.csv e groups.json, mantenendo denominatori, esiti incompleti e metriche non calcolate. Nessun tuning o selezione automatica.

Pacchetto locale di solo codice e configurazione: `shared_exports/common_runner_20261114_v1/`, con manifest degli hash. Nessun dato/peso/accesso personale o pubblicazione Git inclusi.

## Verifica effettiva e prossimo passo

**58 test locali superati**, otto nuovi: cinque modalità isolate con equivalenza zero e budget/nuvole comuni nei controlli; punti accumulati disponibili solo al frame successivo; mancanti/denominatori; varianti fallite; attesa/replay e costi; condivisione modelli vietata; provenienze separate; CSV senza metriche inventate; manifest del worker corrotto riportato senza nascondere gli altri risultati. Usati metodi originali con componenti controllati e input sintetici; non un esperimento di tracking reale.

Sintassi dei cinque Python interessati e help delle due CLI verificati. Log/hash in `outputs/common_runner_20261114/`. Un primo lancio della nuova suite ha preceduto la conclusione di un aggiornamento locale del file ed è fallito su un campo assente; le suite finali complete sul codice stabilizzato sono passate. Nessun esito di quel primo tentativo trattato come verifica riuscita.

Il runner comune non è ancora eseguito sul prefisso ufficiale o su GPU; nessun nuovo job inviato e snapshot dei job attivi invariati. Prossimo: collegare il valutatore originale ai nuovi export, definire copertura e protocollo di calibrazione/test senza scegliere sul test, quindi eseguire le varianti autorizzate. Diagnosi della registrazione resta aperta: i controlli software non dimostrano fusioni reali valide.
