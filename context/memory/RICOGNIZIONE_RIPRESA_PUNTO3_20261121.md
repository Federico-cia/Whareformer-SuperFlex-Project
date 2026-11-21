# Ricognizione dopo il lavoro con altro provider — 21 novembre 2026

## Perimetro della verifica

Letti riassunto fornito da Marco, istruzioni aggiornate, stato/TODO/registro, SUPERVISIONE_AMMISSIONE_20261121.md, verifica operativa, roadmap, guida di passaggio, codice del registratore/memoria e audit, ricevuta locale dell'audit, strumenti di controllo/scarico e schede pertinenti della mappa JSON. Verifica locale e statica: nessun accesso HPC, job, training, test di runtime, pubblicazione o modifica del metodo. La cartella radice non è un repository Git: nessun confronto storico Git effettuato, nessuna deduzione sul main remoto.

## Stato scientifico consolidato

Direzione corrente approvata, non più semplice proposta: DA allineata alla mesh e coordinate scena da pose EPIC-Fields; MoGE confronto; niente fusione se allineamento fallisce. Memoria senza privilegio fisso della prima vista; forma distinta dalla collocazione, stati candidati confermati nel tempo ispirati a DenStream; fusione pesata per cella dei duplicati, superficie nuova e filtro outlier, decadimento senza perdere copertura unica; 4096 punti FPS per SuperFlex. Verificatore appreso direttamente sulla coppia allineata, classificatore delle diagnostiche come baseline e verificatore preaddestrato come confronto. Soglia operativa/parametri solo su sviluppo. Prima tappa: fusione da fermo; obiettivo esplicito non negoziabile: fondere nella stessa forma anche le viste dopo spostamento.

Compagno sul punto 2; Marco sul punto 3; punti 1 e 4 successivi, salvo prerequisiti necessari al punto 3. Test indipendente ancora da scegliere, P01_01 solo sviluppo. Due memorie matching/ricostruzione da concordare con il compagno; altri 55 video rinviati. Scelte dettagliate di staticità, architettura/loss, utilità e costo degli errori ancora da formalizzare.

## Decisioni e implementazione restano distinte

cloud_memory.py conserva ancora prima vista + viste recenti e i tre gate numerici; cloud_updater.py lavora ancora su punti camera DA grezzi/MoGE. Nuova memoria a stati, DA allineata come ingresso della memoria, deduplicazione pesata/FPS e verificatore non sono implementati in questi moduli. audit_ammissione.py esiste e produce diagnostica grezzo/allineato e confronto del registratore con posa relativa dalle camere. Le schede R09/R12/R28/R32/R34 annotano le decisioni nelle descrizioni/proposte, non certificano implementazione. Nessun verificatore addestrato trovato fra i moduli correnti ispezionati.

## Precisazioni rispetto al riassunto ricevuto

1. CV 9–23% del rapporto profondità allineata/grezza non misura da solo l'errore vero di DA: può includere rumore del fit di allineamento. Mesh/pose consentono un riferimento comune ma non garantiscono accuratezza fisica.
2. Oggetto fermo + pose corrette forniscono un riferimento, ma non abbiamo ancora certificato automaticamente quali coppie siano ferme. Il solo centroide non esclude rotazioni, né le viste devono coincidere completamente se parziali.
3. Audit e arricchimento non sono dichiarabili RUNNING oggi sulla base delle ricevute storiche. VERIFICA_ARRICCHIMENTO_CORRENTE_20261121.md prevale: acquisizione 110580/110590 abbinate, dieci mancanti; otto blocchi completati nell'ultimo resoconto locale, ripresa 783490/783491 e audit 783586 documentati all'invio, successiva squeue senza job. Esito corrente ignoto senza accounting/log aggiornati. Il tempo per blocco non basta per una nuova previsione verificata.
4. Le ricerche Consensus sono sintesi secondarie già lette in parte; paper/modelli specifici e compatibilità non sono stati rivalidati qui. Non sostenere assenza di metodi nel dominio sulla sola ricerca disponibile.

## Cautele verificate leggendo l'audit

- Coppie consecutive per identità oracle, stratificate per spostamento XYZ: nessun certificatore di staticità. Errori rispetto alle pose camera condizionati all'ipotesi di oggetto fermo, non target reali già validati.
- reg_*_surface_err_R è media di ||(b R_est+t_est)-(b R_ref+t_ref)||/R sugli stessi punti, non distanza fra insiemi di superfici. Può penalizzare simmetrie geometricamente equivalenti; non usarla come target finale invariante alle simmetrie senza revisione.
- Lo script salva numero di alternative ambigue, ma non pose/errori di ogni candidato: non risolve ancora se la soluzione corretta esiste fra i candidati scartati.
- L'allineamento viene ricostruito con least-squares affine e controlli locali di validità; la funzione originale align_metric_and_scene_depth è caricata ma non chiamata. Parità completa di maschere, validità e fallback con la procedura originale da verificare prima di affermare equivalenza esatta.
- Statistiche di dimensione sulle nuvole parziali dipendono anche da visibilità e campionamento: variazioni del raggio non sono soltanto scala.

Sono limiti d'interpretazione e verifiche pendenti, non nuovi risultati sperimentali né revoca delle scelte approvate.

## Prossima sequenza

1. Marco esegue strumenti_hpc/esegui_controllo_hpc.bat e strumenti_hpc/esegui_scarica_audit.bat; leggere esito_hpc.txt e archivio/stato audit. Non inviare o riprendere job prima di conoscere accounting/output. Vincolo AGENTS: niente accesso HPC diretto dell'assistente.
2. Interpretare audit distinguendo scala/visibilità, staticità ipotizzata e errori del registratore; verificare qualità della supervisione, non addestrare dai gate.
3. Implementare la prima versione approvata con forma/collocazione separate, senza presentare il caso statico come traguardo finale.
4. Costruire dati/target del verificatore con perturbazioni note e test reali separati; includere dopo-spostamento, parzialità e simmetrie. Definire criterio operativo su utilità di memoria e dati di sviluppo.
5. Scegliere presto il protocollo/test set con Marco e coordinare l'interfaccia con il compagno. Pubblicazione delle modifiche serali preparata nei documenti, non verificata in questa ricognizione.
