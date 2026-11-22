# Acquisizione e arricchimento completo P01_01

## HPC controllato: 15 blocchi conclusi, stop preventivo per quota — 22 novembre 2026

Verifica live delle 11:31:28: **coda vuota**, 15/216 blocchi (0–14), **7680 nuove osservazioni** esportate. Conteggi ricalcolati su tutti i 15 indici: 7680 ready per ciascuna delle quattro rappresentazioni DA/MoGE punti/SuperFlex. Sette blocchi in più dopo la pulizia; non conclusa la run. **45.30/46.56 GiB**, circa 1.26 GiB liberi; 485960/500000 file.

Ultimo blocco terminato con successo alle 00:26:02; **783835 e 783852** fermati preventivamente con codice **75**, spazio sotto la riserva di 2 GiB. Nessun job attualmente attivo/in attesa. Prossimi mancanti: ramo 0 blocco 16, ramo 1 blocco 15. [Accounting, percorsi e limiti](CONTROLLO_HPC_20261122.md). Risolvere conservazione/compattazione degli output e quota file prima di nuovi invii. Nessun rilancio o cancellazione eseguiti; scelte scientifiche invariate. Questo stato supera le precedenti note RUNNING serali.


## Spazio recuperato e nuova ripresa — 21 novembre 2026

**Verifica successiva delle 23:51:38:** 783790/783791 entrambi RUNNING a 3m56s su gnode03; superato l'arresto precedente nelle nuvole, ora blocco 8 con 309/312 report DA/MoGE e blocco 9 con 286/288. Quota 41.19/46.56 GiB (circa 5.37 GiB liberi), otto blocchi ancora conclusi; SuperFlex dei nuovi blocchi non ancora verificata.

Marco autorizza pulizia e, esplicitamente, copia/archiviazione dei tracciati conclusi sul PC. Verificati due volte 377 file (5.47 GiB) e conservati in archivio locale di 636594519 byte con ledger/hash, prima di rimuovere le sole copie remote. Runtime, geometrie e input attuali preservati. Quota scesa da 46.35 a 40.88 GiB su 46.56; archivio da NON eliminare. [Operazioni, percorsi e ripristino](PULIZIA_E_RIPRESA_HPC_20261121.md).

**Job correnti:** 783790/783791, rami 0/1 dai blocchi 8/9, RUNNING su gnode03 al controllo 23:49:54 (2m11s). Preflight quota positivo anche sul nodo di calcolo. Otto blocchi conclusi a quel controllo. I tentativi 783750/751 sono falliti dopo MoGE anche su nodo diverso; 783782/783783 fermati prima delle inferenze per helper quota assente, poi corretto. Nessun precedente tentativo va considerato attivo.

Guard di quota a ogni blocco: riserva operativa 2 GiB/12000 file, stop esplicito codice 75 quando insufficiente; fallback nativo BeeGFS verificato. Tolta l'esclusione del nodo che non risolveva. Nessuna modifica scientifica. **Capacità ancora aperta:** costo misurato 0.64 GiB/blocco, estrapolazione circa 138 GiB/216 blocchi; la pulizia non basta a garantire completamento nella quota di 50 GB. Occorre compattare la conservazione senza perdere informazione necessaria o reperire capacità. Nessuna riduzione di copertura o sorgenti approvata in questa fase. Non promettere funzionamento ininterrotto notturno.


## HPC riavviato su richiesta di Marco — 21 novembre 2026, 23:23

Marco richiede «Fallo ripartire». Diagnosi e ripresa eseguite con accesso esistente autorizzato per l'azione: **783750 e 783751 RUNNING su gnode03**, rami 0/1 dai blocchi 8/9. **MoGE superato: 512/512 ready in entrambi**, DA già pronta, nuvole in costruzione. Ultimo controllo 23:23:51, rispettivamente 3m14s/3m08s; 8/216 blocchi ancora conclusi a quel momento. Catena automatica preesistente preservata, nessun duplicato o reset delle cache.

Escluso gnode02 dai job e successori come intervento controllato dopo quattro arresti osservati durante MoGE, senza pretendere diagnosi hardware conclusiva. Batch remoto salvato in backup e arricchito di log; dati/modelli/codice scientifico invariati. [Intervento, hash, log e ricevute](RIPARTENZA_HPC_20261121.md). Non reinviare mentre i rami sono in coda. SuperFlex dei nuovi blocchi e completamento integrale ancora da verificare; nessuna sorveglianza permanente avviata. Questo stato supera le precedenti note di coda vuota/run ferma. Audit e sviluppo punto 3 restano nello stato documentato.


## Mandato e configurazione

Marco autorizza acquisizione/verifica di RGB e maschere mancanti e successivo avvio SuperFlex per tutte le **110590 osservazioni / 33310 frame** originali. Nessuna nuova annotazione manuale o modifica alle politiche di associazione/ammissione. Due sorgenti già presenti, DA e MoGE, stesso SuperFlex robust e codice geometrico della campagna del 15 novembre; nessun training nuovo.

Archivio RGB ufficiale Bristol raggiungibile, dimensione dichiarata **1716787200 byte**. Spazio filesystem HPC osservato 98 TB liberi, non attestazione di quota personale. Maschere VISOR complete già nel file `data_compare200/P01_01/annotations.zip`; vengono ricontrollate tramite ID/nome/bbox per ogni osservazione originale, non limitate alle categorie del vecchio campione. Mapping VISOR/RGB, intrinseci e pose esistenti riusati. Tutti i target restano nel denominatore; maschere mancanti/ambigue e indici RGB differenti registrati esplicitamente.

