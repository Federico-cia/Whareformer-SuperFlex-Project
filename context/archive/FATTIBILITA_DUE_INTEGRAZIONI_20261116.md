# Due integrazioni della forma: fattibilità e confronto geometrico

## Verifica operativa successiva — 21 novembre 2026

Su mandato di Marco creato il campione supervisionato prima assente: [risultato e disponibilità dei dati](ARRICCHIMENTO_TRAINING_20261121.md). 446 esempi/247 frame P01_01 con oracle originale e geometrie riusate, 429 con forma precedente della candidata corretta; zero Nuova track. Controlli indipendenti e confronto con annotazioni ufficiali passati. Primo collegamento target/geometria verificato, non copertura dell'intero training o prova di efficacia. Ingressi completi degli altri 55 video e RGB mancanti da acquisire/localizzare. Nessun training avviato né nuova politica di memoria scelta.

## Valutazione critica successiva

Su richiesta di Marco, evidenziato un limite comune ai due percorsi: se ricevono la stessa distanza scalare, condividono la perdita d'informazione di quel confronto; il riaddestramento non recupera dettagli già scartati. Verificare complementarità rispetto ad aspetto/posizione, non solo separazione marginale fra categorie: un descrittore discriminativo può essere ridondante, uno debole globalmente può aiutare nei casi ambigui. Proposta di diagnosi su target originali, senza selezionare soltanto casi favorevoli; nessuna nuova analisi quantitativa eseguita. Restano prioritari limiti delle identità del benchmark, mancanti/Nuova track, memorie oracle contro predette e test separato. Ai controlli già proposti aggiungere geometria semplice dagli stessi punti, per distinguere contributo geometrico e contributo specifico SuperFlex. Costo del training completo non misurato. Nessuna modifica alla direzione dei due percorsi, al vincolo di sole etichette esistenti o al protocollo; nessun job avviato.

## Direzione esplicita aggiornata — 16 novembre 2026

Marco vuole tentare sia la fusione geometrica esterna sia il riaddestramento di Whareformer. Prima richiede una valutazione di fattibilità e della distanza fra forma corrente e memoria. Vincolo: nessuna nuova etichettatura manuale; esclusivamente dataset già etichettati, idealmente gli stessi dati di training di Whareformer. Superate la proposta di un campione manuale e la precedente alternativa condizionale fra le due strade. Selezione finale e protocollo ancora aperti; nessun training o nuova campagna avviati in questo passaggio.

## Dati originali: verificato e da verificare

