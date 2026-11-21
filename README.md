# Whareformer–SuperFlex


## Stato al 21 novembre 2026

Punto 3: [prima implementazione della memoria a stati](integration_prototype/SCENE_MEMORY.md),
non verificatore principale addestrato o validazione completa. [Audit acquisito](context/memory/RISULTATI_AUDIT_AMMISSIONE_20261121.md)
e [limite di capacità HPC](context/memory/PULIZIA_E_RIPRESA_HPC_20261121.md).
La ripresa e i job sono registrati con data/ora nello [stato](context/memory/STATO_LAVORO.md);
non sono uno stato live. Priorità della prossima sessione: conservazione più
compatta degli output; scelte di test indipendente ancora aperte.

Studio del contributo della forma 3D all'associazione delle identità in video egocentrici. Il ciclo confronta l'osservazione con la memoria geometrica precedente, associa l'oggetto alla track, aggiorna i punti osservati ammessi e ricostruisce la forma per i frame successivi.

| Area | Contenuto |
|---|---|
| [SuperFlex](SuperFlex/README.md) | Geometria DA/MoGE, ricostruzione e confronto delle forme |
| [Whareformer](Whareformer/) | Consegna e riproducibilità della baseline del collega |
| [Integrazione](integration_prototype/README.md) | Matcher causale, memoria, varianti, valutazione e comando di esecuzione |
| [Mappa](mappa_interattiva/README.md) | Rappresentazione modificabile del sistema |
| [Memoria corrente](context/memory/README.md) | Decisioni, roadmap e ripresa del lavoro con qualsiasi assistente |
| [Evidenze](context/evidence/README.md) | Risultati acquisiti e inventario con hash |
| [Archivio scientifico](context/archive/) | Resoconti storici, distinti dalle istruzioni operative |

La [prima run completa su P01_01](context/evidence/full_video_20261114/REPORT.md) è conclusa: 33310 frame/110590 osservazioni del protocollo ufficiale, geometria a peso non nullo, sette fusioni ammesse e 25 nuove ricostruzioni SuperFlex. Le forme da fusioni entrano nei confronti successivi. Le assegnazioni restano identiche alla baseline: nessun miglioramento del tracking con questa configurazione.

La [campagna estesa del 15 novembre è conclusa](context/evidence/campaign_20261115_v1/REPORT_FINALE.md): 29/29 configurazioni completate e valutate, geometria su 247 frame/446 osservazioni. Tutte le assegnazioni e metriche coincidono con W0: nessun miglioramento nella griglia provata. Nessun job attivo/in attesa; filtri invariati e limiti di sviluppo dichiarati.

Nella prima run, feature visive/XYZ e geometrie delle osservazioni sono riusati da cache verificate, con copertura geometrica di 71 osservazioni in 38 frame. Nella campagna estesa, la geometria DA/MoGE/SuperFlex è rigenerata sulle 446 osservazioni selezionate; feature visive/PCA/XYZ ufficiali restano riusate. Non è una rigenerazione RGB completa o una verifica indipendente dell'accuratezza fisica delle fusioni. Il frontend da immagini rimane aperto; la revisione dei filtri è stata riattivata il 21 novembre, con primo nucleo software e validazione ancora pendente.

Per eseguire codice e test seguire le [istruzioni di integrazione](integration_prototype/README.md). Dati completi e checkpoint richiedono acquisizione separata; gli esempi non li scaricano implicitamente. Per riprendere lo sviluppo leggere [stato](context/memory/STATO_LAVORO.md), [attività](context/memory/TODO.md) e [guida tecnica](context/memory/LEGGIMI_PASSAGGIO_AI.md).

Verifica della struttura, dei collegamenti locali e degli hash:

```bash
python tools/check_repository.py
# Con Node.js, verifica in sola lettura anche il servizio della mappa:
node tools/check_map.cjs
```

La [mappa interattiva](mappa_interattiva/README.md) è aggiornata alla struttura Rami paralleli e ai testi confermati il 21 novembre: 39 riquadri e 49 collegamenti. [Provenienza e verifiche](context/evidence/map_20261121/README.md). Vecchi commenti revisionati e schede del punto 3 aggiornate su conferma di Marco; restano le [due integrazioni richieste, senza nuove etichette manuali](context/memory/FATTIBILITA_DUE_INTEGRAZIONI_20261116.md); nessuna nuova prova o cambio di metodo è implicito nella mappa.
