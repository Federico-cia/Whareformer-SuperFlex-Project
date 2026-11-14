# Analisi dell'aggiornamento GitHub del collega — 13 novembre 2026

> Revisione successiva del 13 novembre: evidenze del codice invariate; la lettura dell’accumulo come sola estensione distinta è superata dal chiarimento esplicito di Marco sul ciclo unitario. Roadmap corrente: [ROADMAP_CICLO_GEOMETRICO.md](ROADMAP_CICLO_GEOMETRICO.md). Le raccomandazioni di direzione sotto restano come storia della prima analisi.

## Esito e perimetro

Il collega ha realizzato il collegamento **offline** fra output Whareformer e nuvole compare200 per `P01_01`. È un avanzamento concreto della dipendenza di mapping, non ancora l'integrazione della forma nel matcher. Il README propone poi accumulo multivista e ricostruzione: esperimento distinto dalla domanda approvata sul miglioramento dell'associazione delle identità, non revisione automaticamente adottata.

Analizzati tutti i sei file cambiati nei commit del 12 novembre `31e3943` e `ab5a946`, rispetto all'ultima pubblicazione comune `71ce4f1`. Snapshot remoto osservato: `ab5a946c1f94018edad90e69bc5544306f913569`; fetch completato senza merge, checkout o push. Fonti: [commit del codice](https://github.com/Federico-cia/Whareformer-SuperFlex-Project/commit/ab5a946c1f94018edad90e69bc5544306f913569) e [README a quella revisione](https://github.com/Federico-cia/Whareformer-SuperFlex-Project/blob/ab5a946c1f94018edad90e69bc5544306f913569/Whareformer/README.md). Nessuna modifica a `SuperFlex/` o al matcher pubblicata in questi commit.

## Che cosa ha fatto

1. **Inferenza baseline dichiarata.** Il README riferisce una run Whareformer preaddestrata su `P01_01`. `track_match_report.json` riporta 33310 frame, 110590 righe predette tutte ricondotte esattamente alle annotazioni sorgenti, zero fallback IoU e zero righe senza corrispondenza, 52 track con osservazioni abbinate. Non sono 110590 identità corrette: si verifica la provenienza delle osservazioni, non la qualità dell'associazione temporale.
2. **Recupero degli ID di osservazione.** `build_tracks_by_id.py` legge `tracking_outputs.pkl` e `object_annotations.json`, cerca per frame categoria e bounding box, usa IoU almeno 0.95 solo se manca la corrispondenza esatta e il migliore è univoco. Consuma ciascuna annotazione al massimo una volta per frame, senza presumere che ordine delle track e ordine delle detection coincidano. Produce `tracks_by_id.json` con track, ID dell'osservazione, indice, box e XYZ; segnala i mancati abbinamenti.
3. **Join alle geometrie.** `link_compare200_tracks.py` collega per `(frame RGB, annotation_id)` il manifest del nostro pacchetto alle track. Conserva DA/MoGE separati e gli esiti mancanti/ambigui. Produce un manifest arricchito, un report e una tabella delle track candidate. Questo è il ponte dati richiesto, non un contributo geometrico alle decisioni Whareformer.
4. **Candidato multivista riferito.** Il collega dichiara di aver controllato visivamente la track 9, padella rossa: 18 osservazioni sparse. Questa revisione non ripete né certifica quella valutazione visiva.

## Risultati caricati e controlli svolti

| Quantità riportata per P01_01 | Valore | Interpretazione |
|---|---:|---|
| Geometrie nel manifest | 73 osservazioni, 40 RGB | Solo il sottoinsieme P01_01 delle 299 osservazioni totali |
| Geometrie collegate | 71/73, circa 97.3% | ID della singola osservazione, non identità fisica persistente |
| Track con geometria | 18 | 9 con almeno due osservazioni, 5 con almeno cinque |
| Track 9 / 35 | 18 / 13 osservazioni, categoria pan | Candidati; stessa categoria non garantisce stessa identità |
| Track 4 | 9, chopping board e grater | Segnale da revisionare prima di trattarla come unico oggetto |
| Track 36 | 5, saucepan e sieve | Stessa cautela; possibili fusioni d'identità o problemi di etichette |

I due casi non collegati sono `frame_0000022584__a02` (pan, ID non trovato nel frame) e `frame_0000040874__a01` (kettle, frame non presente nelle predizioni). Le due osservazioni esistono nel nostro manifest; la causa a monte non si ricava dai soli report. Non assegnarle a una track per somiglianza o vicinanza senza un controllo esplicito.

**Verifiche effettive della revisione:** aritmetica dei JSON e accordo con tutte le 18 righe CSV; 73 osservazioni/40 RGB e ID dei due casi mancanti controllati nel pacchetto originale. Eseguiti controlli sintetici isolati sul codice esatto del commit: ordine diverso fra predizioni e annotazioni con due oggetti della stessa categoria; conservazione delle righe non abbinate; distinzione fra ID assente e frame assente; rifiuto di chiavi duplicate nel join. Tutti superati. Evidenza con hash dei sei file: `outputs/github_review_20261113/verification.json`; procedura locale `shared_exports/audit_github_update_20261113.py`.

