# Nuvole DA allineate alla scena a piena risoluzione — P01_01, v2 (22 novembre 2026)

- 8106 osservazioni allineate (24 identità, 2427 frame), 86 773 738 punti, coordinate scena EPIC-Fields in float32 (unità non certificate come metri). Tutti i 15 blocchi della run `p01_full_enrichment_20261121_v1`.
- Alpha/beta/c2w: audit 783586 per il campione (438); job 786174 per i blocchi 0004–0014 (5635); job 786275 per i blocchi 0000–0003 (2034), con mappe DA recuperate da Drive e verificate per MD5. Stessa procedura (`alpha_beta_p01.py`) in tutti i job. Valori per frame in `alpha_beta/`.
- Escluse 19: 8 con allineamento dell'audit non valido, 11 in frame con allineamento non valido. Fallita 1 (profondità allineata non positiva), registrata in `per_observation.jsonl`.
- Sorgente delle nuvole grezze: `shared_exports/p01_01_correction_received/geometry_received.tar.gz`, hash di ogni nuvola verificato contro `geometry_index.json`.
- Codice: `strumenti_hpc/superflex_allineato/build_aligned_fullres_v2.py`, copia di `integration_prototype/build_aligned_fullres.py` con due sole differenze: etichetta di provenienza dei blocchi 0000–0003 e `.npz` non compresso (tempi di esecuzione); il contenuto numerico non cambia.
- Verifica: le 6073 nuvole della v1 sono tutte presenti; identiche bit per bit su 300 campionate a caso.
