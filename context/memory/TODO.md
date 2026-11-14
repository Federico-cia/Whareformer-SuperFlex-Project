# Attività correnti

## Step attivo, già approvato

- [x] Contratto delle osservazioni e import della cache verificata.
- [x] Collegamento del frontend cache al comando comune e verifica del pilota con storia preservata.
- [ ] Identificare pesi/revisione DINOv2 compatibili, provenienza PCA, asset/convenzione della scala e ambiente originale.
- [ ] Implementare il ramo rigenerato dagli estrattori originali e verificarlo sui frame P01_01 2893/5099/7508, mantenendo la storia.
- [ ] Confrontare input rigenerati e riferimento, esplicitando eventuali differenze; il solo import della cache non prova equivalenza neurale.

[Piano](PIANO_FRONTEND_UNIFICATO_20261114.md) · [Stato verificato](FRONTEND_AVANZAMENTO_20261114.md).

## Dopo il frontend

- [ ] Estendere la copertura con associazioni e geometrie sufficienti; mantenere separati sviluppo/calibrazione/test.
- [ ] Eseguire confronti W0/G0/S-separata/S-accumulo/P-accumulo e DA/MoGE con budget e provenienza dichiarati, secondo la [roadmap](ROADMAP.md).
- [ ] Valutare il contributo del peso geometrico, costi, fallimenti e incertezza senza dedurre benefici dai controlli zero.
- [ ] Completare le schede della mappa con Marco; preservare i contenuti manuali e usare spiegazioni comprensibili alla giuria.

## Esplicitamente rinviato

- [ ] Revisione dei filtri di fusione: simmetrie/ambiguità e viste parziali/supporto bidirezionale. Riprendere soltanto su indicazione di Marco. Le soglie attuali sono provvisorie, non prescrizioni dei paper.

## Manutenzione permanente

- Memoria aggiornata dopo novità; storico distinto dalle istruzioni correnti.
- README unico ingresso, collegamenti validi, dipendenze esterne dichiarate, nessun runner superato fra quelli correnti.
- Eseguire `python tools/check_repository.py` prima di pubblicare; non caricare pesi, accessi o nuovi dati voluminosi implicitamente.
