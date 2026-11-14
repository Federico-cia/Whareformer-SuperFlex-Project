# Step 2B — registrazione e memoria dei punti: primo pilota

13 novembre 2026. Esecuzione autorizzata da Marco con «Procediamo», dopo il piano di avanzamento indipendente. Riutilizzati dati e identità visive già disponibili; nessuna nuova identità certificata e nessuna nuova inferenza neurale. Conclusione: implementazione candidata e controlli tecnici disponibili, **nessun aggiornamento fra viste reali accettato nel pilota**. Non ancora accumulo multivista validato.

## Componenti sviluppati

In `integration_prototype/cloud_memory.py`:

- registrazione rigida multistart, PCA e 24 rotazioni proprie, ICP con trimming e affinamento su punti più densi; restituisce rotazione/traslazione, residui, supporto, rapporto dei raggi e alternative ambigue;
- selezione della posa sui soli campioni di fitting; punti query di validazione separati, confrontati con riferimenti di fitting più densi. Non sono osservazioni indipendenti né validazione della verità 3D;
- memoria di soli punti osservati per video/track/sorgente, prima vista come riferimento, quota per vista e FIFO delle viste successive, copia degli array restituiti, provenienza e trasformazioni esportate;
- rifiuto di aggiornamenti senza modificare i punti o la versione geometrica valida, ordine temporale e chiavi uniche. Un aggiornamento rifiutato resta processato e non è reinseribile con la stessa chiave;
- nessuna stima di scala, fusione di parametri SuperFlex, uso del completamento come nuova misura o inferenza dell'identità. La memoria riceve associazioni esterne; qui sono diagnostiche visive, non predizioni Whareformer.

Configurazione diagnostica fissata prima dei punteggi reali: 700 punti grossolani, fino a 3000 per affinamento, 300 query di validazione, trimming 0.8, supporto entro 0.08 raggi RMS almeno 0.65 in entrambe le direzioni, q90 dei residui trimmati al massimo 0.15 RMS; alternativa entro 5% del costo con posa distinta oltre 15° o spostamento del centro oltre 0.08 RMS causa rifiuto. Queste soglie sono provvisorie, non calibrate o approvate come metodo finale. Memoria: massimo quattro viste, 2048 punti per vista, prima vista preservata; nessun accumulo fisico garantito dalle sole soglie.

## Verifiche e revisione del banco di prova

Sette test dell'accumulatore/registrazione superati: recupero di trasformazione nota su superficie sintetica asimmetrica, rifiuto di forma incompatibile, conservazione dello stato su rifiuto, budget/ancora e provenienza, trasformazioni non rigide e duplicati, degenerazione/configurazione, invarianza al cambio d'origine. Il set finale è quello di sette test, non la somma dei test ripetuti durante la correzione.

Prima versione conservata in `outputs/registration_pilot_v1/`, inclusi sorgenti. Il confronto fra due piccoli insiemi di validazione confondeva posa e densità di campionamento: perfino con trasformazione esatta nota, il supporto DA/MoGE sul tagliere risultava circa 0.627/0.637 in una direzione, sotto 0.65. Inoltre confrontare direttamente le traslazioni delle pose candidate dipendeva dall'origine. Corretti riferimento dei residui, confronto dello spostamento del centro e affinamento. **Nessuna soglia rilassata per far passare le viste reali.**

Controlli su nuvole reali trasformate artificialmente: con versione corretta entrambi i rami del tagliere e della bottiglia superano i gate, ma il recupero non è perfetto. Errore RMS con corrispondenze note, normalizzato al raggio: tagliere 0.0605 DA/0.0676 MoGE; bottiglia 0.00393 DA/0.00313 MoGE. Quindi il solo passaggio dei gate non certifica la posa esatta, soprattutto su superfici poco distintive. Non confondere questi controlli con nuove viste o misura della ricostruzione reale.

## Pilota su viste reali

