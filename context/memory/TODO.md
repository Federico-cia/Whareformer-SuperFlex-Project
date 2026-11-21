# To-do corrente — collegamento alla baseline reale

## Pubblicazione verificata a chiusura della sessione

Su richiesta di Marco, controllo complessivo e push eseguiti. Commit
[5827c32](https://github.com/Federico-cia/Whareformer-SuperFlex-Project/commit/5827c323854d8a4f776d2417dd43e7c1ea4c328d)
pubblicato su **main**, riferimento remoto verificato identico tramite Git.
48 file: primo nucleo del punto 3, dati oracle/audit in codice portabile,
evidenze numeriche selezionate, schede confermate della mappa e memoria corrente.
Contributi del collega e storia preservati; nessun force-push.

Verifiche della copia pubblicabile: **105 casi, 103 superati e due saltati**
(motmetrics assente); 636 collegamenti, 53 sorgenti Python e 222 hash senza
errori; mappa 39 riquadri/49 collegamenti/792 campi e copia offline coerenti.
Scansione finale dei 48 file senza riscontri per pattern sensibili, dati pesanti
o accessi personali, nei limiti del controllo. Archivi completi, immagini,
nuvole, pesi e strumenti di accesso privati restano fuori da Git.

Il problema di capacità degli output è rinviato da Marco alla prossima sessione.
Il punto 3 resta incompleto sul piano di training e validazione; il push non
certifica efficacia scientifica. Gli stati HPC restano quelli datati negli
ultimi resoconti, senza nuova interrogazione durante la pubblicazione.
Le note precedenti di pubblicazione preparata/non eseguita sono cronologia.

## Spazio recuperato e nuova ripresa — 21 novembre 2026

**Verifica successiva delle 23:51:38:** 783790/783791 entrambi RUNNING a 3m56s su gnode03; superato l'arresto precedente nelle nuvole, ora blocco 8 con 309/312 report DA/MoGE e blocco 9 con 286/288. Quota 41.19/46.56 GiB (circa 5.37 GiB liberi), otto blocchi ancora conclusi; SuperFlex dei nuovi blocchi non ancora verificata.

Marco autorizza pulizia e, esplicitamente, copia/archiviazione dei tracciati conclusi sul PC. Verificati due volte 377 file (5.47 GiB) e conservati in archivio locale di 636594519 byte con ledger/hash, prima di rimuovere le sole copie remote. Runtime, geometrie e input attuali preservati. Quota scesa da 46.35 a 40.88 GiB su 46.56; archivio da NON eliminare. [Operazioni, percorsi e ripristino](PULIZIA_E_RIPRESA_HPC_20261121.md).

**Job correnti:** 783790/783791, rami 0/1 dai blocchi 8/9, RUNNING su gnode03 al controllo 23:49:54 (2m11s). Preflight quota positivo anche sul nodo di calcolo. Otto blocchi conclusi a quel controllo. I tentativi 783750/751 sono falliti dopo MoGE anche su nodo diverso; 783782/783783 fermati prima delle inferenze per helper quota assente, poi corretto. Nessun precedente tentativo va considerato attivo.

Guard di quota a ogni blocco: riserva operativa 2 GiB/12000 file, stop esplicito codice 75 quando insufficiente; fallback nativo BeeGFS verificato. Tolta l'esclusione del nodo che non risolveva. Nessuna modifica scientifica. **Capacità ancora aperta:** costo misurato 0.64 GiB/blocco, estrapolazione circa 138 GiB/216 blocchi; la pulizia non basta a garantire completamento nella quota di 50 GB. Occorre compattare la conservazione senza perdere informazione necessaria o reperire capacità. Nessuna riduzione di copertura o sorgenti approvata in questa fase. Non promettere funzionamento ininterrotto notturno.


## Ripresa interrotta; quota personale quasi piena — 21 novembre 2026

Aggiornamento successivo: 783750/783751 hanno superato MoGE ma sono poi entrambi FAILED 1:0 alle 23:23:53 anche su gnode03, durante le nuvole. La precedente nota RUNNING è storica: il solo cambio di nodo non risolve. Diagnosi con `myquota`: 46.35 GiB usati su 46.56 GiB, circa 0.21 GiB disponibili; il precedente df del filesystem totale non misurava questo limite personale. Quota quasi esaurita è un problema verificato e spiegazione plausibile degli errori di scrittura/silenzi; risoluzione dello spazio e successiva ripresa ancora in corso. Nessun altro job inviato dopo questo arresto. I parziali sono preservati. Non dichiarare la run attualmente in avanzamento senza nuova verifica.


## HPC riavviato su richiesta di Marco — 21 novembre 2026, 23:23

Marco richiede «Fallo ripartire». Diagnosi e ripresa eseguite con accesso esistente autorizzato per l'azione: **783750 e 783751 RUNNING su gnode03**, rami 0/1 dai blocchi 8/9. **MoGE superato: 512/512 ready in entrambi**, DA già pronta, nuvole in costruzione. Ultimo controllo 23:23:51, rispettivamente 3m14s/3m08s; 8/216 blocchi ancora conclusi a quel momento. Catena automatica preesistente preservata, nessun duplicato o reset delle cache.

Escluso gnode02 dai job e successori come intervento controllato dopo quattro arresti osservati durante MoGE, senza pretendere diagnosi hardware conclusiva. Batch remoto salvato in backup e arricchito di log; dati/modelli/codice scientifico invariati. [Intervento, hash, log e ricevute](RIPARTENZA_HPC_20261121.md). Non reinviare mentre i rami sono in coda. SuperFlex dei nuovi blocchi e completamento integrale ancora da verificare; nessuna sorveglianza permanente avviata. Questo stato supera le precedenti note di coda vuota/run ferma. Audit e sviluppo punto 3 restano nello stato documentato.


## Chiusura sessione e ripresa successiva — 21 novembre 2026

Marco chiede di chiudere la sessione e proseguire domani con il prossimo problema del TODO. Nessuna nuova scelta metodologica o attestazione di chiusura del punto 3: piano approvato, primo nucleo implementato e testato (103 test superati, due saltati), audit 783586 acquisito e interpretato. Riferimenti: [implementazione](IMPLEMENTAZIONE_PUNTO3_20261121.md), [audit](RISULTATI_AUDIT_AMMISSIONE_20261121.md).

**Situazione da non perdere:** arricchimento fermo a 8/216 blocchi, riprese 783490/783491 FAILED 1:0 e nessun job in coda nell'ultimo controllo delle 23:01. Non avanza automaticamente durante la notte. Diagnosi aggiornata predisposta ma non ancora eseguita: esito_diagnosi.txt è ancora quello delle 20:39 sui vecchi job. Marco può eseguire `strumenti_hpc/esegui_diagnosi_hpc.bat` alla ripresa; assistente senza accesso HPC diretto, nessun rilancio prima della lettura dell'esito.

**Punto 3 ancora aperto:** staticità/target reali da validare, dati e training del verificatore principale, parametri selezionati sullo sviluppo, worker SuperFlex con FPS e validazione del caso dopo spostamento. Le 438 nuvole allineate sono locali e consentono lavoro indipendente dalla run. Test set indipendente ancora prioritario; punto 2 al compagno. Le modifiche di questa sessione sono locali, non pubblicate. Non riaprire decisioni approvate né rilanciare audit concluso. Nessuna ulteriore azione indispensabile per chiudere la chat; riprendere da questi pendenti quando Marco torna.


## Audit acquisito; arricchimento fermo — 21 novembre 2026, esiti 23:01–23:06

Marco esegue gli script: **783586 COMPLETED 0:0, 16m53s**, sette hash verificati; 446 osservazioni, 438 allineamenti validi e nuvole locali finite, otto fit con alpha negativo. Confronto appaiato su 415 coppie: sovrapposizione mediana 3.27% grezza → 22.80% allineata (28.08% → 68.16% nel terzile di minore spostamento, non staticità certificata). 24 osservazioni con sole maschere del catalogo. Nessuna etichetta di fusione corretta ancora certificata: mantenere limiti di staticità, simmetrie ed errori condivisi. [Risultati, provenienza e interpretazione](RISULTATI_AUDIT_AMMISSIONE_20261121.md).

**Arricchimento:** coda vuota, 8/216 blocchi, nessun riepilogo finale; riprese 783490 e 783491 entrambe FAILED 1:0. Causa non identificata dai log disponibili. Aggiornata la diagnosi di sola lettura per questi job e per gli stadi parziali; prossimo intervento di Marco: `strumenti_hpc/esegui_diagnosi_hpc.bat`, poi leggere `esito_diagnosi.txt` prima di riprendere. Nessun accesso diretto HPC, invio o training dell'assistente. Le nuvole locali consentono di proseguire la preparazione dei dati da trasformazioni note senza attendere la run completa. Decisioni metodologiche approvate invariate.


## Punto 3: prima implementazione autorizzata ed eseguita — 21 novembre 2026

Marco autorizza di procedere secondo il piano approvato iniziando dalle parti indipendenti dall'audit. Implementati allineamento DA→scena con fallimento esplicito, memoria pesata a stati senza vista fissa, separazione forma/collocazione e percorso esplicito dopo spostamento, FPS 4096 con provenienza, contratti del verificatore, baseline regressiva addestrabile e replay/adapter del coordinatore. [Dettagli, verifiche e limiti](IMPLEMENTAZIONE_PUNTO3_20261121.md); [guida software](../../integration_prototype/SCENE_MEMORY.md).

**Verificato localmente:** 105 casi, 103 superati e 2 saltati per motmetrics, inclusi 23 nuovi test tutti passati; nessuna inferenza neurale reale. Il verificatore principale non è addestrato: senza modello non si confermano/fondono ipotesi. Mancano evidenze validate di staticità, calibrazione sullo sviluppo, collegamento FPS al worker SuperFlex e validazione reale dopo spostamento. Il runner storico resta distinto e invariato nei suoi algoritmi; la nuova memoria non è già la pipeline sperimentale completa.

**Audit/HPC:** nessun accesso diretto o job in questa fase; stato live ignoto. Marco deve avviare `strumenti_hpc/esegui_controllo_hpc.bat` e `esegui_scarica_audit.bat`; scarico aggiornato per il job 783586, con accounting, hash e log anche parziali, nuova cartella a ogni tentativo. Poi interpretare gli esiti prima di training/ripresa. Nessun nuovo metodo principale, parametro calibrato, modifica della mappa o pubblicazione. Log e ricevuta in `outputs/point3_implementation_20261121/`.


## Ricognizione di ripresa — 21 novembre 2026

Confrontati riassunto dell'altra chat, documenti correnti, codice, ricevute locali e schede della mappa. [Stato consolidato, differenze e limiti dell'audit](RICOGNIZIONE_RIPRESA_PUNTO3_20261121.md). Nessuna nuova scelta o esecuzione: piano approvato del verificatore/memoria ancora da implementare nei moduli correnti, che conservano gate fissi e prima vista. Scala 9–23% = variabilità del rapporto allineata/grezza, non errore vero certificato. Audit: staticità non certificata; errore denominato di superficie è spostamento punto a punto, non invariante alle simmetrie; non esporta tutte le pose candidate. Tenerne conto prima di costruire target.

