# Confronto su 200 nuove immagini — protocollo e avanzamento

**Fase conclusa:** risultati e limiti in [RISULTATI_CONFRONTO_200.md](RISULTATI_CONFRONTO_200.md). 299 osservazioni/200 RGB nuovi, cinque video, 890 mesh disponibili. Le note operative sotto conservano la sequenza di acquisizione e ripresa; non descrivono job ancora in corso.

Archivio completo scaricato e verificato localmente: 6185 checksum e 891 provenienze delle nuvole, oltre ai due artefatti appaiati. Nessun job lasciato attivo; non ripetere acquisizione o confronto. Manifest finale `manifests/compare200_749968.json`.

9 novembre 2026. Marco approva il confronto appaiato su un campione più ampio prima di scegliere la sorgente geometrica. Nessun vincitore assunto. Questa fase segue i test diagnostici precedenti e precede la scelta del ramo geometrico per l'integrazione.

## Campione fissato prima delle inferenze

Cinque video nel train della configurazione Whareformer fissata, con mesh già disponibili: **P01_01, P02_03, P03_04, P08_09, P22_01**. Cinque partecipanti distinti, senza presumere cinque ambienti fisicamente indipendenti. Obiettivo: **40 nuovi frame per video**, totale 200; tutti i 19 frame P01_01 già usati sono esclusi.

Acquisizione limitata ai primi 16 MiB di ciascun TAR RGB ufficiale, con maschere dense VISOR, mapping ufficiale e pose EPIC-Fields. Fra i frame recuperabili con annotazioni, posa e almeno un oggetto candidato, scegliere 40 quantili temporali. Nessuna selezione basata sulle predizioni. Se i candidati sono meno di 40, segnalare il problema senza ridurre silenziosamente la numerosità. Il campione resta condizionato alla disponibilità nel frammento TAR, non casuale rispetto all'intero dataset.

Categorie candidate definite da un elenco di nomi di oggetti solidi/utensili (in `acquire_compare200.py` e manifest finale). Conservare tutte le osservazioni candidate nei frame scelti; soglia di area maschera 128 pixel a 456×256, esclusioni/fallimenti rendicontati. Nessuna identità fisica dedotta dal solo nome di categoria.

## Sistemi e misure

- Stessi RGB, maschere, pixel validi confrontabili, checkpoint SuperFlex robust, 4096 punti con seed 42, normalizzazione degli autori. Coordinate camera senza canonicalizzazione; nessuna modifica agli XYZ Whareformer.
- Depth Anything V2 Metric Indoor Large grezzo e allineato alla scena; MoGE-2 ViT-L. Stesse revisioni dei test precedenti. Allineamento ancora diagnostico in unità scena, senza equivalenza metrica alla baseline certificata.
- Misurare copertura, esclusioni/fallimenti, tempi per fase e memoria. Residui ai rispettivi punti stimati solo come diagnostica secondaria di fitting.
- Figure e giudizio qualitativo con criteri dichiarati: struttura generale, dettagli visibili e primitive incoerenti. Senza superfici 3D ground truth non è una misura di accuratezza fisica.
- Prima delle nuove inferenze, aggiunta una misura comune alle sorgenti: IoU e copertura della maschera VISOR rispetto alla mesh riproiettata con la camera usata da ciascun ramo. Misura la compatibilità 2D con il supporto visibile, non l'accuratezza 3D: una parte corretta ma occlusa può estendersi fuori dalla maschera. Rendicontare eventuali vertici dietro la camera. Tutte le osservazioni vengono misurate; per la lettura qualitativa predisporre 12 osservazioni per video a quantili dell'elenco eleggibile, selezione indipendente dal risultato, conservando tutti gli output.
- Per stabilità e discriminatività servono identità verificate, ancora da ottenere: questa misura non va dichiarata eseguita dal solo confronto geometrico. Il confronto nel tracking resta successivo.

Budget iniziale proposto: circa un'ora di calcolo, da verificare sul primo blocco del nuovo campione. Download, attesa in coda e valutazione separati. Più frame non implicano indipendenza statistica; non promettere significatività o generalizzazione dal solo numero 200.

