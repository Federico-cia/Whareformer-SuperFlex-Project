# Accumulo → SuperFlex differita → memoria futura — 14 novembre 2026

**Scelta successiva esplicita di Marco:** inferenza dopo ogni aggiornamento geometrico ammesso, mantenendo inizializzazione valida, conservazione su fallimento e pubblicazione causale. Politiche a intervalli non adottate. È una decisione di frequenza, non un nuovo risultato di inferenza; esiti HPC seguono il resoconto separato.

## Collegamento realizzato

`integration_prototype/deferred_superflex.py` prepara richieste da una versione accettata di `CloudState`, riusa la pipeline neurale esistente per il worker e verifica i risultati prima della pubblicazione. Non è una nuova rete o un training. Configurazione di default: checkpoint/config SHA-256 già dichiarati nel nucleo portabile, seed 42; campionamento e normalizzazione tramite `prepare_superflex_input` esistente (4096 punti). Inversa conservata: centro, scala e indici del campione. La normalizzazione non canonicalizza la posa.

Ogni richiesta è identificata dal contenuto: video, ID track, sorgente DA/MoGE, frame, versione/hash della nuvola, provenienza, configurazione SuperFlex e hash dei quattro moduli portabili coinvolti. `input.npz` conserva punti osservati nel riferimento d'oggetto, input normalizzato e inversa; `request.json` lega il file al suo SHA-256. Le richieste possono essere riusate nel replay solo se il contenuto coincide esattamente. Directory parziali/corrotte non vengono sovrascritte automaticamente.

Il worker di produzione richiama `shape_tools.pipeline.superflex`: controllo dei pesi/config, CUDA assegnata, inferenza congelata, denormalizzazione e mesh/primitive con soglia degli autori. Le feature per il confronto sono estratte con `comparison.load_features` esistente (1024 campioni della superficie normalizzati, D2 e spettro). `result.json` lega l'esito alla richiesta e all'hash dell'artefatto; conserva anche provenienza del backend reale. Il caricatore verifica scope/versione/configurazione, input e normalizzazione, hash e coerenza dei descrittori. I risultati dei sostituti di test sono marcati e rifiutati per default.

## Causalità e gestione dei fallimenti

`FrameCoordinator` accetta un `reconstructor` opzionale solo per rappresentazioni SuperFlex abilitate con accumulatore. Dopo tutte le associazioni/aggiornamenti del frame prepara le richieste per le sole nuvole ammesse, inclusa l'inizializzazione. Finché mancano gli esiti non elabora frame successivi. `resolve_reconstructions()` valida tutti gli esiti prima di pubblicare insieme le forme pronte. Esito esplicitamente fallito: conserva la forma precedente e permette di proseguire; risultato mancante/corrotto: resta bloccato. Non inserisce tardivamente nuove forme in una storia già processata.

L'adattatore mantiene separata una memoria di ricostruzioni di capacità uno per track. Una ricostruzione valida sostituisce le distanze basate sulle forme separate per quella track; in sua assenza resta il controllo precedente. Se il risultato successivo fallisce, conserva l'ultima ricostruzione valida, anche se la nuvola ha una versione più recente. Per detection senza forma il contributo diretto resta assente. New Track non è corretto direttamente; peso zero continua a preservare i logits originali. Le versioni geometriche e gli identificativi delle ricostruzioni restano distinti e registrabili.

La pubblicazione avviene dopo il frame che ha generato la nuvola, per confronti strettamente successivi. I punti della ricostruzione predetta non entrano mai nella memoria dei punti osservati. Il fallimento di una nuova inferenza non annulla un accumulo già accettato. Rimane il blocco del coordinatore dopo errori del nucleo tracker; nessun rollback/checkpoint completo aggiunto.

## Uso predisposto

- API: `FrameCoordinator(tracker, ObservedCloudUpdater(), DeferredSuperflex(cache_dir))`; `step(...)`, poi `resolve_reconstructions()` prima del prossimo frame se ci sono richieste pendenti. Un nuovo tracker/coordinatore per variante/video.
- Worker su ambiente SuperFlex esistente: `python deferred_superflex.py --request <directory_richiesta> --config <pipeline_config.json>`. Percorsi pesi/config relativi risolti rispetto al JSON. Un solo worker per richiesta; eventuale risultato già presente non viene sovrascritto.
- Runner diagnostico: `run_real_prefix.py --root <nuovo_bundle> --accumulate --reconstruct`. Se gli esiti non sono disponibili stampa gli ID/cache e si ferma prima dei frame successivi. Dopo il worker si ripete il prefisso dall'inizio usando la cache esatta. Questo è replay, non ripresa da checkpoint. Restano peso zero e assert di equivalenza.
- Il preparatore include i moduli necessari nel bundle futuro. Preparatore e runner aggiornati e controllati sintatticamente, non eseguiti sul prefisso ufficiale in questa fase. Bundle storici invariati.

## Verifiche e limiti effettivi

**43 controlli locali passati**, inclusi otto nuovi: export/inversa e pausa; evidenza della nuova forma soltanto nel frame successivo; fallimento che conserva forma e nuvola; rifiuto dei backend di test per default; manomissioni e richiesta non corrispondente; versione obsoleta/cache esatta nel replay; richieste multiple pubblicate insieme; assenza di richieste per aggiornamenti rifiutati e nessun punto predetto reinserito nell'accumulo. Verificato anche il cablaggio del worker di produzione con pipeline GPU e caricamento mesh simulati, non con una vera inferenza.

Log/hash in `outputs/deferred_superflex_20261114/`. Help del worker e sintassi dei sei Python interessati controllati. Nessuna inferenza SuperFlex, run tracking, accesso HPC, training o push effettuati. I risultati artificiali non sono prestazioni della rete né nuove geometrie reali. Restano 0/12 aggiornamenti reali ammessi nel pilota di registrazione, esiti HPC preesistenti da acquisire e calibrazione/test separato ancora necessari.

Il percorso del ciclo è collegato a livello software; non è certificata l'efficacia su EPIC o l'equivalenza del nuovo runner con Torch. Prossima fase senza HPC: organizzare runner/configurazioni comuni per baseline, forme separate e accumulo, completare il controllo comparabile sui punti e l'aggregazione di metriche/costi/copertura/fallimenti. Non fissati automaticamente nuovi split, pesi o conclusioni scientifiche.