Stato HPC corrente NON verificato: ultima verifica documentata squeue vuota, senza accounting/esiti successori; RUNNING storici non attuali. Prossimo passo: controllo e scarico audit avviati da Marco con gli script predisposti; assistente senza accesso diretto HPC. Preservate tutte le decisioni approvate e la storia; nessun training, job o pubblicazione in questa ricognizione.


## Passaggio corrente — 21 novembre 2026, sera

**Verifica operativa da chiudere:** acquisizione verificata (110580 abbinate, dieci mancanti), ma la ripresa/audit sotto sono stati storici. Ultima interrogazione squeue senza job; servono accounting e conteggio aggiornati tramite `strumenti_hpc/esegui_controllo_hpc.bat` eseguito da Marco. [Evidenze](VERIFICA_ARRICCHIMENTO_CORRENTE_20261121.md). Nessun nuovo invio o ripresa in questa verifica.

**Questo blocco prevale sulle sezioni sottostanti, che sono cronologia.** Punto 3 (ammissione e aggiornamento della memoria geometrica) seguito da Marco; punto 2 dal compagno; punti 1 e 4 dopo. Decisioni e piano in [SUPERVISIONE_AMMISSIONE_20261121.md](SUPERVISIONE_AMMISSIONE_20261121.md), sezione «Sintesi corrente»; registro in [REGISTRO_DECISIONI.md](REGISTRO_DECISIONI.md).

