# Revisione prima della pubblicazione

**Pubblicazione e riservatezza, 11 novembre:** nucleo sotto `SuperFlex/` e memoria separata in `context/memory` pubblicati sul ramo `prepare/superflex-core`; `main` invariato. Controllati contenuti, nomi, snapshot raggiungibili e metadati dei nuovi commit; nessun pattern di credenziali rilevato. Rimosse dalle copie le configurazioni personali HPC e usata email autore GitHub no-reply. Originali locali conservati; escluso lo storico indipendente. Rapporto locale `shared_exports/publication_security.json`; controllo con pattern e revisione mirata, non garanzia assoluta. Il commit di solo codice ora è `cbd6ca1`, sostitutivo del non pubblicato `eac7002` senza variazione dei file. Le sezioni seguenti documentano la revisione precedente al caricamento.

11 novembre 2026. Richiesta: condividere soltanto codice essenziale, leggibile e verificato. Nessun file caricato su GitHub durante questa revisione.

## Esito e perimetro

La cartella storica non è il contenuto da pubblicare in blocco. Conserva prove concluse, duplicazioni e runner dipendenti da layout/cache HPC e identificativi di vecchi job. Gli originali e i risultati restano invariati per riproducibilità.

Preparata una candidata separata, basata sul ramo comune `origin/main` al commit `78eefcc2185330eb8b2e6b0241f34cc256e44dd8`:

- Directory: `shared_exports/publish_candidate/`.
- Ramo locale: `prepare/superflex-core`, commit `eac7002`.
- Delta: dieci file, circa 25 KB, tutti sotto `SuperFlex/`.
- Contenuto: sei moduli Python per geometria, preprocessing, distanze, analisi e CLI; un file di test; configurazione installabile, esclusioni e README breve.
- Per la futura pubblicazione usare questo ramo basato sulla repository comune. La cronologia `main` dell'archivio locale resta separata e comprende memoria/risultati non selezionati per questa consegna.

La candidata non include inferenza DA/MoGE/SuperFlex, acquisizione dei dati, modifiche al matcher o memoria delle track. Quei runner storici richiedono ancora separazione delle dipendenze dai vecchi esperimenti e verifiche dedicate prima dell'inclusione. Non presentare il nucleo pubblicabile come pipeline neurale completa o integrazione tracking realizzata.

## Problemi rilevati e trattamento

| Problema del materiale storico | Trattamento nella candidata |
|---|---|
| Funzioni ripetute e script pilota/generatori accanto alla pipeline corrente | Moduli unici per geometria, distanze, confronto e analisi; diagnostici fuori dalla pubblicazione |
| Riferimenti a run precedenti, directory personali o fisse e sorgenti estratte via AST | Input e percorsi espliciti; nessun import dai vecchi run, account o copie temporanee |
| Rilettura di manifest/hash e decompressione delle feature per ogni coppia | Geometrie caricate, verificate e descritte una volta, poi riusate in memoria |
| Ripresa basata su metadati che non coprono tutti i contenuti intermedi | Nessuna cache persistente implicita; hash delle geometrie verificati e registrati, output distinti senza sovrascrittura |
| Riepiloghi aggregati che possono mescolare categorie/video e favorire interpretazioni improprie | AUC sulle coppie comuni, separata per video e categoria; nessun punteggio globale presentato come beneficio tracking |
| Validazione degli output separata dal valutatore | Controlli di duplicati, coerenza video/frame, copertura, valori finiti/non negativi e scritture atomiche |

Il controllo statico critico dei 25 script Python storici non segnala errori sintattici o nomi indefiniti nelle regole esaminate. Questo non certifica portabilità o correttezza semantica di tutti gli script. Le fragilità di riuso non sono evidenza che i run già verificati fossero errati.

## Verifiche effettive

- Ambiente di revisione isolato: Python 3.11, NumPy 1.26.4, SciPy 1.15.3 e trimesh 4.6.8, coerenti con il confronto numerico. Nessun ambiente HPC modificato.
- Ruff: controllo statico e formato superati sui sei moduli e sul file di test.
- Sette test comportamentali superati: coordinate/pixel comuni, sampling/normalizzazione, invarianza e simmetria, interruzioni e sovrascrittura, forme mancanti, AUC/pareggi e separazione delle categorie.
- Installazione del pacchetto e comandi `python -m shape_tools` / `shape-tools` verificati nell'ambiente isolato.
- Regressione su dati salvati: **8797 coppie, 35188 righe**, stati mancanti concordi; errore massimo D2/spettro **5.06e-15**.
- Tutte le **12 AUC** P22_01 concordi con il resoconto originale; la nuova analisi evita il pooling fra categorie.
- **597 preprocessing** SuperFlex e **299 retroproiezioni** concordi con gli input salvati.
- **40 confronti ICP** del pilota concordi, errore massimo circa **5.28e-16**.
- Nessun riferimento personale/vecchio job o pattern di credenziali nella candidata; diff limitato a `SuperFlex/`, albero locale pulito dopo il commit.

Le due distanze economiche sono state ricalcolate in circa 10.4 secondi durante la regressione. Questo tempo **esclude ICP e inferenza** e non è confrontabile con i 47m26s del run completo originale. Non è una nuova misura di qualità scientifica.

Inventario/hash: `manifests/repository_candidate.json`. Evidenza numerica: `shared_exports/review_22ee8121/validation.json`. I controlli non sostituiscono la futura valutazione del tracking; nessun nuovo job HPC o inferenza neurale eseguiti.