Aggregazione delle misure di maschera: prima media per immagine delle osservazioni misurabili, poi media per video e fra video con peso uguale. Riportare anche numerosità, copertura e risultati per categoria. Non eliminare dal resoconto i fallimenti: conteggiarli separatamente e dichiarare il denominatore di ogni confronto appaiato. Nessun test che tratti tutte le osservazioni come indipendenti. La scelta finale non va basata sul solo residuo ai punti stimati.

Durante l'esecuzione è emerso un output SuperFlex senza primitive attive con MoGE (soglia originale 0.5). Il job 749968 si è fermato dopo 19m33s sul quarto video. Ripresa predisposta senza cambiare modello/soglie o selezione: riusare i tre video conclusi, gli input geometrici del quarto e le predizioni complete; registrare il caso come fallimento e proseguire. Verifica finale dipendente 749976 annullata perché il prerequisito è fallito. Aggiungere al riepilogo descrittivo anche la IoU di servizio con output mancanti trattati come sagoma vuota (zero), per tutti i rami; mantenere separati punteggi condizionali/appaiati e tassi di fallimento. Questa lettura aggiuntiva è successiva all'emergere del fallimento, non una misura confermativa preregistrata.

Ripresa **750019** inviata sullo stesso run. `superflex_batch_probe.py` conserva il corpo di inferenza/esportazione del probe verificato e aggiunge gestione dei fallimenti per osservazione e riuso degli output con provenienza coerente; non modifica i pesi o la soglia. Caso originario `P08_09/frame_0000010781__a01`. Risultati finali ancora da verificare.

## Stato operativo

Mapping dei cinque video e mesh predisposti per l'HPC. Pose P01_01 riutilizzate. Il precedente collegamento Dropbox non consente accesso all'indice; acquisizione degli altri quattro JSON tramite streaming dell'[archivio ufficiale Oxford](https://thor.robots.ox.ac.uk/epic-fields/json-format.tar.gz), conservando solo i file richiesti, senza salvare l'archivio completo da 7.5 GB. Fonte documentata nella [pagina ufficiale EPIC-Fields](https://github.com/epic-kitchens/epic-fields/blob/main/site.html).

Job CPU di acquisizione **749955** inviato; stato finale non ancora verificato. Log `~/cv_project/compare200_acquire_749955.{out,err}`; dati/manifest di avanzamento in `~/cv_project/data_compare200/`. Nessuna nuova inferenza del confronto da 200 immagini ancora eseguita.

Aggiornamento acquisizione: 749955 terminato FAILED/1:0 dopo 4m12s, dopo aver recuperato tutte le pose e fissato 120 immagini nei primi tre video. P08_09 è nel train Whareformer, ma il suo TAR RGB è nel percorso ufficiale originale `rgb/test/` (HTTP 200), non `rgb/train/` (404). Le due suddivisioni hanno finalità diverse: il video resta nel train della configurazione Whareformer, senza modificare il campione o usare un suo video di test. Corretto il recupero e predisposto riavvio con riuso dei tre campioni già fissati.

**Stato successivo:** acquisizione **749966 COMPLETED/0:0**, 1m15s. Campione finale fissato: **200 nuove immagini**, 40 per ciascuno dei cinque video; **299 osservazioni candidate** (73/59/58/52/57). Manifest finale remoto `data_compare200/selection_final.json`. Job GPU **749968** inviato con validazione preventiva di dimensioni, hash, mapping, pose e annotazioni; limite un'ora. Run `~/cv_project/runs/compare200_749968/`, tempi per video/fase in `timings.csv`. Esito e misure ancora da verificare. Hash degli script trasferiti coincidono con quelli locali.

Avanzamento verificato: tutti i 200 RGB e cinque mesh hanno hash coincidenti anche nelle copie locali, campione in `data/compare200/`, selezione in `manifests/compare200_selection.json`. Primi due video completati: P01_01 fasi DA/MoGE/nuvole/SF 64/44/33/160s, P02_03 62/42/28/153s. Verifica anticipata P01_01 **749989 COMPLETED/0:0** in 47s: 73 osservazioni, nessuna esclusione, 219 output controllati; errore massimo di riproiezione dei punti <0.00002 pixel. Quattro tavole delle 12 osservazioni prefissate ispezionate, note in `outputs/compare200_749968/P01_01/visual_review.json`. Non trarre conclusioni comparative dai soli primi video. Verifica finale CPU **749976** programmata dopo il successo del job GPU; riutilizzerà i controlli già completati per video.