- **Decisioni del punto 3:** profondità DA allineata alla mesh della scena e riferimento scena tramite pose EPIC-Fields (procedura Whareformer); MoGE solo confronto; vista non fusa se l'allineamento fallisce. Memoria senza vista fissa; forma separata dalla collocazione; stati confermati nel tempo (DenStream adattato); accumulo con fusione dei duplicati e 4096 punti FPS per SuperFlex. Verificatore appreso sulla coppia allineata, classificatore sulle diagnostiche come base, verificatore preaddestrato come confronto. Prima versione con fusione solo da fermo; **obiettivo non negoziabile: fusione anche dopo uno spostamento**. Parametri scelti solo su sviluppo. Posizione per il tracking: quella di Whareformer.
- **Valutazione:** P01_01 è video di training, quindi sviluppo; il test set è priorità da discutere (TODO).
- **Operativo:** run di arricchimento P01_01 (110590 osservazioni, 216 blocchi) in corso con catena GPU; ripresa 783490/783491 dai blocchi 8/9. Audit del punto 3 783586 inviato. L'assistente non accede direttamente all'HPC: script in `strumenti_hpc/` avviati da Marco con doppio clic (controllo, diagnosi, ripresa, audit, scarico risultati). Nessun training avviato.
- **Mappa HTML:** schede R09, R12, R28, R32, R34 aggiornate con le decisioni (testi confermati da Marco); non ancora pubblicata.

