# Memoria 3D accumulata: risultato del lavoro del 22 novembre 2026

> **Lettura dopo il consolidamento del 22 novembre 2026:** questo documento conserva specifiche ed evidenze delle fasi descritte. Per stato operativo, attività e scelte successive consultare [stato corrente](../memory/STATO_LAVORO.md), [TODO](../memory/TODO.md) e [decisioni](../memory/REGISTRO_DECISIONI.md); il contratto attuale della memoria è [opzione A](../memory/MEMORIA_OPZIONE_A_E_SELEZIONE_20261122.md). Le note di attesa o di lavoro non ancora eseguito qui sotto sono datate, non un nuovo stato corrente.

## Perimetro chiarito successivamente — 22 novembre 2026

Questo documento riguarda il prototipo semplificato a singola forma. Marco richiede ora di predisporre il sistema multi-ipotesi discusso originariamente. Il funzionamento e gli export qui descritti non ne certificano l’implementazione. [Confronto e requisiti mancanti](CONFRONTO_MEMORIA_ORIGINARIA_20261122.md). Nessuna modifica algoritmica in questa revisione.

**Il prototipo locale è utilizzabile per prime prove di training del punto 2 sulle nuvole accumulate. La variante con nuovi completamenti SuperFlex deve ancora essere eseguita e verificata sull’HPC.** Non è ancora dimostrato un miglioramento del tracking.

## Che cosa fa il sistema

Il tracker deve riconoscere un oggetto quando lo vede di nuovo. La memoria geometrica raccoglie le sue osservazioni precedenti per offrire una descrizione più completa della forma.

Ho completato un percorso che allinea ogni nuova nuvola di punti alla forma già disponibile, ne stima l’affidabilità con un modello addestrato e aggiunge i punti soltanto quando la verifica passa. Questo percorso funziona anche senza presumere che l’oggetto sia rimasto fermo. Occorrono almeno due osservazioni accettate per confermare una forma; rifiuti e fallimenti conservano la memoria precedente.

Per il training, ciascun esempio riceve esclusivamente le memorie costruite prima del suo frame. L’osservazione corrente non entra nella memoria con cui viene confrontata. Posizione del tracker, punti osservati e superfici eventualmente completate da SuperFlex restano distinti.

## Che cosa ho realizzato e verificato

- **Dati:** 3312 esempi da 414 nuvole locali, con ritagli, rumore e trasformazioni note. Gli errori geometrici sono ricalcolabili; le decisioni dei vecchi filtri non diventano etichette.
- **Modello:** addestrata la baseline leggera autorizzata, che predice l’errore da otto misure geometriche. Identità separate per addestramento, calibrazione e valutazione descrittiva. Non è il futuro modello neurale direttamente sulla coppia di punti.
- **Memoria:** collegati registrazione reale, verifica appresa, accumulo pesato e gestione dei rifiuti. La prima vista non mantiene un privilegio permanente.
- **Export per il compagno:** preservati input numerici, etichette e ordine delle candidate originali; aggiunti descrittori delle nuvole accumulate, disponibilità della geometria, provenienza e versioni. Incluso un lettore Python per accedere agli esempi.
- **SuperFlex:** preparati input di 4096 punti distribuiti con FPS, normalizzazione e trasformazione inversa. Il nuovo worker usa questi input senza il ricampionamento casuale del precedente. Collegamento verificato con prove controllate, comprese ricostruzioni fallite.
- **Controlli:** 131 test, 129 superati e due saltati per una dipendenza assente. Verificati separatamente tutti gli esempi esportati: etichette preservate, input numerici identici agli originali e nessun riferimento alla memoria corrente o futura rilevato.

## Perché raccomando la politica prudente

Ho confrontato due punti operativi dello stesso modello. La versione prudente sceglie la soglia sui dati di calibrazione cercando meno ammissioni errate, a costo di rinunciare a più viste. Il budget empirico del 5% sulla calibrazione non è una garanzia sui dati nuovi.

| Risultato | Politica iniziale | Politica prudente |
|---|---:|---:|
| Versioni accumulate nel replay reale | 263 | 33 |
| Tracce con forma confermata | 14 | 6 |
| Esempi con memoria precedente della candidata corretta | 353/446 | 267/446 |
| Fusioni ammesse nella prova con movimento simulato | 16/17 | 8/17 |
| Di queste, oltre la tolleranza geometrica | 7 | 0 |

La prova di movimento usa superfici osservate, ritagli e spostamenti noti: verifica il percorso, non il movimento reale nel video. Il risultato prudente è incoraggiante ma limitato a 17 casi. Nella diversa valutazione sulle perturbazioni sintetiche, la politica prudente ammette ancora 30 dei 194 casi oltre tolleranza, contro 62 della versione iniziale. **La memoria resta sperimentale.**

Procedo con la prudente come raccomandazione operativa, coerentemente con il successivo «vai» di Marco; questo non equivale ad approvazione scientifica definitiva. Entrambi gli export sono conservati e riproducibili.

## Che cosa si può usare ora e che cosa manca

Il compagno può iniziare prove del punto 2 con i **descrittori delle nuvole osservate accumulate**, usando `outputs/point3_training_conservative_proposal_20261122_v1/`. Sono disponibili 446 esempi originali e 414 query geometriche; le geometrie mancanti sono esplicite. Il campione non contiene esempi della classe «Nuova track», quindi non costituisce tutto il training necessario al matcher.

Per la variante con **forme completate da SuperFlex** manca l’esecuzione GPU effettiva. Ho preparato una prova di soli quattro input, due memorie e due viste singole, con controllo della quota e recupero dei risultati. Non ho inviato il job e non esiste un identificativo osservato per questa prova. La regola di accesso del progetto riserva l’avvio HPC a Marco.

Si avvia con `strumenti_hpc/esegui_point3_fps_smoke.bat`; i risultati si recuperano con `scarica_point3_fps_smoke.bat`. Dopo la prova riuscita, il worker può elaborare gli input completi e collegare i completamenti agli esempi, mantenendo la causalità. La prova ridotta verifica il contratto FPS e usa due memorie della versione iniziale: non è l’elaborazione completa della variante prudente.

**Stato conclusivo:** dati, training della baseline, memoria, replay ed export locale sono realizzati e verificati. Rimangono la verifica GPU reale, l’elaborazione dei completamenti necessari e la valutazione del beneficio nel tracking. Non dichiaro quindi conclusa l’intera pipeline SuperFlex del punto 3.

Guida tecnica e comandi: [POINT3_PROTOTYPE.md](../../integration_prototype/POINT3_PROTOTYPE.md). Il dataset P01_01 rimane sviluppo; il test indipendente resta una decisione separata.
