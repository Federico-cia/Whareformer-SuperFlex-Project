# Mappa interattiva Whareformer–SuperFlex

Cartella dedicata nella repository locale: mappa_interattiva/. Non pubblicata su GitHub.

## Organizzazione

| File | Funzione |
|---|---|
| index.html | Pagina e comandi |
| stile.css | Aspetto grafico |
| app.js | Interazioni ed editor |
| server.cjs | Servizio locale di salvataggio |
| Avvia mappa.cmd | Avvio Windows |
| contenuti.json | **Sorgente principale dei testi** e disposizione iniziale |
| contenuti.js | Copia generata dal servizio per consultazione offline |
| backup/ | Versioni precedenti, locali ed escluse da Git |
| LEGGIMI.md | Rimando a questo README |

## Ripresa in un’altra chat

- Leggere AGENTS.md e i documenti di continuità del progetto, poi questo README.
- Leggere contenuti.json aggiornato. Non rigenerarlo dalle vecchie proposte: contiene le modifiche manuali di Marco.
- Prima revisione: RGB B01, Maschere VISOR B02, Feature d’aspetto B03 e collegamenti E01/E02/E03. Altre schede da compilare. Testi modificati non equivalgono automaticamente a conclusioni scientifiche approvate.
- Conservare i campi non richiesti. Le parentesi quadre sono richieste di completamento all’assistente: verificare le fonti prima di risolverle.
- Proporre in chat i contenuti dei gruppi successivi. Scrivere per lettori esterni e giuria, spiegando i termini tecnici.
- Riordino grafico secondario; revisione dei filtri di fusione esplicitamente rinviata.
- Il salvataggio dell’HTML non aggiorna i Markdown scientifici: la memoria viene aggiornata separatamente dall’assistente quando necessario.
- Le posizioni trascinate restano nel browser: esportare/importare per trasferirle. Il servizio legge i testi autorevoli dal JSON.

## Avvio
Aprire «Avvia mappa.cmd». Avvia il servizio locale Node.js in background e apre http://127.0.0.1:8767/mappa_interattiva/index.html. Node.js è già presente sul computer. In alternativa eseguire node server.cjs da questa cartella e aprire lo stesso indirizzo.

Aprire direttamente index.html resta possibile per consultare la mappa offline, ma la modifica è disabilitata: usare il servizio locale per salvare nei file.

## Modifica e salvataggio
1. Cliccare un riquadro oppure scegliere una freccia dal menu «Collegamenti…», poi scegliere «Modifica descrizione» nella scheda.
2. Modificare i campi separati (sintesi, funzione, stato, evidenze, motivazione, alternative, miglioramenti, convenzioni e fallimenti).
3. Premere «Salva» e attendere «Descrizione salvata nei file del progetto». «Annulla» lascia invariato il file.

Sono modificabili i testi descrittivi dei riquadri e dei collegamenti. Titoli, fonti, estremi delle frecce e struttura restano esclusi da questo editor. Il servizio scrive contenuti.json (sorgente principale) e aggiorna contenuti.js per la consultazione offline. I Markdown scientifici collegati non vengono modificati o sincronizzati automaticamente.

Prima di ogni cambiamento effettivo viene conservato il contenuto precedente in backup/. Salvataggi senza variazioni non creano copie. Se un’altra finestra o un editor ha modificato la stessa descrizione, il servizio segnala il conflitto senza sovrascrivere e mantiene il modulo: copiare il testo da conservare, annullare, ricaricare e riprovare. In caso di errore il modulo resta aperto e il testo non viene scartato. Ricaricare legge sempre i testi dai file del progetto; il vecchio salvataggio browser viene usato solo per la disposizione dei nodi.

## Importazione ed esportazione
Esportazione salva una copia JSON completa per consegna/archivio. Nel servizio locale, l’importazione ripristina soltanto la disposizione: non sovrascrive descrizioni già salvate. Le posizioni vengono conservate nel browser, non salvate dal servizio. Per condividere la disposizione, esportare/importare.

## Navigazione
Scheda e × aprono/chiudono il pannello sinistro; inizialmente chiuso. Hover aggiorna la scheda, clic la fissa. Zoom con rotella/trackpad e +/−, pan trascinando lo sfondo, Mostra tutta la mappa e 100%. Ripristina disposizione mantiene i testi. Nessuna ulteriore revisione della disposizione avviata in questa fase.

## Fonti e contenuti
REGISTRO_DECISIONI.md per decisioni, STATO_LAVORO.md/TODO.md per stato, ROADMAP_CICLO_GEOMETRICO.md per contratto e piano, resoconti tecnici per risultati e codice per dettagli implementativi. Tre riquadri e tre collegamenti hanno proposte iniziali; le altre schede sono esplicitamente da completare. Le modifiche editoriali non certificano nuove evidenze scientifiche.

Il servizio è locale (127.0.0.1), non pubblicato. Non è collaborazione simultanea sincronizzata: le altre finestre vedono i nuovi testi dopo ricaricamento, con protezione dai conflitti al salvataggio.

## Linguaggio delle schede
Scrivere per persone che non conoscono il progetto: descrivere prima la funzione concreta, spiegare i termini tecnici necessari, distinguere cosa è stato controllato dai limiti ancora aperti. Titoli aggiornati: Possibili miglioramenti, Coerenza dei dati, Possible points of failure. Le modifiche manuali ai contenuti vanno preservate; aggiornare solo i campi richiesti e usare il controllo di revisione.
