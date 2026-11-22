# Ripresa con altro provider — ammissione geometrica, 21 novembre 2026

> **Nota successiva:** documento di ripresa iniziale della discussione del 21 novembre. Le decisioni prese dopo (scala, memoria, verificatore, obiettivo di fusione dopo spostamento) sono in [SUPERVISIONE_AMMISSIONE_20261121.md](SUPERVISIONE_AMMISSIONE_20261121.md) e prevalgono sulle frasi «non ancora scelti» qui sotto.

## Lettura e precedenza

Leggere questo documento, poi ISTRUZIONI_SUPERVISORE_SCIENTIFICO.md, STATO_LAVORO.md, TODO.md e le ultime revisioni di REGISTRO_DECISIONI.md. La guida generale è LEGGIMI_PASSAGGIO_AI.md. Le revisioni esplicite più recenti prevalgono sulle note storiche. Italiano scientifico, conciso, comprensibile; spiegare i concetti senza assumere conoscenze non mostrate. Aggiornare autonomamente memoria dopo decisioni e risultati; non registrare conversazione informale o credenziali.

## Decisioni di Marco in questa discussione

Quattro temi: (1) confronto delle forme/descrittore; (2) ingresso e forza della forma nel matcher Whareformer; (3) ammissione di nuovi punti nella memoria geometrica; (4) collocazione/aggiornamento della forma nella scena 3D.

Il compagno si occupa del punto 2; Marco prende in carico il punto 3. Punti 1 e 4 dopo la risoluzione di entrambi. Non attribuire al compagno metodi o risultati non comunicati. Il precedente rinvio della revisione dei gate è SUPERATO: Marco vuole procedere sul punto 3.

Indicazione esplicita: le soglie di accettazione devono essere apprese, non imposte manualmente. Obiettivo: conservare viste parziali valide. Approvata questa direzione, NON ancora scelti modello, supervisione, loss, protocollo o nuove soglie. Nessun training, modifica del registratore o esperimento effettuato in questa discussione. Resta il vincolo già approvato di nessuna nuova annotazione manuale. Scelte scientifiche decisive da discutere con Marco; attività reversibili già autorizzate da eseguire senza conferme ripetute.

## Meccanismo implementato e verificato nel codice

File integration_prototype/cloud_memory.py e cloud_updater.py. Associazione Whareformer prima; registrazione/ammissione dopo. Rifiutare la geometria non annulla l'associazione. Memorie separate DA/MoGE. Allineamento rigido con PCA, più inizializzazioni e ICP; rotazione/traslazione, nessuna correzione di scala. I completamenti SuperFlex non entrano nei punti osservati. Aggiornamento ammesso -> accumulo osservazioni -> nuova richiesta SuperFlex, disponibile per frame futuri. Rifiuto preserva memoria geometrica valida.

Gate attuali provvisori, aggiunte nostre, non prescrizioni dei paper:
- Supporto: almeno 65% in ciascuna direzione entro 0.08R.
- Residuo: q90 sull'80% delle distanze più vicine non oltre 0.15R, in entrambe le direzioni.
- Ambiguità: un'altra soluzione entro 5% dello score migliore più epsilon, ma diversa oltre 15 gradi oppure con centroide spostato oltre 0.08R, causa rifiuto.
- Basta fallire un gate. R = raggio RMS del riferimento fit, non centimetri.
- Rapporto dei raggi registrato, non gate autonomo. Query di validazione separate da fitting/selezione, ma dalle medesime osservazioni: non nuove viste indipendenti.
- Prima osservazione inizializza senza confronto di registrazione; soli controlli di validità dell'input. Una cattiva inizializzazione può condizionare la memoria.

## Evidenze e criticità

Campagna conclusa 15 novembre: 446 osservazioni/247 frame, DA 23 inizializzazioni, 31 fusioni, 392 rifiuti; MoGE 23/40/383 per variante. Non sommare varianti con stesse associazioni come prove indipendenti. 29 configurazioni, assegnazioni identiche a baseline; nessun beneficio tracking dimostrato. Non è una misura indipendente di qualità fisica delle fusioni. Resoconto RISULTATI_CAMPAGNA_HPC_20261115.md.

Audit del prefisso, RIPRESA_HPC_20261114.md: tagliere frame 5099 DA/MoGE supera supporto/residui ma rifiutato per sola ambiguità. Tagliere MoGE 7508: 99% dei punti correnti vicino al riferimento, 42.3% nell'altra direzione; compatibile con vista parziale, non prova di posa corretta. Altri casi falliscono anche supporto/residui: distinguere parzialità, posa, scala, rumore, maschera e associazione errata; nessuna causa unica dimostrata.

Parzialità: se memoria ampia e nuova vista piccola, nuova->memoria può essere alta mentre memoria->nuova è bassa perché molte parti non sono visibili. Viceversa, punti nuovi fuori dalla parte comune possono essere superficie utile, non errore. Obiettivo proposto: verificare posa nella parte comune e conservare superficie nuova compatibile. Senza overlap o altri riferimenti, geometria sola può non identificare la posa; conservazione separata temporanea è una proposta, non politica adottata.

