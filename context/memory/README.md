# Memoria della forma 3D per Whareformer

Progetto di Deep Learning for Computer Vision, Bocconi, 2026/2027. Domanda approvata: verificare se confrontare la forma SuperFlex di ogni osservazione con una memoria delle forme delle track, anch'esse stimate con SuperFlex, migliori l'associazione delle identità di Whareformer a parità degli altri input. EPIC-KITCHENS è la base comune approvata per sviluppo e valutazione, con test finale separato. Nessun beneficio nel tracking dimostrato; metodo e protocollo dettagliato restano da definire.

## Da dove iniziare

- **[Passaggio di consegne per qualsiasi AI](LEGGIMI_PASSAGGIO_AI.md):** stato aggiornato al 14 novembre, evidenze, vincoli, istruzioni e prossime attività. I riepiloghi storici sotto vanno letti alla luce di questa guida.

- **[Mappa interattiva e ripresa delle modifiche](mappa_interattiva/README.md):** HTML locale, contenuti modificabili e istruzioni.

- **[Roadmap del ciclo unitario dopo rilettura dei paper](ROADMAP_CICLO_GEOMETRICO.md):** confronto della forma, associazione, aggiornamento geometrico e verifiche; prevale sulle precedenti note che separavano l’accumulo dall’integrazione.

- **[Analisi aggiornamento GitHub del collega — 13 novembre](ANALISI_AGGIORNAMENTO_GITHUB_20261113.md):** ponte offline P01_01, risultati riportati e verificati, limiti e priorità proposte per l'integrazione.
- **[Piano di chiusura del ramo geometrico](PIANO_CHIUSURA_RAMO_GEOMETRICO.md):** mandato esecutivo, consegne, criteri di chiusura e passaggio ad Astra.
- [Revisione per GitHub](REVISIONE_CODICE_REPOSITORY.md): codice e consegna autonoma pubblicati su `main`, controlli ed esclusioni; memoria condivisa in `context/memory`, archivio storico conservato localmente.
- **[Che codice abbiamo prodotto](docs/CODICE_PRODOTTO.md):** componenti sviluppati, input/output, dipendenze dagli autori e integrazione ancora mancante.
- **[Come condividere il progetto](docs/CONDIVISIONE.md):** repository GitHub, risultati essenziali e pacchetti dati separati.
- **[Mappa completa degli script](scripts/README.md):** pipeline attuale, controlli, diagnostici storici e limiti di portabilità.
- **[Ultimo test: procedimento e risultati](RISULTATI_IDENTITA_DA_MOGE.md):** 8797 coppie, primo campione visivo e limiti dell'interpretazione.

Stato scientifico al 13 novembre 2026: ramo geometrico portabile e memoria candidata consegnati, confronti disponibili; nessun beneficio nel tracking dimostrato. DA e MoGE restano entrambi in valutazione. Il collega ha caricato due script e report del collegamento offline P01_01: 71/73 geometrie su 18 track. Coerenza e controlli sintetici verificati; output completi e configurazione baseline non ancora acquisiti per ripetere il join reale. Restano collegamento nel ciclo del tracker, contributo nel matcher e valutazione. Marco ha chiarito che l’accumulo alimenta la memoria geometrica del ciclo unitario; roadmap tecnica aggiornata, algoritmi e parametri ancora da validare.

```text
scripts/       codice nostro e job HPC documentati
docs/          orientamento e collaborazione
manifests/     versioni, hash e inventari
results/       risultati numerici selezionati per la consegna
*.md           stato, decisioni, protocolli e resoconti scientifici
```

Le directory locali `data/`, `outputs/`, `external/`, `Whareformer-repo/`, `SuperFlex-repo/` e `shared_exports/` restano fuori da Git. Leggere i risultati non richiede di rieseguire i modelli.

## Documenti di lavoro

