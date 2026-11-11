# Roadmap operativa — progetto Computer Vision

Aggiornata l'11 novembre 2026. Domanda approvata in `FASE_0.md`: utilità della memoria di forme SuperFlex per l'associazione Whareformer, con osservazioni, feature e XYZ comuni. Scadenza confermata: 23 novembre. Nessuna nuova data intermedia fissata.

| Fase | Contributo e stato |
|---|---|
| Fattibilità geometrica | Installazioni, input EPIC, DA/MoGE e SuperFlex funzionanti; confronto 200 concluso. Dimostrata eseguibilità e compatibilità 2D descrittiva, non fedeltà 3D o beneficio tracking. |
| Verifica del segnale | 8797 coppie precalcolate; prima analisi di identità disponibile. Il campione con negativi entro categoria è troppo limitato per scegliere una sorgente o validare SuperFlex in generale. |
| **Chiusura autonoma attuale** | Marco ha approvato sviluppo del codice e run HPC necessari: pipeline portabile, evidenze consolidate, export e componente di confronto/memoria, consegna riproducibile. Piano unico in `PIANO_CHIUSURA_RAMO_GEOMETRICO.md`; checklist in `TODO.md`. Non attendere il codice del collega. |
| Integrazione e valutazione comune | Richiede baseline reale, mapping alle detection e controllo con contributo geometrico zero. Confrontare baseline, punti e SuperFlex mantenendo DA/MoGE configurabili; calibrazione e test separati. Non ancora completata. |

DA e MoGE restano in parallelo fino a convenienza chiara per utilità, affidabilità e costo; l'IoU 2D da sola non decide. Nessuna superiorità generale assunta. Confronti appaiati e fallimenti espliciti; più coppie correlate non equivalgono a più identità indipendenti.

Marco segue geometria/SuperFlex; il collega Whareformer/integrazione/valutazione; protocollo e report sono condivisi. `roadmap separata per ruolo.md` riassume i confini. Risultati nei due resoconti `RISULTATI_CONFRONTO_200.md` e `RISULTATI_IDENTITA_DA_MOGE.md`; stato operativo in `STATO_LAVORO.md`. Le vecchie sequenze dei piloti sono storiche, non ulteriori attività da svolgere.
