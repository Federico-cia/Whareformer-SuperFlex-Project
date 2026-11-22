> Aggiornamento: [mappa opzione A](map_20261122/README.md), [evidenze del prototipo](point3_20261122/README.md), [preparazione e test](clean_update_20261122/README.md), [asset esterni](ASSET_ESTERNI.md).

# Evidenze verificate

Report numerici e log dei controlli acquisiti, suddivisi per fase:

- [Mappa approvata del 21 novembre](map_20261121/README.md): struttura, commenti e controlli dell’applicazione; documentazione editoriale, non nuova evidenza sperimentale.
- [Campagna estesa conclusa](../archive/CAMPAGNA_HPC_20261115.md): specifica, selezione, preflight e ricevute di invio in [campagna](campaign_20261115_v1/). Risultati finali acquisiti: 29/29 configurazioni valutate, assegnazioni e metriche identiche a W0.
- [Prima run completa attiva](full_video_20261114/REPORT.md): intero protocollo P01_01, sette fusioni ammesse, 25 nuove SuperFlex e audit causale; metriche invariate.
- [Riordino corrente](repository_cleanup_20261114/): suite dopo la pulizia e hash dei sorgenti.
- [Baseline e registrazione](hpc_ripresa_20261114/): replay zero, conteggi e audit dei rifiuti.
- [Valutatore](tracking_evaluation_20261114/): riproduzione delle metriche originali e suite HPC.
- [Runner comune](common_runner_20261114/): verifica del comando e delle varianti.
- [Frontend](frontend_20261114/): cache reale, inventario asset e pipeline 763531 conclusa.

Le copie dei risultati conservano i dati originali; i percorsi assoluti al loro interno descrivono la macchina dell'esecuzione. Non sono percorsi operativi del clone. Per significato scientifico, scope e limiti leggere la [guida](../memory/LEGGIMI_PASSAGGIO_AI.md).

[Inventario SHA-256](publication_inventory.json): snapshot dei file mantenuti nella consegna attuale, con percorsi relativi alla repository. Non include se stesso. La verifica `python tools/check_repository.py` controlla hash, collegamenti locali e sintassi dei sorgenti mantenuti; non sostituisce test funzionali o inferenze.
