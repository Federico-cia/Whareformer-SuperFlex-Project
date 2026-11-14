# Proposta per concludere la pipeline — 14 novembre 2026

## Priorità esplicita: un video dall’inizio alla fine — 14 novembre 2026

Marco chiarisce che il primo obiettivo è chiudere una singola esecuzione integrata su un video completo, prima della selezione delle alternative o dell’ottimizzazione. La proposta precedente non va interpretata come obbligo di completare prima calibrazione, confronti o revisione dei filtri. Il codice esistente esegue il percorso da input preparati a report, verificato sul prefisso; non è ancora verificato l’ingresso completo da immagini per l’intero video.

Direzione approvata: costruire il percorso minimo completo con una configurazione esplicita e provvisoria, riusando modelli/componenti presenti e dichiarando gli input necessari (RGB, maschere, camera/pose e asset scena). Primo candidato operativo: P01_01 già disponibile, come video di sviluppo, non nuovo test indipendente. Preparare gli input per l’intera sequenza prevista dal protocollo, collegare il frontend, eseguire tracking/memoria/ricostruzioni ammesse e produrre output finale. La verifica sul piccolo prefisso serve solo a eliminare errori prima della run completa, non sostituisce il video completo richiesto.

Nessuna ottimizzazione o griglia di metodi come prerequisito. Filtri invariati e loro revisione ancora rinviata. Se tutte le fusioni vengono respinte, dichiararlo: il completamento dell’esecuzione non prova accumulo multivista funzionante o beneficio tracking. Le alternative e il tuning vengono dopo la prima esecuzione integrata. Il percorso non equivale a video arbitrario RGB-only: un segmentatore nuovo resta fuori dal primo traguardo.

Le fasi sotto conservano la proposta precedente. La selezione delle alternative non precede più il primo traguardo operativo.

**Stato: proposta di pianificazione, non nuova approvazione esecutiva.** Formulata rileggendo main remoto verificato al commit 0865949eab4d916bad6626fcdfc786a9032b7d7b, codice corrente, stato, attività, piano frontend e risultati acquisiti. Nessun nuovo esperimento o controllo HPC. Il piano frontend resta già approvato; revisione dei filtri esplicitamente rinviata.

## Perimetro della conclusione

Pipeline completa per il benchmark dichiarato: RGB + maschere + intrinseci/pose/asset scena → feature di aspetto/XYZ e geometria → associazione causale → aggiornamento dei punti osservati ammessi → SuperFlex → memoria per frame futuri → valutazione/report. Questo non implica ingresso da un video arbitrario senza metadati, nuovo segmentatore o funzionamento strettamente online. Il replay con cache rimane ammesso se costi e dipendenze sono dichiarati.

Tre traguardi distinti: collegamento software già presente; esecuzione integrata da input dichiarati ancora da chiudere; efficacia scientifica ancora da misurare. Un risultato negativo non impedisce una consegna scientificamente corretta.

## Sequenza proposta e criteri di uscita

| Fase | Attività concreta | Criterio di uscita |
|---|---|---|
| 1. Asset e configurazione riproducibile | Identificare DINOv2/revisione, provenienza PCA, checkpoint, scala della scena, ambienti; manifest con hash e verifica preventiva | Ogni stadio ha input/modello/ambiente identificati e segnala dipendenze mancanti prima di avviare calcolo |
| 2. Frontend rigenerato e comando unico | Collegare estrattori originali, DA/MoGE/SuperFlex al formato comune; cache esplicita; pilota dieci detection P01_01 2893/5099/7508 con storia 3398 frame preservata | Input effettivamente rigenerati, ordine/maschere/coordinate/PCA verificati, differenze rispetto alla cache misurate con tolleranze motivate; esecuzione fino al report sul pilota dichiarato |
| 3. Copertura temporale sufficiente | Breve segmento con viste ripetute, punti osservati e candidati di associazione reali; preparazione generica senza percorsi macchina o frame fissi | Memoria geometricamente utilizzabile e confronti su osservazioni ripetute; selezione motivata prima del punteggio e distinta dal test finale |
| 4. Verifica del ciclo multivista | Quando Marco riattiva la revisione: diagnosticare simmetrie/parzialità, rivedere criteri solo con evidenza, verificare rifiuti e fusioni controllate | Per i casi validi: registrazione plausibile, provenienza dei punti osservati, crescita entro budget, nuova SuperFlex e forma disponibile solo ai frame futuri; per i casi non validi: memoria preservata. Senza fusioni reali, non dichiarare validata la parte multivista |
| 5. Confronti a peso geometrico attivo | W0 e zero; S-separata vs S-accumulo; controllo P-accumulo; DA/MoGE con budget comparabili; calibrazione sullo sviluppo, configurazione congelata sul test separato | Verifica reale del contributo della forma ai logits senza richiedere artificialmente un cambio di associazione; IDF1/mPCL a scope uguale, copertura, errori, tempi e costi di replay; nessuna selezione sul test |
| 6. Consegna riproducibile | Ambiente nuovo, sorgenti/asset predisposti da fonti dichiarate, istruzioni e configurazione finale, controllo repository, risultati e limiti | Esecuzione dalla configurazione documentata senza percorsi privati impliciti, artefatti completi e hash; documenti correnti coerenti, nessun runner sostituito nell'interfaccia attuale |

Fasi 1–2 completano il frontend già approvato e sono la priorità immediata. Preparazione della copertura e protocollo possono avanzare in parallelo. La fase 4 non è autorizzata da questa proposta: conserva il rinvio esplicito di Marco. Le fasi 5–6 dipendono dai risultati e dalla disponibilità degli asset; l'infrastruttura di report è già presente e va riusata.

## Scelte e limiti

- Non ripetere i nove controlli zero precedenti senza modifiche che lo giustifichino; eseguirli sui nuovi input o dopo interventi che introducono rischi di regressione.
- I sei risultati SuperFlex attuali sono inizializzazioni singole; i dodici rifiuti non provano associazioni errate. Non allentare filtri per ottenere un esempio positivo.
- La copertura attuale di pochi frame non basta per stimare il beneficio dell'accumulo. Un breve prefisso con storia e un segmento geometricamente coperto hanno scopi diversi: diagnosticare frontend e misurare aggiornamenti.
- Reti congelate, nessun training da zero o fit PCA implicito. Aspetto/XYZ baseline e nuvole camera restano distinti. Tutte le query del frame precedono i commit.
- Se gli asset originali non sono identificabili, presentare a Marco la scelta fra consegna con cache verificata e limiti espliciti oppure rigenerazione con configurazione diversa dichiarata e nuova baseline comune. Non spacciare la seconda per replica numerica identica.
- Il protocollo IDF1/mPCL originale è limitato da nomi oggetto e XYZ stimati; eventuale revisione fisica mirata dei casi non sostituisce il protocollo ufficiale né giustifica GT inventata.

## Organizzazione indicativa

Con scadenza 23 novembre: 14–17 asset/frontend; 17–19 copertura e, solo se riattivata, revisione multivista; 20–21 confronti mirati; 22 verifica della riproducibilità e documentazione; 23 consegna. Finestre proposte, subordinate a disponibilità asset/HPC e risultati, non stime garantite. Marco segue frontend/geometria; il collega può preparare in parallelo segmenti/split, baseline e valutazione. Gli incarichi nuovi vanno concordati, non sono già assegnazioni eseguite.

Priorità per comprimere il lavoro: nessun nuovo segmentatore, nessun ridisegno del tracker, nessuna griglia indiscriminata di configurazioni o estensione su molti video prima del pilota informativo. Il test conclusivo deve restare separato dalla selezione dei parametri.