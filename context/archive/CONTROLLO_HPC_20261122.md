# Controllo HPC — 22 novembre 2026

Marco richiede controllo live. Verifica in sola lettura alle **11:31:28 Europe/Rome**, con accesso già configurato. Nessun rilancio, cancellazione, download di geometrie o modifica scientifica.

## Stato effettivo

- **Coda personale vuota.** La catena non è attiva né in attesa.
- **15/216 blocchi conclusi** (0–14), contro gli otto del precedente controllo serale.
- **7680 nuove osservazioni esportate**. Ricalcolati i conteggi da tutti i 15 observations.json: 7680 `ready` per ciascuna rappresentazione DA punti, DA SuperFlex, MoGE punti, MoGE SuperFlex. Sono due ricostruzioni per osservazione, non 15360 osservazioni indipendenti.
- Il riepilogo finale `final_status.json` è assente: arricchimento completo non concluso.
- **45.30 GiB usati / 46.56 GiB**, circa **1.26 GiB liberi**; 485960 file / 500000, circa 14040 rimanenti.

## Accounting della ripresa dopo la pulizia

783790/783791, blocchi 8/9: COMPLETED 0:0, 8m39s/8m48s. Successori 783804/783805 e 783818/783819: COMPLETED 0:0, circa dieci minuti ciascuno. 783834, blocco 14: COMPLETED 0:0 alle **00:26:02**.

783835, blocco 15: fermato dal controllo della quota alle **00:16:24**, codice 75. 783852, blocco 16: fermato allo stesso modo alle **00:26:04**, codice 75. Log esplicito `STORAGE_RESERVE_STOP`: spazio inferiore alla riserva operativa di 2 GiB. Lo stato Slurm è FAILED, ma in questi due job è un arresto preventivo prima delle inferenze, distinto dai precedenti arresti senza traceback.

Prossimi blocchi mancanti: ramo 0 → **16**; ramo 1 → **15**. Non reinviare senza prima risolvere spazio e limite dei file; il preflight si fermerebbe di nuovo.

## Evidenze e limiti

Log locali `strumenti_hpc/controllo_20261122.txt` e `esiti_blocchi_20261122.txt`. Radice remota `~/cv_project/p01_full_enrichment_20261121_v1/`; ricevute `submissions/0015.json`, `0016.json`; log di stop `geometry_783835.out/.err`, `geometry_783852.out/.err`; risultati in `geometry/0000`–`0014`, marker in `completed/`.

Verificati accounting, marker e stati delle rappresentazioni esportate; non ricontrollati tutti gli hash/mesh o accuratezza fisica. Le nuove geometrie restano sull'HPC. Le 446 geometrie preesistenti riusate sono distinte dalle 7680 nuove osservazioni dei blocchi, senza nuovo audit combinato della copertura.

La pulizia autorizzata ha consentito sette ulteriori blocchi; la limitazione di capacità già documentata è tornata vincolante. Prossimo passo: politica di conservazione/compattazione degli output e gestione degli inode prima della ripresa. Nessuna riduzione di dataset/sorgenti o nuova eliminazione decisa durante questo controllo.
