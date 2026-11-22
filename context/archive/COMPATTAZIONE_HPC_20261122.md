# Conservazione compatta e rigenerazione HPC — 22 novembre 2026

**Contestualizzazione successiva:** il budget di 160 GiB sotto è lo scenario della vecchia run DA+MoGE completa. La direzione scientifica aggiornata è DA completo/MoGE campione; aggiunte di allineamento/world richiedono un nuovo pilota. Marco ha inoltre dichiarato 1 TB su Drive: [piano di archivio esterno e lavoro HPC a spazio limitato](ARCHIVIAZIONE_DRIVE_PIANO_20261122.md), non ancora collegato/eseguito. Le misure della pulizia riportate qui restano verificate e valide.

## Esito finale verificato

**Migrazione conclusa:** 785105 COMPLETED 0:0, 45m14s; **audit finale 785556 COMPLETED 0:0**, 4m09s. Compattati tutti i 15 blocchi 0000–0014; **46080 derivati** intenzionalmente assenti e registrati: 15360 input, 15360 PLY e 15360 diagnostiche. Ogni file è stato rigenerato e confrontato con il proprio SHA originale prima della rimozione; audit finale su tutti i registri, archivi e assenze. La campagna resta a 15/216 blocchi e 7680 nuove osservazioni, nessuna nuova copertura prodotta.

**Spazio:** 5.0936 GiB di derivati rimossi; 1.7853 GiB di nuovi archivi delle assegnazioni e ledger, differenza per-file circa **3.31 GiB** prima delle altre differenze di metadati. Quota ufficiale finale **41.92/46.56 GiB**, circa **4.64 GiB liberi**, circa **440040/500000 file/inode**; prima 45.30 GiB/485960. Variazione della quota complessiva circa **3.38 GiB**, distinta dal conto per-file: riportare prudentemente **circa 3.3 GiB netti recuperati**, non 5.09 GiB. I contatori di allocazione dei file e di quota globale non sono la stessa misura.

**Recupero finale reale:** comando per blocco eseguito su tre file DA (input, diagnostica, PLY), tutti byte-identici; descrittori ricostruiti identici, quattro record riutilizzati dal controllo cache e comando reale `retained_pipeline.py export` passato senza inferenza. Payload della prova rimossi dopo verifica, ricevuta mantenuta. Tempo interno del recupero di quei tre file **20.90 s**, quasi interamente nella prima diagnostica/caricamento delle dipendenze e archivio; non è una garanzia di tempi su altri dati o cache. La prova iniziale CPU di 18 file e gli otto test locali restano evidenze aggiuntive.

**Politica futura abilitata:** `retention_tools/enabled.json`; driver `full_p01_enrichment.py` aggiornato, originale conservato in backup con hash. Il wrapper applica la stessa conservazione dopo ogni nuovo export e riconosce le assenze registrate. Hash driver prima `0f73f716b6c1d61bbfb08e33d8880f3f2652fe969347a89955f4c84b2ce66e9f`, dopo `f1d710029d25884790136a9f5878693fba8ce3dc4bff3f3513fc947984828238`. Codice scientifico originale e firme preservati. **Coda personale vuota al controllo finale; nessun arricchimento rilanciato.**

**Capacità non risolta:** proiezione separata per 32266 frame/blocco e 110134 osservazioni: circa 60.0 GiB mappe dense, 42.1 GiB nuvole; con altri risultati conservati circa **130.5 GiB di geometria**, più circa 33.1 GiB di base software/input/storia: **ordine di 160 GiB complessivi**. È un'estrapolazione dai primi 7680 oggetti/2134 frame, sensibile a maschere, primitive e compressione, non un requisito esatto. Anche gli inode resterebbero eccessivi (ordine di 1.85 milioni nell'attuale organizzazione). **Non basta a completare i 201 blocchi restanti.** Occorre un'ulteriore politica di consumo/conservazione delle mappe dopo l'allineamento, contenitori per nuvole/parametri e/o capacità persistente; nessuna nuova riduzione scientifica decisa qui.

Evidenze locali principali: `final_verification.json`, `migration_completed.json`, `pilot_roundtrip.json`, `cpu_regeneration_verified.json`, `final_observation.json`, `driver_enablement.txt`, `capacity_plan.json` e `capacity_summary.json` in `outputs/storage_compaction_20261122/`. Script di ricalcolo del budget: `strumenti_hpc/riassumi_compattazione.py`. Le note di migrazione in corso nelle revisioni preliminari sono superate da questo esito.

Snapshot esatto del driver installato: `outputs/storage_compaction_20261122/deployed_full_p01_enrichment.py`, SHA uguale a quello dopo l'abilitazione sopra. Il sorgente portabile locale conserva `CV_SLURM_ACCOUNT` opzionale; il deployment conserva il parametro account Slurm personale già preesistente. È l'unica differenza di contenuto verificata fra i due driver; non sovrascrivere la gestione portabile con lo snapshot operativo. Nessuna credenziale salvata.

## Autorizzazione e metodo

Marco approva esplicitamente: preparare/verificare gli script, eliminare i file non necessari recuperabili, registrare i risultati non conservati integralmente e misurare risparmio/capacità per l'intera campagna. Questa approvazione supera le precedenti note di sola proposta, non autorizza cambi di dati, campionamento, precisione o metodo scientifico.

Percorso remoto: `~/cv_project/p01_full_enrichment_20261121_v1/`. Modifica del solo ciclo di vita dei derivati nei blocchi completati `geometry/0000`–`0014`. Nuvole oggetto, mappe dense, parametri della forma, input RGB/maschere, pesi, codice scientifico originale e consegna locale delle mesh restano conservati.

## Risultati di verifica già acquisiti

