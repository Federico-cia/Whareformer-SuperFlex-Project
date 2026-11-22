# Verifica dei dati originali e campione supervisionato arricchito

## Mandato e stato

Marco richiede di verificare i dati del training originale disponibili e l'esistenza di un campione con SuperFlex, target e provenienza; se assente, crearlo prima dell'estensione. Nessuna nuova etichetta manuale. Il campione geometrico esistente non conteneva gli esempi oracle supervisionati: completata la loro costruzione, non un training o una nuova inferenza geometrica.

Job CPU **782875 COMPLETED 0:0, 3m15s**. Due CPU, 8 GB, limite 25 minuti, nessuna GPU. Radice HPC `~/cv_project/training_enrichment_20261121_v1/`; log `enrich_782875.out/.err`; output `dataset/receipt.json` e `dataset/independent_verification.json`. Copia locale dei dati numerici/metadati acquisita con hash e verificata; geometrie grandi conservate sull'HPC e referenziate nel catalogo. [Ricevuta locale](../evidence/ASSET_ESTERNI.md#asset-c98dc9eb485e), [guida al campione](../evidence/ASSET_ESTERNI.md#asset-ae0b21d1b03d). Nessun job di questo lavoro ancora attivo o in attesa; non rilanciarlo.

## Risultato verificato

- **446 esempi supervisionati / 247 frame / 17 identità del benchmark**, tutti P01_01 e tutti associazioni a tracce esistenti. **Zero esempi Nuova track**: il campione non basta per apprendere/valutare l'intera decisione di associazione.
- Replay originale di 33310 frame/110590 osservazioni, 47 tracce oracle, 47 creazioni e 110543 associazioni successive. Nessuna predizione Whareformer usata come etichetta.
- 429/446 query hanno almeno una geometria precedente della candidata corretta; 445/446 hanno geometria precedente per almeno una candidata. Tutte le viste precedenti conservate, nessuna del frame corrente/futuro. Memoria di provenienza, non nuova politica di fusione/selezione.
- Input numerici e target coincidono con manifest builder/contratto loader originali; verificati 4460 artefatti geometrici, RGB/maschere e hash delle sorgenti. Tre test locali/remoti passati, audit indipendente del dataset passato e ledger confrontato localmente con tutte le annotazioni ufficiali conservate separatamente: 110590 corrispondenze.
- Originale split di 56 video verificato, uguale nelle configurazioni Whareformer/oracle. La configurazione effettiva del vecchio replay era limitata a P01_01: distinto questo dato nella ricevuta corrente e conservata la ricevuta iniziale che lo chiamava erroneamente split originale. Nessun input o target cambiato nell'audit dei metadati; dettagli nella guida.
- Zero etichette manuali, training o inferenze neurali nuovi. Archivio acquisito di 18.2 MB, SHA-256 `bc2d0c5090d10443d824190f25d4aa4feba305b8fbcdd3a4447f111c0b0933f8`.

**Disponibilità e limite per l'estensione:** verificati completi feature/XYZ/annotazioni di **1/56 video (P01_01)**; RGB/maschere/camera acquisiti solo parzialmente su cinque video. Le geometrie 446/247 non coprono l'intero P01_01. Per gli altri 55 non risultano ingressi completi verificati nell'inventario delimitato; non è prova di assenza globale o dentro archivi non aperti. [Inventario sintetico](../evidence/ASSET_ESTERNI.md#asset-796ba1d8fe21). L'estensione richiede acquisire/localizzare gli input originali mancanti e generare la geometria con la stessa pipeline, conservando anche Nuova track e mancanti; nessun nuovo training o download massivo avviato in questo primo step.

## Evidenze già disponibili

- Locale: P01_01 completo, feature ufficiali aspetto/PCA/XYZ e annotazioni, acquisizione originale con hash in `data/whareformer_official_P01_01_v2/`. Il bundle completo contiene 33310 frame/110590 osservazioni.
- HPC: campagna del 15 novembre con 446 osservazioni in 247 frame; quattro rappresentazioni pronte per osservazione (punti/SuperFlex DA e MoGE). Input RGB/maschere, parametri, superfici e hash già esistenti, riusati senza rigenerazione.
- Campione geometrico esistente con target di training e storia oracle: non presente nei prodotti esaminati; i campi delle associazioni registrate erano predizioni della baseline, non supervisione.
- Dati grezzi parziali compare200 per P01_01/P02_03/P03_04/P08_09/P22_01. Inventario HPC su 5650 directory dello spazio personale, profondità massima sette ed esclusioni esplicite: nessun `data.mdb`, manifest originale di training o file ufficiale di feature estratto trovato; due archivi del nostro codice restituiti dal filtro sul nome non sono training LMDB. Zero errori di scansione, non prova di assenza globale o dentro archivi non aperti. Disponibili i bundle numerici di P01_01; non attestata disponibilità completa dei 56 video di training.

## Contratto del nuovo campione

Riutilizzo del tracker e matcher oracle originali, con DenStream e memoria posizione originali, sull'intera storia ufficiale P01_01. Per le 446 osservazioni geometriche si esportano input aspetto/posizione e target one-hot confrontati con manifest builder/contratto del loader originali; identità/candidate oracle, ID dell'annotazione e della detection, riferimenti alle quattro geometrie e provenienza.

Archivio causale di tutte le viste geometriche precedenti per candidata: aggiornamento dopo l'intero frame, nessuna geometria corrente/futura. Questo è un indice dei dati disponibili, non adozione di nuova politica di memoria, distanza, fusione o gate. Le etichette seguono i nomi oggetto del benchmark, non nuove identità fisiche certificate. Non si dichiara uguaglianza con la training LMDB pubblicata, non ancora disponibile per il confronto diretto.

Sorgenti nuove: `integration_prototype/training_enrichment.py`, `verify_training_enrichment.py` e tre test del contratto passati localmente e sull'HPC. Verifica indipendente conclusa su ledger, target, numeri e completezza della storia. Contenuti grandi e dipendenze geometriche rimangono espliciti sull'HPC; nessun commit/push in questo lavoro.
