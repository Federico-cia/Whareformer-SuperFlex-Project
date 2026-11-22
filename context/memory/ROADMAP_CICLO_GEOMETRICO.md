# Contratto del ciclo Whareformer–SuperFlex

Consolidato il 22 novembre 2026. Sequenza tecnica corrente; esiti in [STATO_LAVORO](STATO_LAVORO.md), fasi in [ROADMAP](ROADMAP.md), attività in [TODO](TODO.md).

## Ordine causale

1. Preparare osservazioni originali, maschere, feature/XYZ e geometria DA allineata con identità/provenienza verificate. FPS-4096 per SuperFlex delle osservazioni.
2. Tutte le detection del frame leggono la stessa memoria precedente; confronto fra forma dell'osservazione e forme delle candidate già disponibili, fallback esplicito sui mancanti.
3. Il matcher produce le associazioni; GT solo per supervisione/valutazione, mai per il metodo in inferenza. Ricostruire la memoria per ciascuna variante, senza imporre le track baseline alla variante modificata.
4. Dopo le assegnazioni, il criterio C sceglie lo stato di posizione; il verificatore decide separatamente l'ammissione della vista nella forma. [Contratto opzione A](MEMORIA_OPZIONE_A_E_SELEZIONE_20261122.md).
5. L'aggiornamento ammesso genera una versione della forma osservata, campionata FPS-4096 e passata a SuperFlex. Pubblicare il completamento solo ai frame successivi; fallimenti/mancanti conservano l'ultimo risultato valido, senza versioni future.

## Controlli necessari

Equivalenza W0/peso zero; modificare/rimuovere il futuro non cambia il passato; snapshot comune al frame; fallback e stato valido sui fallimenti; reset per video; contaminazione/recupero dopo associazione errata. Le verifiche del percorso storico non certificano automaticamente il nuovo percorso.

## Confronti da fissare prima del test

W0; accumulo senza influenza sul matching (associazioni W0 identiche); forme separate; accumulo SuperFlex; controllo punti a input/budget comparabili. Sviluppo per selezione, test indipendente congelato per conclusioni. Qualità della memoria su viste escluse scelte prima, distinguendo consistenza con profondità stimata e accuratezza 3D fisica. Evitare Chamfer simmetrico contro una sola vista parziale come unica misura del completamento.

I confronti sono il piano di validazione, non nuovi esperimenti già eseguiti. Dettagli delle proposte e riletture precedenti nella [roadmap tecnica storica](../evidence/ASSET_ESTERNI.md#asset-fbd7fcfeb777).
