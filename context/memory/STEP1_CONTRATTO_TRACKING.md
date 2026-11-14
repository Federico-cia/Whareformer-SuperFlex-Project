# Step 1 — contratto delle osservazioni e baseline

## HPC ripristinato, arretrati inviati — 14 novembre

SSH/accounting/coda accessibili. Recuperati 761899 (prefisso storico a peso zero esatto, 3398 frame/10264 detection, zero differenze dal collega) e 761905 (IDF1 73.2697% sulle predizioni registrate train, non test). Nuovi job: 763321 COMPLETED/0:0, 50 test ambiente passati; 763322 replica aggiornata e 763323 accumulo RUNNING nell’ultima osservazione; 763324 SuperFlex differita PENDING per dipendenza dai due CPU. Nessun nuovo esito sperimentale ancora dichiarato; prossima acquisizione dei risultati. [RIPRESA_HPC_20261114.md](RIPRESA_HPC_20261114.md). Le note precedenti sul blocco DNS e sui due esiti ancora da leggere sono storiche.

**Stato prevalente al 14 novembre 2026:** configurazione, checkpoint e input ufficiali acquisiti; ordine/metadati/XYZ verificati su tutte le 110590 osservazioni. Il candidato 2A è collegato al tracker originale nel runner isolato; 120 controlli a peso zero con modello reale e input controllati superati. Replica del prefisso reale 761899: ultima osservazione RUNNING a 3000/3398 frame, esito finale ancora da acquisire. Metriche 761905: COMPLETED, valore IDF1 non ancora letto. Recupero bloccato da DNS, prossimo tentativo con VPN Bocconi; nessun rilancio. Restano due alias JPEG e validazione 2B (0/12 fusioni reali). Le note sottostanti su asset mancanti o assenza del collegamento al tracker sono storiche; non considerare completata la replica. [Resoconto tecnico](INTEGRAZIONE_BASELINE_REALE_20261113.md).

13 novembre 2026. Marco ha approvato ROADMAP_CICLO_GEOMETRICO.md e richiesto l'avvio dello step 1. Stato: avviato, non concluso; verifica sui dati reali dipendente da asset non ancora disponibili nei percorsi controllati. Non è accertato se siano già condivisi altrove.

> Revisione successiva: Marco autorizza lavoro indipendente negli altri step e replica minima se necessaria. L'incompletezza di questo step non blocca adattatore/accumulo controllati; vedi [AVANZAMENTO_AUTONOMO_20261113.md](AVANZAMENTO_AUTONOMO_20261113.md). Il criterio di chiusura della verifica della run del collega resta invariato.

## Nuova consegna: esito corrente

A bbf0e5e sono arrivati i due manifest; audit reale del join passato (71/73), controlli di box VISOR e byte delle 146 nuvole effettuati. I due casi mancanti sono ritrovati al nome-frame VISOR di un indice prima; rimane da controllare il JPEG sorgente delle feature. Report corrente [VERIFICA_CONSEGNA_WHAREFORMER_20261113.md](VERIFICA_CONSEGNA_WHAREFORMER_20261113.md). La richiesta minima sotto è storica: punti 1 acquisiti, gli altri asset della run ancora mancanti. Step 1 completo aperto, acquisizione dei manifest superata.

## Verifiche svolte prima della nuova consegna

- Remoto ricontrollato: main ancora a `ab5a946c1f94018edad90e69bc5544306f913569`, nessun upload successivo. Whareformer contiene due script, README e tre riepiloghi, non i manifest completi.
- Ricerca mirata dei nomi richiesti nel workspace, incluse directory ignorate: nessun output completo o feature baseline trovato.
- Accesso HPC esistente riuscito. Ricerca di file regolari nello spazio personale `~/cv_project`, profondità massima sette, per output, annotazioni, feature e checkpoint Whareformer previsti: nessun risultato. Cartelle fino a profondità due inventariate per delimitare il controllo. Non cercati account del collega o storage esterni; nessuna inferenza, installazione o job lanciato, nessun controllo aggiornato della coda.
- Riutilizzate le verifiche della precedente analisi senza ripeterle: coerenza report/CSV, manifest compare200 e casi sintetici degli script del collega.
- Preparato `scripts/audit_tracking_contract.py`: confronto JSON delle 73 osservazioni con track e join, controllo provenienza dichiarata delle nuvole, unicità, track_id, campi copiati e indice nelle annotazioni sorgenti se fornite. Sei casi sintetici superati, inclusi errori introdotti di track, hash, duplicato, omissione e indice. Non eseguito su output reali mancanti. Il confronto degli hash nei manifest non ricontrolla i byte delle nuvole; non carica pickle e non certifica l'ordine delle feature.

Evidenza: `outputs/step1_tracking_contract/status.json`. Riferimento per il controllo: `outputs/step1_tracking_contract/reference_P01_01.json`, estratto dal manifest originale; non assegna identità alle track. Il controllo legge solo la memoria sorgente e scrive un nuovo report senza sovrascrivere report esistenti.

## Richiesta minima al collega

Per verificare il collegamento già calcolato, condividere un archivio con struttura preservata e:

1. `tracks_by_id.json` completo e `compare200_joined_observations.json` completo per P01_01. I riepiloghi già caricati non li sostituiscono.
2. Configurazione effettivamente usata, comando di inferenza, commit/versione dei sorgenti ed eventuali modifiche, versione ambiente essenziale; nome/provenienza e SHA-256 del checkpoint. Non occorre copiare pesi o variabili d'ambiente personali.
3. Output dell'evaluator e log pertinenti, con IDF1/mPCL se disponibili; se la valutazione non è stata eseguita, dichiararlo.
4. `object_annotations.json` effettivamente usato, oppure inizialmente le annotazioni dei frame compare200 conservando l'ordine originale e il checksum del file completo. Questo sottoinsieme permette verifiche locali, non la riproduzione dell'intero video.
5. Contatti/percorso di accesso ai file di input e output originali: `tracking_outputs.pkl`, feature PCA-256 e XYZ allineati, metadati video e checkpoint. Per ripetere davvero la baseline serviranno accesso a questi file o una procedura verificata per recuperarli; il pacchetto minimo non basta da solo.

Gli asset possono restare esterni a Git. Niente nuovo training o rigenerazione delle nuvole. Non includere credenziali. Nessuna richiesta è stata inviata automaticamente al collega.

## Ripresa quando arrivano i file

1. Preservare originali e registrare hash/versioni; rieseguire il join su input effettivi o confrontare il manifest completo con il contratto.
2. Eseguire il controllo JSON, indicando `--reference`, `--tracks`, `--joined`, `--annotations` e un nuovo `--output`. Lo script descrive in modo separato ciò che non verifica.
3. Usare i mapping individuali per costruire le tavole delle track 4/36 e 9/35; conservare i due casi mancanti senza forzare assegnazioni. Il report aggregato non identifica tutte le osservazioni delle track: revisione per-track ancora pendente.
4. Verificare input/feature/configurazione prima di qualsiasi inferenza baseline, usando o adattando `prepare_baseline.py`; eventuale esecuzione isolata senza sovrascrivere la run del collega. Definire poi il segmento comune ripercorribile.

**Criterio di chiusura:** segmento P01_01 con origine di detection/feature/XYZ verificata, associazioni baseline riproducibili, riferimenti geometrici validi e casi esclusi spiegati. Attualmente questo criterio non è soddisfatto. Non passare implicitamente al ciclo completo per aggirare la dipendenza.
