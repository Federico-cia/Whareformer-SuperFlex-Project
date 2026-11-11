# Prima esecuzione Whareformer — preparazione

**Fine sessione del 4 novembre:** Marco sta scaricando feature e checkpoint. Download non ancora verificati; nessuna esecuzione HPC avviata. Riprendere dai controlli in `STATO_LAVORO.md`.

4 novembre 2026. **Stato: preparazione locale, esecuzione HPC non ancora effettuata.** Marco ha confermato accesso da terminale e download manuale dello ZIP al commit fissato. I materiali HPC forniti indicano SSH a `slogin.hpc.unibocconi.it`, rete Bocconi o VPN da casa, partizione/QoS `stud` e modulo `/software/modules/miniconda3`. Restano da ottenere feature e checkpoint e verificare l'assegnazione reale sul cluster. Il repository condiviso non è un prerequisito tecnico per questa prova.

**Archivio locale verificato:** Marco ha estratto il codice in `Whareformer-repo/`. Tutti i **75 file** dell'inventario GitHub precedentemente salvato per il commit `82dd349957e1f04f92a2979b4c92c2f3fed445c5` corrispondono ai rispettivi hash Git blob; nessun file atteso manca o risulta modificato. Inventario di riferimento non troncato; confronto effettuato localmente, senza una nuova interrogazione GitHub. Checksum SHA-256 registrati in `manifests/whareformer_archive.json`. La cartella contiene già `data/epic_osnom/EPIC_100_video_info.csv`, ma non checkpoint o feature per osservazione.

Per questa copia usare `--repo` puntato a `Whareformer-repo` e l'opzione `--archive`. La cartella degli autori è esclusa dalla cronologia del nostro repository; il manifest resta tracciabile. Non occorre spostare o rinominare la cartella.

## Indicazioni ricavate dal materiale HPC

Esaminato il testo delle pagine pertinenti di Lesson 1 (pp. 5–10), Lesson 2 (pp. 5–18) e Lesson 3 (pp. 7–10), presenti in `Introduction to Linux for HPC/`. Le slide di marzo/aprile 2026 indicano 100 GB di spazio personale, massimo 32 GB di RAM per studente e massimo quattro GPU. Sono regole documentate, da confermare nell'account attuale; la RAM di sistema è distinta dalla memoria GPU. Gli esperimenti vanno eseguiti in batch sui nodi di calcolo, non sul nodo di accesso.

Prima connessione dal terminale locale, sostituendo `MATRICOLA`:

```bash
Dettagli personali di accesso HPC omessi dalla copia condivisa; configurazione conservata solo localmente.
```

Preparato `scripts/hpc_probe.sbatch`: richiede una GPU, due CPU, 4 GB di RAM e cinque minuti per registrare hardware visibile, ambiente Conda e quota. Dopo averlo trasferito in una cartella di lavoro sul cluster, inviarlo da quella cartella con:

```bash
sbatch --account="$USER" hpc_probe.sbatch
```

Il comando assume che il nome dell'account di calcolo coincida con la matricola di login, come negli esempi del corso. Leggere poi `cv_probe_JOBID.out` e `.err`. La prova non installa né esegue modelli. Lo script è preparato ma non ancora inviato.

## Obiettivo della prova

Eseguire il codice ufficiale senza modificare il metodo, con checkpoint preaddestrato e feature ufficiali di **un video del train**. `P01_01` è un candidato tecnico presente nella configurazione ufficiale. Questo controllo non seleziona il campione scientifico definitivo e non replica i numeri aggregati del paper: verifica caricamento, tracking e valutazione. Nessun training richiesto.

## Risorse e accesso

