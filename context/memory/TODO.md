# To-do corrente — chiusura del ramo geometrico

Mandato esecutivo approvato l'11 novembre: sviluppare codice ed eseguire le run HPC necessarie per concludere la parte autonoma. Piano e criteri: [PIANO_CHIUSURA_RAMO_GEOMETRICO.md](PIANO_CHIUSURA_RAMO_GEOMETRICO.md). Stato verificato e asset: [STATO_LAVORO.md](STATO_LAVORO.md).

## Consegna autonoma — completata

- [x] Pipeline portabile DA/MoGE → punti → SuperFlex, provenienza, fallimenti e ripresa verificati.
- [x] Audit delle annotazioni originali: documentate semantica, alternative e limiti; nessuna identità globale inventata.
- [x] Valutazione consolidata su risultati disponibili: stabilità/discriminatività, copertura, fallimenti e costi; diagnostica locale separata.
- [x] Export di 299 osservazioni e memoria causale configurabile; 11 test ed esempio eseguibile verificati.
- [x] Codice, figure e istruzioni consegnati; rapporto [CONSEGNA_RAMO_GEOMETRICO.md](CONSEGNA_RAMO_GEOMETRICO.md).

## Pubblicazione richiesta il 12 novembre

- [x] Consegna selezionata pubblicata su `main`: codice, esempi, risultati essenziali e memoria ripulita. Riferimento remoto verificato; esclusa la storia indipendente del main locale.

## Dipendenze della fase comune

- [ ] Collegare le forme alle detection effettive, feature e XYZ di Whareformer; risolvere il mapping VISOR/RGB con il loader reale.
- [ ] Integrare il contributo geometrico e verificare equivalenza alla baseline con contributo zero; calibrare sullo sviluppo e valutare tracking su test separato con associazioni predette.

## Già concluso — riusare

Setup dei modelli, piloti e diagnostici, confronto 200, precalcolo 8797 coppie, prima revisione visiva, validazione numerica del nucleo pubblicato e accesso HPC senza password. Evidenze e limiti in `STATO_LAVORO.md` e resoconti collegati. Job di chiusura conclusi, nessun job attivo nell’ultima verifica; dettagli nello stato.

SAM3, fusione delle nuvole, training da zero ed estensioni robotiche non sono prerequisiti della consegna attuale. DA e MoGE restano entrambi attivi; il test finale non si usa per scegliere il metodo.
