# Sviluppo del ciclo geometrico Whareformer–SuperFlex

## Spazio recuperato e nuova ripresa — 21 novembre 2026

**Verifica successiva delle 23:51:38:** 783790/783791 entrambi RUNNING a 3m56s su gnode03; superato l'arresto precedente nelle nuvole, ora blocco 8 con 309/312 report DA/MoGE e blocco 9 con 286/288. Quota 41.19/46.56 GiB (circa 5.37 GiB liberi), otto blocchi ancora conclusi; SuperFlex dei nuovi blocchi non ancora verificata.

Marco autorizza pulizia e, esplicitamente, copia/archiviazione dei tracciati conclusi sul PC. Verificati due volte 377 file (5.47 GiB) e conservati in archivio locale di 636594519 byte con ledger/hash, prima di rimuovere le sole copie remote. Runtime, geometrie e input attuali preservati. Quota scesa da 46.35 a 40.88 GiB su 46.56; archivio da NON eliminare. [Operazioni, percorsi e ripristino](PULIZIA_E_RIPRESA_HPC_20261121.md).

**Job correnti:** 783790/783791, rami 0/1 dai blocchi 8/9, RUNNING su gnode03 al controllo 23:49:54 (2m11s). Preflight quota positivo anche sul nodo di calcolo. Otto blocchi conclusi a quel controllo. I tentativi 783750/751 sono falliti dopo MoGE anche su nodo diverso; 783782/783783 fermati prima delle inferenze per helper quota assente, poi corretto. Nessun precedente tentativo va considerato attivo.

Guard di quota a ogni blocco: riserva operativa 2 GiB/12000 file, stop esplicito codice 75 quando insufficiente; fallback nativo BeeGFS verificato. Tolta l'esclusione del nodo che non risolveva. Nessuna modifica scientifica. **Capacità ancora aperta:** costo misurato 0.64 GiB/blocco, estrapolazione circa 138 GiB/216 blocchi; la pulizia non basta a garantire completamento nella quota di 50 GB. Occorre compattare la conservazione senza perdere informazione necessaria o reperire capacità. Nessuna riduzione di copertura o sorgenti approvata in questa fase. Non promettere funzionamento ininterrotto notturno.


## HPC riavviato su richiesta di Marco — 21 novembre 2026, 23:23

Marco richiede «Fallo ripartire». Diagnosi e ripresa eseguite con accesso esistente autorizzato per l'azione: **783750 e 783751 RUNNING su gnode03**, rami 0/1 dai blocchi 8/9. **MoGE superato: 512/512 ready in entrambi**, DA già pronta, nuvole in costruzione. Ultimo controllo 23:23:51, rispettivamente 3m14s/3m08s; 8/216 blocchi ancora conclusi a quel momento. Catena automatica preesistente preservata, nessun duplicato o reset delle cache.

Escluso gnode02 dai job e successori come intervento controllato dopo quattro arresti osservati durante MoGE, senza pretendere diagnosi hardware conclusiva. Batch remoto salvato in backup e arricchito di log; dati/modelli/codice scientifico invariati. [Intervento, hash, log e ricevute](RIPARTENZA_HPC_20261121.md). Non reinviare mentre i rami sono in coda. SuperFlex dei nuovi blocchi e completamento integrale ancora da verificare; nessuna sorveglianza permanente avviata. Questo stato supera le precedenti note di coda vuota/run ferma. Audit e sviluppo punto 3 restano nello stato documentato.


## Audit acquisito; arricchimento fermo — 21 novembre 2026, esiti 23:01–23:06

