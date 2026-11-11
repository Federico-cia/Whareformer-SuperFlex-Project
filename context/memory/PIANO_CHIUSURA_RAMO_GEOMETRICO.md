# Chiusura del ramo geometrico autonomo

Mandato approvato da Marco l'11 novembre 2026 per la nuova chat con Astra: completare codice e run HPC necessari, senza micro-proposte o attese del collega. L'obiettivo finale resta l'utilità delle forme SuperFlex nell'associazione Whareformer; questa fase consegna il componente autonomo e le evidenze che possiamo ottenere senza la baseline reale.

## Risultati da consegnare

1. **Pipeline riutilizzabile.** Da RGB/maschere/camera a punti DA oppure MoGE, poi inferenza SuperFlex robust ed export. Percorsi e sorgente configurabili, versioni/checksum, preprocessing, fallimenti espliciti e ripresa coerente con codice/configurazione/input. Eliminare dai runner pubblicabili dipendenze implicite da vecchi run; riusare il nucleo già revisionato. Non riscrivere le reti degli autori o reinstallare ambienti funzionanti.
2. **Valutazione consolidata.** Accertare prima la semantica degli identificativi nelle annotazioni originali: UUID diversi nei manifest non escludono identità persistenti nel dataset. Conservare evidenza e incertezza delle etichette; le 37 osservazioni attuali sono revisione visiva, non GT certificata. Cercare ripetizioni della stessa istanza e istanze diverse della stessa categoria. Riutilizzare le distanze esistenti; aggiungere dati di sviluppo/calcoli soltanto per lacune effettive, con selezione dichiarata prima delle predizioni. Confrontare punti/SuperFlex × DA/MoGE su osservazioni comuni, riportando stabilità, discriminatività, copertura, fallimenti, costo ed esempi. Non scegliere etichette/campione in funzione dei punteggi; non confondere coppie correlate con identità indipendenti.
3. **Interfaccia pronta.** Export per osservazione con chiave, video/frame/maschera, sorgente, unità/assi, geometria, validità e provenienza. Collegamento alla detection esterna previsto ma non dichiarato verificato. Componente indipendente di confronto/memoria semplice e configurabile, aggiornato causalmente dopo l'associazione; casi mancanti e test significativi. Regole e distanze candidate vanno motivate e distinte dal metodo definitivo, che richiede validazione.
4. **Consegna riproducibile.** Codice pulito, esempio eseguibile, istruzioni brevi, tabelle/figure e conclusioni proporzionate. Formati dei dati e dipendenze espliciti; dati/pesi fuori Git, con provenienza e condizioni delle fonti. Memoria aggiornata, controllo riservatezza prima della pubblicazione. Non servono ulteriori esperimenti quando non risolvono un'incertezza rilevante.

## Esecuzione e criteri di chiusura

All'avvio leggere stato, checklist, registro e questo piano; verificare gli asset necessari senza ripetere audit conclusi. Organizzare una sola sequenza di sviluppo e valutazione: recupero/riuso degli output, portabilità dei runner, verifica delle identità, nuovi calcoli informativi se necessari, export/memoria, consegna. Codifica e preparazione dei dati possono procedere mentre i job sono in coda.

Le nuove inferenze dei modelli si eseguono via SLURM sull'HPC. Registrare configurazione/campione prima del lancio, misurare soltanto i nuovi percorsi non ancora validati, dimensionare risorse e limite temporale su evidenze, seguire ogni job fino a esito/output verificati. Conservare identificativi, log, hash e fallimenti; nessuna eliminazione o sovrascrittura dei run originali. Riutilizzare setup, pesi e quattro ambienti già funzionanti. Non rilanciare il confronto 200 o il precalcolo 8797 coppie come nuovo esperimento.

Il mandato autorizza il lavoro ordinario necessario entro EPIC e la domanda già approvata; non richiede conferme a ogni passaggio. Cambi sostanziali di domanda/dataset/protocollo, training da zero o costi rilevanti restano decisioni da discutere. Mantenere test finale separato; nessun tuning sul test.

**Parte autonoma conclusa** quando una persona può elaborare nuove osservazioni, ottenere punti/forme validati, confrontarli e utilizzare la memoria attraverso un'interfaccia documentata senza ricostruire i vecchi esperimenti, e quando il rapporto descrive evidenze e limiti dell'utilità del segnale. Se le identità disponibili non permettono una valutazione più forte, dichiarare il limite e consegnare le altre componenti senza fabbricare etichette.

Restano alla fase comune: mapping alle detection reali e segnali Whareformer, integrazione nel matcher, equivalenza a contributo zero e beneficio tracking. Nessuna simulazione o diagnostica oracle sostituisce queste prove.

## Dove lavorare

- Radice dell'archivio: cartella `lavoro di gruppo/`. Runner e inventario: `scripts/README.md`, `docs/CODICE_PRODOTTO.md`, `manifests/code_inventory.json`.
- Codice selezionato e pubblicabile: `shared_exports/publish_candidate/SuperFlex/`, ramo `prepare/superflex-core`. Memoria condivisa: `shared_exports/publish_candidate/context/memory/`. Usare questo worktree per nuove modifiche condivisibili; mantenere distinta la cronologia dell'archivio locale. Non fare push di `main` locale né merge in blocco dei vecchi script.
- Risorse e risultati: `data/compare200/`, `outputs/compare200_749968/`, `outputs/shape_identity_v1/`, manifest dei run e copie degli autori escluse da Git. I due resoconti `RISULTATI_CONFRONTO_200.md` e `RISULTATI_IDENTITA_DA_MOGE.md` descrivono metodo e limiti; `REVISIONE_CODICE_REPOSITORY.md` elenca le verifiche del nucleo già concluse. L'installazione del pacchetto è stata verificata in `shared_exports/code_review_env/`; non rifare la regressione completa senza modifiche che la giustifichino.
- HPC: `~/cv_project/`; ambienti `cv-superflex`, `cv-epic-depth`, `cv-moge2`, `cv-epic-geometry-cpu`. I job storici esplicitano i layout; verificarli prima del riuso, senza assumere che i runner siano portabili.
- Accesso non interattivo verificato l'11 novembre con la chiave esistente; coda personale vuota, nessun nuovo job inviato per questo passaggio. Configurazione solo locale, consultabile tramite `scripts/abilita_accesso_hpc.ps1`: non rieseguirlo o creare chiavi se SSH funziona. Non leggere/esporre la chiave privata o chiedere password in chat. Usare connessione e verifica del server già configurate; gli eventuali permessi dell'app sono distinti dalle credenziali HPC.

Le informazioni di stato vanno aggiornate dopo risultati e decisioni effettivi, mantenendo brevi i documenti di ingresso e collegando i resoconti invece di duplicarli. Conversazioni informali escluse.
