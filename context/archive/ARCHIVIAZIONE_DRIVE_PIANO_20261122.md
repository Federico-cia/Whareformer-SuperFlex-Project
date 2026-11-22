# HPC entro quota e archivio Google Drive — proposta del 22 novembre 2026

> **Lettura dopo il consolidamento del 22 novembre 2026:** questo documento conserva specifiche ed evidenze delle fasi descritte. Per stato operativo, attività e scelte successive consultare [stato corrente](../memory/STATO_LAVORO.md), [TODO](../memory/TODO.md) e [decisioni](../memory/REGISTRO_DECISIONI.md); il contratto attuale della memoria è [opzione A](../memory/MEMORIA_OPZIONE_A_E_SELEZIONE_20261122.md). Le note di attesa o di lavoro non ancora eseguito qui sotto sono datate, non un nuovo stato corrente.

## Risorsa e direzione

Marco dichiara di avere 1 TB su Google Drive e domanda come completare tutti i blocchi usando i 50 GB HPC senza perdere i dati necessari. La strategia raccomandata è conservare i risultati su Drive e usare l'HPC come area di lavoro a dimensione limitata. È **una proposta operativa**, non un trasferimento già autorizzato/eseguito o una capacità end-to-end già dimostrata. Non richiede riduzione di precisione, copertura o geometria osservata.

**Revisione del budget:** la stima di circa 130.5 GiB di geometria/160 GiB complessivi nella [compattazione precedente](COMPATTAZIONE_HPC_20261122.md) si riferisce alla configurazione storica DA+MoGE su tutta la copertura. La [decisione corrente](RUOLI_DA_MOGE_E_CONSEGNA_P01_02_20261122.md) è DA completo, MoGE solo campione; i risultati MoGE esistenti vanno conservati. Il nuovo percorso aggiunge DA allineato/camera/world e SuperFlex separato: serve un pilota per il budget aggiornato, non basta dimezzare la vecchia stima. P01_01/P01_02 rimangono video distinti sui due account, non due rami del medesimo video.

Un TB è ampiamente superiore agli output stimati della vecchia configurazione per P01_01; spazio effettivamente libero e quota dell'account Drive da verificare una volta collegato. Non è necessario trasferire software e ambienti insieme a ogni blocco.

## Controlli già effettuati, solo lettura

- Ricerca del connettore Google Drive: non utilizzabile in questa sessione (`DISABLED_BY_ADMIN`/`NOT_AVAILABLE`). Nessuna modifica alle impostazioni o tentativo di abilitazione.
- Rclone non rilevato nel PATH HPC né in `~/bin/rclone` o `~/.local/bin/rclone`; verifica delimitata, non inventario di tutti i moduli software.
- Endpoint pubblico di descrizione API Drive raggiunto dall'host login con HTTP 200. Questo **non** dimostra autorizzazione al proprio account, possibilità di upload/download binari, velocità o accesso dalla partizione di calcolo. Un altro controllo di endpoint ha restituito HTTPError; non interpretarlo come blocco OAuth, perché non era un tentativo di autorizzazione.
- Coda personale vuota al controllo. Nessun trasferimento, cancellazione aggiuntiva, installazione, nuova autenticazione o job di produzione.
- Ricevuta locale `outputs/drive_storage_plan_20261122/read_only_preflight.json`.

## Riduzioni senza perdita da valutare

