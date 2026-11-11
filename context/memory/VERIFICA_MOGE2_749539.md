# Controllo MoGE-2 + VISOR → SuperFlex

9 novembre 2026. Job GPU **749539 COMPLETED/0:0**, durata 11m48s comprensiva di installazione; job CPU di verifica **749582 COMPLETED/0:0**, 14s. Run e log completi scaricati in `outputs/moge2_visor_749539/`; run remoto `~/cv_project/runs/moge2_visor_749539/`. Nessun job lasciato in corso dall'assistente.

**Esito:** pipeline eseguita e controlli numerici superati; MoGE-2 non risolve visivamente la scarsa fedeltà SuperFlex su questi tre input. Nessun beneficio d'identità o tracking misurato, nessuna sostituzione della geometria finale adottata.

## Confronto fissato prima dei risultati

Tre RGB P01_01 già verificati (19834, 43735, 95971), stesse maschere VISOR della geometria precedente, stesso checkpoint SuperFlex supervised robust, stessa normalizzazione/campionamento seed 42, nessuna rotazione canonica. Nessuna modifica ai descrittori o XYZ Whareformer. È una diagnostica della sorgente geometrica, non una valutazione del tracking.

MoGE-2 ViT-L `Ruicheng/moge-2-vitl`, sorgenti `07444410f1e33f402353b99d6ccd26bd31e469e8`. Checkpoint risolto a revisione esplicita al download, hash e caricamento strict registrati. RGB completo 456×256, `resolution_level=9`, mixed precision FP16, proiezione forzata, FOV stimato dal modello, nessun allineamento alla scena. Coordinate camera X destra/Y basso/Z avanti. Scala metrica predetta da MoGE, senza accuratezza fisica certificata.

La selezione parte dagli esatti pixel VISOR della prova precedente, verificati contro i file punti già controllati; intersezione con validità MoGE, XYZ finiti e Z positivo. Nessuna erosione o pulizia manuale. Salvare la copertura: l'eventuale esclusione di pixel può cambiare superficie e campionamento. Le scale assolute delle due sorgenti non sono direttamente confrontabili; il confronto delle forme va dichiarato in unità normalizzate.

Ambiente MoGE dedicato `cv-moge2`; ambiente SuperFlex esistente riutilizzato. Inferenza solo via SLURM. Script: `scripts/moge2_visor_probe.py`, `scripts/run_moge2_visor.sbatch`; `superflex_epic_probe.py` ora accetta metadati sulle unità, senza cambiare l'inferenza precedente.

## Verifiche completate

- Installazione separata riuscita, `pip check` superato; ambienti MoGE e SuperFlex registrati. PyTorch 2.6.0+cu124, A100 MIG 4g.40gb. Nessun training.
- Checkpoint MoGE revisione `39c4d5e957afe587e04eec59dc2bcc3be5ecd968`, SHA-256 `3eefd4abb2102f38f12b2d1992e5ff15e4923e5431c67dd494afe157e0111cd5`, caricamento strict riuscito. Robust/config coincidono con gli hash precedenti.
- RGB invariati; tutti i pixel VISOR mantenuti in ciascun frame (copertura 100%). Indici dei 4096 campioni identici alla prova precedente, verificati anche sui file scaricati. Per il primo frame, con reinserimento: 1635 punti distinti.
- Array e mesh finiti, numero primitive e normalizzazione inversa coerenti. Hash delle point map, delle nuvole, del manifest e dello script verificati localmente. Resoconti `verifica_locale.json` e `download_verification.json`.
- Figure `confronto_frontale.png` e `confronto_obliqua.png` ispezionate. Ogni sorgente usa la propria normalizzazione degli autori; stessi assi, centro e zoom fra sorgenti nella stessa riga/vista.

## Risultato geometrico

| Frame | Punti comuni | Primitive DA / MoGE | Residuo medio DA / MoGE |
|---|---:|---:|---:|
| 19834 | 1916 | 4 / 4 | 0.0492 / 0.0522 |
| 43735 | 6330 | 3 / 3 | 0.0406 / 0.0536 |
| 95971 | 19203 | 2 / 1 | 0.0486 / 0.1257 |

DA = Depth Anything allineata della prova precedente. Residuo: distanza approssimata dai pixel non selezionati nel campione a 30000 punti della superficie predetta, in unità normalizzate per input. Le sorgenti producono geometrie diverse: questi valori descrivono l'adesione ai rispettivi punti stimati, **non** una graduatoria di accuratezza fisica o del completamento. Non è un nuovo split di validazione.

Osservazione visiva: le prime due ricostruzioni restano squadrate; nella terza MoGE porta a una singola primitiva squadrata rispetto alla forma precedente più arrotondata. Il manico non è recuperato in modo convincente. Le nuvole differiscono anche dopo normalizzazione: variazione media fra pixel corrispondenti 0.1417 / 0.0690 / 0.0327, senza riferimento geometrico ground truth.

MoGE stima anche gli intrinseci e non usa l'allineamento alla scena del percorso precedente. Il controllo riguarda quindi la sorgente geometrica completa, non il solo valore di profondità a proiezione fissa. Non identifica una causa unica degli errori e non dimostra che MoGE sia peggiore in generale.

## Conseguenza per il progetto

Nessuna evidenza per adottare MoGE come correzione già risolutiva o per rivendicare forme affidabili. Non ripetere setup e prove già completati. Il prossimo passo della roadmap resta un campione con identità fisiche verificate e corrispondenze coerenti, per misurare stabilità e discriminatività del segnale prima di attribuirgli utilità nel tracking; baseline e interfaccia possono essere preparate dal collega in parallelo. Il completamento di questa diagnostica non fissa distanza, memoria o fusione.