## Discussioni aperte e importanti — riepilogo 21 novembre 2026

- [x] Diagnosi 783207/783208: nessun errore di codice o memoria visibile, probabile evento del nodo gnode02.
- [x] Ripresa eseguita: 783490/783491 RUNNING sui blocchi 8/9. Valutare riprova automatica se i fallimenti si ripetono.
- [x] Script dell'audit scritto e testato localmente nella parte matematica.
- [x] Audit inviato: 783586 RUNNING.
- [x] Scaricare e interpretare i risultati dell'audit 783586: concluso 0:0; evidenze e limiti nel resoconto corrente.
- [ ] Ricerca Consensus (link condiviso non leggibile dagli strumenti web): recuperare il testo dei risultati, verificare i paper e collegarli alle scelte.
- [ ] Punto 3: confermare pose/mesh come ingresso (conseguenza della scala allineata); definire cosa conta come fusione corretta e quale errore pesa di più; scegliere il modello del verificatore e il legame con l'ammissione per ipotesi; audit su CPU (approvazione pendente).
- [ ] **Importante:** discutere le due memorie (matching tramite descrittori di forma, ricostruzione tramite punti) e concordare con il compagno la parte del matching (punto 2).
- [ ] **Importante:** orientamento e collocazione della forma nella scena (R, t, s con XYZ Whareformer come ancora e scarto stimato) — punto 4.
- [ ] **Importante:** decidere se e quando estendere l'arricchimento agli altri 55 video di training, dopo la stima dei tempi.
- [ ] Secondario, da valutare: contatto mano-oggetto VISOR sull'HPC come indizio di oggetto fermo.
- [x] ZIP e messaggio sulla LMDB inviati al compagno da Marco.

## PRIORITÀ DA DISCUTERE — test set per dimostrare l'efficacia (Marco, 21 novembre 2026)

- [ ] **Decidere quale test set usare per mostrare l'efficacia della nostra architettura.** Vincolo: video mai usati né per addestrare Whareformer né per addestrare, calibrare o selezionare la componente 3D; P01_01 (training split) resta sviluppo. Opzioni aperte: sottoinsieme dello split di test EPIC (54 video, feature pubblicate dagli autori), tutto lo split se il costo lo consente, IT3DEgo/HD-EPIC come generalizzazione. Da fissare: quanti e quali video (scelti prima, con seme o stratificazione), sorgente geometrica e pipeline congelate, metriche e incertezza per video, baseline anche sui 54 completi per la rappresentatività. Decisione da prendere presto, prima che le scelte dei punti 2 e 3 vengano fatte guardando P01_01. Contesto in STATO_LAVORO.md, sezione «Test indipendente».

## Test indipendente — 21 novembre 2026

- [ ] Protocollo di test: vedere la voce prioritaria sopra.
- [ ] Verificare accesso e dimensioni dell'archivio pubblico (feature di test, training LMDB) dall'HPC prima di scaricare.
- [x] Compagno informato della training LMDB pubblicata (Marco).

