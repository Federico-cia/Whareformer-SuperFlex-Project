# Condivisione tra Marco, collega e docente

**Struttura condivisa attuale, 11 novembre:** [ramo pubblicato](https://github.com/Federico-cia/Whareformer-SuperFlex-Project/tree/prepare/superflex-core), codice verificato in `SuperFlex/`, documenti scientifici in `context/memory/`. Controllo riservatezza superato; originali e pacchetti dati restano locali. Nessun merge su `main`. In questo ramo non sono inclusi `results/`, manifest dei run, script storici o runner neurali. Stato e limiti in [STATO_LAVORO.md](../STATO_LAVORO.md). Le modalità e i pacchetti descritti sotto riguardano l'archivio locale precedente, non il contenuto del clone GitHub.

**Selezione prima della pubblicazione, 11 novembre:** `origin` è collegato a [repository comune](https://github.com/Federico-cia/Whareformer-SuperFlex-Project), ma nessun nostro file è stato caricato. La candidata verificata è il ramo locale `prepare/superflex-core` nel worktree `shared_exports/publish_candidate/`: dieci file sotto `SuperFlex/`, senza memoria, risultati pesanti o diagnostici storici. Il precedente pacchetto completo resta archivio locale, non una lista di file da pubblicare. Perimetro e controlli in [REVISIONE_CODICE_REPOSITORY.md](../REVISIONE_CODICE_REPOSITORY.md).

**Revisione dell'11 novembre:** usare la repository GitHub comune, senza crearne una seconda. Codice e pacchetti locali preparati restano il materiale da importare quando URL/accesso saranno disponibili. Le indicazioni sotto descrivono la struttura e la condivisione, non un incarico ancora attivo di creazione del remoto.

## Scelta raccomandata

Repository **privata su GitHub** per codice, memoria scientifica, manifest e risultati numerici essenziali. Invitare collega e docente quando sono noti i loro account e la modalità richiesta dal corso. Non è necessario rendere pubblici dati e materiali del corso per far valutare il codice.

## Tre livelli di file

| Livello | Contenuto | Dove si condivide |
|---|---|---|
| Repository | Nostri script, documenti, manifest, risultati numerici selezionati e istruzioni | GitHub; comprende lo snapshot in `results/` |
| Pacchetto analisi | JSON per coppia, CSV, revisione delle identità, metadati e controlli dell'ultimo test | `shared_exports/`, tramite cartella condivisa; archivio originale di circa 3.2 MB |
| Input/geometrie complete | RGB, maschere, punti, mesh e output del confronto 200 | Pacchetto separato; circa 1.12 GB non compressi per il solo run geometrico, oltre agli input |

Dataset, pesi, codice degli autori e materiali didattici restano fuori da Git. Usare gli accessi e le condizioni delle fonti originali; i pacchetti non sostituiscono autorizzazioni o licenze. Nessuna password, chiave SSH o token va caricata o scambiata in chat.

`results/` è una **copia di consegna** dei risultati essenziali, con inventario e checksum in `manifests/shared_results.json`; `outputs/` conserva i run completi originali esclusi da Git. Gli script storici scrivono in `outputs/` o nei percorsi HPC: non si assume che scrivano direttamente in `results/`.

## Pacchetto pronto per il collega

`scripts/New-ProjectHandoff.ps1` crea una nuova cartella sotto `shared_exports/`, senza cambiare i risultati originali. Richiede un commit locale e crea:

- archivio del codice/documenti dell'esatto commit Git;
- copia degli archivi leggeri del test d'identità e degli input compare200 già disponibili;
- indice con SHA-256 e istruzioni di estrazione;
- con `-IncludeGeometry`, archivio separato dei cinque run geometrici completi e del piccolo pacchetto di riferimento pilota.

Esecuzione dalla radice del repository, in PowerShell:

```powershell
./scripts/New-ProjectHandoff.ps1
# Solo se servono anche punti, mesh, maschere e profondità già calcolati:
./scripts/New-ProjectHandoff.ps1 -IncludeGeometry
```

Non avvia inferenze, download o job HPC. Gli archivi contengono dati esistenti e non entrano nella cronologia Git. Al collega basta clonare la repository e recuperare il pacchetto necessario, senza scaricare nuovamente tutto il dataset.

## Lettura o riproduzione

**Per capire e valutare il lavoro:** leggere `docs/CODICE_PRODOTTO.md`, i due resoconti risultati e gli snapshot in `results/`; nessuna GPU richiesta.

**Per verificare il test d'identità senza rieseguire le reti:** estrarre `completed_results.tar.gz` nella cartella `outputs/shape_identity_v1/`, mantenendo il prefisso dell'archivio, poi eseguire `verify_shape_identity_results.ps1`. Per ripetere l'analisi serve un ambiente Python con NumPy/SciPy e il valutatore; le coppie già calcolate bastano. Le tavole per la revisione delle identità sono nello snapshot `preparation_review.tar.gz`, precedente al CSV revisionato: non sovrascrivere quest'ultimo con la versione iniziale non etichettata.

**Per nuove inferenze:** servono anche sorgenti/pesi versionati, camera/mapping/RGB/maschere e gli ambienti dei rispettivi stadi. I job storici dipendono da cache e riferimenti del layout HPC. Non sono un'installazione automatica universale e non vanno avviati tutti. Copie degli autori e versioni: `manifests/whareformer_archive.json`, `superflex_archive.json`, `rgb_sources.json`; i dettagli effettivi degli ambienti sono nei run condivisi.

## Spazio per il lavoro del collega

Per aggiungere la baseline alla stessa repository: codice nuovo in un ramo dedicato, configurazioni portabili sotto `configs/`, documentazione sotto `docs/`, riepiloghi in `results/` e manifest dei dati/pesi in `manifests/`. I file pesanti restano nel pacchetto esterno o sul suo account HPC. Non caricare pickle o checkpoint in Git.

Prima dell'integrazione occorre sapere quali osservazioni, checkpoint, feature e XYZ la baseline usa realmente. Questa repository prepara lo scambio e non certifica il lavoro del collega. Nessun invito o messaggio viene inviato automaticamente.
