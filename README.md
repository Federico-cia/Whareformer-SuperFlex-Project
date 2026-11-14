# Whareformer–SuperFlex

Studio del contributo della forma 3D all'associazione delle identità in video egocentrici. Il ciclo confronta l'osservazione con la memoria geometrica precedente, associa l'oggetto alla track, aggiorna i punti osservati ammessi e ricostruisce la forma per i frame successivi.

| Area | Contenuto |
|---|---|
| [SuperFlex](SuperFlex/README.md) | Geometria DA/MoGE, ricostruzione e confronto delle forme |
| [Whareformer](Whareformer/) | Consegna e riproducibilità della baseline del collega |
| [Integrazione](integration_prototype/README.md) | Matcher causale, memoria, varianti, valutazione e comando di esecuzione |
| [Mappa](mappa_interattiva/README.md) | Rappresentazione modificabile del sistema |
| [Memoria corrente](context/memory/README.md) | Decisioni, roadmap e ripresa del lavoro con qualsiasi assistente |
| [Evidenze](context/evidence/README.md) | Risultati acquisiti e inventario con hash |
| [Archivio scientifico](context/memory/README.md) | Resoconti storici, distinti dalle istruzioni operative |

Il percorso da cache verificata è implementato. La rigenerazione neurale completa da immagini rimane aperta. I controlli a peso zero riproducono la baseline; non è ancora dimostrato un miglioramento del tracking o una fusione multivista reale. La revisione dei filtri di fusione è rinviata per decisione di Marco.

Per eseguire codice e test seguire le [istruzioni di integrazione](integration_prototype/README.md). Dati completi e checkpoint richiedono acquisizione separata; gli esempi non li scaricano implicitamente. Per riprendere lo sviluppo leggere [stato](context/memory/STATO_LAVORO.md), [attività](context/memory/TODO.md) e [guida tecnica](context/memory/LEGGIMI_PASSAGGIO_AI.md).

Verifica della struttura, dei collegamenti locali e degli hash:

```bash
python tools/check_repository.py
# Con Node.js, verifica in sola lettura anche il servizio della mappa:
node tools/check_map.cjs
```