Primo campione fissato prima dei punteggi: tagliere verde P01_01, frame 2893/5099/7508; coltello arancione P03_04, 8115/19311/20618. Tre osservazioni per identità visiva, DA/MoGE separati, otto tentativi dopo quattro inizializzazioni. Output corretti in `outputs/registration_pilot_v2/` (33.73 s locali); prima versione e fallimenti conservati.

| Caso | Aggiornamenti accettati | Osservazione |
|---|---:|---|
| Tagliere DA/MoGE, seconda vista | 0/2 | Supporto buono (minimi 0.863/0.843), ma pose alternative simili: rifiuto per ambiguità |
| Tagliere DA/MoGE, terza vista | 0/2 | Supporto asimmetrico e pose ambigue; rapporti di estensione circa 0.74/0.77 |
| Coltello DA/MoGE | 0/4 | Ambiguità e/o residui/supporto insufficienti; estensioni e profondità differenti |

Per distinguere il problema da quello dei frame molto distanti, aggiunto un **diagnostico separato**, selezionato dalla distanza temporale e dalle identità preesistenti prima di leggerne i punteggi: bottiglia del latte P08_09, 7109/7272/7508. Configurazione invariata, quattro tentativi DA/MoGE: **0/4 accettati**, 40.29 s locali. Output `outputs/registration_close_views_v1/`, selezione `integration_prototype/close_views_selection.json`.

Per la bottiglia, rapporti fra raggi RMS correnti/ancora: DA 1.766 e 1.260; MoGE 1.452 e 1.355. Non sono fattori di scala fisici certificati: possono dipendere da parzialità, outlier, profondità o forma osservata diversa. Non normalizzati via per far passare una trasformazione rigida. Essere più vicini nel tempo non basta nel campione verificato.

Totale dei due piloti finali: nove osservazioni, tre identità visive, tre video, 18 nuvole con hash verificati, sei inizializzazioni e **12 aggiornamenti reali rifiutati**. P01_01 resta pilota comune; altri video sono riuso diagnostico, non test finale. Le inizializzazioni non contano come fusioni riuscite. Identità riferite dalla revisione visiva storica con i suoi limiti.

![Proposte di allineamento: le viste rifiutate non sono fuse](outputs/registration_pilot_v2/alignment_diagnostic.png)

Figura ispezionata: proiezioni XY/XZ nella stessa scala RMS dell'ancora, senza normalizzazione indipendente delle viste. Sovrapposizione apparente in un piano non risolve ambiguità 3D o differenze in profondità. Colori distinguono i frame; nessun punto delle viste rifiutate è entrato nella memoria.

## Conseguenza operativa

L'accumulatore gestisce budget, trasformazioni e rifiuti; l'estimatore rigido da soli punti **non è ancora sufficiente per un aggiornamento affidabile su questi casi**. Non dimostrata impossibilità generale della fusione, né superiorità DA/MoGE.

**Nessuna nuova inferenza SuperFlex avviata:** non esiste un accumulo reale ammesso dal pilota. Inferire sull'ancora sola ripeterebbe una ricostruzione già disponibile e non proverebbe il nuovo aggiornamento. Nessun job HPC lanciato o coda ricontrollata in questa fase.

Prossima incertezza da risolvere: separare ambiguità di posa da variazione della geometria/scala. Due diagnostici limitati da progettare senza promuoverli automaticamente a metodo: (a) verificare se pixel/colori/corrispondenze RGB forniscano una posa indipendente per i casi con buon supporto ma ambigui; (b) confronto esplicito rigidità/similarità a scala limitata, valutato su query escluse, per i casi con estensioni diverse, mantenendo visibili trasformazioni, fallimenti e limiti. Rilassare soltanto i gate o normalizzare ogni vista non risolve queste incertezze.

In parallelo il controllo con forme separate e l'adattatore 2A restano utilizzabili; lo step 2B è avviato, non validato sui dati reali. Nessun beneficio tracking misurato, nessuna chiusura fittizia della roadmap.
