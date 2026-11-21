# Mappa interattiva Whareformer–SuperFlex

Versione corrente: **Rami paralleli**, struttura e testi confermati da Marco e applicati il 21 novembre 2026. Contiene 39 riquadri e 49 collegamenti, con nove campi descrittivi per scheda. La repository conserva i testi confermati; la revisione scientifica dei vecchi commenti è una fase successiva.

## Apertura

Avviare `Avvia mappa.cmd`, oppure eseguire `node server.cjs` da questa cartella. Il servizio si collega soltanto a `127.0.0.1`; indirizzo: http://127.0.0.1:8767/mappa_interattiva/index.html. La stessa pagina può essere aperta nel browser integrato della chat.

Aprire direttamente `index.html` permette la consultazione offline; per salvare i commenti usare il servizio locale.

## File autorevoli

| File | Funzione |
|---|---|
| `contenuti.json` | Testi, identificativi, provenienza e disposizione approvata; include il disegno vettoriale |
| `contenuti.js` | Copia dei medesimi dati per consultazione offline, rigenerata dal servizio |
| `app.js` | Consultazione, schede, editor, navigazione e disposizione nel browser |
| `stile.css` | Aspetto dell'interfaccia |
| `index.html` | Pagina principale |
| `fonti.js` | Registro dei percorsi nel clone e dei riferimenti ufficiali esterni, fissati al commit degli autori |
| `server.cjs` | Lettura e salvataggio locale con controllo dei conflitti |
| `backup/` | Versioni precedenti, escluse da Git |

La versione dei dati è 2. I riferimenti `R01–R39` e `C01–C49` proposti in chat sono ora gli identificativi effettivi; `legacyIds`/`legacyId` conservano il legame con B/E della versione precedente. Il gruppo `G01` rappresenta gli ingressi condivisi e non è un ulteriore riquadro di processo.

## Consultazione

- La vista iniziale adatta la larghezza e parte dall'alto. Trascinare lo sfondo per esplorare; usare rotella o pulsanti per lo zoom.
- `Inizio e larghezza` torna all'inizio; `Mostra tutta` mostra la mappa complessiva.
- Cliccare un riquadro o una freccia per aprirne la scheda. I menu `Riquadri…` e `Collegamenti…` consentono di raggiungere un elemento distante.
- `Sblocca scheda` permette l'aggiornamento al passaggio sugli elementi; `Fissa scheda` mantiene il contenuto selezionato.
- Blu: Whareformer; arancione: SuperFlex; viola: aggiunte del progetto; grigio: risorse/modelli esterni. Rombo: decisione. Frecce continue: dati; tratteggiate: controllo; puntinate: frame successivo.

## Modifica e persistenza

`Modifica descrizione` apre i nove campi. `Salva` aggiorna JSON e copia offline; prima di una variazione effettiva il servizio conserva il JSON precedente. Un salvataggio invariato non cambia i file. I conflitti non sovrascrivono modifiche di altre finestre: il modulo resta aperto per conservare il testo.

Titoli, struttura e disegno non vengono modificati dall'editor dei commenti. Le schede manuali rimaste equivalenti sono state conservate; una loro revisione scientifica successiva resta distinta dall'inserimento dei nuovi testi confermati. Conferma editoriale e validazione scientifica non coincidono.

I riquadri possono essere spostati trascinandoli oppure con `Alt` e le frecce dopo il focus. Le posizioni rimangono nel browser, separate dai testi. `Ripristina disposizione` ripristina le coordinate approvate senza cambiare i commenti. `Esporta` conserva dati e disposizione; `Importa disposizione` ripristina soltanto le posizioni di un'esportazione della stessa versione, preservando sempre i commenti attuali. Le vecchie posizioni della versione 1 non vengono riapplicate automaticamente.

## Ripresa del lavoro

Leggere prima AGENTS.md e la memoria del progetto, poi questo README e `contenuti.json`. Il disegno e i commenti non vanno rigenerati dalle vecchie proposte: la versione corrente può contenere ulteriori modifiche manuali.

Anteprima e provenienza della riorganizzazione: [anteprima e provenienza](../context/evidence/map_20261121/ANTEPRIMA_COMPLETA.md); commenti confermati: [specifica dei commenti](../context/evidence/map_20261121/COMMENTI_STRUTTURA_APPROVATA.json) nella stessa cartella. Ricevuta dell'applicazione e percorso della copia precedente: [ricevuta](../context/evidence/map_20261121/APPLICAZIONE_MAPPA.json).

Sul computer di sviluppo la migrazione ha conservato i file della precedente applicazione in una sottocartella `backup/prima-rami-paralleli-*`, con inventario e hash. Il servizio non rende accessibile la cartella dei backup dal browser.

La mappa documenta l'implementazione con accumulo: aspetto/posizione ufficiali riusati nelle prove, geometria disponibile sul campione e controlli geometrici provvisori. Nessun nuovo training, filtro, esperimento o beneficio scientifico è implicato dall'aggiornamento editoriale.

I backup rimangono locali. I collegamenti delle schede sono risolti tramite `fonti.js`: codice mantenuto nel clone, documentazione in `context/`, codice originale degli autori su GitHub a revisione fissata.
