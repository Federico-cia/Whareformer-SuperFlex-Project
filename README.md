# Whareformer–SuperFlex

Studio del contributo della forma 3D all'associazione delle identità in video egocentrici. Il sistema confronta l'osservazione con la memoria precedente, esegue l'associazione, aggiorna gli stati di posizione e i punti ammessi e ricostruisce la forma per i frame successivi. **Nessun beneficio di tracking dimostrato finora.**

## Stato e ingressi

Memoria opzione A implementata: stati di posizione separati dalla forma persistente, criterio di riproiezione e baseline appresa di ammissione. Mappa aggiornata e dati allineati disponibili come asset esterni. Modello del matcher, affidabilità reale, costo della memoria, copertura completa e test indipendente restano da concludere. [Stato datato](context/memory/STATO_LAVORO.md), [attività](context/memory/TODO.md), [decisioni](context/memory/REGISTRO_DECISIONI.md).

| Area | Contenuto |
|---|---|
| [Integrazione](integration_prototype/README.md) | Contratti, memoria, matcher e valutazione |
| [SuperFlex](SuperFlex/README.md) | Nucleo geometrico portabile |
| [Whareformer](Whareformer/) | Consegna e risultati del collega, preservati |
| [Mappa HTML](mappa_interattiva/README.md) | 39 riquadri e 53 collegamenti, testi confermati |
| [Memoria corrente](context/memory/README.md) | Ripresa del lavoro e istruzioni |
| [Evidenze](context/evidence/README.md) | Risultati essenziali, non dati completi |
| [Archivio](context/archive/) | Resoconti e storia delle revisioni |

## Esecuzione e verifiche

Seguire [ambiente e test](integration_prototype/README.md). Il clone non include dataset, checkpoint o sorgenti completi degli autori: [asset richiesti](context/evidence/ASSET_ESTERNI.md). Le prove da input/cache verificati non certificano un frontend RGB autonomo o fusioni fisicamente corrette.

```bash
python tools/check_repository.py
node tools/check_map.cjs
```

La prima run completa e la successiva griglia sono documentate nelle [evidenze](context/evidence/README.md); configurazioni di sviluppo e copertura sparsa non equivalgono a test indipendente. I risultati del collega restano attribuiti al loro autore e non sono ricalcolati da questo aggiornamento.
