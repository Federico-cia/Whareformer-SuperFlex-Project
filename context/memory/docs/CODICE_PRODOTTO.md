# Che cosa abbiamo prodotto in codice

Inventario del 10 novembre 2026. È il codice di esperimenti e verifiche del ramo geometrico, non ancora un nuovo tracker completo. All'avvio della ricognizione erano presenti 44 script: 25 Python, 17 SLURM e due PowerShell. Il catalogo in `manifests/code_inventory.json` elenca i file correnti con funzione, stato e hash.

## Il lavoro originale del progetto

Abbiamo scritto programmi che collegano componenti preaddestrati e rendono gli esperimenti controllabili:

| Componente | Input → output | File principali | Che cosa è stato verificato |
|---|---|---|---|
| Selezione/acquisizione EPIC | RGB, VISOR, pose e mapping → campione fissato e manifest | `acquire_compare200.py`, `select_epic_diagnostic.py`, `validate_compare200.py` | Campione 200 e collegamento VISOR/RGB delle osservazioni |
| Costruzione della geometria | RGB/camera/maschera → profondità e punti per oggetto | `expanded_geometry.py`, `epic_depth_probe.py`, `epic_geometry_probe.py`, `moge2_visor_probe.py` | Rami DA grezzo/allineato e MoGE eseguiti; non accuratezza 3D certificata |
| Esecuzione SuperFlex | Punti parziali → primitive, mesh e rapporti | `superflex_batch_probe.py`, `superflex_epic_probe.py` | Robust preaddestrato, campionamento/provenienza; ripresa e fallimenti per osservazione |
| Confronto delle ricostruzioni | Mesh/punti/maschere → controlli, sagome 2D e tavole | `review_expanded_geometry.py`, `summarize_compare200.py`, `paired_compare200.py` | Confronto appaiato 200 completato; hash e figure controllati |
| Segnale di identità | Punti/mesh già disponibili → distanze e analisi su identità visive | `shape_identity_experiment.py`, `evaluate_shape_identity.py`, `verify_shape_identity_results.ps1` | 8797 coppie calcolate, controllo descrittivo su 37 osservazioni; campione ancora limitato |
| Gestione HPC | Script e percorsi → job riproducibili e log | File `.sbatch` associati | Esecuzioni registrate nei resoconti; gli ambienti esistono sull'account usato |

I nomi della tabella sono relativi a `scripts/`. La mappa completa, compresi i diagnostici storici, è in `scripts/README.md`.

## Il codice degli autori, distinto dal nostro

Non abbiamo scritto le reti DA, MoGE, SuperFlex o Whareformer e non le abbiamo addestrate da zero. Le copie locali `Whareformer-repo/`, `SuperFlex-repo/` ed `external/` sono dipendenze escluse da Git; versioni e provenienza restano nei manifest. Gli script richiamano queste implementazioni o funzioni originali con hash controllati. Conservare attribuzioni e licenze quando si ricostruiscono i pacchetti.

## Che cosa NON è ancora implementato

- Collegamento certificato tra `annotation_index` dei nostri manifest e `detection_idx`, feature e XYZ effettivi della baseline.
- Integrazione della forma nel matcher Whareformer e prova di equivalenza con contributo geometrico zero.
- Memoria di forme per track, aggiornata causalmente dalle associazioni predette.
- Valutazione di tracking DA/MoGE/SuperFlex contro baseline e geometria semplice.

`prepare_baseline.py` controlla input e prepara una configurazione: **non esegue da solo la baseline**. Lo stato del lavoro del collega non è ancora verificato.

## Come leggere il progetto senza perdersi

1. `README.md`: obiettivo, stato e accessi ai documenti.
2. Questo file: cosa è stato sviluppato e cosa manca.
3. `RISULTATI_CONFRONTO_200.md`: confronto delle sagome/ricostruzioni.
4. `RISULTATI_IDENTITA_DA_MOGE.md`: domanda, procedimento, distanze e AUC del test più recente.
5. `docs/CONDIVISIONE.md`: file del repository e pacchetti dati separati.

Gli script sono strumenti di ricerca costruiti per gli esperimenti documentati, non un pacchetto installabile universale. Alcuni richiedono directory/cache di precedenti run e gli ambienti HPC già predisposti. Non eseguire tutti i file in sequenza: partire dal resoconto dell'esperimento e riusare i risultati conclusi.