- Codice: [Whareformer, commit consultato](https://github.com/JacobChalk/Whareformer/tree/82dd349957e1f04f92a2979b4c92c2f3fed445c5). Fissare questo commit per rendere coerenti configurazione e controlli sotto; un aggiornamento richiede ricontrollarli.
- Feature preestratte, CSV e checkpoint: seguire i link del [README ufficiale](https://github.com/JacobChalk/Whareformer#pre-extracted-features). Nella verifica web precedente i link SharePoint hanno reindirizzato a login Microsoft. Serve verificarli nella sessione dell'utente; nessun file è già stato ottenuto.
- Per la prima prova servono `object_annotations.json`, `2D_feat_masked_PCA_256d.pkl`, `3D_feat_aligned.pkl` del video, CSV con colonne `video_id,frames,fps` e checkpoint Whareformer. Non occorrono ancora RGB, maschere dense o mappe di profondità: serviranno nella verifica geometrica successiva.
- La [pagina HPC Bocconi](https://www.unibocconi.it/en/current-students/technology-and-information-services/infrastructure-and-systems/hpc), consultata il 4 novembre, indica nodi dedicati agli studenti con A100 suddivise tramite MIG. La memoria dell'istanza assegnata può essere inferiore agli 80 GB della scheda fisica. Verificare l'assegnazione reale.

Nel computer locale è stato trovato Python 3.11.9 utilizzabile tramite percorso esplicito, ma senza NumPy, PyYAML e PyTorch. Le dipendenze ufficiali non sono installate. Il download Git è fallito per certificati; il successivo tentativo con certificati Windows richiedeva autorizzazione ed è stato rifiutato. La copia in `../tmp/pdfs/repos/Whareformer` resta utilizzabile per ispezione, ma non è un checkout Git verificato. Nessuna verifica TLS è stata disattivata.

## Ambiente sul cluster

Prima individuare modalità di accesso, VPN eventuale, ambiente Python disponibile, spazio scrivibile e regole di richiesta GPU. Installazione e inferenza vanno eseguite secondo le regole del cluster; non assumere che il nodo di accesso abbia una GPU assegnata.

Il README della versione consultata propone Python 3.13.13 e `requirements.txt` con versioni fissate (PyTorch CUDA 12.6). Verificare compatibilità con driver e moduli del cluster prima di installare. Tenere un ambiente separato da quello futuro di SuperFlex. Salvare le versioni effettivamente installate.

Questi comandi sono per un terminale Linux **dopo l'accesso**, in una cartella di lavoro scelta sul cluster:

```bash
git clone https://github.com/JacobChalk/Whareformer.git
git -C Whareformer checkout 82dd349957e1f04f92a2979b4c92c2f3fed445c5
```

La creazione dell'ambiente e la richiesta di risorse saranno adattate alla modalità di accesso confermata. Non è ancora pronto uno script di invio al cluster: partizione, account e risorsa GPU richiesta non sono noti.

## Preparare gli input e la configurazione

Trasferire anche il nostro `scripts/prepare_baseline.py`. Nell'ambiente Whareformer con NumPy e PyYAML installati, eseguire quanto segue sostituendo i percorsi di esempio:

```bash
python scripts/prepare_baseline.py \
  --repo /percorso/Whareformer \
  --observations /percorso/observations \
  --video-info /percorso/EPIC_100_video_info.csv \
  --checkpoint /percorso/model_epoch100.pt \
  --run-dir /percorso/runs/baseline_P01_01_001
```

Con lo **ZIP già scaricato da Marco**, estrarlo e aggiungere `--archive` al comando, indicando con `--repo` la cartella estratta che contiene `src` e `requirements.txt`. Lo ZIP contiene i file della versione scelta senza cronologia Git. In questa modalità lo script registra la versione dichiarata e i checksum dei sorgenti; non pretende di aver verificato un commit tramite Git. Conservare anche lo ZIP originale per verificarne in seguito il checksum.

In modalità Git lo script richiede un checkout al commit fissato senza modifiche ai file tracciati. In entrambe le modalità controlla appartenenza al train, presenza dei file, corrispondenza di frame e osservazioni, dimensioni 256/3, valori finiti e ordine temporale. Registra checksum degli input e genera una configurazione isolata con un solo video. Una cartella di esecuzione già esistente viene rifiutata. Non addestra né esegue tracking.

## Eseguire e valutare

In una sessione con GPU realmente assegnata e ambiente attivo, adattare i due percorsi:

```bash
set -euo pipefail
WHARE_REPO=/percorso/Whareformer
WHARE_RUN=/percorso/runs/baseline_P01_01_001
export PYTHONPATH="$WHARE_REPO/src${PYTHONPATH:+:$PYTHONPATH}"
python --version > "$WHARE_RUN/python_version.txt"
python -m pip freeze > "$WHARE_RUN/environment.txt"
nvidia-smi > "$WHARE_RUN/gpu.txt"
python -c 'import torch; assert torch.cuda.is_available(); print(torch.__version__, torch.version.cuda); print(torch.cuda.get_device_properties(0))' > "$WHARE_RUN/torch_gpu.txt"
python "$WHARE_REPO/src/scripts/run_tracker.py" --config "$WHARE_RUN/config.yaml" 2>&1 | tee "$WHARE_RUN/tracker.log"
test -s "$WHARE_RUN/tracking/P01_01/tracking_outputs.pkl"
test -s "$WHARE_RUN/tracking/P01_01/results.csv"
python "$WHARE_REPO/src/scripts/evaluate.py" --results_dir "$WHARE_RUN/tracking" 2>&1 | tee "$WHARE_RUN/evaluation.log"
```

Il launcher ufficiale legge `CUDA_VISIBLE_DEVICES`: verificarne l'impostazione da parte del cluster. Non sostituirla con identificatori fisici scelti a mano, soprattutto con MIG. Se manca o il launcher non riconosce l'istanza assegnata, fermarsi e adattare l'esecuzione all'ambiente reale.

**Criterio di riuscita:** i due output esistono, il log non contiene eccezioni di tracking/valutazione e l'evaluator produce IDF1 numerico e mPCL. Il solo codice di uscita non basta: l'entry point ufficiale intercetta alcune eccezioni. Eventuali metriche sul singolo video del train sono diagnostiche, non prestazioni fuori training o replica di 84,0 IDF1 / 72,2 mPCL sul benchmark completo.

## Dettagli risolti nell'ispezione del codice locale

- `WhareformerMatcher.match()` chiama `_greedy_assignment()` in `src/tracking/tracker/matcher/matcher_types.py`: la baseline consultata usa greedy.
- `VideoInstance._load_metadata()` carica `object_annotations.json`, coerentemente con l'estrattore; il nome `observations.json` nel documento di architettura è discordante.
- Con PCA a 256 dimensioni viene caricato `2D_feat_masked_PCA_256d.pkl`, non il file visivo senza PCA.
- L'evaluator ufficiale aggrega i risultati: non sostituirlo con una media delle metriche per video.

Questi riscontri si riferiscono alla copia locale documentata. Vanno confermati sul checkout ottenuto prima di dichiarare la replica eseguita.