## Rilancio GPU P01_01 — 21 novembre 2026, 17:19

- [x] Rilancio eseguito: 783119/783120 RUNNING. Non reinviare.
- [ ] Verificare superamento SuperFlex e durata del primo blocco; poi stimare la durata complessiva e preparare lo script di ripresa dei rami fermati.

## Esito job P01_01 — 21 novembre 2026, 16:58

- [x] 782990 COMPLETED 0:0: 110580 osservazioni con input, 10 mancanti espliciti, 216 blocchi.
- [x] Correzione del PATH in `lane()` applicata localmente e script di rilancio preparato (`strumenti_hpc/esegui_rilancio_hpc.bat`); output parziali dei blocchi 0/1 riusabili tramite cache firmata.
- [ ] Eseguire il rilancio (Marco, doppio clic), poi verificare `esito_rilancio.txt`, avvio GPU e primi blocchi completati.
- [ ] Durata da misurare sul primo blocco (stima grezza 12–20 min/blocco, 108 blocchi per ramo). Rischio: un job interrotto (limite 2 h, nodo, errore non gestito) ferma la catena del suo ramo senza perdere le osservazioni già salvate; serve controllo periodico e ripresa dal primo blocco non completato.
- [x] ZIP richiesto dal compagno creato e verificato in `strumenti_hpc/`; invio a cura di Marco.

## Supervisione dell'ammissione — 21 novembre 2026

- [x] Verificare dati e riferimenti disponibili per target indipendenti: pose EPIC-Fields complete sui frame osservati P01_01, mesh di scena, ledger oracle denso; analisi in [SUPERVISIONE_AMMISSIONE_20261121.md](SUPERVISIONE_AMMISSIONE_20261121.md).
- [ ] Decisione di Marco: pose/mesh solo come riferimento di supervisione/validazione o anche come ingresso della registrazione; costo relativo falsa ammissione/falso rifiuto; definizione del target di posa/utilità.
- [ ] Proposta, non approvata: audit CPU sulle 429 coppie consecutive (posa relativa da camere, indicatori di staticità, errore delle 24 soluzioni candidate, effetto di `da_aligned`), senza usare i gate come etichette.
- [ ] Verificare presenza del contatto mano-oggetto nell'archivio VISOR completo sull'HPC.
- [ ] Ricontrollare stato live di 782990/782968/782969 da un ambiente con accesso HPC prima di qualsiasi invio.

## Acquisizione completa e SuperFlex P01_01 avviate — 21 novembre 2026

Ultima verifica: 782990 RUNNING a 9m19s, 20805 maschere, nessun errore osservato; 782968/782969 PENDING per dipendenza. Download RGB completo, copertura finale e avvio effettivo GPU ancora pendenti. La pipeline è inviata e prosegue automaticamente dopo la verifica; non duplicare job o richieste.

Stato corrente: download RGB completo; acquisizione/verifica ora **782990**, che sostituisce 782967 cancellato per ottimizzare l'estrazione con riuso dei file. GPU sempre **782968/782969**, dipendenze aggiornate afterok su 782990. Log corrente `acquire_782990.out/.err`; nessun nuovo invio GPU.

- [x] Verificare archivio RGB ufficiale (1.72 GB) e spazio; predisporre verifica maschere/ID e pipeline a blocchi con riuso delle 446 geometrie.
- [x] Inviare 782967 acquisizione e 782968/782969 GPU afterok; [log, stato e ripresa](ARRICCHIMENTO_COMPLETO_P01_20261121.md). Non reinviarli.
- [ ] Acquisire esito della verifica di tutti gli input (`coverage.json`), distinguendo mancanti, conflitti e alias.
- [ ] Seguire avvio e avanzamento dei due rami, ricevere stati successivi in `submissions/`, verificare risultati per tutte le 110590 osservazioni senza confondere esportazione e riuscita.

## Applicazione dei testi revisionati — 21 novembre 2026

