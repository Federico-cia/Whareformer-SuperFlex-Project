# Piano proposto: preprocessing → runner comune — 14 novembre 2026

**Stato: approvato da Marco («ok»), esecuzione parziale.** Richiesta esplicita: pianificare, poi implementare solo dopo il suo ok. Avanzamento successivo: contratto/cache e collegamento al comando implementati, pilota cache verificato; rigenerazione non eseguita per dipendenze/provenienza ancora da risolvere. Stato attuale in [FRONTEND_AVANZAMENTO_20261114.md](FRONTEND_AVANZAMENTO_20261114.md). Il testo delle fasi sotto conserva il piano approvato. I job già autorizzati rimangono invariati, senza attribuire loro nuovi stati non osservati.

## Obiettivo e confine

Unire gli estrattori esistenti e il runner: frame RGB + maschere VISOR + metadati EPIC → osservazioni coerenti → aspetto/PCA, posizione e geometria → tracking → valutazione/report. Primo supporto EPIC/P01_01 di sviluppo già disponibile. Non è un ingresso da video RGB arbitrario: maschere, intrinseci, pose e riferimenti di scena sono ingressi dichiarati.

Riutilizzare il codice originale Whareformer per aspetto/posizione, la PCA preaddestrata associata al checkpoint e il nucleo portabile per DA/MoGE/SuperFlex. Reti congelate, convenzioni di preprocessing preservate. Filtri di fusione invariati: la revisione resta rinviata. Nessun nuovo segmentatore, training, cambio del registratore, aumento massivo della copertura o tuning in questo step.

## Sequenza di lavoro dopo approvazione

### 1. Verifica preventiva e inventario degli ingressi

Leggere l'esito della run comune 763531 senza rilanciarla inutilmente. Inventariare RGB, maschere/annotazioni, mapping VISOR→RGB, intrinseci, pose, mesh della scena e scala già calcolata; checkpoint, configurazioni/revisioni dei modelli e PCA; ambienti disponibili. Verificare provenienza e hash quando disponibili.

Il codice originale chiama DINOv2 Giant per l'aspetto, estrae la posizione con DA allineata alla scena e può avviare ricostruzione della scena se manca la mesh. L'orchestratore deve segnalare tali dipendenze prima dell'esecuzione: nessuna ricostruzione COLMAP/MVS estesa avviata implicitamente. Una revisione/peso non identificabile non va sostituito silenziosamente né presentato come identico alla baseline. Distinguere asset mancanti, capacità implementata e percorso effettivamente verificato.

**Consegna:** inventario utilizzabile/mancante, piano degli stadi e necessità CPU/GPU/ambienti. Nessuna stima precisa di durata prima della verifica dei backend.

### 2. Contratto unico delle osservazioni

Definire un manifest versionato con video, indice/frame RGB e VISOR espliciti, ID annotazione, indice detection e ordine, RGB/maschera/box/categoria, camera e provenienza. Ogni artefatto derivato deve rimandare a quella chiave. Non usare la categoria come identità persistente; non assumere annotation_index uguale a detection_idx.

Mantenere distinti XYZ nel riferimento scena per Whareformer e punti osservati nel riferimento camera per DA/MoGE, con trasformazioni/convenzioni e inversa della normalizzazione SuperFlex. Non sostituire XYZ con il centroide della nuvola o con un'altra sorgente di profondità. Alias temporali non verificati esplicitamente esclusi dal primo pilota.

**Consegna:** schema, validatore e adattatore verso il formato numerico già letto dal runner. Verifica di ordine, risoluzioni/coordinate dei pixel e associazione RGB-maschera-camera; errori espliciti prima del calcolo.

### 3. Collegare gli stadi con cache verificata

Preparare due modalità:

- **Riuso verificato:** importare feature/PCA/XYZ e geometrie esistenti soltanto se input, configurazione e provenienza sono compatibili. Un file presente non basta a certificare la cache.
- **Rigenerazione controllata:** richiamare gli estrattori originali e il nucleo geometrico su una selezione esplicita. Preservare ordine dei crop mascherati, normalizzazioni prima/dopo PCA e trasformazione PCA esistente; nessun fit sul pilota o sul test. DA per posizione allineata alla scena e DA/MoGE per forma restano ruoli distinti, anche se alcuni input possono essere condivisi quando realmente compatibili.

