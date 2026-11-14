# Roadmap corrente

| Fase | Stato | Criterio di avanzamento |
|---|---|---|
| Contratto dati e consegna collega | Verificati | Mapping e hash controllati, due alias esclusi |
| Matcher causale e aggiornamento geometrico | Implementati e verificati | Memoria precedente alle query; controllo zero esatto |
| SuperFlex differita e ritorno al matcher | Verificati su inizializzazioni | Sei ricostruzioni reali; nessuna fusione multivista dimostrata |
| Varianti, valutatore e comando comune | Collegati e verificati | Nove varianti zero completate e valutate |
| Frontend da immagini | Parziale, step attivo approvato | Cache verificata; asset e rigenerazione ancora da completare |
| Copertura, calibrazione e test separato | Pendenti | Input sufficienti, protocollo e limiti espliciti |
| Conclusioni e consegna finale | Pendenti | Risultati reali a peso geometrico non nullo o esito negativo documentato |

Il metodo è descritto nel [ciclo geometrico](ROADMAP_CICLO_GEOMETRICO.md). Per i dettagli dello step attivo: [piano frontend](PIANO_FRONTEND_UNIFICATO_20261114.md) e [avanzamento](FRONTEND_AVANZAMENTO_20261114.md). Le attività sono in [TODO](TODO.md); la storia metodologica resta nel [registro decisioni](REGISTRO_DECISIONI.md) e nell'[archivio](README.md).

**Vincolo corrente:** la revisione dei filtri di fusione è rinviata. Non trasformare la calibrazione successiva in un'autorizzazione a modificare questi filtri ora. Nessun beneficio nel tracking o fusione multivista ancora dimostrati.

Due persone, circa due ore al giorno ciascuna, scadenza 23 novembre; Marco geometria e collega tracking. Privilegiare controlli piccoli e informativi senza ripetere i job già conclusi.
