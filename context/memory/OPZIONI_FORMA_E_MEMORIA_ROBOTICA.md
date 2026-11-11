# Forma per l'associazione e memoria geometrica per la robotica

**Approfondimento successivo:** `RICOGNIZIONE_MEMORIA_GEOMETRICA_ROBOTICA.md` aggiorna la ricognizione qui preliminare. Utilità ipotetica su ingombro/compattezza, novità debole della sola composizione rispetto a Hickory/SQ-SLAM. Proposto confronto qualità–memoria–costo contro punti compressi/OBB/singola superquadrica; scala e posa aperte. Nessun nuovo obiettivo/dataset/esperimento adottato. La nota sotto che limita ConceptGraphs all'abstract descrive la lettura precedente: nell'approfondimento è stato consultato anche il metodo.

9 novembre 2026. Discussione di Marco: possibile ridondanza della geometria stimata dall'RGB, alternative al confronto diretto delle superfici e ruolo di SuperFlex se la memoria viene aggiornata con nuvole di punti. Ulteriore idea: memoria persistente di identità, posizione, orientamento e forma per applicazioni robotiche. Sono ipotesi/proposte; nessuna implementazione o modifica definitiva dell'obiettivo approvata.

## Ridondanza: distinguere osservazione e rappresentazione

Profondità e forma monoculari non sono misure indipendenti dall'RGB; possono condividere gli errori dell'aspetto. Tuttavia Whareformer usa una rappresentazione compressa, non tutto l'RGB: un'altra trasformazione può rendere accessibili caratteristiche che quel descrittore non conserva. SuperFlex introduce anche prior di forma appresi su altri dati. Questo non garantisce informazione utile all'identità. Oggetti geometricamente uguali restano indistinguibili tramite la sola forma.

Il paper Whareformer usa descrittori DINOv2/PCA e una memoria di apparenze raggruppate online con DenStream; l'assegnazione combina distanze di aspetto e posizione. Non sovrappone pixel di immagini passate. La robustezza alle viste deriva dalla rappresentazione e dalla memoria, non da un'invarianza perfetta garantita. Il codice locale prevede anche altre aggregazioni: non assumere senza verifica la configurazione effettivamente eseguita dal collega.

## Opzioni per confrontare forme nuove e memorizzate

| Candidato | Vantaggio | Limite |
|---|---|---|
| Descrittore geometrico invariabile a traslazione/rotazione, per esempio distribuzione di distanze tra punti campionati sulle superfici SuperFlex | Confronto rapido senza registrazione esplicita; primo controllo fattibile | Perde configurazione/dettagli e può confondere forme diverse; invariabilità matematica alla rotazione non rende uguali predizioni SuperFlex discordanti fra viste |
| Registrazione di superfici e distanza robusta alle parti mancanti | Conserva dettaglio geometrico; può fornire una trasformazione utile per una successiva fusione | Più costosa; richiede sovrapposizione e gestione di simmetrie/scale; allineamento e completamento possono fallire. Il confronto punti osservati → modello riduce la penalità per regioni non viste ma può creare abbinamenti ambigui su piccole parti |
| Descrittore appreso per nuvole/superfici, allenato o adattato per riconoscere la stessa istanza da viste diverse | Analogo geometrico del confronto fra descrittori d'aspetto; potenziale tolleranza alle viste | Richiede scegliere e validare un ulteriore modello e dati adeguati; trasferibilità e invarianza non garantite. Più oneroso per il perimetro attuale |

Conservare poche forme di viste passate evita di fonderle prematuramente, ma non risolve da solo il confronto fra riferimenti diversi: serve comunque un descrittore adeguato o una registrazione. Non usare l'ordine delle primitive come corrispondenza. Normalizzazione della scala e conservazione delle dimensioni hanno effetti diversi da valutare. Una vista non affidabile può ricevere contributo neutro e non aggiornare la memoria, con criteri da validare.

## Perché usare SuperFlex se aggiorniamo una nuvola?

La nuvola conserva l'evidenza geometrica stimata dai frame; SuperFlex può costruirne una rappresentazione compatta e regolarizzata e proporre un completamento. Le funzioni sono distinte: punti per aggiornare, superquadriche per rappresentare/confrontare. Una eventuale fusione dei punti richiede comunque allineamento e controllo della contaminazione; ricampionare primitive passate non recupera osservazioni originali.

SuperFlex è giustificato sperimentalmente soltanto se aggiunge qualcosa rispetto agli stessi punti: associazione, stabilità, compattezza o utilità per un compito geometrico. Per l'obiettivo corrente confrontare Whareformer originale, geometria dai punti senza SuperFlex e geometria con SuperFlex, con memoria, normalizzazione, split e budget di confronto dichiarati e quanto più possibile equivalenti. Separare il guadagno della fusione da quello della rappresentazione SuperFlex.

## Ipotesi robotica, distinta dal miglioramento del tracker

Marco propone Whareformer come gestore di identità/esistenza/posizione, arricchito da geometrie SuperFlex e orientamento degli oggetti. Questa direzione può essere utile anche senza un aumento di IDF1: il contributo sarebbe una memoria geometrica della scena da valutare con un compito proprio. Non presentarla però come obiettivo già adottato o beneficio dimostrato.

Schema concettuale per oggetto: identità della track; forma in un riferimento dell'oggetto; posizione e orientamento nel mondo variabili nel tempo; timestamp/provenienza e qualità delle osservazioni. Le pose delle singole primitive non forniscono automaticamente una posa unica e stabile dell'oggetto. L'associazione può usare descrittori che ignorano la rotazione, ma la collocazione robotica deve stimarla e conservarla separatamente. Simmetrie possono rendere alcuni orientamenti non identificabili. Quando l'oggetto non è osservato, la memoria conserva una stima/ultima posizione nota, non la certezza della posizione reale.

Una dimostrazione possibile è recuperare una track fuori vista e visualizzarne ultima posizione nota e forma stimata, senza dichiarare capacità di manipolazione. Per robotica operativa servono anche accuratezza metrica e della posa, aggiornamento con oggetti mobili e valutazione del compito. La geometria da sola non fornisce massa, attrito, dinamica o azioni: non basta a ottenere dati affidabili per addestrare Physical AI. L'integrazione potrebbe diventare una componente percettiva, da validare.

La famiglia delle memorie/mappature 3D a oggetti è già studiata: l'abstract di ConceptGraphs descrive una rappresentazione 3D per percezione e pianificazione. Non è stata verificata qui la novità della specifica combinazione con Whareformer/SuperFlex.

## Raccomandazione e continuità

Primo controllo proposto: campione con identità verificate, memoria piccola senza fusione e confronto di un descrittore geometrico semplice su punti e superfici SuperFlex. Se emergono ambiguità risolvibili mediante dettaglio, valutare registrazione; embedding appreso come opzione più onerosa. Non fissare ancora descrittore, capacità, soglie o regola di fusione. Primo lavoro operativo invariato: corrispondenze/identità. L'idea robotica resta una direzione da discutere con Marco e docente, non una sostituzione automatica del progetto corrente.

Fonti consultate: [Whareformer, §§3.2–3.6](https://arxiv.org/html/2607.08537), [SuperFlex](https://arxiv.org/html/2607.01015), [registrazione ICP](https://www.open3d.org/docs/latest/tutorial/pipelines/icp_registration.html), [ConceptGraphs, abstract](https://arxiv.org/abs/2309.16650). Verificati anche i sorgenti locali di modello, matcher e memoria in `Whareformer-repo/src/`.