## Esito osservato — 21 novembre 2026, 16:58 (supera gli stati sotto)

782990 COMPLETED 0:0 (41m10s): `coverage.json` con 110580/110590 osservazioni abbinate, 10 mancanti, zero conflitti, 32125 frame RGB verificati, 216 blocchi. 782968/782969 FAILED 1:0 dopo 8–9 minuti nello stadio `superflex`: `Ninja is required to load C++ extensions`. Causa probabile: `lane()` chiama `~/.conda/envs/<env>/bin/python` senza attivare l'ambiente, quindi `ninja` non è nel PATH (la campagna usava `conda activate`). Nessun blocco completato né successivo inviato. Correzione e reinvio in attesa di conferma. Esito completo in `strumenti_hpc/esito_hpc.txt`.

**Correzione preparata (21 novembre, dopo l'esito):** Marco autorizza la modifica dato che la coda risultava vuota. `lane()` ora antepone al PATH la cartella `bin` dell'ambiente di ogni stadio; nessun cambio di metodo o parametri. Applicata a `outputs/p01_full_enrichment_20261121_v1/full_p01_enrichment.py` e `integration_prototype/full_p01_enrichment.py` (SHA-256 `0f73f716…66e9f`, prima `6f782f47…07c7`; copie `.pre_ninja_fix`). Script `strumenti_hpc/esegui_rilancio_hpc.bat` + `rilancio_remoto.sh`: carica il file, si ferma se ci sono job cv_p01 in coda o hash inattesi, verifica `ninja`, conserva backup, aggiorna `runtime_revision.sha256` e invia solo i rami GPU 0/1; esito in `strumenti_hpc/esito_rilancio.txt`. Non ancora eseguito: lo esegue Marco. Blocchi 0/1 riprendono dalla cache firmata della pipeline (DA/MoGE/nuvole già prodotti).

## Job inviati e ripresa

- **782990 acquisizione/verifica**, sostituisce 782967 e riusa l'archivio RGB completo già scaricato. Ultimo stato osservato **RUNNING a 9m19s**, 20805 maschere generate, nessun errore nel log osservato. Verifica complessiva ancora pendente.
- **782968 ramo GPU 0**, PENDING con dipendenza aggiornata afterok su 782990.
- **782969 ramo GPU 1**, PENDING con dipendenza aggiornata afterok su 782990.

782967 CANCELLED dopo 10m56s su nostra richiesta per ottimizzare l'estrazione: la prima versione salvava tutti i JPEG del video. La versione corrente estrae solo i nomi richiesti dalle osservazioni e i corrispondenti indici del mapping, conservando l'archivio completo e i file già validi. Un file eventualmente interrotto viene riscritto se la dimensione differisce dal membro tar. Nessun dato già completato cancellato, nessun job GPU duplicato. Riepilogo finale protetto da scrittura concorrente; revisione runtime verificata tramite `runtime_revision.sha256`.

Radice HPC `~/cv_project/p01_full_enrichment_20261121_v1/`. Log correnti `acquire_782990.out/.err`, storici `acquire_782967.out/.err`, `geometry_<job>.out/.err`; ricevuta corrente `submitted_jobs.json`. [Ricevuta locale](../evidence/ASSET_ESTERNI.md#asset-e2b62cde81ba). Non reinviare i job senza acquisirne stato/esito.

Dopo acquisizione/verifica, `coverage.json` registra corrispondenze, mancanti, conflitti, alias e hash; manifest in `inputs/manifest.json`. Le 446 geometrie già verificate sono riusate. Restanti osservazioni divise in blocchi di massimo 512; due GPU al massimo, una per ramo, due ore massime per job. Ogni blocco esportato invia soltanto il successivo dello stesso ramo, senza accodare centinaia di job e rispettando i limiti precedentemente osservati. Ricevute successive in `submissions/`, risultati `geometry/<blocco>/`, completamenti `completed/`. L'esportazione di un blocco può contenere singole inferenze fallite: leggere sempre gli stati delle rappresentazioni. Nessuna promessa di durata/completamento prima della verifica effettiva.

Risultati aggregati attesi `all_geometry.json` e `final_status.json` quando tutti i blocchi inviati risultano esportati. Sono distinti da copertura completa riuscita: mancanti d'ingresso, conflitti e fallimenti restano espliciti. Gli alias temporali sono conservati come limite del confronto con le feature originali; non dichiarare automaticamente equivalenza del JPEG che produsse le feature ufficiali.

## Verifiche e limiti correnti

Prima dell'invio controllati sintassi Python, disponibilità archivio/spazio/coda e hash dei tre file runtime. Il primo controllo hash ha rilevato terminatori Windows nel solo file di checksum; corretti prima di ogni sbatch, nessun job partito dal tentativo iniziale. Codice e parametri originali dei modelli non modificati.

La verifica del driver completo su dati reali è in corso. Il job acquisizione è condizione necessaria per i due rami GPU; nessuna inferenza di questo nuovo lavoro è ancora osservata in questa fotografia. Modelli/pesi restano offline e già disponibili; geometrie grandi e RGB sull'HPC, niente push o trasferimento massivo sul portatile.
