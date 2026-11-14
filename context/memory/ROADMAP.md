# Roadmap corrente

## Priorità corrente — esecuzione completa prima dei confronti

Il mandato più recente richiede una prima run fino alla fine della sequenza ufficiale P01_01 con geometria attiva, cache dichiarate e SuperFlex sugli aggiornamenti ammessi. Run 764454 conclusa e audit 764474 superato: sette fusioni ammesse, 25 nuove ricostruzioni e uso futuro verificato; nessun miglioramento tracking. Dettagli in STATO_LAVORO.md e REGISTRO_CRITICITA_PIPELINE.md. Frontend RGB rigenerato, copertura estesa e confronti/ottimizzazione restano lavori distinti; nessuno sostituisce o blocca la verifica operativa completata. Revisione dei filtri ancora rinviata. Le fasi precedenti non implicano una nuova approvazione per modificare tali filtri.

| Fase | Stato | Criterio di avanzamento |
|---|---|---|
| Contratto dati e consegna collega | Verificati | Mapping e hash controllati, due alias esclusi |
| Matcher causale e aggiornamento geometrico | Implementati e verificati | Memoria precedente alle query; controllo zero esatto |
| SuperFlex differita e ritorno al matcher | Verificati nella prima run completa | 25 nuove ricostruzioni, sette fusioni ammesse e uso futuro verificato; accuratezza fisica aperta |
| Varianti, valutatore e comando comune | Collegati e verificati | Nove varianti zero completate e valutate |
| Frontend da immagini | Rigenerazione parziale, cache usata nella run completa | Cache verificata; asset e rigenerazione ancora da completare |
| Copertura, calibrazione e test separato | Pendenti | Input sufficienti, protocollo e limiti espliciti |
| Conclusioni e consegna finale | Pendenti | Prima run a peso non nullo chiusa, metriche invariate; validazione generale pendente |

Il metodo è descritto nel [ciclo geometrico](ROADMAP_CICLO_GEOMETRICO.md). Per i dettagli dello step attivo: [piano frontend](PIANO_FRONTEND_UNIFICATO_20261114.md) e [avanzamento](FRONTEND_AVANZAMENTO_20261114.md). Le attività sono in [TODO](TODO.md); la storia metodologica resta nel [registro decisioni](REGISTRO_DECISIONI.md) e nell'[archivio](README.md).

**Vincolo corrente:** la revisione dei filtri di fusione è rinviata. Non trasformare la calibrazione successiva in un'autorizzazione a modificare questi filtri ora. Nessun beneficio tracking con peso 0.1; fusioni eseguite e provenienza verificata, accuratezza fisica non certificata.

Due persone, circa due ore al giorno ciascuna, scadenza 23 novembre; Marco geometria e collega tracking. Privilegiare controlli piccoli e informativi senza ripetere i job già conclusi.