Marco conferma e richiede applicazione e pubblicazione dei vecchi commenti revisionati. Applicati 135 campi a sette riquadri e otto collegamenti, con le ultime formulazioni generali senza riferimenti alle singole esecuzioni. Struttura e altre schede conservate; backup locale precedente disponibile. Pubblicazione completata su main: https://github.com/Federico-cia/Whareformer-SuperFlex-Project/commit/9fe32e6ed8752fddb2c5850e254682bab8f6e0a6. Verificati servizio, copia offline, collegamenti e integrità dei contenuti.

## Estensione P01_01 richiesta — 21 novembre 2026

- [x] Elencare tutte le 110590 osservazioni: `outputs/p01_full_enrichment_20261121_v1/target_observations.json`, 446 geometrie esistenti e 110144 pendenti.
- [ ] Acquisire/verificare RGB e maschere completi, preparare budget/configurazione e arricchire tutto P01_01 come richiesto da Marco. Nessuna nuova inferenza avviata; input attualmente parziali. Registrare mancanti/fallimenti senza eliminare osservazioni.

## Criteri di ammissione appresi — indicazione di Marco, 21 novembre 2026

Marco richiede che le soglie di accettazione siano apprese dai dati anziché imposte manualmente; obiettivo esplicito conservare viste parziali valide. Richiede spiegazione di parzialità, ambiguità, regole correnti e alternative di validazione con pro/contro. Direzione approvata: apprendimento del criterio; modello, target, loss e protocollo non ancora scelti. Nessun training, codice, soglia o job modificati.

Verificato cloud_memory.py/cloud_updater.py: trasformazione rigida senza stima scala; supporto in entrambe le direzioni almeno 0.65 entro 0.08R; q90 dell'80% più vicino non oltre 0.15R; alternative entro 5% dello score più epsilon rifiutate se differiscono oltre 15 gradi o spostano il centroide oltre 0.08R. Basta un gate fallito. R è il raggio RMS del riferimento fit; rapporto dei raggi registrato, non gate autonomo. Query separate dal fit, non viste indipendenti. Inizializzazione senza confronto con memoria precedente, con soli controlli di validità dell'input.

Proposte da discutere: classificatore leggero sulle diagnostiche, criterio condizionato alla sovrapposizione/affidabilità dei punti, oppure apprendimento dell'utilità della fusione. Evitare target ricavati dai gate stessi: replicherebbero le euristiche. Identità oracle non certifica posa o scala. Possibile supervisione automatica con trasformazioni note su dati sintetici/crop, verifiche RGB multivista e viste reali escluse; limiti rispettivi: domain gap, dipendenza da pose/visibilità/movimento, validazione geometrica reale non ancora disponibile. Vincolo precedente di nessuna nuova annotazione manuale preservato. Separare dati per oggetto/sequenza e valutare errori di ammissione/rifiuto e qualità della memoria; nessuna opzione già adottata. Fonti primarie consultate per fattibilità concettuale, non compatibilità EPIC verificata: PREDATOR (CVPR 2021, overlap appreso) e Deep Global Registration (CVPR 2020, affidabilità delle corrispondenze appresa).


## Priorità e divisione del lavoro aggiornate — 21 novembre 2026

Marco comunica che il compagno segue il punto 2 (integrazione della forma nel matcher), mentre Marco prende in carico il punto 3 (ammissione dei punti nella memoria geometrica). Punti 1 (confronto delle forme) e 4 (collocazione/aggiornamento nella scena) dopo la risoluzione di entrambi. Richiede di procedere sul punto 3 iniziando dal recap di stato e criticità: superato il precedente rinvio della revisione dei gate, conservato sotto come storia. Nessuna nuova soglia, alternativa o protocollo già adottati; nessuna modifica del codice o nuovo job in questo passaggio. Nessun metodo o risultato del compagno comunicato.

Ricognizione conclusa sui resoconti esistenti: 31 fusioni DA/40 MoGE per variante nella campagna, senza validazione fisica indipendente; audit del prefisso con rifiuti per sola ambiguità e sovrapposizione asimmetrica compatibile con parzialità. Prossimo passo proposto, da definire: validazione indipendente di ammissioni e rifiuti, distinguendo simmetrie, parzialità, scala e identità. I controlli di scala necessari alla registrazione restano nel punto 3. Evidenze e limiti in [campagna](../evidence/campaign_20261115_v1/REPORT_FINALE.md) e [audit](../archive/RIPRESA_HPC_20261114.md). Nessun nuovo esito sperimentale; stato del job di arricchimento non ricontrollato.


