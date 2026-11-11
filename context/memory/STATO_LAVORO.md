# Stato del lavoro e ripresa

Aggiornamento: 11 novembre 2026. Questo stato prevale sulle note operative storiche nei resoconti.

## Mandato attuale

Marco ha approvato il completamento coordinato di tutto il ramo geometrico eseguibile senza il contributo del collega, compresi codice e run HPC necessari, da proseguire in una nuova chat con Astra. Piano e criteri di chiusura in [PIANO_CHIUSURA_RAMO_GEOMETRICO.md](PIANO_CHIUSURA_RAMO_GEOMETRICO.md); registro voce 25. Non attendere la baseline per completare pipeline, valutazione del segnale, export e componente indipendente di confronto/memoria.

Obiettivo finale invariato: verificare se forme SuperFlex migliorino l'associazione Whareformer a parità di osservazioni, feature visive e XYZ. DA e MoGE restano in parallelo, con controllo sui punti. Distanza e memoria definitive non sono ancora validate; nessun beneficio tracking dimostrato. Scadenza: 23 novembre 2026.

## Evidenze disponibili — non ripetere

| Attività | Esito verificato e riferimento |
|---|---|
| Installazione e primi input | SuperFlex robust, DA, MoGE e geometria EPIC già eseguiti sull'HPC. Diagnostici e limiti nei resoconti `VERIFICA_*.md`; non reinstallare o ripetere gli esempi. |
| Confronto 200 | 200 immagini, cinque video, 299 osservazioni e 890 mesh nelle tre condizioni storiche. IoU appaiata DA grezzo 0.4697 / MoGE 0.4481: compatibilità 2D, non accuratezza 3D. `RISULTATI_CONFRONTO_200.md`, `outputs/compare200_749968/`. |
| Identità v1 | Job CPU 750536 COMPLETED/0:0, 47m26s, 8797 coppie e 35188 righe. Preparazione 750421 e pilota 750424 conclusi. Archivio, hash, firme e AUC verificati. `RISULTATI_IDENTITA_DA_MOGE.md`, `outputs/shape_identity_v1/`. |
| Limite delle identità | 37 osservazioni/sette identità revisionate visivamente; 149 coppie comuni alle quattro rappresentazioni. Negativi entro categoria soltanto due piatti P22_01: AUC D2 punti DA/SuperFlex DA/punti MoGE/SuperFlex MoGE = 0.612/0.627/0.701/0.768. Non è ground truth persistente certificata né un vincitore generale. |
| Codice condiviso | Nucleo installabile geometria/confronto/analisi, sette test e regressione superati: 8797 coppie, 12 AUC, 597 preprocessing, 299 retroproiezioni e 40 ICP. Inferenza neurale e acquisizione storiche ancora da rendere portabili. `REVISIONE_CODICE_REPOSITORY.md`. |

## Asset e accesso

- Archivio locale: `scripts/` per runner storici, `data/compare200/`, `outputs/`, `manifests/`, copie degli autori in `SuperFlex-repo/`, `Whareformer-repo/` ed `external/`. Inventario: `docs/CODICE_PRODOTTO.md` e `scripts/README.md`.
- Sviluppo condivisibile: worktree `shared_exports/publish_candidate/`, ramo `prepare/superflex-core`, repository `https://github.com/Federico-cia/Whareformer-SuperFlex-Project`. Il `main` dell'archivio locale ha storia indipendente: non pubblicarlo né fonderlo in blocco.
- Codice sotto `SuperFlex/`, memoria sotto `context/memory/`; dati/pesi/credenziali esclusi. Pubblicazione iniziale verificata a `65dea7a`, remoto `main` osservato a `78eefcc`. Ricontrollare i riferimenti prima di scrivere sul remoto. Audit di riservatezza locale: `shared_exports/publication_security.json`.
- **Accesso HPC ricontrollato l'11 novembre:** connessione SSH non interattiva riuscita con la chiave del progetto già presente; coda personale vuota. Nessuna nuova chiave necessaria, nessuna password da passare in chat, nessun job inviato in questa fase. Configurazione personale fuori Git; riferimento locale `scripts/abilita_accesso_hpc.ps1`, da consultare senza rieseguirlo se l'accesso funziona.
- HPC: `~/cv_project/`; ambienti già usati `cv-superflex`, `cv-epic-depth`, `cv-moge2`, `cv-epic-geometry-cpu`. Modelli tramite SLURM, partizione/QoS `stud`. Le risorse e i percorsi vanno verificati per il nuovo job senza rifare il setup. Run identità `~/cv_project/runs/shape_identity_v1/`, log `~/cv_project/shape_identity_750536.out/.err`.

## Dipendenze residue

Il mapping VISOR→RGB esiste, ma la corrispondenza con `detection_idx`, feature e XYZ reali della baseline non è certificata. Identificativi tutti distinti nei manifest diagnostici non dimostrano che VISOR sia privo di identità persistenti: controllare le annotazioni originali e documentarne la semantica. Il codice del collega non risultava caricato alla verifica del remoto; ciò non descrive il suo lavoro locale.

L'integrazione effettiva, il controllo di equivalenza a contributo geometrico zero e le metriche tracking dipendono dalla baseline. Preparare l'interfaccia ora, senza dichiarare questi risultati già ottenuti. Prossima esecuzione: seguire il piano di chiusura e la checklist `TODO.md`, non i vecchi ordini di lancio.
