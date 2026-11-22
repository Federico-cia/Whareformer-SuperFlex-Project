# Pacchetto mesh SuperFlex per il compagno — 22 novembre 2026

Richiesta di Marco: preparare mesh e indice delle osservazioni per consegna manuale al compagno. Creato il complemento allo ZIP compare200 già condiviso, senza nuove inferenze o accessi HPC.

- [Pacchetto ZIP](../evidence/ASSET_ESTERNI.md#asset-8db91e7b5b90): **54696713 byte**, circa 55 MB.
- [README](../evidence/ASSET_ESTERNI.md#asset-13d274b90286), [indice JSON](../evidence/ASSET_ESTERNI.md#asset-b23a7b89be59), [indice CSV](../evidence/ASSET_ESTERNI.md#asset-7b656a9dbd12).
- [Esito di verifica](../evidence/ASSET_ESTERNI.md#asset-b349b5982195), [checksum ZIP](../evidence/ASSET_ESTERNI.md#asset-dc659a42687f).
- SHA-256 ZIP: `22f14355067b613bb1fc2e61b9584257a675034b6d862dca85997289a6eea210`.

Stesse **299 osservazioni** del precedente pacchetto, su P01_01/P02_03/P03_04/P08_09/P22_01; **890 mesh**: 299 DA grezzo, 293 DA allineato, 298 MoGE. Il CSV contiene tutte le 897 combinazioni osservazione/sorgente: sei assenze DA allineato per allineamento/profondità non validi e un fallimento MoGE per assenza di primitive attive. Nessuna assenza rimossa dall'indice.

Mesh copiate byte per byte, con report originali disponibili. Controllati cloud SHA rispetto ai report e, per DA grezzo/MoGE, alle effettive nuvole nel vecchio ZIP; conteggi/topologia delle mesh, vertici finiti, indici delle facce, normalizzazione, copia, CRC ZIP e hash di ogni membro. Verifica indipendente utilizzabile dal destinatario con sola libreria standard: `python verify_package.py`; **1786 file verificati** mediante SHA256.json. Controllati i 897 record CSV e nessuna invenzione di detection_idx/track_id.

Join tramite observation_key, mantenuto identico al pacchetto precedente. Annotation_index non è detection_idx Whareformer. Percorsi mesh relativi alla cartella del nuovo pacchetto; RGB/maschera/camera/nuvole restano riferimenti alla radice del vecchio. Mesh denormalizzate in coordinate camera della singola osservazione, non già collocate nella scena o fuse multivista. Scala comune non certificata; DA allineato e MoGE distinti. Copertura del campione, non di tutto P01_01.

Generatori locali: scripts/prepare_superflex_mesh_handoff.py e scripts/verify_superflex_mesh_package.py. Nessuna nuova run, ricostruzione, modifica degli originali, pubblicazione GitHub o invio al compagno in questa fase. Il pacchetto è pronto per essere passato da Marco.
