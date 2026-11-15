# Roadmap corrente

## Campagna estesa conclusa — 15 novembre 2026

[Resoconto e output](../evidence/campaign_20261115_v1/REPORT_FINALE.md). Tutte le 29 configurazioni completate e valutate su 33310 frame/110590 osservazioni; nessuna assegnazione diversa da W0 e metriche identiche (IDF1 73.269735%, mPCL 70.465504%). Quattro controlli zero esatti, nessun timeout/errore di aggiornamento/worker fallito o richiesta pendente.

764678 COMPLETED 0:0 (4h13m00s), 764679 COMPLETED 0:0 (3h54m41s), riepilogo 765084 COMPLETED 0:0 (42s). Preflight/geometria/bundle già conclusi; nessun job della campagna attivo o in attesa. Nuvole/forme per tutte le 446 osservazioni pronte in entrambe le sorgenti. Per ogni variante con accumulo: DA 23 inizializzazioni/31 fusioni/392 rifiuti; MoGE 23/40/383. SuperFlex della memoria 54/63 pronte per variante, ripetizioni non indipendenti.

Report e accounting finali acquisiti localmente in outputs/campaign_20261115_v1/final_reports/; grandi tracce, nuvole e mesh di tutte le varianti ancora sull'HPC in ~/cv_project/campaign_20261115_v1/. Prossimo passo: analizzare margini, distanze, copertura di casi difficili e qualità delle fusioni. Nessun metodo selezionato né modifica dei filtri; revisione ancora rinviata. Non rilanciare i job conclusi.

## Avvio della campagna — stato storico superato

Marco autorizza preparazione e avvio dopo i controlli. [Specifica, limiti e ripresa](CAMPAGNA_HPC_20261115.md): 247 frame/446 osservazioni congelati prima dell'inferenza, geometria DA/MoGE rigenerata e 29 configurazioni sull'intera storia P01_01. Feature/PCA/XYZ ufficiali riusati; nessun nuovo training o filtro modificato. Campagna di sviluppo, non test held-out o beneficio assunto.

Preflight 764670 COMPLETED 0:0 (1m35s), 76 test tutti passati. 764674 COMPLETED 0:0 (11m38s), 764675 COMPLETED 0:0 (1m41s): tutte le 446 osservazioni hanno nuvole e forme pronte per DA/MoGE, feature baseline byte-identiche. 764678 e 764679 RUNNING per 19 trial CPU e dieci GPU. Riepilogo da inviare automaticamente al termine del primo gruppo, con dipendenza su entrambi. Risultati finali ancora pendenti. Ricevuta/stati remoti in ~/cv_project/campaign_20261115_v1/submitted_jobs.json e logs/; snapshot locale outputs/campaign_20261115_v1/.

Limite QoS rilevato: quattro job inviati/due attivi. Primo array respinto, nessun trial partito da quell'array; adattato il solo raggruppamento, senza duplicare i job esistenti. Concorrenza attuale un gruppo CPU/un gruppo GPU, massimo 9.5 ore GPU complessive. Non reinviare i job; acquisire prima stato e output. Revisione dei filtri ancora esplicitamente rinviata.

## Priorità corrente — esecuzione completa prima dei confronti

Il mandato più recente richiede una prima run fino alla fine della sequenza ufficiale P01_01 con geometria attiva, cache dichiarate e SuperFlex sugli aggiornamenti ammessi. Run 764454 conclusa e audit 764474 superato: sette fusioni ammesse, 25 nuove ricostruzioni e uso futuro verificato; nessun miglioramento tracking. Dettagli in STATO_LAVORO.md e REGISTRO_CRITICITA_PIPELINE.md. Frontend RGB rigenerato, copertura estesa e confronti/ottimizzazione restano lavori distinti; nessuno sostituisce o blocca la verifica operativa completata. Revisione dei filtri ancora rinviata. Le fasi precedenti non implicano una nuova approvazione per modificare tali filtri.

| Fase | Stato | Criterio di avanzamento |
|---|---|---|
| Contratto dati e consegna collega | Verificati | Mapping e hash controllati, due alias esclusi |
| Matcher causale e aggiornamento geometrico | Implementati e verificati | Memoria precedente alle query; controllo zero esatto |
| SuperFlex differita e ritorno al matcher | Verificati nella prima run completa | 25 nuove ricostruzioni, sette fusioni ammesse e uso futuro verificato; accuratezza fisica aperta |
| Varianti, valutatore e comando comune | Collegati e verificati | Nove varianti zero completate e valutate |
| Frontend da immagini | Rigenerazione parziale, cache usata nella run completa | Cache verificata; asset e rigenerazione ancora da completare |
| Copertura, calibrazione e test separato | Pendenti | Input sufficienti, protocollo e limiti espliciti |
| Conclusioni e consegna finale | Pendenti | Prima run a peso non nullo chiusa, metriche invariate; validazione generale pendente |

Il metodo è descritto nel [ciclo geometrico](ROADMAP_CICLO_GEOMETRICO.md). Per i dettagli dello step attivo: [piano frontend](PIANO_FRONTEND_UNIFICATO_20261114.md) e [avanzamento](FRONTEND_AVANZAMENTO_20261114.md). Le attività sono in [TODO](TODO.md); la storia metodologica resta nel [registro decisioni](REGISTRO_DECISIONI.md) e nell'[archivio](README.md).

**Vincolo corrente:** la revisione dei filtri di fusione è rinviata. Non trasformare la calibrazione successiva in un'autorizzazione a modificare questi filtri ora. Nessun beneficio tracking con peso 0.1; fusioni eseguite e provenienza verificata, accuratezza fisica non certificata.

Due persone, circa due ore al giorno ciascuna, scadenza 23 novembre; Marco geometria e collega tracking. Privilegiare controlli piccoli e informativi senza ripetere i job già conclusi.
