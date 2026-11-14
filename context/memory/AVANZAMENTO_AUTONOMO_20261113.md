# Avanzamento autonomo mentre manca la consegna baseline

13 novembre 2026. Marco autorizza a cercare lavoro/test indipendenti lungo la roadmap e, se necessario, replicare un esperimento baseline minimo senza attendere gli output del collega. Non cambia la domanda scientifica. La verifica della run specifica del collega resta aperta, ma non è un prerequisito per ogni sviluppo.

> Aggiornamento successivo: il lavoro 2B indicato sotto come futuro è ora implementato e provato come candidato. Nessun aggiornamento reale accettato nei primi piloti; report corrente [RISULTATI_REGISTRAZIONE_ACCUMULO_20261113.md](RISULTATI_REGISTRAZIONE_ACCUMULO_20261113.md). La ricognizione e le misure 2A sotto restano storiche.

## Risultato della ricognizione e lavoro eseguito

| Componente | Dipendenza reale | Azione possibile |
|---|---|---|
| Step 2A, memoria→punteggi | Memoria, descrittori e convenzioni del matcher, già locali | Prototipo costruito e verificato in questa fase |
| Step 2B, registrazione/accumulo | Nuvole già disponibili; associazioni diagnostiche dichiarate | Iniziabile senza Whareformer; successivo lavoro prioritario |
| SuperFlex sulla memoria aggiornata | Accumulo accettato, runner e checkpoint SuperFlex esistenti | Fattibile dopo il primo accumulo; nuova inferenza mirata, non riaddestramento |
| Step 3, ciclo con tracker preaddestrato | Checkpoint Whareformer, feature/XYZ e configurazione reali | Ottenibili anche autonomamente; output del collega non indispensabili |
| Step 4–5, beneficio tracking | Ciclo reale e protocollo/split/copertura adeguati | Non sostituibile dai piccoli test tecnici |

Il codice ICP esistente restituisce una distanza dopo normalizzazione indipendente, non un export della trasformazione di registrazione adatto alla fusione. Non basta chiamarlo e concatenare le nuvole: occorre produrre e verificare trasformazione, supporto e convenzione di scala.

## Primo contributo concreto: adattatore indipendente

Creati `integration_prototype/shape_adapter.py`, test e runner. Nessuna modifica al codice degli autori, al componente pubblicato o ai risultati precedenti. L'adattatore candidato riceve logits baseline, ordine esplicito di detection/track e feature geometriche; interroga la memoria preesistente, corregge solo i logits delle track con forma valida e consente commit dopo assegnazione. Colonna zero New Track intatta come logit, probabilità comunque soggetta a rinormalizzazione. Peso zero evita qualsiasi aritmetica di correzione e conserva dtype/valori. Non è ancora l'integrazione nel tracker reale/Torch.

**Verifiche eseguite:** sette test superati. Fra questi, uguaglianza esatta dei logits a peso zero e identica assegnazione su 120 matrici controllate; eseguito il metodo greedy originale estratto tramite AST dalla copia locale senza importare/eseguire l'intera rete. Verificati forme mancanti, track senza memoria, ordine esplicito, creazione di nuovi ID esterni, interrogazione prima del commit, rifiuto di frame non causali, abort e assenza d'influenza della continuazione futura sui punteggi passati. Softmax NumPy del banco di prova: non prova equivalenza alla softmax Torch nell'inferenza reale.

**Replay su geometrie reali:** P03_04, frame 8115, 19311, 20618, cinque osservazioni di coltello/tagliere dalle identità visive già revisionate; quattro rappresentazioni (punti/SuperFlex, DA/MoGE). Letti e verificati con hash 20 artefatti, 12 transazioni di frame, circa 3.72 secondi misurati nel solo runner locale. Nessuna nuova inferenza neurale. Le associazioni sono etichette diagnostiche esterne e i logits sono fixture a zero: non una replica Whareformer, non tracking validato. Peso 1 e distanza neutra 0.2 usati solo per esercitare il percorso attivo, non valori calibrati o scelte metodologiche adottate.

