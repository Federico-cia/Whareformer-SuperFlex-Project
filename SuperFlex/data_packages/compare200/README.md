# Compare200: dati delle osservazioni

[Scarica il pacchetto ZIP](https://github.com/Federico-cia/Whareformer-SuperFlex-Project/raw/refs/heads/main/SuperFlex/data_packages/compare200/compare200_tracking_inputs_v1.zip) — 73.1 MB.

Sono esattamente i 200 frame dei cinque video usati nella pipeline: P01_01, P02_03, P03_04, P08_09, P22_01. Contiene 299 maschere VISOR e 598 nuvole originali, 299 DA grezzo e 299 MoGE. Le copie coincidono con gli input/output degli esperimenti, verificati tramite SHA-256.

Estrarre lo ZIP in una cartella di lavoro vuota, mantenendo la struttura:

```text
data/compare200/                    RGB, annotazioni, camera, selection_final.json
outputs/compare200_749968/          maschere PNG e nuvole NPZ
scripts/acquire_compare200.py       script originale di acquisizione
observations_for_tracking.json      indice RGB/maschera/nuvole per osservazione
SHA256.json                        checksum dei file estratti
README.md                          istruzioni e convenzioni
```

Il collegamento con detection e track Whareformer resta da verificare; il pacchetto non assegna track ID. Le nuvole sono nel riferimento camera, non normalizzate per il confronto. Dettagli nel README interno. Non occorre ripetere download o inferenze.

L'archivio è conservato qui come pacchetto dati versionato, separato dal codice e dai risultati numerici. Il checksum dello ZIP è in [SHA256SUMS.txt](SHA256SUMS.txt). Pesi, credenziali e run completi non sono inclusi. Usare i dati secondo le condizioni delle fonti EPIC-KITCHENS/VISOR.