## Campione supervisionato del training — 21 novembre 2026

- [x] Verificare struttura dei prodotti esistenti: geometrie e provenienza disponibili, campione oracle supervisionato ancora assente.
- [x] Implementare estrazione con oracle originale, archivio delle viste solo passate e verifica indipendente; tre test locali passati.
- [x] **782875 COMPLETED 0:0, 3m15s**: campione 446/247 validato, tre test locali/remoti, audit indipendente e confronto con 110590 annotazioni ufficiali passati; copia numerica/metadati acquisita. [Dettagli e percorsi](ARRICCHIMENTO_TRAINING_20261121.md). Nessun training/inferenza neurale nuovi, job concluso da non rilanciare.
- [x] Inventario iniziale completato: split originale 56 video; feature/XYZ/annotazioni complete verificate per P01_01, dati grezzi parziali su cinque, nessuna training LMDB trovata nella scansione delimitata. Sintesi e limiti (`outputs/training_enrichment_20261121_v1/availability_summary.json`, risorsa locale non pubblicata).
- [ ] Acquisire/localizzare input originali mancanti degli altri video e RGB mancanti di P01_01; estendere con la stessa pipeline, senza considerare già disponibili tutti i 56 video.
- [ ] Ampliare il campione includendo Nuova track e casi senza geometria: i 446 attuali hanno soltanto associazioni esistenti, 429 con geometria precedente della candidata corretta. Non usarli da soli per calibrare/valutare l'intera politica.

## Pubblicazione della mappa — 21 novembre 2026

