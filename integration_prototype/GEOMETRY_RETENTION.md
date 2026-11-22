# Recupero dei derivati SuperFlex conservati in forma compatta

Il formato compatto conserva le nuvole originali, i parametri SuperFlex, le matrici originali di assegnazione e una piccola palette di colori. Non conserva per intero input normalizzati, predizioni diagnostiche e mesh PLY. Questi tre file si ricostruiscono **senza GPU**, con verifica del checksum originale. Nessun cambio di precisione o punti. Una ripetizione dell'inferenza GPU non ha superato il confronto numerico richiesto ed è esclusa dal recupero ordinario.

## HPC già configurato

Da una shell sull'HPC:

```bash
TASK="$HOME/cv_project/p01_full_enrichment_20261121_v1"
PROJECT="$HOME/cv_project"
module load cuda/12.4
export PATH="$HOME/.conda/envs/cv-superflex/bin:$PATH"
export PYTHONPATH="$PROJECT/campaign_20261115_v1/runtime:$PROJECT/SuperFlex-repo:$TASK/retention_tools"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
PYTHON="$HOME/.conda/envs/cv-superflex/bin/python"
```

Per recuperare un file, leggere il percorso relativo esatto da `geometry/NNNN/retention.json`, poi eseguire:

```bash
"$PYTHON" "$TASK/retention_tools/geometry_retention.py" regenerate \
  --root "$TASK/geometry/0004" \
  --path "superflex_da/001fc5eca275ec9c4c967d45/reconstruction.ply"
```

Lo stesso comando accetta `input.npz` e `prediction.npz` nei rispettivi percorsi registrati. Per scrivere altrove aggiungere `--destination /percorso/nuovo/file.ply` (oppure `.npz`); non sovrascrive file diversi. Se ambiente, prerequisiti o checksum non corrispondono, si arresta senza dichiarare il recupero riuscito.

Per recuperare tutte le mesh di un solo blocco in una cartella separata:

```bash
"$PYTHON" "$TASK/retention_tools/regenerate_geometry_block.py" \
  --root "$TASK/geometry/0004" --kind surface \
  --destination "$TASK/regenerated_on_request"
```

Si può limitare a una fonte con `--source da` o `--source moge`, oppure ai primi file con `--limit 3`. `--kind input`, `--kind diagnostic_prediction` e `--kind all` recuperano gli altri derivati. L'archivio di assegnazione è verificato e caricato una volta per recuperare molte diagnostiche; i checksum finali sono verificati per ciascun file. Non avviare il recupero contemporaneamente alla compattazione dello stesso blocco: il lock lo impedisce. La cartella di destinazione conserva un proprio registro della rigenerazione.

Il recupero di un file richiede pochi prerequisiti e ricostruisce un solo derivato; rigenerare indiscriminatamente tutte le mesh annullerebbe il risparmio. Per molte ricostruzioni usare un job CPU, senza richiedere GPU. Le dipendenze sono quelle dell'ambiente verificato cv-superflex: numpy 1.26.4 e trimesh 5.2.0, codice originale SuperFlex/shape_tools presente. Gli hash di codice/configurazione e dei dati sono registrati nel ledger; il checksum finale intercetta anche variazioni nelle librerie che alterino l'output.

## Lettura per esperimenti

```python
from geometry_retention import retained_features
features = retained_features(block_root, observation['representations']['da_superflex'])
```

Usa l'estrattore di descrittori originale su un PLY temporaneo, ricostruito e verificato, e non lascia una copia permanente. Nuvole `.npz` già presenti sono lette normalmente. I lettori storici che aprono direttamente un PLY vanno preceduti dal comando `regenerate`; non trattare un file non conservato come una nuova inferenza fallita.

## File di conservazione e ripartenza

- `retention.json`: elenco esatto dei derivati intenzionalmente assenti, SHA-256 originali, ricette, prerequisiti e palette.
- `retention_assignments.npz`: solo matrici di assegnazione originali; necessarie a recuperare esattamente le diagnostiche senza ripetere inferenza.
- `retention_result.json`: esito dell'operazione sul blocco. Il risparmio netto include il costo dell'archivio e dei registri.
- `observations.json`: `storage.state=regenerable` esplicita l'assenza intenzionale. Gli indici scientifici e le firme originali restano invariati.

`retained_pipeline.py` avvolge la pipeline originale: controlla gli artefatti ancora presenti e accetta le sole assenze documentate con prerequisiti validi. Un file perso o corrotto senza ricetta resta un errore. `enabled.json` nella cartella `retention_tools` abilita l'adattatore nel driver `full_p01_enrichment.py`; la politica compatta viene applicata dopo l'export di ciascun nuovo blocco.

Il comando `compact` predefinito verifica e pianifica; soltanto `--apply` rimuove file dopo confronto esaustivo con i rispettivi SHA. Conservare ledger, archivi delle assegnazioni, prerequisiti, script e ambiente. Non cancellarli come cache.