Marco esegue gli script: **783586 COMPLETED 0:0, 16m53s**, sette hash verificati; 446 osservazioni, 438 allineamenti validi e nuvole locali finite, otto fit con alpha negativo. Confronto appaiato su 415 coppie: sovrapposizione mediana 3.27% grezza → 22.80% allineata (28.08% → 68.16% nel terzile di minore spostamento, non staticità certificata). 24 osservazioni con sole maschere del catalogo. Nessuna etichetta di fusione corretta ancora certificata: mantenere limiti di staticità, simmetrie ed errori condivisi. [Risultati, provenienza e interpretazione](RISULTATI_AUDIT_AMMISSIONE_20261121.md).

**Arricchimento:** coda vuota, 8/216 blocchi, nessun riepilogo finale; riprese 783490 e 783491 entrambe FAILED 1:0. Causa non identificata dai log disponibili. Aggiornata la diagnosi di sola lettura per questi job e per gli stadi parziali; prossimo intervento di Marco: `strumenti_hpc/esegui_diagnosi_hpc.bat`, poi leggere `esito_diagnosi.txt` prima di riprendere. Nessun accesso diretto HPC, invio o training dell'assistente. Le nuvole locali consentono di proseguire la preparazione dei dati da trasformazioni note senza attendere la run completa. Decisioni metodologiche approvate invariate.


## Punto 3: prima implementazione autorizzata ed eseguita — 21 novembre 2026

Marco autorizza di procedere secondo il piano approvato iniziando dalle parti indipendenti dall'audit. Implementati allineamento DA→scena con fallimento esplicito, memoria pesata a stati senza vista fissa, separazione forma/collocazione e percorso esplicito dopo spostamento, FPS 4096 con provenienza, contratti del verificatore, baseline regressiva addestrabile e replay/adapter del coordinatore. [Dettagli, verifiche e limiti](IMPLEMENTAZIONE_PUNTO3_20261121.md); [guida software](../../integration_prototype/SCENE_MEMORY.md).

**Verificato localmente:** 105 casi, 103 superati e 2 saltati per motmetrics, inclusi 23 nuovi test tutti passati; nessuna inferenza neurale reale. Il verificatore principale non è addestrato: senza modello non si confermano/fondono ipotesi. Mancano evidenze validate di staticità, calibrazione sullo sviluppo, collegamento FPS al worker SuperFlex e validazione reale dopo spostamento. Il runner storico resta distinto e invariato nei suoi algoritmi; la nuova memoria non è già la pipeline sperimentale completa.

**Audit/HPC:** nessun accesso diretto o job in questa fase; stato live ignoto. Marco deve avviare `strumenti_hpc/esegui_controllo_hpc.bat` e `esegui_scarica_audit.bat`; scarico aggiornato per il job 783586, con accounting, hash e log anche parziali, nuova cartella a ogni tentativo. Poi interpretare gli esiti prima di training/ripresa. Nessun nuovo metodo principale, parametro calibrato, modifica della mappa o pubblicazione. Log e ricevuta in `outputs/point3_implementation_20261121/`.


> **Aggiornamento 21 novembre 2026, sera:** il punto 3 (memoria geometrica e ammissione) ha un piano approvato che supera i gate provvisori descritti qui: profondità DA allineata alla scena, memoria a stati con forma separata dalla collocazione, verificatore appreso, fusione dopo spostamento come obiettivo. Vedere [SUPERVISIONE_AMMISSIONE_20261121.md](SUPERVISIONE_AMMISSIONE_20261121.md).

## Estensione completa P01_01 avviata — 21 novembre 2026

Aggiornamento: acquisizione corrente 782990 RUNNING, sostituisce 782967 cancellato per ottimizzare l'estrazione preservando il download. GPU sempre 782968/782969, dipendenza aggiornata dopo verifica. Archivio RGB completo, maschere ancora in elaborazione; nessuna inferenza GPU attestata nell'ultima osservazione. I riferimenti a 782967 nel seguente stato iniziale sono storici.

