# Stato del lavoro e ripresa

Aggiornamento: 12 novembre 2026. Prevale sulle indicazioni operative storiche.

## Stato corrente

**Consegna autonoma completata**, entro il mandato dell'11 novembre: pipeline portabile DA/MoGE → punti → SuperFlex, export, confronto e memoria causale configurabile. Rapporto unico: [CONSEGNA_RAMO_GEOMETRICO.md](CONSEGNA_RAMO_GEOMETRICO.md), con risultati, costi, verifiche e limiti. Guida `shared_exports/publish_candidate/SuperFlex/PIPELINE.md`; codice sul ramo `prepare/superflex-core`. Nessun beneficio tracking o metodo definitivo dichiarato.

Riutilizzate 8797 coppie e 299 osservazioni; nessun rilancio del confronto 200. Audit di cinque archivi VISOR: 183312 record frame, 632169 maschere, 200 annotazioni selezionate verificate. ID di maschera unici, nessun ID globale fisico nei campi verificati; non esclude altre risorse. Conservate 37 osservazioni/sette identità visive e i loro limiti. Nove coppie entro intervallo aggiungono solo una diagnostica locale, separata dalle identità. DA, MoGE e controllo sui punti restano attivi.

## Job ed evidenze verificate

- 755696 GPU COMPLETED/0:0, 5m37s: primo percorso portabile.
- 755697 CPU FAILED/1:0, 1m46s: audit assumeva un solo record per frame; corretta la gestione degli intervalli alternativi.
- 755699 CPU COMPLETED/0:0, 2m14s: audit completo dei cinque archivi.
- 755709 GPU COMPLETED/0:0, 5m36s: versione finale, sei nuvole/cinque superfici e fallimento MoGE atteso, export compatto e ripresa. Undici test superati; hash del codice pipeline corrispondenti, controlli locali e statici superati.

Output `~/cv_project/runs/portable_validation_755709/` e `~/cv_project/runs/visor_original_audit.json`; log `~/cv_project/portable_755696.out/.err`, `portable_755709.out/.err`, `visor_audit_755697.out/.err`, `visor_audit_755699.out/.err`. Copie e verifiche in `outputs/geometric_closure_v1/`; export storico `observations.json` con radice geometrie `outputs/compare200_749968/`. Archivio finale scaricato con hash corrispondente. **Nessun job attivo nell'ultima lettura della coda.**

Il contratto è verificato; equivalenza numerica esatta alle vecchie inferenze no: errore relativo L2 massimo punti 0.0006212, differenza D2 fra superfici fino a 0.00513. Non cambiate le distanze scientifiche storiche. Memoria FIFO/D2/spettro è un candidato implementato, non una scelta validata.

## Asset e prossima fase

Worktree condivisibile `shared_exports/publish_candidate/`, repository `https://github.com/Federico-cia/Whareformer-SuperFlex-Project`, solo ramo `prepare/superflex-core`. Archivio locale con storia indipendente: non pubblicare main né importare lo storico. Dati/pesi/accessi fuori Git. Memoria condivisa in `context/memory/`; risultati essenziali in `SuperFlex/results/geometric_closure_v1/`.

HPC e quattro ambienti esistenti riusati; accesso con chiave già configurata, riferimento personale `scripts/abilita_accesso_hpc.ps1`, da non rieseguire. Non creare chiavi o chiedere password. Conservare run storici e quelli nuovi.

Prossimo passo dipendente dalla baseline: mapping alle detection reali, feature e XYZ; integrazione nel matcher, controllo a contributo zero, calibrazione sviluppo e test tracking separato. Non attribuire al collega attività non osservate. Obiettivo finale invariato, scadenza 23 novembre.