- **785079, prova GPU:** la ripetizione dell'inferenza non riproduce numericamente tutte le assegnazioni entro rtol 1e-5/atol 1e-6; primo errore con massimo assoluto 0.00391525. Non usata come giustificazione per cancellare dati. Non allargate le tolleranze per far passare la prova.
- **Correzione operativa:** conservare le sole matrici di assegnazione originali in un archivio compresso per blocco. Nuvola diagnostica e input si ricostruiscono dai punti originali; parametri da `shape_parameters.npz`. Palette casuale delle primitive recuperata dal PLY e registrata in pochi byte nel ledger. Non basta conservare i soli parametri per riottenere colori/checksum originali.
- **785102 COMPLETED:** prova CPU su tre osservazioni distribuite nell'indice per ciascuna fonte DA/MoGE, tre tipi di artefatto: **18/18 file byte-identici**, checksum completi, non solo geometria simile. Ambiente numpy 1.26.4, trimesh 5.2.0. Ricevuta remota `retention_tools/cpu_regeneration_verified.json`.
- **8 test locali di sicurezza passati:** confini dei percorsi, dati conservati corrotti/mancanti, prova assente/non valida, firme scientifiche incompatibili, assenze registrate e assenze non registrate.
- **785105 COMPLETED:** job CPU di migrazione con due processi per blocchi indipendenti. Prova effettiva di eliminazione/ripristino, descrittori e ripartenza passata; verifica esaustiva e rimozione dei derivati dei 15 blocchi concluse. Log `retention_tools/migrate_785105.out/.err`; dettagli per blocco `retention_tools/migration_logs/NNNN.out`.

## File e contratti

Codice locale in `integration_prototype/`, installato remoto in `retention_tools/`:

- `geometry_retention.py`: rigenerazione, verifica, compattazione e lettura temporanea dei descrittori.
- `retained_pipeline.py`: adattatore attorno alla pipeline scientifica originale, senza modificarne i file o falsificarne gli hash. Accetta solo assenze presenti nel ledger e controlla i prerequisiti conservati. DA/MoGE/nuvole conservano la verifica originale; SuperFlex/export usano il nuovo controllo.
- `migrate_geometry_retention.py`: prova distruttiva circoscritta e migrazione dei soli blocchi con marker di completamento, con log separati.
- `test_geometry_retention.py`: test dei controlli di sicurezza.
- `regenerate_geometry_block.py`: recupero selettivo/in blocco, destinazione separata e archivio caricato una volta; verificato su tre tipi di file reali.
- `validate_geometry_retention.py`: audit finale dei registri, recupero, descrittori e CLI effettiva.

Un blocco compatto conserva `retention_assignments.npz` con le sole matrici originali, `retention.json` con checksum/ricette/palette e `retention_result.json`. Gli artefatti derivati restano dichiarati negli indici scientifici originali; `observations.json` esplicita `storage.state=regenerable`. Non confondere ready scientifico con presenza fisica del file. Un reader storico che richiede il file su disco va preceduto dalla rigenerazione oppure adattato alla lettura temporanea.

La compattazione ricostruisce e confronta **ogni input, PLY e diagnostica con il suo SHA-256 originale** prima dell'eliminazione. Scrive e verifica l'archivio delle assegnazioni e il ledger prima del primo unlink; ricontrolla ogni file immediatamente prima di rimuoverlo. I percorsi devono avere nomi canonici all'interno del blocco; nessuna cancellazione ricorsiva. La ripetizione riconosce le assenze autorizzate; assenze non registrate e prerequisiti alterati restano errori.

## Rigenerazione

Usare l'ambiente HPC `cv-superflex` e il codice originale conservato, come descritto in `integration_prototype/GEOMETRY_RETENTION.md`. La rigenerazione del percorso indicato nel ledger ripristina anche il checksum originale, senza inferenza GPU. Si può usare una destinazione esterna al blocco. La lettura `retained_features` ricostruisce un solo PLY in spazio temporaneo e usa il descrittore originale senza accumulare nuovamente le mesh sul disco persistente.

La vecchia funzione di replay GPU rimane una prova diagnostica esplicita, con destinazione separata e nessuna promessa di checksum originale. Non è la procedura di recupero usata per i file rimossi.

## Evidenze locali e capacità

Log/ricevute in `outputs/storage_compaction_20261122/`. Quota prima della migrazione: **45.30/46.56 GiB**, **485960/500000 file** alle 13:09:53. Coda allora vuota; nessun arricchimento completo rilanciato da questa operazione.

Risparmio netto e proiezione acquisiti nella sezione finale sopra, includendo il costo delle matrici conservate e dei nuovi registri. Le mappe dense restano necessarie all'allineamento del punto 3 e le nuvole osservate non sono sostituite dalle forme ricostruite.

Letti tutti i 216 manifest: **110134 osservazioni** da inferire, **32266 record frame/blocco** (conteggio degli hash RGB unici entro ciascun blocco). Ricevuta locale `capacity_plan.json`; nessun payload immagine scaricato. Questi conteggi consentono una proiezione separata di mappe per frame e dati per oggetto, più corretta di assumere un unico costo costante per blocco. Nei primi 15 blocchi: 7680 osservazioni e 2134 frame/blocco.

Tentativo di accelerazione con un secondo job e tentativo di ottimizzazione dello script durante la migrazione **respinti dal controllo automatico di approvazione**: rispettivamente rischio di sovrapposizione e modifica di codice mentre sono in corso eliminazioni. Nessuna delle due azioni è stata eseguita o aggirata. Proseguita la sola migrazione 785105 con script invariati; sorgenti locali riallineate agli hash della versione verificata. Nessun blocco residuo richiede approvazione dell'utente per questa alternativa.