Evidenze: `outputs/independent_adapter_pilot_v1/summary.json` e `transactions.json`. Il risultato non amplia il campione scientifico precedente e non dimostra qualità di registrazione/fusione. P03_04 serve solo come riuso tecnico delle osservazioni esistenti, non sostituisce P01_01 come pilota comune o il test finale.

## Prossimo lavoro immediato consigliato

1. Implementare il contratto dell'accumulatore: punti realmente osservati, riferimento d'oggetto, provenienza per vista e sorgente, capacità limitata, ultima versione valida e possibilità di rifiutare un aggiornamento. Verificare prima le trasformazioni note su porzioni di una nuvola reale, con perturbazioni controllate; questo dà un riferimento geometrico senza inventare identità.
2. Aggiungere un estimatore di registrazione che restituisca R/t e diagnostiche, inizialmente a scala fissa dichiarata; distinguere il test sintetico da viste EPIC reali. Su poche osservazioni visivamente revisionate misurare supporto, residui su campioni distinti e sensibilità alla scala. Le identità passate al diagnostico non sono associazioni predette.
3. Solo su un piccolo accumulo accettato, usare il runner SuperFlex già operativo e salvare la nuova forma; interrogare l'adattatore con la versione precedente e rendere disponibile la nuova versione soltanto dopo il frame. Nessuna nuova inferenza da lanciare prima che serva effettivamente un accumulo valido.

Queste attività sviluppano componenti della roadmap approvata; non equivalgono a chiudere gli step 2A/2B/3 sui dati reali del tracker.

## Replica autonoma minima: percorso disponibile, non primo prerequisito

Il [README ufficiale](https://github.com/JacobChalk/Whareformer#pre-trained-model) continua a collegare checkpoint e feature preestratte; verificato via web in questa fase. Il link SharePoint del checkpoint non è stato scaricabile con lo strumento web: non dimostra indisponibilità generale. Gli asset non sono già presenti nei percorsi controllati in precedenza. Nuovi RGB non sostituiscono quei requisiti.

**Minimo funzionale proposto:** un video di sviluppo, inizialmente P01_01; tre frame che permettano inizializzazione, riassociazione e uso di una memoria aggiornata, almeno due oggetti complessivi per esercitare la competizione/nuova track. Se le osservazioni selezionate non coprono questi eventi si aggiunge solo quanto serve. Non è una numerosità sufficiente a misurare efficacia o generalizzazione; frame campionati/ripartenza a memoria vuota non replicano le metriche della sequenza completa.

Preferire RGB/geometrie già disponibili, insieme alle righe corrispondenti delle feature PCA-256/XYZ ufficiali e al checkpoint originale. Servono anche annotazioni nello stesso ordine, metadati video e configurazione effettiva. Si esegue una nostra run isolata e tracciabile, poi mapping e join dai nostri output; non si presume di riprodurre gli output esatti del collega. Il pretrained matcher non richiede tutto il video per un test software isolato. Il minimo dei frame non elimina però i prerequisiti di asset/ambiente.

Se le feature non sono recuperabili, estrarle da RGB richiede DINOv2, la PCA compatibile e posizioni 3D nello stesso sistema della baseline: costo maggiore. Sostituire la PCA/XYZ con descrittori o coordinate differenti non sarebbe una replica ufficiale. Non è necessario aprire questa strada per avviare adattatore e accumulatore, che hanno già input sufficienti.

## Esito operativo

Il lavoro autonomo riparte da 2A e 2B; attesa dello step 1 limitata alla certificazione della run del collega e agli asset del tracker reale. Nessun nuovo job HPC o controllo coda in questa fase; nessun download di pesi, training, messaggio al collega o push. Primo risultato tecnico effettivo: adattatore candidato e replay, con limiti sopra. Successivo contributo concreto: registrazione/accumulo controllati, non attesa generica degli output.
