# Attività correnti

## Punti importanti da discutere e validare

- [ ] **Architettura dell'integrazione della forma — decisione condivisa con il compagno ancora aperta:** discutere sia come la rappresentazione/distanza di forma entra nei calcoli di associazione sia con quale influenza. Distinguere correzione esterna attuale dei logits con peso/distanza neutra da calibrare sullo sviluppo; apprendimento supervisionato di pochi parametri di fusione con reti congelate; adattamento/riaddestramento della rete per combinare anche la geometria. Chiarire rappresentazione/distanza, punto d'integrazione, mancanti/New Track, dati con associazioni verificate, obiettivo di apprendimento e valutazione nel ciclo causale completo. Peso 0.1/1 esplorato, non ottimale dimostrato. La proposta dell'assistente di fusione appresa non è approvata: Marco vuole prima discuterne con il compagno. Nessuna nuova implementazione, calibrazione o run avviata; predisposta soltanto nota da inserire manualmente in B12.

- [ ] **Collocazione e aggiornamento della forma nella scena 3D — preoccupazione prioritaria di Marco:** discutere fattibilità e difficoltà di conservare una ricostruzione con dimensioni, rotazione e posizione coerenti con lo spazio della scena e con l'XYZ della traccia, aggiornabile mediante nuovi punti. Distinguere ripristino della normalizzazione SuperFlex, riferimento camera, riferimento della memoria oggetto e riferimento scena; verificare compatibilità di scala e trasformazioni, movimento dell'oggetto e conservazione della coerenza dopo gli aggiornamenti. L'XYZ da solo non determina scala e orientamento; una fusione ammessa o un descrittore invariante non validano la collocazione nella scena. Separare questa discussione da scelta del descrittore e gate di ammissione. Definire il controllo minimo di fattibilità e i limiti prima di assumere disponibile una memoria 3D collocata correttamente. Solo tema da discutere: nessun nuovo sviluppo o esperimento avviato. Vedi C13 in [REGISTRO_CRITICITA_PIPELINE.md](REGISTRO_CRITICITA_PIPELINE.md).

- [ ] **Forma per confronto e memoria 3D nella scena — chiarimento di Marco durante B07:** discutere perdita d'informazione del descrittore D2 e rimozione della dimensione assoluta mediante normalizzazione. Marco vuole considerare la ricostruzione anche come geometria dell'oggetto collocata nello spazio della scena, accanto all'XYZ ricordato dalla traccia, non soltanto come segnale di matching. Distinguere descrittore normalizzato e geometria conservata con trasformazione inversa; verificare scala compatibile con scena/XYZ, riferimento, ancoraggio e orientamento quando stimabile. Non confondere invarianza del confronto con disponibilità della posa per collocare la forma. Requisiti, valutazione e perimetro da discutere: nessun nuovo modulo o risultato già acquisito.

- [ ] **Ammissione dei punti — decisione da discutere con il compagno di gruppo:** discutere approfonditamente e testare i criteri con cui una nuvola associata a una traccia viene ammessa nella memoria geometrica. Marco ribadisce durante E22 che questo passaggio cruciale non va presentato come scelta metodologica definitiva concordata: PCA/multistart+ICP e gate attuali sono un candidato provvisorio. Descrivere chiaramente in E22 e B16 associazione, allineamento, controlli e conseguenze di ammissione/rifiuto. Alternative discusse: fusione dopo allineamento senza ulteriori gate (rischio da valutare), revisione dei criteri per simmetrie/viste parziali e confronto con forme separate senza fusione. Valutare supporto, residui, ambiguità e scala; controllare sia fusioni errate ammesse sia fusioni utili respinte con evidenza indipendente, senza premiare il solo numero di ammissioni. **Priorità di discussione e validazione, non avvio immediato:** il rinvio operativo resta valido; nessuna soglia, codice o job modificati. Riferimento: C05 in [REGISTRO_CRITICITA_PIPELINE.md](REGISTRO_CRITICITA_PIPELINE.md).

## Revisione guidata della mappa — 15 novembre 2026

