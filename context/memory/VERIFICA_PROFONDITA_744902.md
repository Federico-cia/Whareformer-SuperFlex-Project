# Verifica profondità — job 744902

8 novembre 2026. Job HPC completato (0:0, 12m20s); risultati recuperati in `outputs/epic_depth_744902/`.

- Tre mappe grezze 456×256: valori finiti e positivi, input e sorgente verificati tramite hash, estremi coerenti con il report.
- Modello Depth Anything V2 Metric Indoor Large, revisione `d2fc6a93601aabb1139a3bf0ebfcb4e89c67817f`; funzioni originali Whareformer. Nessun training.
- Figura `outputs/epic_depth_744902/controllo_profondita.png` ispezionata: stessa scala cromatica per le tre viste, separazione visibile delle superfici e padella più vicina nel terzo frame. Nelle prime due viste la maschera conserva solo parti della padella, per taglio dell'immagine e occlusioni/cibo esclusi dalla maschera. Il nome pan non certifica l'identità fisica comune.
- Questo conferma il funzionamento dell'estrazione, non l'accuratezza geometrica: mancano profondità di riferimento e allineamento alla scena. Nessuna nuvola EPIC o inferenza SuperFlex su EPIC ancora prodotta.

Prossimo passo: verificare scala e procedura di allineamento Whareformer, poi generare sull'HPC le nuvole parziali e controllarle prima di applicare SuperFlex robust. Il valore di scala nel config non sostituisce automaticamente la scala calcolata dall'estrattore.