Su mandato di Marco, acquisizione completa RGB/verifica maschere in 782967 e due rami GPU 782968/782969 dipendenti; [configurazione e ripresa](ARRICCHIMENTO_COMPLETO_P01_20261121.md). Target tutte le 110590 osservazioni, riuso delle 446 geometrie e blocchi progressivi, mancanti/fallimenti espliciti. Non è training o validazione finale; nessun nuovo criterio di ammissione adottato. Esiti ancora da seguire, non rilanciare gli invii esistenti.

## Criteri di ammissione appresi — indicazione di Marco, 21 novembre 2026

Marco richiede che le soglie di accettazione siano apprese dai dati anziché imposte manualmente; obiettivo esplicito conservare viste parziali valide. Richiede spiegazione di parzialità, ambiguità, regole correnti e alternative di validazione con pro/contro. Direzione approvata: apprendimento del criterio; modello, target, loss e protocollo non ancora scelti. Nessun training, codice, soglia o job modificati.

Verificato cloud_memory.py/cloud_updater.py: trasformazione rigida senza stima scala; supporto in entrambe le direzioni almeno 0.65 entro 0.08R; q90 dell'80% più vicino non oltre 0.15R; alternative entro 5% dello score più epsilon rifiutate se differiscono oltre 15 gradi o spostano il centroide oltre 0.08R. Basta un gate fallito. R è il raggio RMS del riferimento fit; rapporto dei raggi registrato, non gate autonomo. Query separate dal fit, non viste indipendenti. Inizializzazione senza confronto con memoria precedente, con soli controlli di validità dell'input.

Proposte da discutere: classificatore leggero sulle diagnostiche, criterio condizionato alla sovrapposizione/affidabilità dei punti, oppure apprendimento dell'utilità della fusione. Evitare target ricavati dai gate stessi: replicherebbero le euristiche. Identità oracle non certifica posa o scala. Possibile supervisione automatica con trasformazioni note su dati sintetici/crop, verifiche RGB multivista e viste reali escluse; limiti rispettivi: domain gap, dipendenza da pose/visibilità/movimento, validazione geometrica reale non ancora disponibile. Vincolo precedente di nessuna nuova annotazione manuale preservato. Separare dati per oggetto/sequenza e valutare errori di ammissione/rifiuto e qualità della memoria; nessuna opzione già adottata. Fonti primarie consultate per fattibilità concettuale, non compatibilità EPIC verificata: PREDATOR (CVPR 2021, overlap appreso) e Deep Global Registration (CVPR 2020, affidabilità delle corrispondenze appresa).


## Priorità e divisione del lavoro aggiornate — 21 novembre 2026

Marco comunica che il compagno segue il punto 2 (integrazione della forma nel matcher), mentre Marco prende in carico il punto 3 (ammissione dei punti nella memoria geometrica). Punti 1 (confronto delle forme) e 4 (collocazione/aggiornamento nella scena) dopo la risoluzione di entrambi. Richiede di procedere sul punto 3 iniziando dal recap di stato e criticità: superato il precedente rinvio della revisione dei gate, conservato sotto come storia. Nessuna nuova soglia, alternativa o protocollo già adottati; nessuna modifica del codice o nuovo job in questo passaggio. Nessun metodo o risultato del compagno comunicato.

Ricognizione conclusa sui resoconti esistenti: 31 fusioni DA/40 MoGE per variante nella campagna, senza validazione fisica indipendente; audit del prefisso con rifiuti per sola ambiguità e sovrapposizione asimmetrica compatibile con parzialità. Prossimo passo proposto, da definire: validazione indipendente di ammissioni e rifiuti, distinguendo simmetrie, parzialità, scala e identità. I controlli di scala necessari alla registrazione restano nel punto 3. Evidenze e limiti in [campagna](../evidence/campaign_20261115_v1/REPORT_FINALE.md) e [audit](../archive/RIPRESA_HPC_20261114.md). Nessun nuovo esito sperimentale; stato del job di arricchimento non ricontrollato.


## Primo campione supervisionato pronto — 21 novembre 2026

