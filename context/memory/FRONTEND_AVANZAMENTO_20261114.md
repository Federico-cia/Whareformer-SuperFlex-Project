# Frontend unificato: avanzamento verificato — 14 novembre 2026

Marco approva il piano del frontend. Implementati frontend_inputs.py e tre test; run_pipeline.py accetta ora --frontend-manifest in alternativa a --root. Il contratto lega video/frame RGB-VISOR, ID annotazione, ordine detection, box/categoria, poligoni della maschera, immagine e camera a hash e dimensioni espliciti. Mantiene distinti XYZ baseline nel riferimento scena e punti di forma nel riferimento camera. Nessun gate di fusione modificato.

## Percorso in cache eseguito

Manifest reale su P01_01, frame 2893/5099/7508, tutte le dieci detection. Validati mapping esatti (alias esclusi), annotazioni e box, risoluzioni dichiarate, pose e hash. Ricreato il bundle con tutta la storia di 3398 frame, senza ripartire dai tre frame sparsi. frames.json, features.npz, shape_features.npz e observed_clouds.npz byte-identici al riferimento. Ricevuta del frontend e origine del bundle aggiunte al nuovo input_manifest; originali preservati. Output: outputs/frontend_20261114/observations.json, bundle_v2/, verified_replay.json.

Il primo controllo leggeva ripetutamente gli array compressi: interrotto e corretto per leggerli una sola volta, poi rieseguito con successo. Il primo bundle resta storico; bundle_v2 è quello con provenienza integrata.

Tre test nuovi: video generico/copia/provenienza, mapping/ordine/risoluzioni/pose errati prima della copia, cache o immagine alterate. Suite locale: 72 casi, 70 passati e due motmetrics saltati per dipendenze locali (già verificati su HPC nelle fasi precedenti). Log/hash in outputs/frontend_20261114/verification.json. Nessuna nuova equivalenza neurale inferita dal solo import: i file di input sono identici e non è stato rilanciato inutilmente il tracking.

Uso dell’ingresso: python integration_prototype/run_pipeline.py --frontend-manifest <manifest.json> --config <varianti.json> --output <nuovo_output> --cache <cache_dedicata> --policy <policy.json>. Il modulo prepara un nuovo bundle e poi usa il runner originale del progetto. Questo è il percorso cache, non estrazione neurale nuova da RGB.

## Inventario e limite della rigenerazione

RGB, annotazioni e camera del pilota disponibili localmente; su HPC verificati fields.json e mesh.ply di P01_01. PCA_model_masked_256d.pkl presente localmente e hash registrato, ma associazione alla trasformazione che ha prodotto le feature ufficiali non certificata. Nei percorsi controllati ~/.cache/torch, ~/cv_project/hf_cache e ~/cv_project/external, profondità massima cinque, nessun file corrispondente a DINOv2/PCA/metric_scale.json. Non è prova di assenza globale. Asset e limiti in asset_inventory.json.

Rigenerazione non eseguita e backend cold non dichiarato completato. Restano da identificare/predisporre pesi e revisione DINOv2 compatibili, provenienza PCA e asset/convenzione della scala della scena, oltre all’ambiente di estrazione. Nessun download sostitutivo, fit PCA, ricostruzione MVS implicita o dati artificiali usati per simulare il percorso. La lettura della cache non certifica retrospettivamente il JPEG sorgente delle feature. Le parti indipendenti del piano sono sviluppate; il pilota rigenerato e il suo confronto restano aperti.

## Consolidamento dei job precedenti

763531 COMPLETED/0:0 in 23m24s: nove configurazioni a peso zero completate e valutate, tutte con zero_baseline_exact true. Valutazione e tabella terminate, copie in outputs/frontend_20261114/pipeline_763531/. Nessun nuovo job per questo frontend; gli esiti non dimostrano beneficio del peso geometrico o fusione multivista. Registro precedente corretto conservando gli stati storici.

Prossimo lavoro: risolvere le dipendenze/provenienza del ramo rigenerato, collegare e verificare gli estrattori originali sul pilota previsto. Piano approvato ancora parzialmente eseguito; filtri rinviati, nessun push o messaggio a terzi.
