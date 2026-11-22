# Memoria geometrica originaria e prototipo: confronto verificato

## Mandato corrente

Marco richiede il recupero della discussione originale e il confronto con il codice,
prima di ulteriori modifiche. Obiettivo esplicito: predisporre il sistema discusso
originariamente, ispirato alla memoria di appearance. Nessuna modifica algoritmica,
training, test di runtime, nuova inferenza, pubblicazione o azione HPC in questa analisi.

## Fonti effettivamente recuperate

- Cronologia della chat «Sviluppo del criterio di selezione delle nuvole di punti in…»,
  incluse la richiesta di apprendere il criterio e la successiva ripresa delle decisioni.
- Riassunto incollato da Marco al rientro dalla discussione con un altro provider,
  recuperato dall'allegato originale. Non è una trascrizione integrale dell'altra chat.
- [Discussione scientifica del 21 novembre](SUPERVISIONE_AMMISSIONE_20261121.md),
  sezioni sulla memoria, DenStream, scala, collocazione e verificatore; registro delle
  decisioni, ricognizione e resoconto dell'implementazione del 21 novembre.
- Codice originale locale: `Whareformer-repo/src/tracking/tracker/memory/denstream.py`,
  `track.py`, `matcher/matcher_types.py`; configurazioni EPIC con `app_aggregation: clusters`.
- Codice geometrico: `scene_memory.py`, `registered_scene_memory.py`,
  `export_point3_training.py`, `shape_adapter.py` e ShapeMemory del pacchetto riutilizzato.

Il riassunto originale dice esplicitamente: «Le viste dopo lo spostamento formano
prima un'«ipotesi», che viene accettata solo se confermata da più frame».
La sintesi corrente del 21 novembre conferma stati di collocazione sostenuti nel tempo,
forma separata dalla collocazione e verificatore come componente della compatibilità.
Le proposte iniziali non vanno tutte trasformate retrospettivamente in decisioni:
la memoria di descrittori per il matching rimaneva da concordare con il compagno;
valori dei parametri, regole complete di potatura e modello principale non erano fissati.

## Come funziona davvero la memoria di appearance

Per ogni traccia conserva più microcluster di vettori di aspetto. Una nuova osservazione
prova a entrare nel gruppo consolidato più vicino, poi in quello debole più vicino;
la fusione è ammessa se il raggio risultante del gruppo è compatibile. Altrimenti nasce
un nuovo gruppo debole. Non c'è un rifiuto definitivo della feature per sola incompatibilità.

Il peso decade nel tempo; il supporto promuove un gruppo debole, e una potatura periodica
può eliminare gruppi non più sostenuti. Nel codice originale anche i gruppi consolidati
possono essere rimossi quando il peso diventa insufficiente. Il matcher riceve tutti
i centroidi attivi, anche deboli: non è corretto dire che gli arrivino soltanto quelli
promossi. I valori predefiniti sono raggio 0.25, supporto 10, decadimento 0.001:
sono parametri, non soglie magicamente apprese da DenStream.

## L'adattamento geometrico discusso

L'unità del gruppo geometrico è uno stato/collocazione dell'oggetto con viste e punti
compatibili, non un insieme arbitrario di punti XYZ vicini. Nello stesso riferimento
scena, viste compatibili rinforzano lo stato; una vista valida incompatibile alimenta
una nuova ipotesi. La conferma temporale deve precedere l'inserimento di una nuova
ipotesi nella forma persistente. Dopo uno spostamento la vecchia forma resta disponibile;
il nuovo stato viene registrato sulla forma e unito soltanto se la registrazione regge.
Se non regge, lo stato rimane separato e può ricevere nuove osservazioni.

Il verificatore serve a stabilire compatibilità e affidabilità di registrazione.
Non sostituisce gestione delle ipotesi, supporto temporale, promozione e potatura.
DenStream non elimina il problema della registrazione 3D o quello delle false fusioni.

La forma persistente si accumula con celle pesate, senza privilegio della prima vista,
conservando superficie nuova e 4096 punti FPS per SuperFlex. Copiare la cancellazione
dei microcluster di appearance direttamente sui punti della forma cancellerebbe copertura:
la durata degli stati e la conservazione della superficie devono rimanere distinte,
come già discusso. Il decadimento dei punti non è di per sé la potatura degli stati.

## Confronto col codice