1. **Una sola profondità per frame**, identificata da hash RGB/modello/configurazione/revisione, condivisa dalle osservazioni e dai blocchi. Evita copie per confini di blocco; il risparmio reale dipende dalle ripetizioni, non va dato per enorme.
2. **Nuvole DA derivate da profondità e pixel.** Conservare profondità originale, intrinseci, selezione esatta e ordine dei pixel, RGB/maschere/provenienza permette di progettare la ricostruzione CPU dei punti. Colori e punti XYZ non devono necessariamente esistere in tutte le copie contemporaneamente. Il codice attuale conserva questi contenuti separati: la nuova rappresentazione richiede prova esaustiva di equivalenza prima di rimuoverli. Preservare la selezione effettiva: i vecchi confronti con pixel comuni DA/MoGE differiscono dalla futura produzione DA-only.
3. **Coordinate camera, allineate e mondo.** `align_video_scene.py` usa alpha/beta, intrinseci, pixel e trasformazione camera→mondo. Le copie derivate possono essere ricostruite se si conservano trasformazioni, normalizzazione, selezioni dopo filtri e precisione/ordine delle operazioni. Il file world contiene già la trasformazione; verificare prima il contenuto completo e tutti gli hash. Proposta, non nuovo codec implementato.
4. **Contenitori per blocco**, con elenco dei membri e checksum, invece di migliaia di file per oggetto. Riduce gli inode e migliora trasferimento/recupero. Gli NPZ sono già compressi: non promettere un grande risparmio aggiuntivo soltanto inserendoli in ZIP/TAR.

La profondità completa resta necessaria all'allineamento con background/mesh finché non viene consumata e verificata. Le nuvole stimate/osservate non sono sostituite dalle mesh SuperFlex. Mappe e nuvole possono essere **archiviate integralmente su Drive**, evitando di rinunciare ora a informazioni che potranno servire ai controlli. Le riduzioni di rappresentazione diventano ottimizzazioni ulteriori, non prerequisito per avere un archivio capiente.

Precisazione sul codice letto: l'allineamento corrente mantiene tutti i pixel/colori osservati e rifiuta l'osservazione se una profondità allineata risulta non positiva/non finita; non applica un nuovo sottocampionamento selettivo. Le ricette future devono mantenere anche questa semantica di fallimento. Per sbloccare la capacità conviene iniziare dall'archivio dei formati attuali, poi valutare il nuovo formato deduplicato separatamente.

## Ciclo proposto, con capienza limitata sull'HPC

1. Produrre un blocco e verificarne copertura, stati, hash e conservazione compatta già approvata.
2. Creare un archivio immutabile del blocco con mappe/nuvole, parametri, matrici originali, palette, configurazione e indici necessari al recupero. Conservare separatamente un piccolo catalogo locale e il riferimento agli input originali condivisi. Evitare un secondo archivio dell'intera campagna sul disco HPC.
3. Copiare l'archivio in una cartella dedicata Drive, conservando ID remoto, byte, checksum e ricevuta. Verificare contenuto caricato, con controllo effettivo di hash e non sola dimensione; primo pilota con download/ripristino completo e confronto dei membri. Per gli archivi successivi prevedere controllo di integrità dopo upload e verifica all'atto del recupero.
4. Solo dopo verifica positiva, rimuovere i payload locali di quel blocco e l'eventuale archivio temporaneo; lasciare catalogo/manifest/stati necessari per sapere cosa esiste e dove recuperarlo. Eliminare anche i piccoli report per oggetto/directory ormai contenuti nell'archivio, mantenendo l'informazione nel catalogo: altrimenti il limite di inode resta.
5. Proseguire con il blocco successivo. Usare inizialmente una sola unità di calcolo/upload in volo e un limite esplicito alla cache di recupero; aumentare concorrenza solo dopo misura del picco. Upload fallito → dati locali conservati e nuovi blocchi sospesi per non accumulare backlog. Il trasferimento non deve mantenere occupata la GPU inutilmente: separare calcolo da archiviazione/trasferimento sul percorso CPU consentito dal centro.

**Primo recupero di spazio:** archiviare progressivamente i 15 blocchi già compattati può liberare nell'ordine di ulteriori 8–9 GiB di geometria locale. Stima dal conto precedente, non misura post-upload. Si tornerebbe vicino alla base di circa 33 GiB, lasciando circa 13 GiB per blocco attivo, archivio temporaneo, cache e riserva. La fattibilità effettiva richiede che il picco misurato del pilota resti entro 46.56 GiB e 500000 inode; se il trasferimento è più lento del calcolo, applicare attesa e non accumulare blocchi indefinitamente.

## Contratti da adeguare prima della produzione

