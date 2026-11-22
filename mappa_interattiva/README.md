# Mappa interattiva Whareformer–SuperFlex

Versione corrente: **Rami paralleli — opzione A**, struttura e testi confermati da Marco e applicati il 22 novembre 2026. Contiene **39 riquadri e 53 collegamenti**, con nove campi per scheda. Distinti stati di posizione, forma persistente e verificatore di ammissione. Aggiornamento locale, non ancora pubblicato su GitHub; la versione precedente è conservata nel backup indicato nella [ricevuta](../context/evidence/map_20261122/APPLICAZIONE.json).

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
| `server.cjs` | Lettura e salvataggio locale con controllo dei conflitti |
| `backup/` | Versioni precedenti, escluse da Git |

La versione dei dati è 2. Restano R01–R39; rimosse C34/C40 e aggiunte C50–C55, senza rinumerare le altre. `legacyIds`/`legacyId` conservano i riferimenti precedenti. Il gruppo G01 raccoglie gli ingressi condivisi, senza essere un ulteriore processo. Il nuovo `layoutId` isola i vecchi salvataggi di posizione: non vengono riapplicati al disegno aggiornato.

## Consultazione

- La vista iniziale adatta la larghezza e parte dall'alto. Trascinare lo sfondo per esplorare; usare rotella o pulsanti per lo zoom.
- `Inizio e larghezza` torna all'inizio; `Mostra tutta` mostra la mappa complessiva.
- Cliccare un riquadro o una freccia per aprirne la scheda. I menu `Riquadri…` e `Collegamenti…` consentono di raggiungere un elemento distante.
- `Sblocca scheda` permette l'aggiornamento al passaggio sugli elementi; `Fissa scheda` mantiene il contenuto selezionato.
- Blu: Whareformer; arancione: SuperFlex; viola: aggiunte del progetto; grigio: risorse/modelli esterni. Rombo: decisione. Frecce continue: dati; tratteggiate: controllo; puntinate: frame successivo.
- Nelle finestre strette la scheda compare sotto il disegno; nelle larghe resta laterale. La selezione si ricentra nello spazio disponibile. «Mostra tutta» offre l'orientamento generale: per leggere i testi usare zoom e selettori.

## Modifica e persistenza

`Modifica descrizione` apre i nove campi. `Salva` aggiorna JSON e copia offline; prima di una variazione effettiva il servizio conserva il JSON precedente. Un salvataggio invariato non cambia i file. I conflitti non sovrascrivono modifiche di altre finestre: il modulo resta aperto per conservare il testo.

Titoli, struttura e disegno non vengono modificati dall'editor dei commenti. Le 19 schede di nodo e 31 di collegamento fuori revisione sono state conservate integralmente nei nove campi e nei metadati descrittivi. Le altre 20/22 schede usano i testi confermati. Conferma editoriale e validazione scientifica non coincidono.

I riquadri possono essere spostati trascinandoli oppure con `Alt` e le frecce dopo il focus. Le posizioni rimangono nel browser, separate dai testi. `Ripristina disposizione` ripristina le coordinate approvate senza cambiare i commenti. `Esporta` conserva dati e disposizione; `Importa disposizione` ripristina soltanto le posizioni di un'esportazione della stessa versione, preservando sempre i commenti attuali. Le vecchie posizioni della versione 1 non vengono riapplicate automaticamente.

## Ripresa del lavoro

Leggere prima AGENTS.md e la memoria del progetto, poi questo README e `contenuti.json`. Il disegno e i commenti non vanno rigenerati dalle vecchie proposte: la versione corrente può contenere ulteriori modifiche manuali.

Specifiche confermate: [struttura](../context/archive/STRUTTURA_PROPOSTA_MAPPA_20261122.md), [testi](../context/evidence/map_20261122/TESTI_PER_REVISIONE.md). [Esito e limiti](../context/evidence/map_20261122/ESITO_APPLICAZIONE.md), [ricevuta e backup](../context/evidence/map_20261122/APPLICAZIONE.json), [verifiche](../context/evidence/map_20261122/VERIFICA_APPLICAZIONE.json). I documenti del 21 novembre restano la provenienza storica della disposizione Rami paralleli e della migrazione B/E → R/C.

La migrazione ha conservato i file della precedente applicazione in una sottocartella `backup/prima-rami-paralleli-*`, con inventario e hash. Il servizio non rende accessibile la cartella dei backup dal browser.

La mappa documenta il percorso con DA allineata, memoria opzione A e baseline appresa di ammissione; D2/correzione esterna restano il riferimento implementato. Copertura, stato del matcher e limiti scientifici correnti sono in [STATO_LAVORO](../context/memory/STATO_LAVORO.md). Nessun nuovo training, esperimento o beneficio scientifico è implicato dall'aggiornamento editoriale.