Ambiguità: più trasformazioni con score simile. Distinguere simmetria innocua (superficie equivalente) da alternative che collocano diversamente le nuove parti. Gate corrente confronta trasformazioni, non equivalenza esplicita delle superfici. Mancanza di alternative trovate non prova unicità globale.

## Proposte discusse, NON approvate come metodo

A. Apprendere soglie delle diagnostiche esistenti: interpretabile, ma eredita limiti delle misure.
B. Piccolo classificatore che combina diagnostiche e contesto: raccomandazione dell'assistente, può condizionare accettazione a overlap/qualità; occorrono target indipendenti.
C. Affidabilità/overlap per punto: più flessibile ma maggiori dati e sviluppo; possibile passo dopo dimostrati limiti delle diagnostiche.

Non addestrare sui sì/no dei gate attuali: sarebbe imitazione delle euristiche. Identità oracle/stesso oggetto non certifica posa, scala o utilità della fusione. Distinguere apprendimento della decisione e validazione indipendente. Non dire che il training rimuova ogni scelta: target, loss e politica decisionale vanno definiti e verificati.

Possibili fonti di supervisione/validazione senza nuove annotazioni manuali:
- Coppie/crop con trasformazioni note e rumore: automatici e controllabili; rischio domain gap e geometria di partenza imperfetta.
- Evidenze RGB/corrispondenze multivista: informazione aggiuntiva; limiti texture, occlusioni, movimento e pose incerte.
- Viste reali escluse dalla fusione: confronto prima/dopo su osservazioni non usate; richiede visibilità/riferimenti affidabili, possibili errori sistematici condivisi.
- Dataset con geometria/pose note: riferimento diretto; compatibilità, accesso e trasferimento EPIC da verificare.

Raccomandazione ancora da valutare: supervisione automatica con trasformazioni note, parzialità e negativi difficili; piccolo modello iniziale; valutazione del trasferimento su viste reali escluse. Separare oggetti/sequenze nei dati per evitare leakage. Misurare false ammissioni, falsi rifiuti e qualità della memoria; non ottimizzare il solo numero delle fusioni.

Fonti primarie consultate come precedenti concettuali, non prova di compatibilità EPIC:
- PREDATOR, CVPR 2021, overlap appreso: https://openaccess.thecvf.com/content/CVPR2021/html/Huang_Predator_Registration_of_3D_Point_Clouds_With_Low_Overlap_CVPR_2021_paper.html
- Deep Global Registration, CVPR 2020, affidabilità corrispondenze appresa: https://openaccess.thecvf.com/content_CVPR_2020/html/Choy_Deep_Global_Registration_CVPR_2020_paper.html
Non dichiarare nuova lettura integrale dei paper in questa discussione.

## Dati e attività parallele: non perdere lo stato corrente

Lo STATO_LAVORO.md è stato aggiornato anche da altri lavori durante questa chat: NON ripristinare snapshot precedenti.
- Campione oracle: 782875 COMPLETED 0:0, 446 esempi/247 frame/17 identità benchmark, controlli superati secondo memoria corrente. Zero query Nuova track nel campione; non è training completo o supervisione di pose. ARRICCHIMENTO_TRAINING_20261121.md.
- Estensione completa P01_01 autorizzata: 110590 osservazioni/33310 frame, 446 geometrie già verificate, 110144 pendenti nella preparazione. ARRICCHIMENTO_COMPLETO_P01_20261121.md.
- Ultimo stato DOCUMENTATO, non ricontrollato live in questa consegna: RGB ufficiali scaricati; 782967 cancellato, sostituito da 782990 (PENDING all'invio); 782968/782969 GPU restano gli stessi, dipendenze aggiornate su 782990. Radice ~/cv_project/p01_full_enrichment_20261121_v1/, log acquire_782990.out/.err e geometry_<job>.out/.err; ricevute submissions/. Verificare stato/output prima di ogni azione, non duplicare invii. Copertura maschere e avvio GPU ancora da osservare nella memoria letta.
- Vecchi commenti mappa applicati e pubblicati, commit 9fe32e6ed8752fddb2c5850e254682bab8f6e0a6 secondo memoria corrente. Non considerarli ancora in attesa di approvazione.

## Ripartenza consigliata

Riprendere dalla domanda: quali target indipendenti di correttezza della registrazione/fusione possiamo costruire automaticamente con dati e riferimenti disponibili? Verificare prima disponibilità/qualità, poi proporre modello e protocollo minimo a Marco con pro/contro. Non assumere già scelti dataset sintetico, classificatore, rete preaddestrata o nuove soglie. Non rilanciare campagne concluse. Nessun push o contatto con il compagno autorizzato da questa richiesta di memoria.

## Aggiornamento successivo

Analisi della supervisione disponibile in [SUPERVISIONE_AMMISSIONE_20261121.md](SUPERVISIONE_AMMISSIONE_20261121.md): pose EPIC-Fields e mesh P01_01 verificate come riferimento potenziale; proposte e domande aperte, nessuna decisione.