- [x] Pubblicare su main mappa e memoria corrente: [c612cad](https://github.com/Federico-cia/Whareformer-SuperFlex-Project/commit/c612cad4c161fd3bfcca11ba31525102cee5ab58); riferimento remoto verificato, controlli superati. Restano le attività scientifiche e la revisione dei vecchi commenti riportate sotto.

## Priorità mappa — mandato del 21 novembre 2026

- [x] Verificare aggiornamenti remoti: main ccc1376, un commit di sola memoria/documentazione dopo 0fce33b; nessuna novità di codice/mappa nel confronto, nessun commit aggiuntivo sul ramo prepare/superflex-core.
- [x] Chiarire perimetro: tutti i campi mancanti, «-» se non sostanziale; esistenti rinviati, implementazione attuale, una mappa interattiva, libertà strutturale e proposte grafiche da approvare.
- [x] Preparare i testi dei nove nodi e tredici collegamenti mancanti e del campo E10, preservando lo stile manuale e distinguendo implementazione e proposte. [Bozze](../evidence/map_20261121/TESTI_PROPOSTI.md), da revisionare in chat prima dell'applicazione.
- [x] Preparare tre proposte visive separate sul ciclo critico: Rami paralleli, Asse centrale, Fasi separate; nessun cambiamento alla mappa attuale.
- [x] Fornire le tre proposte anche come immagini PNG, dopo la segnalata impossibilità di visualizzare la versione interattiva; esportazione e ispezione completate, scelta ancora pendente.
- [x] Raccogliere la scelta grafica e l'approvazione dell'intera disposizione: «Rami paralleli», poi conferma di Marco «Va bene questa mappa» sull'anteprima completa.
- [x] Preparare e mostrare l'anteprima completa prima dell'applicazione, come richiesto: [immagine](../evidence/map_20261121/mappa-completa-rami-paralleli.png), SVG e ritagli; [specifica e limiti](../evidence/map_20261121/ANTEPRIMA_COMPLETA.md). Mappa attuale invariata.
- [x] Preparare i commenti per la struttura confermata: 28 riquadri e 39 collegamenti nuovi/ridistribuiti, altri conservati o ripresi dalle bozze già presentate. [Revisione in chat](../evidence/map_20261121/COMMENTI_PER_REVISIONE_CHAT.md); nove campi per tutte le 39/49 schede, verifica formale completata, mappa invariata.
- [x] Conferma esplicita ricevuta: «Ok, aggiungi il testo. Poi aprimi qui l'html»; R/C ora identificano gli elementi effettivi della mappa.
- [x] Applicare struttura «Rami paralleli» e testi confermati: 39 riquadri, 49 frecce, 792 campi; copia precedente conservata, nessuna modifica del metodo.
- [x] Verificare JSON/copia offline e consultazione, salvataggio invariato e spostamento con ripristino; aprire l'HTML nel browser della chat e conservarlo come risultato.
- [x] Preparare la revisione dei vecchi commenti: sette riquadri e otto collegamenti, 135 campi; [proposte non applicate](../evidence/map_20261121/TESTI_PROPOSTI.md), mappa invariata per hash.
- [ ] Raccogliere revisioni e conferma esplicita di Marco sui vecchi commenti proposti in chat.
- [x] Riformulare le proposte senza riferimenti a singole campagne/run, date o conteggi sperimentali, come richiesto da Marco; conservare indicazioni generali su verifiche e limiti. Regola da mantenere nelle revisioni successive.
- [ ] Applicare soltanto i testi confermati e verificare la conservazione degli altri contenuti; nessuna autorizzazione all’inserimento ricevuta in questa fase.

## Aggiornamenti GitHub pubblicati — 15 novembre 2026

Aggiornamenti pubblicati su `main`, commit [0fce33b](https://github.com/Federico-cia/Whareformer-SuperFlex-Project/commit/0fce33b6acdea13d6d36bf557fcbf0c311b34ae7), riferimento remoto verificato dopo il push. Inclusi snapshot manuale della mappa, checklist di revisione, decisioni ancora pendenti e memoria corrente; corretto il README sui dati riusati rispetto alla geometria rigenerata. Codice e risultati della campagna erano già su remoto a d8fb991. Preservati contributi del collega e storia Git; nessun nuovo esperimento o cambio dei filtri. Controlli: 467 collegamenti, 41 sorgenti Python e 179 hash senza errori, servizio mappa in sola lettura superato; 13 file controllati senza pattern sensibili rilevati, nei limiti del controllo. Mappa copiata byte per byte dalla versione manuale locale.

- [x] Caricare gli aggiornamenti verificati su main. Restano aperte le attività scientifiche e la compilazione manuale indicate sotto.

## Punti importanti da discutere e validare

**Prioritario (21 novembre):** scelta del test set per dimostrare l'efficacia; dettaglio nella voce in cima al file.

Valutazione critica successiva, registro voce 82: verificare complementarità della distanza rispetto ad aspetto/posizione, non sola separazione delle categorie; preservare controlli senza geometria con pari nuovo training e proporre geometria semplice dagli stessi punti per attribuire l'effetto specifico SuperFlex. Nessuna nuova analisi quantitativa o modifica del protocollo già eseguita. Dettaglio nel [resoconto delle due integrazioni](FATTIBILITA_DUE_INTEGRAZIONI_20261116.md).

**Direzione corrente del 16 novembre:** Marco vuole tentare entrambe le strade; nessuna nuova etichettatura manuale, preferenza per dati/target originali Whareformer. Superate alternativa condizionale e proposta di campione manuale delle voci 79/80; decisione aggiornata nella voce 81. [Fattibilità, distanze e dipendenze](FATTIBILITA_DUE_INTEGRAZIONI_20261116.md). Nessun training avviato; protocollo dettagliato ancora da fissare.

- [ ] **Prerequisiti dei due percorsi:** verificare accesso ai dati/target originali e ricostruire automaticamente oracle con provenienza delle osservazioni e geometria solo passata. Rispettare limiti nomi/esclusioni del benchmark; nessuna conversione automatica delle track predette in GT. Misurare costo su sottoinsieme di sviluppo prefissato prima di promettere copertura integrale del training.
- [ ] **Confronto geometrico condiviso:** diagnosticare D2 esistente e Chamfer dopo allineamento su target originali, senza etichette manuali. Chiarire scala/parzialità, riduzione della memoria e sensibilità alle superfici interne: l'export SuperFlex concatena le primitive. Distanza finale non selezionata.
- [ ] **Due integrazioni richieste:** fusione esterna con pochi coefficienti appresi e riaddestramento/adattamento del matcher con ingresso geometrico. Stessi dati/distanza/memorie per il confronto, gestione mancanti/Nuova track e replay causale completo; controllo senza geometria con pari nuovo training. Fine-tuning dal checkpoint raccomandato, non già scelto rispetto al training da zero. Scelta finale con il compagno ancora aperta; nessuna nuova run o modifica di B12/mappa.

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
