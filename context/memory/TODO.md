# To-do corrente — chiusura del ramo geometrico

Mandato esecutivo approvato l'11 novembre: sviluppare codice ed eseguire le run HPC necessarie per concludere la parte autonoma. Piano e criteri: [PIANO_CHIUSURA_RAMO_GEOMETRICO.md](PIANO_CHIUSURA_RAMO_GEOMETRICO.md). Stato verificato e asset: [STATO_LAVORO.md](STATO_LAVORO.md).

## Consegna autonoma

- [ ] Rendere riutilizzabile e condivisibile la pipeline RGB/maschere→DA o MoGE→nuvole→SuperFlex, con percorsi espliciti, provenienza, fallimenti e ripresa affidabile. Integrare il nucleo già revisionato; non copiare in blocco i runner storici.
- [ ] Verificare semantica e disponibilità delle identità persistenti nelle annotazioni originali; consolidare campione e ambiguità senza usare le distanze per decidere le etichette. Ampliare i dati di sviluppo soltanto dove mancano confronti informativi, prima delle nuove predizioni.
- [ ] Completare il confronto appaiato punti/SuperFlex × DA/MoGE: stabilità, discriminatività entro categoria, copertura, fallimenti e costi. Riutilizzare distanze e inferenze concluse; nuovi job mirati con budget dichiarato.
- [ ] Preparare export per osservazione e componente di confronto/memoria configurabile indipendente dal tracker; testare causalità, forme mancanti e contratto. Capacità/regole/distanza sono candidati da documentare, non scelte definitive già validate.
- [ ] Consegnare codice pulito, esempio eseguibile, risultati essenziali, figure e rapporto sintetico con limiti; allineare memoria condivisa e ricontrollare riservatezza prima del push.

## Dipendenze della fase comune

- [ ] Collegare le forme alle detection effettive, feature e XYZ di Whareformer; risolvere il mapping VISOR/RGB con il loader reale.
- [ ] Integrare il contributo geometrico e verificare equivalenza alla baseline con contributo zero; calibrare sullo sviluppo e valutare tracking su test separato con associazioni predette.

## Già concluso — riusare

Setup dei modelli, piloti e diagnostici, confronto 200, precalcolo 8797 coppie, prima revisione visiva, validazione numerica del nucleo pubblicato e accesso HPC senza password. Evidenze e limiti in `STATO_LAVORO.md` e resoconti collegati. Nessun job attivo osservato l'11 novembre.

SAM3, fusione delle nuvole, training da zero ed estensioni robotiche non sono prerequisiti della consegna attuale. DA e MoGE restano entrambi attivi; il test finale non si usa per scegliere il metodo.
