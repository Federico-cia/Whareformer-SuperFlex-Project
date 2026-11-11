# Roadmap separata per ruolo

**Ultimo avanzamento del 9 novembre:** confronto su 200 nuove immagini di cinque video concluso: 299 osservazioni e 890 mesh, risultati in `RISULTATI_CONFRONTO_200.md`. DA grezzo raccomandato, scelta definitiva ancora aperta. Persona B: corrispondenze e campione con identità verificate, stabilità/discriminatività e geometria semplice; persona A: baseline, interfaccia e poi valutazione del tracker. I blocchi sotto restano storici.

**Revisione del 9 novembre:** checklist corrente in [TODO.md](TODO.md), prevalente sul calendario iniziale sotto. Marco/persona B: MoGE-2 + VISOR → SuperFlex completato senza miglioramento visivo sistematico; prossimo lavoro corrispondenze e campione con identità verificate, poi forme e geometria semplice. Persona A: baseline Whareformer e interfaccia per forma/memoria nel matcher in parallelo; poi prototipo e valutazione. Insieme: campione, distanza, memoria e protocollo. SAM3 opzionale. Nessuna nuova data intermedia concordata.

**Aggiornamento: 7 novembre 2026.** Ruoli confermati dal gruppo: **Marco segue geometria e SuperFlex (persona B); l'altro membro segue Whareformer, integrazione e valutazione (persona A)**. Dettagli operativi e date intermedie restano una bozza da discutere e aggiornare in base ai progressi. Scadenza del progetto: **23 novembre 2026**.

Le righe seguono lo stesso calendario. Gli step condivisi hanno testo identico nelle due colonne. Tutte le esecuzioni dei modelli avvengono sull'HPC Bocconi.

| Persona A — altro membro: Whareformer e valutazione | Persona B — Marco: geometria e SuperFlex |
|---|---|
| **4–5 nov · Insieme.** Preparare il repository, scegliere il campione EPIC iniziale e concordare il formato dei dati da scambiarsi. | **4–5 nov · Insieme.** Preparare il repository, scegliere il campione EPIC iniziale e concordare il formato dei dati da scambiarsi. |
| **5–8 nov.** Eseguire Whareformer sull’HPC con i file degli autori. Verificare il funzionamento e calcolare le metriche ufficiali. | **5–8 nov.** Eseguire SuperFlex robust sull’HPC con gli esempi degli autori. Verificare le forme prodotte. |
| **8–11 nov.** Studiare l’associazione delle identità e preparare il codice per ricevere le forme degli oggetti. | **8–11 nov.** Ricavare le nuvole di punti degli oggetti EPIC da maschere e profondità. Applicare SuperFlex e controllare la qualità. |
| **11 nov · Insieme.** Esaminare gli input 3D e le forme ottenute. Decidere se sono abbastanza affidabili per proseguire. | **11 nov · Insieme.** Esaminare gli input 3D e le forme ottenute. Decidere se sono abbastanza affidabili per proseguire. |
| **11–13 nov.** Individuare gli errori di Whareformer e verificare se la forma può aggiungere informazioni rispetto ad aspetto e posizione. | **11–13 nov.** Verificare se le forme sono coerenti fra viste dello stesso oggetto e distinguono oggetti diversi. Confrontarle con una geometria semplice. |
| **13 nov · Insieme.** Scegliere come confrontare le forme, aggiornare la memoria e valutare il metodo, mantenendo separato il test finale. | **13 nov · Insieme.** Scegliere come confrontare le forme, aggiornare la memoria e valutare il metodo, mantenendo separato il test finale. |
| **14–17 nov.** Integrare forma corrente e memoria geometrica nell’associazione di Whareformer. Verificare il funzionamento dell’integrazione. | **14–17 nov.** Preparare forme SuperFlex e geometria semplice per gli esperimenti. Registrare tempi di elaborazione e casi falliti. |
| **17 nov · Insieme.** Provare la pipeline completa su pochi dati di sviluppo e correggere eventuali problemi. | **17 nov · Insieme.** Provare la pipeline completa su pochi dati di sviluppo e correggere eventuali problemi. |
| **18–20 nov.** Confrontare Whareformer originale, geometria semplice e SuperFlex. Raccogliere IDF1, mPCL e tabelle dei risultati. | **18–20 nov.** Analizzare successi e fallimenti, preparare esempi visivi e misurare il costo della componente geometrica. |
| **20 nov · Insieme.** Interpretare i risultati: quando aiuta la forma e quale vantaggio offre specificamente SuperFlex? | **20 nov · Insieme.** Interpretare i risultati: quando aiuta la forma e quale vantaggio offre specificamente SuperFlex? |
| **21–22 nov.** Completare il report su Whareformer, integrazione e valutazione. Revisionare la parte della persona B. | **21–22 nov.** Completare il report su dati 3D, SuperFlex e analisi degli errori. Revisionare la parte della persona A. |
| **23 nov · Insieme.** Controllare report, presentazione, repository e istruzioni per riprodurre gli esperimenti. Completare la consegna. | **23 nov · Insieme.** Controllare report, presentazione, repository e istruzioni per riprodurre gli esperimenti. Completare la consegna. |

La scrittura delle rispettive sezioni comincia durante gli esperimenti. Se i controlli sulla qualità o sull'utilità della forma falliscono, discutere una riduzione dello scope prima dell'integrazione completa. La roadmap scientifica e i criteri di verifica sono descritti in `ROADMAP.md` e `FASE_0.md`.