[Campione e disponibilità effettiva](ARRICCHIMENTO_TRAINING_20261121.md): 782875 concluso 0:0, 446 esempi/247 frame P01_01 con oracle e provenienza, controlli indipendenti passati. Geometrie riusate, nessuna nuova etichetta/inferenza/training. Primo prerequisito verificato su un video; prima dell'estensione servono input originali mancanti e copertura Nuova track, assente nei 446 esempi. Gli ingressi completi degli altri 55 video non sono verificati. Distanza, politica della memoria e due percorsi di integrazione restano da decidere/testare; nessun job di questo step attivo.

## Mappa corrente — 21 novembre 2026

Struttura Rami paralleli e nuovi commenti confermati da Marco e applicati: 39 riquadri, 49 collegamenti. La sorgente corrente è [la mappa interattiva](../../mappa_interattiva/README.md). Superata la riserva storica della scrittura al solo Marco: l’assistente può applicare i testi dopo conferma esplicita. Vecchi commenti conservati, revisione scientifica successiva ancora aperta. Nessun cambiamento del metodo o nuovo esperimento.

## Direzione corrente — 16 novembre 2026

Marco vuole tentare sia fusione esterna sia riaddestramento del matcher, dopo verifica di dati e distanza, senza alcuna nuova etichettatura manuale e preferibilmente con i dati originali Whareformer. Registro voce 81 e [fattibilità/dipendenze](FATTIBILITA_DUE_INTEGRAZIONI_20261116.md). Proposta di sequenza: target/replay oracle con provenienza → geometria di sviluppo e costo → confronto delle distanze → due integrazioni con stessi ingressi e controllo senza geometria riaddestrato. Confronto richiesto, protocollo finale non ancora congelato e nessun training avviato. Le precedenti indicazioni di sole reti congelate non escludono più l'adattamento del matcher; estrattori congelati restano raccomandazione. Prima run e campagna già concluse, filtri ancora invariati/rinviati.

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

Le due direzioni SuperFlex → Whareformer e Whareformer → SuperFlex sono parti di un ciclo unitario.

1. Estrarre la geometria dell'oggetto osservato nel frame e la sua rappresentazione di forma.
2. Confrontarla con la memoria geometrica delle track al termine del frame precedente. Tutte le detection del frame interrogano lo stesso stato precedente.
3. Correggere il matcher conservando aspetto/XYZ della baseline e lasciare a Whareformer l'assegnazione effettiva.
4. Per ogni assegnazione, proporre registrazione e accumulo dei soli punti osservati; registrare separatamente inizializzazione, fusione, rifiuto ed errore.
5. Dopo ogni aggiornamento ammesso, eseguire SuperFlex e pubblicare la forma per confronti nei frame successivi. Non usare completazioni come nuovi punti osservati.

DA e MoGE rimangono fonti separate. Distinguere coordinate camera della forma, coordinate scena/XYZ della baseline e normalizzazioni del confronto da quelle di ingresso a SuperFlex. Un nuovo video richiede nuove istanze e memorie. Il replay seriale con cache non è una ripresa generale da checkpoint.

Controlli: W0 baseline, G0 zero, forma separata, forma da accumulo e punti da accumulo; reti congelate, stesso budget geometrico dichiarato e tracker indipendenti. Gli esempi zero verificano la compatibilità del codice, non l'utilità del metodo.

Il protocollo originale IDF1/mPCL usa nomi oggetto e XYZ stimati: non certifica identità fisiche indipendenti. Mantenere scope, split e provenienza espliciti; non confrontare metriche del prefisso con il video completo.

Implementazione, risultati e prossime attività: [stato](STATO_LAVORO.md), [roadmap](ROADMAP.md), [codice](../../integration_prototype/README.md). Motivazioni e revisioni storiche: [registro](REGISTRO_DECISIONI.md) e [archivio](README.md). La revisione dei filtri resta esplicitamente rinviata da Marco.
