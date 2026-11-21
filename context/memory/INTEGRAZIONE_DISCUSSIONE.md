# Interfaccia geometrica e integrazione Whareformer

## Punto 3: prima implementazione autorizzata ed eseguita — 21 novembre 2026

Marco autorizza di procedere secondo il piano approvato iniziando dalle parti indipendenti dall'audit. Implementati allineamento DA→scena con fallimento esplicito, memoria pesata a stati senza vista fissa, separazione forma/collocazione e percorso esplicito dopo spostamento, FPS 4096 con provenienza, contratti del verificatore, baseline regressiva addestrabile e replay/adapter del coordinatore. [Dettagli, verifiche e limiti](IMPLEMENTAZIONE_PUNTO3_20261121.md); [guida software](../../integration_prototype/SCENE_MEMORY.md).

**Verificato localmente:** 105 casi, 103 superati e 2 saltati per motmetrics, inclusi 23 nuovi test tutti passati; nessuna inferenza neurale reale. Il verificatore principale non è addestrato: senza modello non si confermano/fondono ipotesi. Mancano evidenze validate di staticità, calibrazione sullo sviluppo, collegamento FPS al worker SuperFlex e validazione reale dopo spostamento. Il runner storico resta distinto e invariato nei suoi algoritmi; la nuova memoria non è già la pipeline sperimentale completa.

**Audit/HPC:** nessun accesso diretto o job in questa fase; stato live ignoto. Marco deve avviare `strumenti_hpc/esegui_controllo_hpc.bat` e `esegui_scarica_audit.bat`; scarico aggiornato per il job 783586, con accounting, hash e log anche parziali, nuova cartella a ogni tentativo. Poi interpretare gli esiti prima di training/ripresa. Nessun nuovo metodo principale, parametro calibrato, modifica della mappa o pubblicazione. Log e ricevuta in `outputs/point3_implementation_20261121/`.


## Passaggio corrente: ammissione geometrica — 21 novembre 2026

Leggere prima [RIPRESA_AMMISSIONE_GEOMETRICA_20261121.md](RIPRESA_AMMISSIONE_GEOMETRICA_20261121.md): discussione completa, decisioni/proposte distinte, regole nel codice, criticità, alternative di supervisione/validazione e prossimo passo. Marco sul punto 3, compagno sul 2; punti 1 e 4 dopo entrambi. Soglie/criterio di accettazione da apprendere; conservare viste parziali valide. Superato il rinvio storico dei gate; nessun nuovo modello, target o protocollo scelto e nessun training/modifica del codice in questa discussione. Memoria preparata per continuare con altro provider; nessun invio esterno o push eseguito.

Attenzione alle attività parallele: 782967 sostituito da 782990; 782968/782969 con dipendenza aggiornata, stato live non ricontrollato qui. Seguire STATO_LAVORO.md e ARRICCHIMENTO_COMPLETO_P01_20261121.md, non duplicare job. Le note di rinvio e attesa dei vecchi commenti sotto sono storiche e superate.


## Primo campione supervisionato pronto — 21 novembre 2026

[Esito e limiti](ARRICCHIMENTO_TRAINING_20261121.md): 446 query da 247 frame di P01_01, target/input oracle originali e geometria con archivio strettamente passato; 429 con geometria precedente della candidata corretta. Tutte query di tracce esistenti, nessuna Nuova track. Non è stata adottata una politica di fusione/riduzione, né avviato training. Prima dell'estensione ai 56 video servono gli ingressi originali mancanti; geometrie grandi sull'HPC, copia numerica/metadati locale verificata. 782875 concluso 0:0, nessun job di questo lavoro attivo.

## Mappa corrente — 21 novembre 2026

Struttura Rami paralleli e nuovi commenti confermati da Marco e applicati: 39 riquadri, 49 collegamenti. La sorgente corrente è [la mappa interattiva](../../mappa_interattiva/README.md). Superata la riserva storica della scrittura al solo Marco: l’assistente può applicare i testi dopo conferma esplicita. Vecchi commenti conservati, revisione scientifica successiva ancora aperta. Nessun cambiamento del metodo o nuovo esperimento.

## Direzione corrente — 16 novembre 2026

Richiesti entrambi i percorsi: fusione esterna e riaddestramento Whareformer. Vincolo esplicito: nessuna nuova etichettatura manuale, preferenza per training/target originali; superate le precedenti alternative condizionali e la proposta manuale. [Fattibilità, dati e distanze candidate](FATTIBILITA_DUE_INTEGRAZIONI_20261116.md), registro voce 81. Scelta finale e protocollo aperti; prima verificare provenienza oracle/geometria e costo. Nessuna nuova implementazione, calibrazione o run; filtri invariati, scrittura della mappa riservata a Marco.

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

Marco ha chiarito che confronto delle Super Quadrics per l'associazione e ricostruzione aggiornata della track sono due componenti dello stesso sistema. Il lavoro del collega rende disponibili associazioni/osservazioni; il nostro aggiunge confronto causale, accumulo e ritorno della forma al matcher.

L'associazione di un'osservazione a una track non implica che la sua nuvola sia stata ammessa alla fusione. Il prototipo applica filtri di registrazione provvisori: nel pilota acquisito tutte le fusioni successive sono state respinte. Questo non dimostra che le associazioni fossero errate, né che l'oggetto in pose diverse sia irriconoscibile.

La revisione dei filtri è stata richiesta e poi esplicitamente rinviata da Marco. Nel frattempo si completa il frontend già approvato senza cambiare questa parte del metodo. [Ciclo](ROADMAP_CICLO_GEOMETRICO.md), [attività](TODO.md), [audit dei rifiuti](../archive/RIPRESA_HPC_20261114.md).

Le discussioni e proposte precedenti sono conservate nell'[archivio](README.md) e nel [registro decisioni](REGISTRO_DECISIONI.md). La nuova run completa dimostra sette fusioni ammesse con uso futuro, senza miglioramento tracking; accuratezza fisica e generalizzazione rimangono da validare.