Letti README originale, `src/config/epic/oracle_config.yaml`, `src/tracking/tracker/matcher/matcher_types.py`, `src/utils/manifest_builder.py`, `src/training/data/track_dataset.py`, dataset/configurazione di estrazione EPIC e [paper, appendice C](https://arxiv.org/html/2607.08537).

- README dichiara distribuzione di feature/training LMDB e istruzioni per generarlo con oracle e merge LMDB. Oracle usa le annotazioni esistenti per creare target one-hot: candidata corretta oppure Nuova track. Supervisione riusabile senza nuove etichette. Accesso/download completo non verificato in questo turno.
- Il codice EPIC usa nomi oggetto, ID VISOR per maschera e lista `multiple_instances` per video. Per esempio `plate` è escluso in P22_01. Riusare queste etichette non prova discriminazione fra diverse istanze della stessa categoria; conservare protocollo e limiti. Il vecchio confronto dei due piatti revisionati visivamente non diventa la base del nuovo training.
- I manifest contengono chiavi di feature e target, non una memoria geometrica con provenienza completa. La deduplicazione per hash implica che una chiave non identifichi necessariamente l'osservazione corrente. Il vicino d'aspetto non determina quale forma riusare; PCA/XYZ non contengono la superficie.
- Percorso proposto: rigenerare il replay oracle dalle annotazioni originali, aggiungere ID di osservazioni/candidate e forme solo passate, verificare accordo con feature/target originali sui casi confrontabili. Geometria automatica da RGB/maschere, nessuna nuova etichetta. Coprire tutti i 56 video di training richiede geometrie aggiuntive; un sottoinsieme prefissato resta sviluppo ridotto, non replica dell'intero training.
- Ricerca delimitata nei file locali di `lavoro di gruppo`: nessun `data.mdb`, `_manifest.pkl` o `train_manifest.txt` restituito. Non è una verifica dello spazio HPC o dell'accessibilità della distribuzione ufficiale. Nessun download o controllo remoto eseguito.

## Confronto delle forme

SuperFlex produce insiemi di primitive deformabili: ordine, numero, simmetrie e granularità della scomposizione possono variare. Confrontare vettori di parametri indice per indice è inadeguato; Hungarian fra primitive non risolve da solo il caso una primitiva contro due. Raccomandazione: confrontare superfici campionate, con politica dichiarata.

**Dettaglio verificato:** `SuperFlex-repo/superflex/utils/predictions_handler.py:get_mesh` concatena facce/vertici delle primitive attive; non estrae la superficie esterna dell'unione. `shape_tools/comparison.py` campiona per area su quella mesh, centra e normalizza RMS. Superfici interne/sovrapposte possono quindi influenzare le distanze: non dichiarare indipendenza dalla scomposizione. Valutare filtraggio interno o occupazione unificata se tale sensibilità è rilevante. Nessuna correzione eseguita.

Due candidati per diagnosi automatica con target originali:

| Confronto | Vantaggio | Limite |
|---|---|---|
| D2 + Wasserstein 1D, già implementato | Distribuzione delle distanze interne; confronto senza registrazione, basso costo e precalcolo | Non identifica univocamente la forma; può perdere disposizione locale/manici. Non è probabilità d'identità. |
| Chamfer simmetrica dopo allineamento rigido | Confronta direttamente disposizione delle superfici; candidato più ricco | Registrazione più costosa, minimi locali, dettagli piccoli diluiti nella media e ricostruzioni/completion incoerenti. |

Per Chamfer, su X/Y normalizzati, considerare media delle distanze al vicino più prossimo nelle due direzioni e minimizzazione rispetto alla rotazione; traslazione mediante centratura/registrazione. PCA/multistart+ICP già presente approssima il minimo, non lo garantisce. Non certifica la posa fisica nella scena. Il [paper SuperFlex §4.3](https://arxiv.org/html/2607.01015) confronta superfici campionate con Chamfer per le primitive, non offre già il nostro matcher d'identità.

D2 è verificato nel nostro codice. La fonte originale Osada et al., *Shape Distributions* (2002), è stata identificata; recupero integrale del PDF/pagina autori non riuscito (403), quindi nessuna nuova attestazione di lettura integrale. La centratura/RMS attuale rimuove dimensione assoluta dal confronto, non dagli artefatti conservati per la scena. Eventuale dimensione assoluta richiede scala affidabile; non già certificata. Confronto ricostruzione–ricostruzione resta dipendente dalla completion; osservato–memoria richiederebbe gestione distinta della parzialità. Distanza finale e riduzione della memoria non fissate.

## Percorso A: fusione esterna appresa

Stessi esempi/target originali, Whareformer congelato. Correzione candidata `z* = zW + m(b - w d)`, con `w >= 0`, indicatore di confronto valido m e candidata Nuova track inclusa nella softmax. Apprendere w/b mediante cross-entropy con regolarizzazione. Non si etichetta il peso né lo scenario in cui la forma aiuta: sono sufficienti associazioni corrette. Includere esempi in cui la forma aiuta, danneggia o manca, senza selezionare solo successi. Peso nullo/non stabile è un esito possibile; non forzare effetto. Le unità del coefficiente dipendono da distanza/logits.

Esempio esclusivamente illustrativo: zA=2.1,zB=2.0,dA=0.3,dB=0.1,target B; fra queste candidate valide B supera A per w>0.5. Altri esempi possono richiedere un peso inferiore. La loss trova un compromesso sull'intero insieme, senza annotazioni aggiuntive sul contributo geometrico.

## Percorso B: riaddestramento/adattamento del matcher

Aggiungere distanza e indicatore di disponibilità all'embedding originale a due distanze. Proposta: fine-tuning dal checkpoint, colonne originali copiate e nuove colonne inizializzate a zero per recuperare la baseline iniziale; poi apprendere il matcher con gli stessi target. DINOv2/PCA/SuperFlex congelati. Alternativa da zero distinta e non ancora scelta. Il codice calcola le distanze in no_grad: il confronto geometrico può essere precalcolato, non occorre differenziarlo rispetto alle primitive per addestrare il matcher. Costo non misurato; né impossibilità né tempi garantiti.

## Confronto e prossimo passo proposti

Stessi dati, distanza, disponibilità, memorie e regole causali per A/B. Controllo necessario: Whareformer senza geometria riaddestrato/fine-tuned con stessi dati e budget, per distinguere effetto geometrico ed effetto del nuovo training. Teacher forcing per la prima stima; valutazione con memorie predette e replay completo, non soli esempi fissi.

Separare stima/scelta/valutazione per gruppi coerenti con la generalizzazione desiderata. Checkpoint originale eventualmente già esposto ai gruppi di sviluppo: dichiararlo. Test ufficiale intatto; loader originale carica `test.lmdb` se presente e trainer lo valuta ogni epoca: non usare quel percorso per scegliere parametri/checkpoint sul test.

Ordine proposto: verificare disponibilità/target e replay con provenienza; generare geometrie per sottoinsieme di sviluppo prefissato e misurarne il costo; confrontare distanze su target automatici; usare lo stesso confronto nei due percorsi. Consegna 23 novembre: copertura integrale del training non promessa. Nessuna nuova run, modifica agli algoritmi/filtri o attività del collega in questa analisi.
