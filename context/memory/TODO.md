# Attività correnti

## Prima run completa conclusa — 14 novembre 2026

Job 764454 COMPLETED 0:0 (8m40s), audit/valutazione 764474 COMPLETED 0:0 (53s); nessun job di questa run attivo/in attesa. Tutti i 33310 frame e 110590 osservazioni del protocollo ufficiale P01_01 elaborati (937–98099; metadati video 99135). Non tutti i RGB: feature/PCA/XYZ e 71 geometrie su 38 frame riusati con hash, nuova inferenza Whareformer e 25 nuove SuperFlex sugli stati ammessi. Copertura geometrica 0.0642% delle osservazioni.

S-accumulo DA, peso 0.1 non calibrato, filtri invariati: 18 inizializzazioni, 7 fusioni ammesse, 46 rifiuti, nessun errore o richiesta pendente. 695 logits modificati; 76 confronti futuri usano forme da fusioni. Memoria finale: 18 track, 38732 punti osservati, provenienza verificata; accuratezza fisica delle fusioni non certificata. Assegnazioni identiche alla baseline: 52 track, IDF1 73.269735%, mPCL 70.465504%, nessun miglioramento.

[Resoconto verificato ed evidenze](../evidence/full_video_20261114/REPORT.md).

Percorso HPC `~/cv_project/full_video_20261114_v1/`; log `cv_full_active_764454.out/.err`, `cv_full_audit_764474.out/.err`, `tests_764454.log`; output `run_764454/`, `cache_764454/`, `final_evaluation/`, `final_comparison/`, `audit/`. Tutti gli output scaricati in `outputs/full_video_20261114/results/` nella cartella locale. La valutazione iniziale a 98099 è superata da quella finale con orizzonte originale 99135; nessuna nuova inferenza per correggerla.

Prossimo passo: discutere qualità/validazione indipendente delle fusioni e copertura prima di conclusioni di efficacia; frontend RGB rigenerato e calibrazione/test rimangono aperti. Revisione dei filtri ancora rinviata: non avviarla automaticamente. Prima esecuzione operativa chiusa; non rilanciare job conclusi. Pubblicazione verificata su main: 8694e4b (codice ed evidenze della run).

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
