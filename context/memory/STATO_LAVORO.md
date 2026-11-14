# Stato corrente — 14 novembre 2026

## Prima run completa conclusa — 14 novembre 2026

Job 764454 COMPLETED 0:0 (8m40s), audit/valutazione 764474 COMPLETED 0:0 (53s); nessun job di questa run attivo/in attesa. Tutti i 33310 frame e 110590 osservazioni del protocollo ufficiale P01_01 elaborati (937–98099; metadati video 99135). Non tutti i RGB: feature/PCA/XYZ e 71 geometrie su 38 frame riusati con hash, nuova inferenza Whareformer e 25 nuove SuperFlex sugli stati ammessi. Copertura geometrica 0.0642% delle osservazioni.

S-accumulo DA, peso 0.1 non calibrato, filtri invariati: 18 inizializzazioni, 7 fusioni ammesse, 46 rifiuti, nessun errore o richiesta pendente. 695 logits modificati; 76 confronti futuri usano forme da fusioni. Memoria finale: 18 track, 38732 punti osservati, provenienza verificata; accuratezza fisica delle fusioni non certificata. Assegnazioni identiche alla baseline: 52 track, IDF1 73.269735%, mPCL 70.465504%, nessun miglioramento.

[Resoconto verificato ed evidenze](../evidence/full_video_20261114/REPORT.md).

Percorso HPC `~/cv_project/full_video_20261114_v1/`; log `cv_full_active_764454.out/.err`, `cv_full_audit_764474.out/.err`, `tests_764454.log`; output `run_764454/`, `cache_764454/`, `final_evaluation/`, `final_comparison/`, `audit/`. Tutti gli output scaricati in `outputs/full_video_20261114/results/` nella cartella locale. La valutazione iniziale a 98099 è superata da quella finale con orizzonte originale 99135; nessuna nuova inferenza per correggerla.

Prossimo passo: discutere qualità/validazione indipendente delle fusioni e copertura prima di conclusioni di efficacia; frontend RGB rigenerato e calibrazione/test rimangono aperti. Revisione dei filtri ancora rinviata: non avviarla automaticamente. Prima esecuzione operativa chiusa; non rilanciare job conclusi. Pubblicazione verificata su main: 8694e4b (codice ed evidenze della run).

## Vincoli e ripresa

Le precedenti prove zero e i risultati dei piloti sono conservati nelle [evidenze](../evidence/README.md) e nell'[archivio](../archive/). Le note storiche di zero fusioni si riferiscono ai piloti precedenti, non alla nuova run completa.

Preservare query prima degli aggiornamenti, punti osservati distinti da completazioni e riferimenti camera/scena/normalizzazione. Reti congelate. Non presentare l'ammissione dei gate come verifica fisica indipendente; mantenere distinta efficacia tracking e funzionamento software. [Registro critico](REGISTRO_CRITICITA_PIPELINE.md).

Codice corrente nel worktree locale shared_exports/handoff_ai_20261114, branch run/full-video-20261114; documentazione corrente distinta dalla storia e README unico ingresso. Dati completi e checkpoint sono esterni al clone.