- [Ricognizione critica sulla memoria geometrica robotica](RICOGNIZIONE_MEMORIA_GEOMETRICA_ROBOTICA.md): letteratura primaria aggiornata, precedenti, utilità/fattibilità/novità e test minimo proposto; nessun cambio di obiettivo adottato.
- [Opzioni di confronto e memoria robotica](OPZIONI_FORMA_E_MEMORIA_ROBOTICA.md): ridondanza, pro/contro, ruolo di SuperFlex e ipotesi applicativa ancora aperta; ricognizione bibliografica preliminare aggiornata dal documento sopra.
- [Comprensione DA, MoGE e SuperFlex](COMPRENSIONE_DA_MOGE_SUPERFLEX.md): sintesi del dialogo con Marco per l'esposizione, ruolo della camera e limiti del confronto.
- [Risultati sulle 200 immagini](RISULTATI_CONFRONTO_200.md): confronto appaiato, disponibilità delle mesh, tempi, tavole e raccomandazione motivata.
- [Confronto su 200 immagini](CONFRONTO_200_IMMAGINI.md): protocollo corrente approvato, cinque video, acquisizione e valutazione dei due rami.
- [Confronto geometrico esteso](CONFRONTO_GEOMETRIA_ESTESO.md): protocollo e risultati su nuovi frame, 27 oggetti e tre condizioni geometriche.
- [Controllo MoGE-2](VERIFICA_MOGE2_749539.md): esecuzione con VISOR e robust, confronto con la geometria precedente e limiti.
- [Registro delle decisioni](REGISTRO_DECISIONI.md): storia scientifica delle scelte, motivazioni, revisioni e limiti, per report e presentazione.
- [To-do corrente](TODO.md): checklist prioritaria per verificare il ponte caricato e completare l'integrazione SuperFlex–Whareformer, aggiornata il 13 novembre.
- [Replica RGB SuperFlex](REPLICA_RGB_SUPERFLEX.md): preparazione SAM3 → MoGE-2 → robust, versioni e accesso ai pesi.
- [Stato del lavoro](STATO_LAVORO.md): decisioni, verifiche e punto da cui riprendere nella prossima sessione.
- [Roadmap separata per ruolo](<roadmap separata per ruolo.md>): bozza da discutere e condividere con l'altro membro del gruppo.
- [Fase 0](FASE_0.md): proposta concreta, confronti e verifiche di accesso.
- [Prima esecuzione](PRIMA_ESECUZIONE.md): input necessari, controlli e procedura per Whareformer ufficiale su un video.
- [Prima esecuzione SuperFlex](PRIMA_ESECUZIONE_SUPERFLEX.md): preparazione della prova robust sull'HPC, parte di Marco.
- [Verifica SuperFlex](VERIFICA_SUPERFLEX_744144.md): esito della prima inferenza e confronto visivo della lampada.
- [Input EPIC pilota](INPUT_EPIC_PILOTA.md): dati necessari per passare dai frame alle prime nuvole degli oggetti.
- [Roadmap](ROADMAP.md): attività, gate e calendario di lavoro fino al 23 novembre.
- [Starting point](Starting_point.md): obiettivi e vincoli concordati.
- [Base scientifica](LETTURA_E_BASE_SCIENTIFICA.md): evidenze della lettura preparatoria e limiti.
- [Inventario](INDICE_MATERIALI_LETTI.md): materiali consultati.
- [Istruzioni del supervisore](ISTRUZIONI_SUPERVISORE_SCIENTIFICO.md): criteri di collaborazione.

## Organizzazione e riproducibilità

Questa cartella è il perimetro del repository di progetto. Le slide e i PDF del corso restano nella cartella superiore; `Fonti/` conserva le copie locali dei paper. Le copie di codice consultate in `../tmp/pdfs/repos/` sono materiale preparatorio esterno al repository, non dipendenze già installate.

Dati, checkpoint e output voluminosi sono esclusi dalla cronologia. Prima degli esperimenti, registrare URL e versione di ogni risorsa, checksum dei file scaricati, ambiente, configurazione, split, seed e comando eseguito. Conservare in Git il nostro codice, configurazioni, manifest e risultati aggregati necessari a riprodurre le conclusioni.

La pubblicazione remota e il pacchetto di condivisione sono registrati in `STATO_LAVORO.md`; non presumere che l'assenza di dati/pesi dal clone significhi che non siano mai stati elaborati. Gli esperimenti conclusi sono documentati nei resoconti e negli snapshot in `results/`. Per le versioni del codice degli autori usare i manifest; non attribuire al nostro progetto l'implementazione delle reti preaddestrate.
