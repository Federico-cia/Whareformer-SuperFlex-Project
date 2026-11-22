# Preparazione locale dei dati del verificatore — 22 novembre 2026

## Mandato ed esito

Marco autorizza l'avvio del primo passaggio: costruire dati affidabili per il
verificatore del punto 3. Preparata e verificata la componente con trasformazioni
note sulle nuvole locali. Non completata la certificazione di coppie reali ferme:
il passaggio 1 nel suo insieme rimane parzialmente aperto. Nessun training,
accesso HPC, nuova inferenza, modifica del test indipendente o pubblicazione.

## Dati prodotti

Cartella: `outputs/verifier_data_20261122_v1/`. Input originali preservati in
`strumenti_hpc/audit_risultati/audit_783586_3577_5954/out_783586/`.

- 446 osservazioni di partenza, 438 allineate; usate 414. Escluse otto con
  allineamento invalido e 24 con sole maschere del catalogo.
- 3312 esempi (otto per osservazione), due nuvole da 256 punti ciascuna.
- Ritagli da proiezioni casuali, frazione 45–90%; rumore gaussiano 0 oppure
  deviazione standard 0.01 del raggio RMS per coordinata.
- Errori rigidi residui: (0°, 0), (5°, 0.03), (20°, 0.15), (60°, 0.5), con
  traslazioni in unità del raggio RMS. Sono profili diagnostici dichiarati,
  non parametri calibrati su errori reali o criteri di ammissione.
- Ogni sorgente viene anche spostata con trasformazione rigida nota; salvati
  registrazione vera, stima perturbata, indici dei punti, centro/raggio di
  normalizzazione, seed, osservazione/frame/identità oracle e provenienza.
- Target continuo: distanza NN media simmetrica fra la stessa superficie
  osservata sotto trasformazione vera e perturbata, normalizzata per raggio.
  Calcolato prima di crop e rumore per non etichettare la parzialità come errore
  di posa. Nessun gate storico usato come etichetta; nessun target binario.
- `examples.npz`: 73526612 byte; `samples.jsonl`, `exclusions.json`, `summary.json`
  e `verification.json` completano il pacchetto. Hash input/output e codice
  nel riepilogo. File in sola creazione, nessun output preesistente sovrascritto.

## Separazione e limiti

Partizione diagnostica deterministica per identità benchmark (più conservativa
del solo frame), entro P01_01: 13 gruppi/1432 esempi training, quattro gruppi/1880
validazione (pan, spatula, tofu box, tofu container). Tutte le varianti di una
stessa osservazione/identità sono nello stesso gruppo. Sbilanciamento conservato,
non corretto cambiando split dopo aver visto risultati del modello.

È una fixture di sviluppo, non una scelta del protocollo finale di valutazione.
Scene e frame condivisi possono introdurre dipendenze residue. Non estrapolare
prestazioni a nuovi video, oggetti o coppie reali indipendenti.

Le superfici sono singole nuvole parziali rumorose, non oggetti completi. Crop,
rumore e movimento sono simulati e il loro realismo resta da validare. Le
simmetrie sono quelle rappresentate nel campione osservato; mancano errori di
scala, esempi di identità diversa e target di utilità della fusione. Il movimento
simulato non dimostra recupero della posa dopo spostamento reale. Zero coppie
reali certificate statiche: non sono ancora dati GT per fusione multivista reale.
Questo pacchetto non è l'export della memoria accumulata per il punto 2.

## Verifiche effettive

Tre test passati: target nullo anche con crop/rumore a posa corretta; inversione
del movimento e convenzione della trasformazione; invarianza del target e delle
diagnostiche a unità e origine. Verifica separata di tutti i 3312 esempi: hash,
array finiti, dimensioni, matrici rigide, gruppi disgiunti, 828 target esattamente
nulli; ricalcolo indipendente sulla superficie originale, differenza massima
8.43e-16. Script non collegato al codice del generatore per il ricalcolo.

Codice: `integration_prototype/prepare_verifier_data.py`,
`verify_verifier_data.py`, `test_prepare_verifier_data.py`. Eseguito con Python
Miniconda locale e dipendenze già presenti in `../tmp/point3_test_deps`, senza
installazioni o variazioni dell'ambiente HPC.

## Ripresa

Il campione è utilizzabile per prove della baseline e del contratto del modello.
Prima di dichiarare conclusa la preparazione scientifica: reperire/verificare
evidenze di staticità indipendenti dai gate e costruire una valutazione reale;
validare o ampliare le corruzioni simulate. Architettura principale, training,
calibrazione operativa, replay e collegamento SuperFlex restano da completare.
