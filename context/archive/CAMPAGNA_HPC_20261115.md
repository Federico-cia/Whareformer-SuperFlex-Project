# Campagna HPC estesa — 15 novembre 2026

## Campagna estesa conclusa — 15 novembre 2026

[Resoconto e output](RISULTATI_CAMPAGNA_HPC_20261115.md). Tutte le 29 configurazioni completate e valutate su 33310 frame/110590 osservazioni; nessuna assegnazione diversa da W0 e metriche identiche (IDF1 73.269735%, mPCL 70.465504%). Quattro controlli zero esatti, nessun timeout/errore di aggiornamento/worker fallito o richiesta pendente.

764678 COMPLETED 0:0 (4h13m00s), 764679 COMPLETED 0:0 (3h54m41s), riepilogo 765084 COMPLETED 0:0 (42s). Preflight/geometria/bundle già conclusi; nessun job della campagna attivo o in attesa. Nuvole/forme per tutte le 446 osservazioni pronte in entrambe le sorgenti. Per ogni variante con accumulo: DA 23 inizializzazioni/31 fusioni/392 rifiuti; MoGE 23/40/383. SuperFlex della memoria 54/63 pronte per variante, ripetizioni non indipendenti.

Report e accounting finali acquisiti localmente in outputs/campaign_20261115_v1/final_reports/; grandi tracce, nuvole e mesh di tutte le varianti ancora sull'HPC in ~/cv_project/campaign_20261115_v1/. Prossimo passo: analizzare margini, distanze, copertura di casi difficili e qualità delle fusioni. Nessun metodo selezionato né modifica dei filtri; revisione ancora rinviata. Non rilanciare i job conclusi.

## Preparazione e avvio — registro storico

Marco richiede una grande run e autorizza esplicitamente «prepara e avvia dopo i controlli». Campagna avviata; risultati finali ancora pendenti. Le proposte precedenti diventano esecuzione soltanto nel perimetro qui definito; revisione dei filtri ancora rinviata.

## Scopo e dati

Rigenerare geometria DA/MoGE su un campione esteso e confrontare l'influenza delle forme separate, dei punti accumulati e di SuperFlex accumulato. Ogni tracker mantiene tutta la sequenza ufficiale P01_01: 33310 frame, 110590 osservazioni, fps 60, valutazione originale fino al frame 99135. È sviluppo/train, non test indipendente né ricerca di un risultato favorevole.

Campione congelato prima delle inferenze: **247 frame, 446 osservazioni** (contro 38/71 nella prima run), tutte le disponibilità ammissibili del frammento RGB già acquisito, sotto il limite previsto di 250 frame. Scansionate 41070 annotazioni VISOR, recuperati 971 JPEG completi; corrispondenze esatte con ID/nome/box nel medesimo frame ufficiale. Esclusi alias temporali e frame privi delle feature baseline. Categorie dalla politica già usata, maschere almeno 128 pixel. Nessuna selezione da risultati dei modelli o da identità di track predette.

Il controllo sul bundle è concluso: **446 osservazioni pronte per tutte e quattro le rappresentazioni**, 892 nuvole DA/MoGE e 892 ricostruzioni SuperFlex delle osservazioni, su 247 frame. Feature baseline byte-identiche al riferimento. Copertura geometrica 0.4033% delle 110590 osservazioni: ampliamento di circa 6.28 volte, ancora sparso. La soglia preventiva di almeno 300 nuvole pronte per ciascuna sorgente è superata; nessun fallimento di rappresentazione nell’export. Campione di disponibilità: non rappresentativo di tutti gli oggetti/video; restano viste dipendenti, scala/identità fisica non certificate.

Riusati byte per byte feature ufficiali DINOv2/PCA/XYZ e checkpoint Whareformer. Rigenerati dalle immagini selezionate profondità DA, mappe MoGE, nuvole su pixel validi comuni e forme SuperFlex per osservazione; nuove SuperFlex dopo ogni aggiornamento ammesso della memoria. Nessun nuovo DINOv2/PCA/XYZ dalle immagini, nessun training, modello sostitutivo, MVS o download esteso implicito. RGB/maschere/camera, config originali e pesi esistenti verificati con hash.

## Matrice congelata: 29 configurazioni

| Gruppo | Numero | Configurazione |
|---|---:|---|
| W0 | 1 | Baseline, geometria disabilitata |
| G0 | 2 | DA e MoGE, aggiornamenti diagnostici a peso zero |
| S-accumulo zero | 2 | DA e MoGE, ciclo SuperFlex a peso zero |
| Forme separate attive | 8 | DA/MoGE × peso 0.1/1 × distanza neutra 0/0.1 |
| Punti accumulati attivi | 8 | Stessa griglia |
| SuperFlex accumulato attivo | 8 | Stessa griglia |

Griglia finita di sviluppo, fissata prima dei nuovi risultati, senza selezione automatica del vincitore. Seed 0, tracker CPU con un thread, modelli e memorie indipendenti, capacità forme separate 2. Stesso budget geometrico dei candidati: massimo quattro viste/2048 punti per vista, osservazioni limitate a 12000 punti. Registrazione e soglie di ammissione **invariate**.

Aggiunta sola telemetria: logits prima/dopo, probabilità e margini delle prime due colonne per le righe geometricamente confrontabili. Sono confronti sullo stesso stato corrente della singola run; dopo divergenze di storia non vanno descritti come una baseline W0 indipendente. Assegnazioni effettive esportate e confronto con W0 nel riepilogo finale. Punti predetti dalle completazioni mai reinseriti nella memoria osservata; tutte le query precedono gli aggiornamenti del frame.

