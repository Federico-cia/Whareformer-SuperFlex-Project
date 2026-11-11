# Prima inferenza SuperFlex su EPIC — 9 novembre 2026

Job 749180 eseguito direttamente dall'assistente via SSH: COMPLETED/0:0 in 1m07s. Run e log scaricati in `outputs/sf_epic_749180/`. Modelli eseguiti solo sull'HPC; nessun training, modifica della baseline o filtraggio manuale delle nuvole.

Checkpoint robust/config con gli stessi hash della prova lampada, caricamento strict riuscito. Ambiente esistente cv-superflex, torch 2.6.0+cu124, A100 MIG 3g.40gb. Nuvole camera del job 747518 verificate tramite hash. Campionamento 4096 punti, normalizzazione media/scala e denormalizzazione dalle funzioni originali; nessuna rotazione verso una posa canonica. Config/checkpoint, ambiente, parametri e campioni salvati.

| Frame | Punti originali | Indici distinti nel campione | Primitive attive | Forward |
|---|---:|---:|---:|---:|
| 19834 | 1916 | 1635 | 4 | 1.066 s |
| 43735 | 6330 | 4096 | 3 | 0.00880 s |
| 95971 | 19203 | 4096 | 2 | 0.00859 s |

La prima vista usa campionamento con reinserimento: 4096 ingressi non significano 4096 osservazioni distinte. I tempi sono tre singoli forward sincronizzati: il primo può includere inizializzazioni, gli altri non costituiscono un benchmark di throughput. Non includono profondità, allineamento, caricamento, esportazione o trasferimento.

Controlli locali sui risultati: predizioni e mesh finite; campionamento, normalizzazione inversa e punti salvati nel prediction NPZ coerenti; indici mesh e conteggio primitive validi. Originali, campioni, primitive, superfici e report conservati. Avviso TORCH_CUDA_ARCH_LIST non fatale.

## Esito visivo

Figura `outputs/sf_epic_749180/confronto_superflex_epic.png` ispezionata: prime due ricostruzioni squadrate e poco fedeli al bordo circolare osservato; terza più arrotondata ma senza manico ben ricostruito. Modello funzionante tecnicamente, **fedeltà geometrica e utilità per l'identità non dimostrate**. Non chiamare questo esito riconoscimento corretto della padella. I colori indicano primitive, non categorie.

Questo non basta a scartare il metodo o dimostrare instabilità temporale: i tre frame sono diagnostici, non è verificata l'identità fisica comune e cambiano visibilità/posa. Servono controlli mirati prima di aumentare il campione o integrare la memoria.

## Problema da verificare prima dell'estensione

Il loader ASE_Object degli autori trasforma le nuvole parziali nel riferimento ABO tramite T_world_model e conversione degli assi prima della normalizzazione (`superflex/data/dataloader.py`, circa righe 774–795). Il nostro primo test mantiene il riferimento della camera. È una differenza di preparazione verificata; **non dimostra** che l'orientamento sia la causa delle ricostruzioni squadrate. Rumore, occlusione e differenze dei dati possono contribuire. Non usare trasformazioni canoniche basate su identità/posa ground truth come se fossero disponibili nel tracking.

Prossima priorità: diagnosticare l'effetto di orientamento e qualità delle nuvole sugli stessi input, senza cambiare silenziosamente il metodo o selezionare a posteriori solo le viste favorevoli. La semplice produzione di mesh non giustifica ancora una memoria di forma affidabile.

Scala rimasta in unità scena, non metri; equivalenza geometrica con baseline non verificata. Nessun risultato di tracking o miglioramento rivendicato.