Consultata anche la copia locale originale Whareformer: `load_object_data` conserva l'ordine delle annotazioni e `_prepare_detections` usa quell'ordine per box, feature e posizione. Il recupero dell'indice è quindi compatibile con quel loader. Questo non dimostra che la versione effettivamente eseguita dal collega sia identica.

**Limite di riproducibilità:** i nuovi upload non includono il pickle completo, le annotazioni effettivamente lette, `tracks_by_id.json`, `compare200_joined_observations.json`, feature visive, configurazione/ambiente/checkpoint della run o metriche dell'evaluator. I conteggi reali restano risultati riportati dal collega e internamente coerenti, non una run o un join indipendentemente ripetuti. Gli script richiedono la repository originale e asset esterni. Non controllano esistenza/hash delle nuvole: i percorsi assoluti generati non ne provano la disponibilità.

## Conseguenze scientifiche

**Mapping e correttezza della track sono due problemi distinti.** Il primo indica da quale maschera/nuvola proviene una detection. Il secondo richiede sapere se osservazioni assegnate alla stessa track rappresentino lo stesso oggetto nel tempo. Le categorie miste delle track 4 e 36 motivano una revisione prioritaria; i report da soli non certificano la causa. La coerenza di categoria delle track 9 e 35 non basta a escludere scambi fra padelle.

**Identità comune e registrazione 3D sono ulteriormente distinte.** Le nuvole sono camera-frame; DA grezzo e MoGE non condividono una scala metrica certificata. Per accumulare serve un riferimento comune dell'oggetto, con scala/posa e movimento gestiti. La sola posa della camera non allinea una padella manipolata. Una fusione sbagliata può compromettere l'input SuperFlex anche se il mapping degli ID è esatto. Nessuna registrazione, fusione, nuova inferenza su accumuli o misura di qualità è pubblicata qui.

**Direzione del flusso.** Il nuovo codice realizza Whareformer → raggruppamento delle geometrie. La domanda approvata richiede inoltre geometria SuperFlex → decisione Whareformer. Ricostruire meglio usando track fisse non dimostra che la forma migliori IDF1/mPCL. Per l'eventuale valutazione tracking la memoria deve usare soltanto il passato e aggiornarsi dopo le associazioni predette; accumuli dell'intero video non possono essere usati retroattivamente.

## Priorità operative raccomandate, non nuovo metodo approvato

1. **Rendere verificabile il ponte su P01_01.** Acquisire i due manifest completi prodotti dagli script, riferimento/versione della baseline e configurazione/comando/checkpoint; rendere disponibili o rigenerabili gli input della run. Ripetere il join con controlli di unicità, ordine reale delle detection, hash/percorso delle nuvole, due mancati abbinamenti e disponibilità delle metriche baseline. Non ripetere le inferenze geometriche già concluse.
2. **Diagnosticare le track.** Revisionare almeno i casi misti 4/36 e i candidati padella 9/35. Annotazioni visive indipendenti restano per valutazione; non sostituire le associazioni predette del metodo con etichette oracle. Non scegliere solo le track riuscite per sostenere conclusioni generali.
3. **Chiudere l'integrazione approvata.** Usare il ponte per collegare il componente di confronto/memoria esistente al ciclo matcher/tracker reale; prima registrazione diagnostica senza influenza, poi controllo a peso geometrico zero equivalente alla baseline. DA/MoGE configurabili, punti come controllo; feature/XYZ originali e gestione delle geometrie mancanti invariati. L'architettura dell'adattatore rimane da scegliere.
4. **Sviluppo e test separato.** Calibrare il contributo soltanto sullo sviluppo, fissare le scelte e confrontare baseline, punti e SuperFlex su associazioni predette, con metriche ufficiali, copertura/fallimenti e costo. Le geometrie sparse di compare200 sono utili per il ponte e la diagnosi, non garantiscono copertura adeguata di una valutazione tracking completa. Definire la copertura necessaria prima di ampliare i calcoli.

**Opzioni rispetto all'accumulo:** raccomandato mantenere il tracking come percorso principale, senza aggiungere registrazione/fusione come prerequisiti; un piccolo pilota multivista su una track verificata può essere un'estensione separata, purché non ritardi integrazione/test e dichiari criteri di qualità; sostituire la domanda con la ricostruzione richiederebbe una scelta esplicita di Marco e un protocollo diverso. Nessuna di queste alternative viene adottata automaticamente dalla revisione.

Domanda, dataset, DA/MoGE, controllo sui punti, separazione sviluppo/test e scadenza del 23 novembre restano invariati. Nessun messaggio al collega, push, nuovo job HPC o esperimento neurale in questa analisi.
