# Consegna del ramo geometrico autonomo

Sessione avviata l'11 novembre, consegna consolidata il 12 novembre 2026. La parte autonoma è eseguibile: pipeline RGB/maschere → DA o MoGE → punti → SuperFlex, export per osservazione, confronto e memoria causale. Il beneficio per Whareformer resta da misurare con la baseline reale.

## Codice e utilizzo

Worktree `shared_exports/publish_candidate/`, ramo `prepare/superflex-core`. Guida operativa `SuperFlex/PIPELINE.md`; esempio CPU `SuperFlex/examples/memory_demo.py`; manifest/configurazione e launcher SLURM in `SuperFlex/examples/`. Moduli nuovi: `pipeline.py`, `memory.py`, `report.py`. Reti e pesi degli autori restano esterni; ambienti HPC riusati senza reinstallazione.

La pipeline accetta percorsi espliciti, intrinseci alla risoluzione RGB e maschere binarie. Può elaborare una sola sorgente o entrambe, con pixel comuni per il confronto. Non dipende da mesh di scena o vecchi run. Ripresa controllata tramite hash di input, configurazione, codice e artefatti; sorgenti Python dei backend e versioni Torch/CUDA registrati. Fallimenti conservati, nessuna variazione automatica di soglia. Un job completato non implica che tutte le forme siano disponibili.

L'export conserva chiave/video/frame, provenienza RGB/maschera, sorgente, assi, unità, geometria e stato. `detection_idx=null`: non è una detection Whareformer certificata. I parametri della forma sono separati da input e matrici diagnostiche; restano anche mesh e normalizzazione. L'export storico di 299 osservazioni è in `outputs/geometric_closure_v1/observations.json`, con percorsi relativi a `outputs/compare200_749968/`. Nel manifest storico `da_raw_*` corrisponde al ramo non allineato chiamato `da_*` dalla nuova pipeline.

La memoria è un candidato FIFO configurabile: capacità positiva intera, D2 o spettro, minimo o media fra forme conservate. `score` precede `commit`, che riceve associazioni esterne uno-a-uno; nessuna identità annotata entra nel modulo. Una forma mancante conserva le precedenti e produce un contributo indisponibile, indicato da maschera esplicita. Capacità, distanza e riduzione non sono state selezionate come metodo definitivo. Non sono implementati fusione delle nuvole o aggiornamento dei logits Whareformer.

## Identità: verifica delle annotazioni originali

Letti integralmente i cinque archivi densi originali già disponibili: **183312 record di frame e 632169 maschere**, tutti gli ID di maschera unici entro video. I campi osservati sono `id`, `name`, `class_id`, `type`, `segments`; il contesto immagine specifica video e intervallo di interpolazione, non un ID fisico globale. Le 200 annotazioni selezionate corrispondono esattamente a record originali. Due frame selezionati hanno anche un record alternativo in un'interpolazione adiacente (P08_09 e P22_01): conservata la scelta originale, non reinterpretata dopo aver visto le distanze. Evidenza completa in `runs/visor_original_audit.json` nella cartella di consegna locale.

