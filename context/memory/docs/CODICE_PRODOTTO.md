# Che cosa abbiamo prodotto in codice

## Memoria a stati del punto 3 — 21 novembre 2026

Nuovi moduli scene_geometry, scene_memory, registration_verifier e run_scene_memory; adapter del coordinatore e 23 nuovi test. [Resoconto e limiti](../IMPLEMENTAZIONE_PUNTO3_20261121.md), [contratti e uso](../../../integration_prototype/SCENE_MEMORY.md). Nucleo software verificato, non modello addestrato o pipeline GPU completa. Script di scarico audit aggiornato; nessun accesso HPC dell'assistente.

## Codice aggiunto il 21 novembre 2026 (sera)

- `integration_prototype/full_p01_enrichment.py`: acquisizione/verifica di RGB e maschere e arricchimento geometrico di tutte le osservazioni P01_01 a blocchi, con catena di job per ramo e cache della pipeline. Corretto il PATH dell'ambiente per stadio (errore `ninja`).
- `integration_prototype/audit_ammissione.py`: audit di fattibilità del punto 3 in sola lettura (DA grezza contro allineata con funzioni originali Whareformer, riferimento di posa dalle camere, confronto con il registratore attuale; nessuna soglia decisionale).
- `strumenti_hpc/`: script locali di controllo, diagnosi, ripresa e invio usati da Marco sull'HPC; contengono l'utente HPC e non sono destinati alla pubblicazione.

## Estrazione supervisionata del training — 21 novembre 2026

`integration_prototype/training_enrichment.py` ricostruisce input/target con oracle e memorie originali e collega geometrie esistenti con provenienza/archivio strettamente passato, senza nuova selezione/fusione. `verify_training_enrichment.py` verifica target, storia completa e artefatti. Tre test locali/remoti passati; 782875 concluso 0:0 e 446 esempi/247 frame validati, copia locale confrontata con 110590 annotazioni ufficiali. [Resoconto](../ARRICCHIMENTO_TRAINING_20261121.md). Campione di sviluppo con zero Nuova track, non training completo; nessuna nuova inferenza o addestramento. Codice originale/mappa/filtri preservati.

## Esito campagna — 15 novembre 2026

29/29 configurazioni completate e valutate, tutti i job conclusi 0:0, controlli zero esatti e nessuna assegnazione diversa dalla baseline. Report finali acquisiti; dettagli nella memoria corrente, risultati della campagna del 15 novembre. Non introdotte nuove modifiche al codice in fase di acquisizione.

## Campagna estesa — 15 novembre 2026

Aggiunti selezione/validazione del campione, costruzione del bundle e gestore HPC con ricevute e dipendenze. Rigenerazione DA/MoGE/SuperFlex su 247 frame/446 osservazioni selezionate, 29 configurazioni di sviluppo; risultati ancora pendenti. Solo telemetria estesa nel runner, nessuna modifica a reti o filtri. Dettaglio operativo in CAMPAGNA_HPC_20261115.md nella memoria corrente.

## Pubblicazione della prima run completa — 14 novembre 2026

Codice, configurazione, audit e report pubblicati su main al commit 8694e4b46be288e7be8ab008a21c765bba01ee15, riferimento remoto verificato dopo il push. Storia precedente preservata da 0865949, nessun force push; contributi del collega e ultime modifiche manuali della mappa preservati. Input completi, pesi e accessi esclusi. Controllo finale: 408 collegamenti, 36 sorgenti Python e 156 hash senza errori; servizio mappa verificato in sola lettura. Locale 72 casi, 70 passati e due skip motmetrics; HPC 72/72 senza skip. I job 764454 e 764474 sono conclusi 0:0, output completi acquisiti.

Il riferimento corrente è la [documentazione dell’integrazione](../../../integration_prototype/README.md), insieme al [nucleo geometrico](../../../SuperFlex/README.md). Stato e attività sono in [memoria corrente](../README.md).
