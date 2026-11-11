# Diagnosi di orientamento, profondità e checkpoint

9 novembre 2026. Marco ha autorizzato i controlli 1 e 2 proposti dopo il job 749180. Job 749200 eseguito direttamente dall'assistente: COMPLETED/0:0 in 1m40s, tutti gli 84 casi esportati. Run e log archiviati in `outputs/sf_diagnostics_749200/`. Nessun training, MoGE, raffinamento iterativo, pulizia manuale o cambio della baseline finale.

Piano fissato prima di leggere gli esiti: per tre frame, checkpoint supervised su tutte le 24 rotazioni proprie che permutano/invertono assi, profondità allineata; anche identità con profondità grezza e ripetizione identità/allineata. Checkpoint unsupervised su identità con entrambe le profondità. Totale 84 casi; nessuna selezione della rotazione migliore da usare come metodo.

Le rotazioni mantengono invariata la scala di normalizzazione e vengono invertite sui parametri predetti prima di esportare le superfici. Stessi pixel, stessi 4096 indici campionati per le due profondità e i due checkpoint, seed 42 prima di ogni forward. La profondità grezza è retroproiettata sugli stessi pixel delle nuvole allineate, senza nuova stima neurale.

Metriche diagnostiche in unità normalizzate: distanza media/p95 di pixel osservati non selezionati nel campione verso 30000 punti campionati sulle superfici triangolari predette; distanza simmetrica fra superfici predette e caso identità dopo inversione della rotazione. Sono approssimazioni tramite campionamento, non distanza esatta alla mesh. Pixel esclusi nello stesso frame non sono un nuovo split di valutazione e non misurano generalizzazione. Adesione ai punti osservati non equivale a completamento corretto o migliore associazione d'identità.

Secondo checkpoint scaricato sull'HPC in `~/cv_project/external/superflex_unsup_robust/` dal link ufficiale nel README/script degli autori: folder Google Drive `1bw-HHwQYKC62uUHF9t8QVdx_XVibESQb`; ckpt file `1JsQzV3Xda6xln35iR9RqWsyhrokIOV0r`, config `1A4CGxVSd68QWAFJGMN3ENpLS7XgVEEhl`. Hash e config archiviati nel run; configurazioni dell'architettura dei due modelli identiche. Nessuna modifica al repository SuperFlex fissato o ai pesi supervised.

## Risultati verificati

Predizioni di tutti gli 84 casi finite, primitive coerenti con i report, punti riportati nel riferimento originale e matrici di rotazione proprie/ortonormali. Caricamento di entrambi i checkpoint con confronto completo delle chiavi prima del load. Config e hash nei report; checkpoint unsupervised SHA-256 `4d69c4d326a128ca2912a3791471b79f931e00bfd40699b4f3dd51053a91c5ae`, config SHA-256 `8ac88f0a3fa8cedbaeb8b0c140c90a2a523993bcd1348bcbbaf9622118512255`.

### Sensibilità alla rotazione

| Frame | Variazione mediana superficie vs identità (23 rotazioni non identità) | Ripetizione identica | Intervallo primitive attive |
|---|---:|---:|---:|
| 19834 | 0.0782 | 0.00000443 | 1–7 |
| 43735 | 0.0953 | 0.0000256 | 1–8 |
| 95971 | 0.0742 | 0.0000854 | 1–6 |

Distanze simmetriche approssimate in unità normalizzate. La variazione da rotazione è molto maggiore del rumore osservato ripetendo lo stesso caso. La sensibilità all'orientamento della pipeline è confermata su questi tre input; non dimostra che sia l'unica causa della scarsa fedeltà o che esista una rotazione corretta recuperabile dalle osservazioni.

Ispezionati tutti e tre i contact sheet da 24 rotazioni (`frame_..._24_rotazioni.png`): cambiano decomposizioni e forme anche dopo l'inversione della rotazione. Le prime due viste rimangono spesso squadrate/strutturate in modo poco fedele; la terza è frequentemente arrotondata ma senza manico affidabile. Nessuna rotazione scelta per l'impiego finale. L'orientamento da solo non risolve visivamente il problema.

### Profondità e checkpoint, orientamento originale

| Frame | Supervised allineata | Unsupervised allineata | Supervised grezza | Unsupervised grezza |
|---|---:|---:|---:|---:|
| 19834 | 0.0492 | 0.0516 | 0.0278 | 0.0349 |
| 43735 | 0.0406 | 0.0817 | 0.0293 | 0.0418 |
| 95971 | 0.0486 | 0.1278 | 0.0792 | 0.1085 |

Distanza media approssimata dei pixel esclusi dal campione verso la superficie predetta, in unità normalizzate: più bassa = maggiore adesione a questi punti osservati, non maggiore accuratezza del volume completo.

Il checkpoint unsupervised ha valore medio peggiore in tutti e sei i confronti a parità di input. Nessuna evidenza per sostituire il supervised con questo modello sul pilota. Profondità grezza migliore per questa misura in due frame e peggiore nel terzo con supervised; non è una correzione universale. Le nuvole grezze/allineate differiscono anche dopo normalizzazione (distanza media fra pixel corrispondenti 0.0412/0.0225/0.0295): l'allineamento cambia la forma locale oltre alla scala globale.

Figura `confronto_obliquo.png` ispezionata con punti osservati sovrapposti: nessuna delle quattro combinazioni offre una soluzione visivamente convincente e sistematica. `confronto_frontale.png` è un'ulteriore vista generata; sintesi numerica in `sintesi_diagnostica.json`.

## Conseguenze operative

Mantenere per ora checkpoint e pipeline condivisa esistenti; nessuna sostituzione finale decisa. Prima di ampliare/integrare la memoria serve isolare ulteriormente qualità geometrica e trasferimento del modello a questi oggetti. Una semplice correzione fissa degli assi o il secondo checkpoint non sono soluzioni dimostrate. Possibile prossimo controllo già discusso: MoGE sugli stessi RGB/maschere, solo diagnostico, senza cambiare silenziosamente il protocollo comune. Un riferimento dell'oggetto derivato dai punti va verificato per stabilità sotto occlusione; non usare trasformazioni ABO ground truth indisponibili o scegliere per ogni frame la rotazione più favorevole.

Nessuna inferenza sull'identità comune fra i frame, nessuna misura di tracking e nessuna generalizzazione oltre questo pilota. Nessun job lasciato in corso.