Dipendenze fra stadi, configurazioni/hash, log, durate, output e fallimenti registrati. Cache separata per sorgente e configurazione; nessuna sovrascrittura dei risultati storici o mescolanza di ambienti. Riusare gli ambienti già predisposti quando compatibili. Le decisioni sui fallimenti devono rispettare il contratto esistente: dati essenziali baseline mancanti fermano il frame/run; geometria opzionale indisponibile resta dichiarata e usa il fallback già previsto, senza eliminare a posteriori la detection.

**Consegna:** modulo di preparazione generico che produca il bundle atteso, superando le assunzioni P01_01/frame 7508 codificate nel preparatore diagnostico. Nessuna duplicazione delle reti o del tracker.

### 4. Collegare l'ingresso al comando unico

Estendere l'orchestrazione per scegliere input già preparati oppure manifest di frame/maschere/metadati. La seconda modalità esegue/verifica il preprocessing e poi richiama la stessa catena varianti → valutazione → confronto. L'ingresso attuale resta disponibile e coperto da regressione.

Il piano degli stadi deve poter essere verificato prima di lanciare modelli. Riprese tramite artefatti verificati/cache e replay già implementato, senza promettere un checkpoint completo del tracker. Conservare policy temporale di valutazione esplicita, modelli/memorie distinti fra varianti e inferenza SuperFlex dopo ogni aggiornamento ammesso.

**Consegna:** comando unico esteso, configurazione d'esempio e istruzioni per ambienti/dipendenze.

### 5. Verifiche locali e pilota HPC limitato

Prima controlli locali sulle nuove interfacce: riordini/duplicati, frame mapping, maschere e risoluzioni incompatibili, mancanti, cache alterata o con configurazione diversa, PCA non corretta e separazione dei riferimenti 3D. Riutilizzare le regressioni concluse; nuovi test solo sui rischi introdotti.

Poi due verifiche distinte su P01_01:

1. **Percorso in cache:** ricreare il bundle di riferimento e verificare ordine e valori riusati, quindi associazioni e risultati a peso zero. Mantenere la storia del prefisso dall'inizio: partire soltanto dai tre frame geometrici cambierebbe le memorie del tracker.
2. **Percorso rigenerato:** RGB dei frame 2893, 5099 e 7508, tutte le dieci detection presenti. Verificare aspetto/PCA e XYZ rispetto agli asset disponibili; provare la generazione geometrica sulle maschere valide dei tre frame, confrontando le sei osservazioni geometriche già disponibili e dichiarando le altre come nuove. Budget di validazione limitato a questi frame, senza rigenerare il video intero. Riusare gli artefatti compatibili fuori dalla selezione.

Nel secondo percorso, hash identici solo dove l'esecuzione è deterministica e comparabile. Per rigenerazioni numeriche definire tolleranze motivate prima di osservare l'effetto tracking; differenze di modello, immagine, PCA o preprocessing devono essere diagnosticate, non assorbite con soglie arbitrarie. Se la parità non è stabilita, distinguere esplicitamente run rigenerata e replica della baseline. Nessuna fusione riuscita è requisito di questa verifica del frontend.

**Consegna:** test, report del piccolo pilota, differenze e limiti, costi misurati. Se mancano asset indispensabili, completare le parti indipendenti e dichiarare il percorso non ancora eseguito; niente dati o risultati sostitutivi non dichiarati.

### 6. Chiusura e documentazione

Pacchetto di codice/configurazioni senza dati, pesi o accessi personali, istruzioni, manifest e aggiornamento della memoria. Nessun push o messaggio a terzi previsto.

**Criteri di uscita:** manifest validato; generazione del formato comune; riuso controllato della cache; ordine/coerenza dei riferimenti verificati; percorso attuale senza regressioni; pilota di frontend eseguito e documentato nei limiti degli asset disponibili. Distinguere il collegamento software, la rigenerazione effettiva e l'equivalenza scientifica della baseline.

## Dipendenze successive, fuori da questo step

Ampliamento a segmenti geometricamente coperti, revisione della registrazione/filtri quando richiesta, calibrazione delle alternative e del peso della forma, congelamento/test separato. Il pilota non dimostra beneficio tracking, correttezza delle fusioni o funzionamento RGB-only/strettamente online.

## Codice consultato per il piano

`Whareformer-repo/src/scripts/extract_features.py`, `scripts/apply_pca.py`, `feature_extraction/extractors/epic_extractor.py` e `base_extractor.py`, `datasets/epic_dataset.py`, `utils/models.py`, configurazione EPIC; nucleo `shape_tools.pipeline` e manifest d'esempio; preparatore diagnostico e comando unico dell'integrazione. Lettura locale, nessun nuovo esperimento.