- [ ] Residui verificati nel JSON dopo la compilazione manuale: nove nodi B08/B09/B10/B11/B13/B15/B17/B18/B19 e 13 frecce E07/E13/E14/E16/E17/E19/E24/E28/E30/E31/E32/E33/E34 ancora segnaposto. Completare anche «[da espandere]» nelle alternative E10; per E21 indicare eventualmente «-» nel campo miglioramenti vuoto. 10 nodi e 21 frecce già commentati, senza attestazione automatica di correttezza scientifica di tutti i testi.

- [x] Ricostruire contesto e diagnosticare tutte le 19 schede di nodo/34 frecce; [checklist separata](REVISIONE_MAPPA_20261115.md), senza modificare la mappa.
- [ ] Marco riscrive e salva i commenti; l'assistente chiarisce contenuti, evidenze e limiti e verifica le formulazioni discusse. Priorità proposta: input → posizione/camera → forma → matching → aggiornamento/memoria. Questa modalità supera per la revisione corrente le precedenti attività di compilazione automatica, incluse le richieste storiche tra parentesi quadre. Nessun filtro o metodo da cambiare nell'ambito della revisione editoriale.

## Campagna estesa conclusa — 15 novembre 2026

[Resoconto e output](../evidence/campaign_20261115_v1/REPORT_FINALE.md). Tutte le 29 configurazioni completate e valutate su 33310 frame/110590 osservazioni; nessuna assegnazione diversa da W0 e metriche identiche (IDF1 73.269735%, mPCL 70.465504%). Quattro controlli zero esatti, nessun timeout/errore di aggiornamento/worker fallito o richiesta pendente.

764678 COMPLETED 0:0 (4h13m00s), 764679 COMPLETED 0:0 (3h54m41s), riepilogo 765084 COMPLETED 0:0 (42s). Preflight/geometria/bundle già conclusi; nessun job della campagna attivo o in attesa. Nuvole/forme per tutte le 446 osservazioni pronte in entrambe le sorgenti. Per ogni variante con accumulo: DA 23 inizializzazioni/31 fusioni/392 rifiuti; MoGE 23/40/383. SuperFlex della memoria 54/63 pronte per variante, ripetizioni non indipendenti.

Report e accounting finali acquisiti localmente in outputs/campaign_20261115_v1/final_reports/; grandi tracce, nuvole e mesh di tutte le varianti ancora sull'HPC in ~/cv_project/campaign_20261115_v1/. Prossimo passo: analizzare margini, distanze, copertura di casi difficili e qualità delle fusioni. Nessun metodo selezionato né modifica dei filtri; revisione ancora rinviata. Non rilanciare i job conclusi.

## Avvio della campagna — stato storico superato

Marco autorizza preparazione e avvio dopo i controlli. [Specifica, limiti e ripresa](CAMPAGNA_HPC_20261115.md): 247 frame/446 osservazioni congelati prima dell'inferenza, geometria DA/MoGE rigenerata e 29 configurazioni sull'intera storia P01_01. Feature/PCA/XYZ ufficiali riusati; nessun nuovo training o filtro modificato. Campagna di sviluppo, non test held-out o beneficio assunto.

Preflight 764670 COMPLETED 0:0 (1m35s), 76 test tutti passati. 764674 COMPLETED 0:0 (11m38s), 764675 COMPLETED 0:0 (1m41s): tutte le 446 osservazioni hanno nuvole e forme pronte per DA/MoGE, feature baseline byte-identiche. 764678 e 764679 RUNNING per 19 trial CPU e dieci GPU. Riepilogo da inviare automaticamente al termine del primo gruppo, con dipendenza su entrambi. Risultati finali ancora pendenti. Ricevuta/stati remoti in ~/cv_project/campaign_20261115_v1/submitted_jobs.json e logs/; snapshot locale outputs/campaign_20261115_v1/.

Limite QoS rilevato: quattro job inviati/due attivi. Primo array respinto, nessun trial partito da quell'array; adattato il solo raggruppamento, senza duplicare i job esistenti. Concorrenza attuale un gruppo CPU/un gruppo GPU, massimo 9.5 ore GPU complessive. Non reinviare i job; acquisire prima stato e output. Revisione dei filtri ancora esplicitamente rinviata.

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
