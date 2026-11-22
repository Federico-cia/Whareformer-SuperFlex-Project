# Integrazione della forma nel matcher

Consolidamento del 22 novembre 2026. Questo documento conserva le questioni architetturali; [stato](STATO_LAVORO.md), [TODO](TODO.md) e [decisioni D03–D06](REGISTRO_DECISIONI.md) ne sono i riferimenti operativi.

## Direzione approvata

Tentare due percorsi senza nuove etichette manuali: correzione esterna con pochi coefficienti appresi e adattamento/riaddestramento del matcher con geometria. Input/target originali, archivio strettamente passato, stessa distanza/dati/memorie per confronto e controllo senza geometria a pari training. Fine-tuning dal checkpoint è una raccomandazione, non decisione finale.

Federico segue il punto 2; nessun modello concluso attestato nel passaggio disponibile. Marco genera la memoria e i dati del punto 3. Confermato l'uso delle forme SuperFlex, sia per osservazione sia per memoria aggiornata. L'adattatore storico non ha cambiato le assegnazioni nelle 29 configurazioni del 15 novembre: questo risultato non anticipa quello del nuovo matcher.

## Questioni da concordare con Federico

- Formato/tempi/versioni dell'export, forma dell'osservazione e memoria precedente, gestione delle geometrie mancanti e Nuova track.
- Distanza (D2 esistente o Chamfer allineato), scala e parzialità, trattamento delle superfici interne concatenate dalle primitive; nessuna distanza finale selezionata.
- Modalità e forza del segnale nel matching; distinzione memoria dei descrittori e memoria dei punti. DenStream sui descrittori non già concordato; quello appearance originale espone anche centroidi deboli.
- Configurazione iniziale della memoria per i dati, poi griglia sul sistema intero; se cambia molto, un riaddestramento. Nessuna promessa di ottimo prima di copertura e costo misurato.
- Validazione dell'ammissione (pose simmetriche, parzialità, scala e errori), ablation, split e test indipendente prima delle conclusioni.

La collocazione 3D della forma con R, t e scala resta il punto 4: un descrittore invariante o l'XYZ della track non forniscono da soli la posa. [Criticità](REGISTRO_CRITICITA_PIPELINE.md), [fattibilità dei due percorsi](../archive/FATTIBILITA_DUE_INTEGRAZIONI_20261116.md).

Discussioni, alternative, formule e passaggi precedenti restano nella [versione storica integrale](../evidence/ASSET_ESTERNI.md#asset-0700476ef2d2); non sono tutte decisioni approvate.