| Meccanismo | Nucleo del 21 novembre: SceneObjectMemory | Percorso del replay del 22: RegisteredObjectMemory |
|---|---|---|
| Più ipotesi per traccia | Sì, dizionario di stati | No: unica voce `registered-shape` |
| Vista valida incompatibile | Crea nuovo stato debole | Respinta: non conserva i punti come ipotesi |
| Supporto e conferma temporale | Per ciascuno stato | Solo promozione iniziale; poi singole viste subito fuse se passano |
| Decadimento | Punti e supporto degli stati | Punti e supporto dell'unico stato |
| Potatura | Evizione del più debole quando si esaurisce il budget pendenti | Nessun ciclo reale di vita di più ipotesi |
| Demozione/rimozione per tempo | Non equivalente alla potatura periodica DenStream; confermati mai rimossi | Assente per lo stato confermato |
| Forma distinta dagli stati | Sì | Distinzione ridotta alla forma e all'ultima trasformazione |
| Fusione dopo movimento | API disponibile, con trasformazione e verifica fornite dal chiamante | Registratore effettivo chiamato su ogni vista |
| Presupposto di staticità | Richiede `stationary` ed evidenza esterna | Non richiede staticità |
| Celle pesate, filtro, FPS, provenienza | Presenti | Riutilizzati |
| Memoria descrittori come appearance | Non implementata dal nucleo dei punti | Non implementata: ShapeMemory legacy è FIFO, export offre una forma per candidata |

Il primo nucleo contiene quindi già parti significative dell'architettura originaria;
non dobbiamo ripartire da zero. Non basta però cambiare il nome della classe nel replay:
richiede staticità esterna non risolta e non coordina autonomamente la registrazione
degli stati consolidati dopo spostamento. Inoltre la sua evizione a budget non replica
il ciclo temporale di DenStream.

## Dove è avvenuta la deviazione

Il 22 novembre ho proposto registrazione/verifica per ogni vista per evitare il requisito
preventivo di staticità. Marco ha approvato questa semplificazione. Ho implementato
anche un unico stato e il rifiuto immediato delle viste incompatibili: queste conseguenze
non erano necessarie per eliminare il requisito di staticità e non erano state chiarite
come rinuncia al sistema multi-ipotesi. La precedente descrizione di semplice estensione
del piano originale era quindi incompleta. La richiesta corrente ripristina esplicitamente
l'architettura originaria come obiettivo; non basta migliorare la regressione o la soglia.

## Che cosa manca per predisporre il sistema originario

1. **Riattivare il gestore multi-ipotesi** come percorso effettivo di replay e coordinatore,
   partendo da SceneObjectMemory. Distinguere input invalido da input valido incompatibile:
   solo il primo viene escluso senza ipotesi; il secondo può iniziare uno stato debole.
2. **Completare il ciclo temporale degli stati:** assegnazione, rinforzo, promozione,
   decadimento e potatura. Confrontarlo col comportamento reale di FeatureDenStream;
   documentare gli adattamenti geometrici e selezionare i parametri sullo sviluppo.
3. **Separare conferma dello stato e fusione nella forma.** Una nuova collocazione non
   deve contaminare subito la forma persistente. La conferma non dimostra da sola
   la correttezza di posa: rimane la verifica geometrica.
4. **Collegare il registratore già disponibile agli stati confermati**, mantenendo separate
   le ipotesi che non possono essere unite. Definire esplicitamente se e come usare la
   prima tappa statica del piano originale: rimuovere il blocco di staticità non richiede
   eliminare gli stati. Nessuna certificazione automatica di staticità va dichiarata esistente.
5. **Esportare e verificare il percorso corretto:** stati deboli/confermati/scaduti,
   trasformazioni, cronologia e forma persistente; query sempre prima degli aggiornamenti.
   Ripetere il replay per produrre nuovi dati di training, senza rinominare gli export attuali
   come risultati del sistema multi-ipotesi. Provare in particolare una vista inizialmente
   incompatibile che riceve conferme successive, un outlier che resta isolato e uno spostamento.
6. **Coordinare la memoria di descrittori del punto 2**, se si vuole DenStream anche sul
   segnale di matching. È distinta dalla fusione dei punti; descrittore e metrica compatibile
   vanno fissati col compagno. Non assumere che le soglie dei vettori di appearance abbiano
   senso per D2 né che la media dei descrittori equivalga alla fusione di superfici.

Riutilizzabili: allineamento DA/scena, filtro/celle pesate, registratore, interfacce e baseline
del verificatore (con limiti noti), FPS, worker SuperFlex e controlli di causalità/provenienza.
Non necessari per questo riallineamento: nuova rete neurale o nuova campagna di generazione
geometrica completa. La baseline del verificatore resta un confronto debole, non il modello
principale originariamente previsto.

## Stato e limiti della verifica

Confronto statico di documenti e codice; non prova di efficacia del sistema originario.
Gli esempi già mostrati e i conteggi del report del 22 novembre appartengono al percorso
semplificato. Restano conservati come confronto, senza certificare DenStream geometrico.
La gestione multi-ipotesi può differire fusioni rischiose e recuperare viste utili respinte,
ma non garantisce di correggere errori sistematici confermati ripetutamente.
