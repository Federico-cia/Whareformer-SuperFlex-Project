# Risultati finali della campagna HPC — 15 novembre 2026

**29 configurazioni su 29 completate e valutate**, senza timeout, errori di aggiornamento o fallimenti dei worker. Nessun job della campagna rimane attivo o in attesa. Tutte le configurazioni producono le stesse assegnazioni della baseline W0, comprese le 24 a peso non nullo: nessun miglioramento o peggioramento del tracking in questa griglia di sviluppo.

## Completamento verificato

| Job | Stadio | Esito | Durata |
|---|---|---|---|
| 764670 | Test, asset e selezione | COMPLETED 0:0 | 1m35s |
| 764674 | DA, MoGE, nuvole, SuperFlex delle osservazioni | COMPLETED 0:0 | 11m38s |
| 764675 | Bundle completo e controlli di copertura/hash | COMPLETED 0:0 | 1m41s |
| 764678 | 19 configurazioni CPU | COMPLETED 0:0 | 4h13m00s |
| 764679 | 10 configurazioni con SuperFlex della memoria | COMPLETED 0:0 | 3h54m41s |
| 765084 | Riepilogo automatico e controlli zero vs W0 | COMPLETED 0:0 | 42s |

Tutti i codici per singolo trial sono zero. Ogni configurazione ha elaborato e valutato l'intero protocollo ufficiale P01_01: 33310 frame e 110590 osservazioni; orizzonte di valutazione 99135, fps 60. I quattro controlli zero (G0 DA/MoGE e S-accumulo DA/MoGE) coincidono con W0. Non sono stati rilanciati job per questa acquisizione.

## Risultato del tracking

| Metrica | W0 | Tutte le altre 28 configurazioni |
|---|---:|---:|
| IDF1 (%) | 73.2697350574193 | 73.2697350574193 |
| mPCL originale (%) | 70.46550449586454 | 70.46550449586454 |
| Assegnazioni diverse da W0 | 0 | 0 |

Non esiste un vincitore empirico di tracking in questa matrice. La maggiore copertura e la griglia peso 0.1/1 × distanza neutra 0/0.1 non hanno modificato nessuna delle 110590 assegnazioni per variante. Il risultato non distingue ancora margini troppo ampi della baseline, insufficiente copertura di casi difficili, scala del termine e discriminatività del descrittore: servirà analizzare la telemetria prima di modificare il metodo o aumentare ulteriormente i pesi.

## Geometria e ricostruzioni

Geometria rigenerata dalle immagini selezionate: 247 frame/446 osservazioni, tutte pronte per punti e forme DA/MoGE (892 nuvole e 892 ricostruzioni per osservazione). Feature ufficiali aspetto/PCA/XYZ conservate byte-identiche; copertura geometrica ancora 0.4033% delle osservazioni. Nessuna nuova estrazione completa DINOv2/PCA/XYZ da RGB.

| Sorgente | Inizializzazioni per variante con accumulo | Fusioni ammesse | Rifiuti | SuperFlex pronte per variante S-accumulo |
|---|---:|---:|---:|---:|
| DA | 23 | 31 | 392 | 54 |
| MoGE | 23 | 40 | 383 | 63 |

Questi conteggi si ripetono nelle varianti della stessa sorgente, perché le associazioni sono identiche. Non vanno sommati come prove indipendenti. Le dieci varianti S-accumulo riportano complessivamente 585 ricostruzioni della memoria pronte (5×54 + 5×63), con zero fallimenti e zero richieste pendenti. Il maggiore numero di fusioni MoGE non certifica migliore accuratezza fisica o utilità per il tracking.

Filtri, registratore, reti congelate e separazione punti osservati/completamenti invariati. Questa acquisizione verifica i report di completamento, conteggi e confronti con W0; non sostituisce un audit indipendente di tutte le pose, delle identità fisiche e della qualità delle nuove fusioni.

## Output e ripresa

[Tabella completa](../evidence/ASSET_ESTERNI.md#asset-8baba7242a2c), [riepilogo](../evidence/ASSET_ESTERNI.md#asset-819dcd54ccdb), [accounting finale](../evidence/ASSET_ESTERNI.md#asset-f1fcdffa0c8b), [specifica e avvio storico](CAMPAGNA_HPC_20261115.md).

Output completi sull'HPC: `~/cv_project/campaign_20261115_v1/`, in `runs/<variante>/`, `caches/<variante>/`, `geometry/`, `bundle/`. Risultati finali `campaign_summary.json`, `comparison/`, ricevuta `submitted_jobs.json`, accounting `accounting_final.txt`; log finali `logs/summarize_765084_4294967294.out/.err`. Localmente sono acquisiti i riepiloghi, le metriche, i codici dei trial e l'accounting; i grandi JSONL, le nuvole e le mesh di tutte le varianti restano sull'HPC, non sono dichiarati già scaricati.

Prossimo lavoro distinto: diagnosi dei margini e delle distanze sui casi geometrici, correttezza/qualità delle fusioni e opportunità di associazione nei frame coperti. Reti e filtri restano congelati; revisione dei gate ancora esplicitamente rinviata. P01_01 è sviluppo/train; non dedurre generalizzazione o inutilità generale della geometria. La campagna di esecuzione è chiusa, l'analisi scientifica approfondita resta da svolgere.
