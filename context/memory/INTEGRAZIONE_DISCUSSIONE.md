# Integrazione: decisione corrente

## Campagna estesa avviata — 15 novembre 2026

Marco autorizza preparazione e avvio dopo i controlli. [Specifica, limiti e ripresa](CAMPAGNA_HPC_20261115.md): 247 frame/446 osservazioni congelati prima dell'inferenza, geometria DA/MoGE rigenerata e 29 configurazioni sull'intera storia P01_01. Feature/PCA/XYZ ufficiali riusati; nessun nuovo training o filtro modificato. Campagna di sviluppo, non test held-out o beneficio assunto.

Preflight 764670 COMPLETED 0:0 (1m35s), 76 test tutti passati. 764674 COMPLETED 0:0 (11m38s), 764675 COMPLETED 0:0 (1m41s): tutte le 446 osservazioni hanno nuvole e forme pronte per DA/MoGE, feature baseline byte-identiche. 764678 e 764679 RUNNING per 19 trial CPU e dieci GPU. Riepilogo da inviare automaticamente al termine del primo gruppo, con dipendenza su entrambi. Risultati finali ancora pendenti. Ricevuta/stati remoti in ~/cv_project/campaign_20261115_v1/submitted_jobs.json e logs/; snapshot locale outputs/campaign_20261115_v1/.

Limite QoS rilevato: quattro job inviati/due attivi. Primo array respinto, nessun trial partito da quell'array; adattato il solo raggruppamento, senza duplicare i job esistenti. Concorrenza attuale un gruppo CPU/un gruppo GPU, massimo 9.5 ore GPU complessive. Non reinviare i job; acquisire prima stato e output. Revisione dei filtri ancora esplicitamente rinviata.

## Priorità corrente — esecuzione completa prima dei confronti

Il mandato più recente richiede una prima run fino alla fine della sequenza ufficiale P01_01 con geometria attiva, cache dichiarate e SuperFlex sugli aggiornamenti ammessi. Run 764454 conclusa e audit 764474 superato: sette fusioni ammesse, 25 nuove ricostruzioni e uso futuro verificato; nessun miglioramento tracking. Dettagli in STATO_LAVORO.md e REGISTRO_CRITICITA_PIPELINE.md. Frontend RGB rigenerato, copertura estesa e confronti/ottimizzazione restano lavori distinti; nessuno sostituisce o blocca la verifica operativa completata. Revisione dei filtri ancora rinviata. Le fasi precedenti non implicano una nuova approvazione per modificare tali filtri.

Marco ha chiarito che confronto delle Super Quadrics per l'associazione e ricostruzione aggiornata della track sono due componenti dello stesso sistema. Il lavoro del collega rende disponibili associazioni/osservazioni; il nostro aggiunge confronto causale, accumulo e ritorno della forma al matcher.

L'associazione di un'osservazione a una track non implica che la sua nuvola sia stata ammessa alla fusione. Il prototipo applica filtri di registrazione provvisori: nel pilota acquisito tutte le fusioni successive sono state respinte. Questo non dimostra che le associazioni fossero errate, né che l'oggetto in pose diverse sia irriconoscibile.

La revisione dei filtri è stata richiesta e poi esplicitamente rinviata da Marco. Nel frattempo si completa il frontend già approvato senza cambiare questa parte del metodo. [Ciclo](ROADMAP_CICLO_GEOMETRICO.md), [attività](TODO.md), [audit dei rifiuti](../archive/RIPRESA_HPC_20261114.md).

Le discussioni e proposte precedenti sono conservate nell'[archivio](README.md) e nel [registro decisioni](REGISTRO_DECISIONI.md). La nuova run completa dimostra sette fusioni ammesse con uso futuro, senza miglioramento tracking; accuratezza fisica e generalizzazione rimangono da validare.