- Stato distinto per calcolato, archivio remoto verificato, payload locale rilasciato. Un blocco archiviato non va rielaborato perché mancano i file su disco.
- Catalogo locale per video/run/blocco con ID Drive e checksum, coordinate/provenienza, esiti scientifici e ricette di rigenerazione. Dopo archiviazione anche i prerequisiti delle ricette CPU possono essere remoti: prima scaricare il blocco in cache, poi rigenerare i derivati.
- Aggregazione e lettori devono supportare riferimenti remoti e recupero selettivo. Non lasciare falsi percorsi locali come se i payload fossero presenti; non avviare l'attuale driver su directory spostate manualmente.
- Recuperare pochi archivi per volta per training/analisi, estrarre i dati necessari e limitare la cache. Non ricostruire permanentemente tutta la campagna sull'HPC, né affidare al montaggio di Drive una cache senza limite.
- Prova iniziale su un blocco: upload, controllo remoto, download, confronto membro per membro, lettura nuvole/forme/trasformazioni e ripartenza con payload locale archiviato. Poi applicazione ai 15 blocchi precedenti e alla futura produzione.

## Collegamento a Drive e fonti

Rclone supporta [Google Drive](https://rclone.org/drive/) e il [controllo dei trasferimenti](https://rclone.org/commands/rclone_check/), incluso confronto con riscaricamento in streaming. Le API Google supportano [upload riprendibili](https://developers.google.com/workspace/drive/api/guides/manage-uploads); la ripresa esatta tra job/processi dipende dal client e va verificata, non assunta dal solo supporto API.

Per un HPC senza browser è previsto il [collegamento da una macchina con browser o mediante tunnel SSH](https://rclone.org/remote_setup/). La documentazione corrente di Rclone segnala il ritiro nel 2026 del client OAuth condiviso: configurare un client proprio quando richiesto, senza basare il piano su un'autenticazione condivisa garantita. L'autorizzazione personale va completata dall'utente nel browser; non chiedere token/password in chat e non salvarli nella memoria del progetto. Installazione/configurazione e prova di un archivio rimangono da eseguire.

Preferenza proposta: trasferimento diretto HPC→Drive, così il PC non deve rimanere acceso per tutta la campagna. Alternativa se la rete del centro non lo consente: passaggio sul PC di un archivio alla volta, caricamento e verifica su Drive prima del rilascio; anche sul PC va limitata la copia temporanea.

## Aggiornamento 22 novembre 2026, sera: vincoli HPC e accesso condiviso

Fonte: slide Linux4HPC Bocconi (aprile 2026) in `Introduction to Linux for HPC/`. Nodi di calcolo 2x Dell R750XA (2x Xeon 5317, 512 GB, 4 A100 80 GB ciascuno; una slide parla di tre nodi GPU, incoerenza non risolta), RHEL 9.6, SLURM, partizione/QoS `stud`, per studente fino a 32 GB RAM e 4 GPU. Regola: sul nodo login non si eseguono programmi; quindi i trasferimenti rclone vanno in job SLURM CPU, e l'accesso a Internet dai nodi di calcolo resta da verificare (il controllo precedente riguardava solo il login). La slide indica 100 GB di home, ma la quota misurata è 50 GB (46.56 GiB): prevale la misura.

Accesso Drive: nessuna cartella pubblica necessaria. Rclone con OAuth sull'account di Marco; token in `~/.config/rclone/rclone.conf` privato sull'HPC; autorizzazione da browser sul PC (configurazione remota). Client OAuth proprio obbligatorio nel 2026; in stato Testing i permessi scadono dopo una settimana, quindi pubblicare l'app per uso personale (avviso app non verificata) oppure ripetere `rclone config reconnect`. Limite non documentato circa 750 GiB/giorno di upload. Condivisione con il compagno tramite condivisione nominativa della cartella dedicata, non link pubblico; i file caricati dal compagno nella cartella occupano la sua quota, salvo uso di un Drive condiviso. Credenziali mai in chat o nella memoria del progetto. Stato: proposta, nessuna configurazione eseguita.
