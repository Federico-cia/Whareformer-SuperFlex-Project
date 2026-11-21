# Anteprima completa — Rami paralleli

**Stato successivo:** questa anteprima è stata approvata e applicata alla mappa corrente, insieme ai testi confermati. Rimane una copia della proposta per documentarne la provenienza; la sorgente attuale è [contenuti correnti](../../../mappa_interattiva/contenuti.json). Ricevuta: `APPLICAZIONE_MAPPA.json`. Le formulazioni di attesa nei paragrafi seguenti descrivono lo stato alla preparazione dell'anteprima.

Marco sceglie «Rami paralleli» e richiede di vedere l'intera mappa prima dell'applicazione. Questa è una bozza grafica separata, non la mappa corrente e non un'approvazione dei commenti.

## File per la revisione

- `mappa-completa-rami-paralleli.png`: immagine complessiva, 2750 × 6967 pixel.
- `mappa-completa-rami-paralleli.svg`: versione vettoriale ingrandibile.
- I tre ritagli della revisione sono conservati soltanto nell’archivio locale; qui sono disponibili immagine completa e versione vettoriale.
- `mappa-completa-rami-paralleli.json`: sola specifica della bozza, con provenienza dai nodi precedenti; non importare nella mappa corrente.

## Scelte grafiche proposte

- Tre rami iniziali: aspetto e posizione originali Whareformer, forma ottenuta da stima geometrica, punti isolati, SuperFlex e descrittore del progetto.
- Risorse fornite e modelli esterni in grigio; le maschere VISOR non sono presentate come prodotte dal frame. Gli ingressi sono raggruppati come dati condivisi; ogni processo dichiara gli elementi pertinenti.
- Whareformer in blu, SuperFlex in arancione e aggiunte del progetto in viola. Distinte memoria originale e memoria geometrica prima del frame; memoria finale con attribuzione mista.
- Rettangoli per elaborazioni/stati e rombi per decisioni. Separati rete originale, correzione esterna e assegnazione originale.
- Creazione/inizializzazione baseline o aggiornamento baseline precedono l'uso dell'ID effettivo da parte del coordinatore geometrico, coerentemente con il codice corrente. Lo stato baseline prosegue direttamente alla memoria finale anche se la geometria è assente/rifiutata.
- Controlli distinti per disponibilità della nuvola, esistenza della memoria di punti, ammissione della fusione ed esito SuperFlex. La prima nuvola valida può inizializzare una traccia già esistente. Si conserva la differenza fra rifiuto della geometria e fallimento della ricostruzione dopo l'ammissione dei punti.
- Punti dell'osservazione trasferiti su una linea laterale dedicata. La superficie completata non entra nell'accumulo dei punti osservati.
- Ritorni temporali sui margini, per le due memorie. Le intersezioni senza punto restano incroci, evidenziati con un'interruzione visiva; i punti indicano confluenze.

## Corrispondenza con i blocchi precedenti

| Blocchi precedenti | Rappresentazione nella bozza |
|---|---|
| B01/B02/B09 | Ingressi forniti raggruppati |
| B03 | Ritaglio, estrazione, riduzione e descrittore d'aspetto |
| B04–B07 | Geometria esterna, punti osservati, SuperFlex, descrittore |
| B08/B10 | Profondità, allineamento alla scena, calcolo ed esito XYZ |
| B11 | Osservazione corrente con forma opzionale |
| B12 | Punteggi originali, distanza di forma, correzione esterna, assegnazione |
| B13 | Memorie precedenti baseline e geometrica separate |
| B14/B17/B15 | Diramazione nuova/esistente e aggiornamenti baseline |
| B18 | Inizializzazione baseline distinta dall'inizializzazione geometrica, anche tardiva |
| B16 | Disponibilità, registrazione, ammissione, accumulo, ricostruzione |
| B19 | Conservazione/aggiornamento degli stati e memoria futura |

## Limiti e verifica

Le etichette degli step della bozza non sostituiscono le schede manuali. I testi completi precedentemente proposti restano da confermare; le nuove eventuali schede richiederanno redistribuzione e revisione dopo l'approvazione della struttura. La rappresentazione mostra il metodo con accumulo, senza includere riaddestramento o altre alternative come processi già eseguiti.

Segnalato nell'immagine che aspetto e posizione sono stati riusati nelle prove e la geometria è disponibile soltanto sul campione; i controlli di ammissione sono provvisori. L'inizializzazione senza ricostruzione riuscita e gli stati privi di geometria non sono una fusione riuscita.

Riletti adattatore, coordinatore e aggiornamento dei punti; generate e ispezionate l'immagine e le tre sezioni, corretti testi che uscivano dai riquadri e separati i percorsi di conservazione. Controllata la copertura dei 19 nodi precedenti nella specifica. Nessun test scientifico, inferenza, job, commit o pubblicazione nuovi. File applicativi e contenuti della mappa corrente invariati, verificati mediante hash.