La [documentazione ufficiale VISOR](https://github.com/epic-kitchens/VISOR-VIS/blob/main/README.md) distingue ID della maschera, categoria, sottosequenza e intervallo interpolato. Il [convertitore ufficiale VOS](https://github.com/epic-kitchens/VISOR-VOS/blob/main/visor_to_davis.py) costruisce etichette usando il nome dell'entità entro sottosequenza. Questo sostiene una consistenza temporale locale, non certifica che due oggetti con lo stesso nome in intervalli lontani siano la stessa istanza fisica. Non abbiamo dimostrato l'assenza di identità in ogni altra risorsa EPIC/VISOR; abbiamo verificato il contenuto dei cinque archivi effettivamente usati.

Le **37 osservazioni/sette identità visive restano invariate** e non sono promosse a ground truth persistente. L'audit non giustifica nuove etichette globali o negativi fra intervalli. Per questo non sono state aggiunte inferenze scientifiche su nuovi frame: aumentare osservazioni senza identità affidabili non risolve la lacuna.

Diagnostica aggiuntiva separata: tutte le **nove coppie** esistenti con stesso video, intervallo e nome esatto, in frame distinti (18 osservazioni, sei intervalli, due video). Selezione salvata dai soli metadati prima della lettura delle distanze, in `local_intervals.selection.json`; script riproducibile `examples/local_interval_diagnostic.py`. Non sono nuove identità persistenti né negativi certificati. Mediane D2 punti DA/SuperFlex DA/punti MoGE/SuperFlex MoGE: **0.0277 / 0.0305 / 0.0316 / 0.0257**. Con ICP le mediane sono **0.0818 / 0.1403 / 0.0733 / 0.1367**: non emerge una stabilizzazione sistematica di SuperFlex. Le scale dipendono dalla rappresentazione; senza negativi questa diagnostica non misura discriminatività.

## Evidenza consolidata sul segnale

Riutilizzate integralmente le 8797 coppie già calcolate, senza nuove inferenze del confronto 200. Il riepilogo `summary.json`/`separation.json` mostra stabilità per video/categoria e discriminatività sullo stesso insieme di coppie disponibili. Le etichette restano separate dalle geometrie.

| Rappresentazione | Osservazioni disponibili | AUC D2 entro categoria | Mediana D2 stessa/diversa identità |
|---|---:|---:|---:|
| Punti DA | 299/299 | 0.612 | 0.0693 / 0.0936 |
| SuperFlex DA | 299/299 | 0.627 | 0.0400 / 0.0607 |
| Punti MoGE | 299/299 | 0.701 | 0.0989 / 0.1226 |
| SuperFlex MoGE | 298/299 | 0.768 | 0.0602 / 0.1117 |

AUC e mediane della tabella riguardano **solo i due piatti P22_01**, 11 osservazioni, 25 coppie positive e 30 negative. Il confronto completo sulle identità revisionate ha 149 coppie comuni su 158 etichettate. Le coppie condividono osservazioni: non sono repliche indipendenti. Il fallimento SuperFlex MoGE sul tagliere P08_09 rimane esplicito; non gli viene attribuita una distanza favorevole.

Con lo spettro, i punti rimangono competitivi (AUC 0.744 DA e 0.763 MoGE); con ICP le superfici raggiungono 0.717/0.728. Nessuna distanza è stata scelta a posteriori come vincitrice. Il confronto storico di sagoma favorisce modestamente DA (IoU appaiata 0.4697 contro 0.4481), ma misura compatibilità 2D, non correttezza 3D. Questi risultati motivano il mantenimento di entrambe le sorgenti e del controllo sui punti, non un beneficio tracking.

Figure: `identity_signal.png` (discriminatività e mediane), `confronto_appaiato.png` (sagoma storica). L'esito dipende dal campione e dalla distanza; non vi sono intervalli di confidenza basati su una falsa indipendenza delle coppie.

## Costi e ingombro

Dal run storico: DA **318 s** e MoGE **217 s** per 200 immagini, includendo avvio/caricamento dei cinque blocchi; non è un benchmark universale di throughput. SuperFlex aggiunge forward mediani di **8.45 ms** da DA e **8.25 ms** da MoGE sui successi, esclusi caricamento ed export. Totale storico GPU **26m48s**; il CSV delle fasi omette la parte del tentativo fallito, quindi non sostituisce SLURM.

I soli array dei sette gruppi di parametri SuperFlex occupano **2432 byte**, mantenendo tutti i 16 slot; il vecchio archivio completo include anche nuvola e assegnazioni e occupa molto di più. Nuvole complete: mediane XYZ non compresse 120576 byte DA e 60288 byte MoGE, con precisioni diverse (float64/float32); non è un confronto a pari budget. I descrittori D2 attuali conservano 16384 float64, ossia **131072 byte per forma**; lo spettro ne usa 24. Una forma parametrica compatta non rende automaticamente compatta questa implementazione della memoria D2. Compressione, capacità e qualità a parità di byte restano valutazioni distinte, non risultati acquisiti. Dettagli in `costs.json`.

## Verifiche della consegna

| Job | Esito | Durata | Scopo |
|---|---|---:|---|
| 755696 GPU | COMPLETED / 0:0 | 5m37s | Primo percorso portabile su tre casi |
| 755697 CPU | FAILED / 1:0 | 1m46s | Audit interrotto dall'assunzione errata di un solo record per frame |
| 755699 CPU | COMPLETED / 0:0 | 2m14s | Audit corretto, cinque archivi completi |
| 755709 GPU | COMPLETED / 0:0 | 5m36s | Versione finale, export compatto, ripresa e test |

Tre casi prefissati: prima osservazione P01_01, prima P22_01 e fallimento noto P08_09. Sei nuvole valide, cinque superfici valide e fallimento MoGE riprodotto senza cambiare soglia. **11 test** superati localmente e nel job finale; controllo statico senza errori. Esempio CPU eseguito. Verificati hash dei file, pixel comuni, estrazione esatta dalla nuova predizione, campionamento/normalizzazione e parametri compatti. I tre file che firmano la pipeline locale coincidono con quelli del job finale. Successivamente soltanto la validazione del tipo della capacità nella memoria è stata rafforzata e ricontrollata localmente.

**Limite numerico osservato:** il confronto iniziale con le nuvole storiche non supera `allclose(rtol=1e-5, atol=1e-6)`. Non è stata allargata una tolleranza per dichiararlo superato. Differenza relativa L2 massima delle nuove nuvole: **0.0006212**; D2 fra superfici nuove e storiche fino a **0.00513**. I parametri possono variare più delle superfici. Hardware osservato A100 MIG 4g.40gb contro 3g.40gb storico; non è stata isolata la causa delle differenze. Funzionamento, estrazione e contratto sono verificati; equivalenza numerica esatta e determinismo fra esecuzioni no. Le nuove predizioni non sostituiscono le distanze storiche nel rapporto scientifico.

Output remoti `~/cv_project/runs/portable_validation_755709/`; log `~/cv_project/portable_755709.out/.err`, e analoghi per gli altri job. Copie locali sotto `outputs/geometric_closure_v1/`. Archivio finale SHA-256 `fc889a1b9671503f011a18e6e70430d79280b84adab2862a6561ae06a571615d`, verificato dopo il trasferimento. Nessun job attivo nell'ultima lettura della coda.

## Cosa resta alla fase comune

Collegare chiavi VISOR/RGB a detection, feature e XYZ reali; integrare il contributo nel matcher; verificare equivalenza a peso zero; calibrare sullo sviluppo e valutare tracking con associazioni predette e test separato. Nessuna di queste prove è dichiarata conclusa. La consegna autonoma è utilizzabile senza attendere tali asset, ma non chiude la domanda scientifica finale.
