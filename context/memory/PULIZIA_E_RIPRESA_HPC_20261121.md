# Pulizia autorizzata e ripresa dopo quota piena — 21 novembre 2026

## Decisioni e problema verificato

Marco chiede di riavviare l'HPC, poi autorizza la pulizia dei file inutili.
Alla richiesta esplicita di trasferire e archiviare i tracciati conclusi sul PC,
risponde «Sì, autorizzo copia e archiviazione». Il primo trasferimento era stato
fermato dalla revisione automatica prima dell'esecuzione; ripreso solo dopo
questa autorizzazione specifica. Nessuna pubblicazione o invio a terzi.

La prima ripresa 783750/783751 su gnode03 aveva superato MoGE, poi entrambi
i job sono falliti alle 23:23:53 durante le nuvole. L'esclusione di gnode02 non
è una soluzione dimostrata ed è stata rimossa: non attribuire il problema a
quel nodo sulla sola correlazione iniziale.

`myquota` mostra **46.35 GiB usati / 46.56 GiB disponibili come limite**,
434.30k file / 500k: circa 0.21 GiB di spazio rimasto. `df` mostrava invece
98 TB liberi del filesystem condiviso, irrilevanti per il limite personale.
Quota quasi piena verificata; spiegazione plausibile dei fallimenti di
scrittura senza traceback completo, senza pretendere un errno EDQUOT già letto.

## Archiviazione senza perdita di informazione

Origine: `~/cv_project/campaign_20261115_v1/runs/`, campagna conclusa.
Non sono runtime, geometrie originali, pesi o input della run corrente.

- **377 file**, **5875262449 byte** originali (circa 5.47 GiB).
- Archivio locale `outputs/hpc_storage_recovery_20261121/campaign_runs_verified.tar.gz`:
  **636594519 byte**, circa 607 MiB; SHA-256
  `79739ae659892203187b49b33c1427b4c0a05c91ece242685c65cce7652e9717`.
- Contiene 145 JSON, 87 log, 58 CSV, 58 JSONL e 29 NPZ, non soltanto log:
  tutti conservati nell'archivio, incluso ledger SHA-256 di ogni file.
- Verifica locale integrale del tar e di ogni contenuto; poi seconda verifica
  integrale degli originali remoti, con corrispondenza esatta di nomi/hash.
- Solo dopo questi controlli rimossi i 377 originali già archiviati, senza
  cancellazione ricorsiva. Marker remoto
  `campaign_20261115_v1/runs/ARCHIVED_TO_LOCAL_20261121.json` con riferimento
  alla copia e relativo hash. La copia compressa va conservata.

Ricevuta con ledger e percorso assoluto locale:
verified_archive_receipt.json (`outputs/hpc_storage_recovery_20261121/verified_archive_receipt.json`, risorsa locale non pubblicata).
Log `archive_transfer.log` e `remote_cleanup.log` nella stessa cartella.
Il contenuto dei vecchi `runs/<variante>/...` ora si legge dall'archivio sul PC;
per usarlo nuovamente come file ordinari sull'HPC serve un ripristino esplicito
compatibile con la quota. I riepiloghi già scaricati e le altre cartelle della
campagna restano disponibili. Nessuna cancellazione dei blocchi correnti 0–9.

Dopo la pulizia: **40.88/46.56 GiB**, circa **5.68 GiB liberi**. L'archivio RGB
`P01_01.tar` non è stato rimosso. Nessun ambiente, modello o parametro alterato.

## Controllo preventivo e correzione operativa

`strumenti_hpc/hpc_quota_guard.py`: prima di ogni blocco, controlla la quota
personale con riserva operativa di **2 GiB e 12000 file**. Valori di prudenza
operativa, non soglie scientifiche apprese o garanzia di spazio per l'intera run.
Il conteggio del server può avere ritardo di circa 30 secondi; i blocchi possono
avere costi diversi. Riserva non sufficiente → arresto esplicito con codice 75,
senza riavvio automatico infinito o prosecuzione cieca fino a saturazione.

783782/783783 si sono arrestati preventivamente, senza inferenze, perché
`/userScripts/myquota` esiste sul login ma non sul nodo di calcolo. Corretta
la compatibilità: fallback al comando nativo `/usr/sbin/beegfs quota list-usage`
per il proprio UID, pool_home, con fattore 0.5 di mirroring usato dal helper
ufficiale. Non modifica o aggira la quota. Parser verificato sui due formati
reali e controllo eseguito con esito positivo in uno step CPU di Slurm.

Batch remoto derivato dall'originale, senza esclusione nodi, con guard e
diagnostica; backup `geometry.sbatch.before_quota_guard_20261121` e
`geometry.sbatch.before_restart_20261121` preservati. Controller scientifico
`full_p01_enrichment.py` rimasto invariato. Guard nel task remoto, catena dei
due rami preesistente preservata. Nessun duplicato in coda prima degli invii.

## Ripresa corrente

Alle 23:47 inviati **783790** (ramo 0, blocco 8) e **783791** (ramo 1,
blocco 9). Entrambi RUNNING su gnode03 al controllo delle **23:49:54**, a 2m11s;
preflight positivo. Quota 41.07/46.56 GiB, otto blocchi conclusi a quel momento.
Avanzamento successivo da registrare nel prossimo controllo, non anticipato.

Radice `~/cv_project/p01_full_enrichment_20261121_v1/`, log
`geometry_783790.out/.err` e `geometry_783791.out/.err`, ricevute
`submissions/resume_0008_783790.json` e `resume_0009_783791.json`.
File locali `strumenti_hpc/esito_ripresa_quota_corretta_20261121.txt`,
`test_quota_compute_20261121.txt`, `stato_ripresa_dopo_pulizia_20261121.txt`.
Gli stati dei tentativi precedenti sono cronologia, non job ancora attivi.

## Limite di capacità ancora aperto

Un blocco concluso misurato (0004) occupa **686428672 byte**, circa 0.64 GiB.
Estrapolazione grezza di costo costante: **circa 138 GiB per 216 blocchi**, senza
input e ambienti; non una misura finale, perché viste/oggetti cambiano il costo.
La pulizia consente una ripresa ma **non dimostra che la run completa entri
nella quota di 50 GB**. Anche il numero di file è limitato.

Serve un piano di rappresentazione/ritenzione più compatto degli intermedi,
oppure altra capacità. Non cancellare automaticamente mesh, profondità o punti
unici: alcune profondità DA servono ancora ad allineare alla scena, mentre
eventuali superfici derivabili da parametri richiedono prima prova di
ricostruibilità e adattamento dei loader. Nessuna riduzione di copertura o
eliminazione del confronto MoGE adottata implicitamente.

## Ultimo controllo prima della consegna

**Verifica successiva delle 23:51:38:** 783790/783791 entrambi RUNNING a 3m56s su gnode03; superato l'arresto precedente nelle nuvole, ora blocco 8 con 309/312 report DA/MoGE e blocco 9 con 286/288. Quota 41.19/46.56 GiB (circa 5.37 GiB liberi), otto blocchi ancora conclusi; SuperFlex dei nuovi blocchi non ancora verificata.