## Controlli, coda e job inviati

**Preflight 764670 COMPLETED 0:0, 1m35s:** 76 test HPC eseguiti/passati senza skip, asset/codice/checkpoint verificati, selezione congelata. Locale: 76 casi del pacchetto, 74 passati e due skip motmetrics; tre test aggiuntivi del gestore invii raggruppati passati localmente. Questi tre non sono compresi nei 76 del preflight remoto.

La prima richiesta di array è stata respinta con QOSMaxSubmitJobPerUserLimit. Il limite osservato è quattro job inviati, due attivi, 12 CPU e due GPU per utente, massimo 24 ore/job. Nessun array di confronti è partito. Conservati i due invii già accettati e corretto solo il raggruppamento: un job esegue serialmente 19 configurazioni CPU, un altro dieci configurazioni che richiedono SuperFlex/GPU. La storia del rifiuto è nella ricevuta. Nessun algoritmo o trial cambiato.

| Job | Stadio | Ultimo stato acquisito |
|---|---|---|
| 764670 | Test, asset e selezione | COMPLETED 0:0 |
| 764674 | Geometria DA → MoGE → nuvole → SuperFlex → export | COMPLETED 0:0, 11m38s |
| 764675 | Bundle completo, hash e copertura pronta | COMPLETED 0:0, 1m41s |
| 764678 | 19 configurazioni CPU | RUNNING |
| 764679 | 10 configurazioni con SuperFlex reale | RUNNING |
| Da acquisire | Riepilogo e controllo zero vs W0 | Inviato automaticamente dal primo gruppo terminato, dipendenza afterany su entrambi |

Questi sono stati osservati, non monitoraggio in tempo reale. Leggere la ricevuta remota e sacct per gli stati successivi; non reinviare i job. Il riepilogo non ha ancora un ID e non è dichiarato già in coda. Una pausa/errore non viene trasformata in successo; la continuazione degli altri trial consente di acquisire risultati e fallimenti separatamente.

Limiti di risorse: geometria un GPU per massimo due ore; gruppo GPU uno per massimo 7h30, totale massimo **9.5 ore GPU**; gruppo CPU 14h15. Ogni configurazione ha timeout 45 minuti. Un solo gruppo CPU e un solo gruppo GPU possono procedere contemporaneamente, entro i due job attivi consentiti. I limiti non sono stime di durata effettiva o garanzie di completamento.

## Percorsi e ripresa

Radice remota: `~/cv_project/campaign_20261115_v1/`.

- Specifica immutabile: campaign.json; ingressi congelati inputs/manifest.json, inputs/selection.json, inputs/config.json.
- Geometria e ambiente per stadio: geometry/; bundle e copertura effettiva: bundle/, bundle_receipt.json.
- Configurazioni, tracce e metriche per variante: configs/, runs/<nome>/; memoria finale e ricostruzioni: runs/<nome>/inference/<nome>_memory/, caches/<nome>/.
- Log generali: logs/preflight_764670_4294967294.out/.err, logs/geometry_764674_4294967294.out/.err, logs/build_764675_4294967294.out/.err, logs/cpu_group_764678.out/.err, logs/gpu_group_764679.out/.err.
- Ricevuta invii: submitted_jobs.json; esiti/timeout: group_cpu_results.jsonl e group_gpu_results.jsonl; riepilogo atteso campaign_summary.json e comparison/.

Prima leggere stato/log della geometria; poi bundle_receipt e log dei gruppi. Se un predecessore fallisce, i job afterok restano in attesa: diagnosticare prima di qualsiasi rilancio. A gruppi terminati acquisire l'ID del riepilogo dalla ricevuta, verificare tutti i 29 stati e la parità dei controlli zero; non trattare run incomplete come risultati completi. Successivamente verificare qualità fisica e casi di errore, senza usare track/categorie come GT certificata o scegliere sul test.

Documenti locali: [ricevuta e fotografia dei job](../evidence/ASSET_ESTERNI.md#asset-239a57b3dd1e), [specifica](../evidence/ASSET_ESTERNI.md#asset-ddb057967934), [selezione](../evidence/ASSET_ESTERNI.md#asset-8cbaa2b1ea3c), [bundle verificato](../evidence/ASSET_ESTERNI.md#asset-7b6cc28d19ed), [pacchetto verificato](../evidence/ASSET_ESTERNI.md#asset-ec79434afba2), [analisi precedente](VALUTAZIONE_PRIMA_RUN_20261114.md).

Worktree corrente shared_exports/handoff_ai_20261114, branch run/hpc-campaign-20261115, base GitHub 61731ff. Codice e metadati leggeri sono condivisibili; input numerici completi, RGB, pesi e accessi rimangono esterni al clone. Le revisioni manuali della mappa e i contributi del collega sono preservati.

Pubblicazione di codice e ricevute verificata su main al commit 27f58d8a2bd238fb02af755498d6d21114adf925; nessun risultato finale della campagna ancora dichiarato.

Ultimo avanzamento acquisito: W0 (indice CPU 0) concluso con codice 0 e pipeline completed; Sacc_da_zero osservato a 11432/33310 frame. I gruppi 764678/764679 restano RUNNING. Dato parziale, nessuna conclusione comparativa.
