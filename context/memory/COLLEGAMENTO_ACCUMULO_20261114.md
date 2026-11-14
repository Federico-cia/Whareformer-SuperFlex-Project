# Collegamento associazione → registrazione/accumulo — 14 novembre 2026

## Risultato software

Implementato `integration_prototype/cloud_updater.py`: l'aggiornatore puro `ObservedCloudUpdater` collega l'interfaccia del coordinatore ai candidati esistenti `register_rigid` e `ObservedCloudMemory`, invariati. La prima osservazione inizializza il riferimento; le successive propongono una trasformazione rigida verso la nuvola precedente e sono accumulate solo se ammesse dai gate esistenti. Inizializzazione non equivale a fusione riuscita.

L'aggiornatore lavora su una copia della memoria. Se una proposta viene rifiutata o genera errore, il coordinatore conserva l'ultima nuvola valida e non modifica l'associazione già decisa. Il numero di versione avanza solo su ammissione. Ancora iniziale conservata, altre viste FIFO, quote di punti per vista e budget sull'input riusano il comportamento del candidato; configurazione di default coincide con il pilota di accumulo precedente (quattro viste, 2048 punti/vista, massimo 12000 punti d'input). Gate e metodo non ricalibrati.

DA e MoGE restano separati; `ObservedCloudInput` richiede sorgente, dichiarazione esplicita di soli punti osservati, convenzione di coordinate/scala e provenienza. Il riferimento precedente deve corrispondere a video/track/sorgente, configurazione, versione e convenzioni. Input non compatibili sono errori registrati, non fusioni. Le dichiarazioni non dimostrano posa, scala fisica o correttezza dell'identità predetta. Nessun adattamento automatico della scala; simmetrie e manipolazioni restano problemi aperti.

`CloudState` conserva memoria dei punti e trasformazioni/provenienza; `summary()` restituisce metadati e hash della nuvola senza esporre gli array interni. Lo stato completo resta un oggetto in memoria, non un checkpoint persistente. Il caricatore NPZ verifica SHA-256 e legge solo `camera_points`, con pickle disabilitato; deve essere il chiamante a certificare che l'artefatto provenga dalla profondità osservata mascherata e non dal completamento. Hash numerico canonico float64 little-endian distinto dall'hash del file.

Il coordinatore registra anche diagnostiche delle proposte rifiutate (supporto, residui, ambiguità e trasformazione candidata). Corretto l'ordine della pubblicazione: una proposta non viene accettata se le sue diagnostiche non possono essere copiate in sicurezza; test specifico aggiunto.

## Runner e preparazione successiva

`prepare_real_prefix.py` è predisposto a esportare anche `observed_clouds.npz`, riferimenti per detection/sorgente, hash degli artefatti e convenzioni; usa gli stessi join exact del prefisso, senza promuovere i due alias. I bundle futuri includono i moduli del registratore e dell'aggiornatore. Dichiarata esplicitamente la scala non verificata tra viste.

`run_real_prefix.py --root <nuovo_bundle> --accumulate` abilita l'aggiornatore a valle delle associazioni predette e verifica l'hash del NPZ preparato; senza opzione l'accumulo resta disattivato. Restano gli assert di equivalenza a peso zero. Log JSON con esiti/provenienza/diagnostiche e riepiloghi delle nuvole. Il confronto del matcher continua a usare forme separate già disponibili: nessuna nuova inferenza SuperFlex o sostituzione del descrittore con la nuvola accumulata.

Preparatore e runner modificati e controllati sintatticamente, **non eseguiti sul prefisso ufficiale in questa fase**. Nessun bundle storico sovrascritto, accesso HPC o nuovo job. La modalità futura è diagnostica di accumulo con contributo matching zero, non il ciclo completo già dimostrato.

## Verifiche e limiti

**35 test locali passati:** 7 adapter, 9 wrapper, 12 coordinatore e 7 nuovo aggiornatore. I sette nuovi coprono inizializzazione→registrazione reale del candidato su superficie sintetica con trasformazione nota, rifiuto di una nuvola sintetica incompatibile, separazione sorgenti/convenzioni e rifiuto di completamenti dichiarati, purezza e stato/versione precedente, budget/ancora/provenienza e caricamento NPZ con manomissione. Alcuni controlli di ammissione/budget usano decisioni simulate, dichiarate nei test; il controllo della trasformazione nota e quello della forma incompatibile chiamano il registratore effettivo. Tracker/modello/tensor sono sostituti controllati con metodi originali compilati dal sorgente.

Esiti, log e hash in `outputs/cloud_updater_20261114/verification.json` e `tests.txt`; sintassi verificata per i sei Python interessati. Nessun dato reale rielaborato, test Torch/checkpoint, inferenza SuperFlex, training o push. Il risultato reale precedente resta **0/12 aggiornamenti ammessi**: i test sintetici non lo sostituiscono.

**Prossimo passo:** collegare nuvola/versione accettata alla richiesta di inferenza SuperFlex differita, conservando normalizzazione inversa e provenienza; pubblicare una nuova forma soltanto per i frame successivi secondo il replay causale. Validazione della registrazione e risultati HPC pendenti restano necessari prima delle conclusioni di efficacia.
