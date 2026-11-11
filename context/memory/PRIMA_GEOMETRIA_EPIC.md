# Prime nuvole EPIC — prova diagnostica

**9 novembre: job CPU 747518 completato e risultati controllati.** Vedere `VERIFICA_GEOMETRIA_747518.md` e `outputs/epic_geometry_cpu_747518/controllo_nuvole.png`. Non ripetere setup o job riusciti. Le istruzioni seguenti documentano preparazione e risoluzione del problema EGL.

## Aggiornamento dopo il job 747498

Il primo job è fallito dopo 3m16s all'apertura di EGL: `Invalid device ID (0)`. Non ha raggiunto allineamento o punti. Preparato il sostituto `scripts/setup_epic_geometry_cpu.sbatch`: rendering OSMesa sulla CPU dell'HPC, ambiente separato `cv-epic-geometry-cpu` (Python 3.11, NumPy 1.26.4, Mesa 25.0.5; release precedenti alla rimozione di OSMesa), senza nuovi forward neurali. Fork PyOpenGL indicato da Pyrender, commit risolto registrato e checkout riutilizzato nelle esecuzioni successive. Ambiente depth e SuperFlex non modificati da questo nuovo job.

Prima dei dati reali, `render_backend_probe.py` verifica la profondità nota di un box (1.5 unità) e registra vendor/renderer/versione OpenGL. Riutilizza la stessa geometria/alignment di prima; backend/versioni diversi non costituiscono prova di equivalenza numerica con la baseline. La sintassi è verificata localmente; installazione, rendering OSMesa e risultato sull'HPC restano da verificare. Nessun cambiamento ai sorgenti Whareformer fissati.

Nel PowerShell locale trasferire **solo** `epic_geometry_probe.py`, `render_backend_probe.py` e `setup_epic_geometry_cpu.sbatch` in `~/cv_project/`. Poi sul cluster: `sbatch --account="$USER" setup_epic_geometry_cpu.sbatch`. Log `epic_geometry_cpu_JOB.out/.err`, risultati `runs/epic_geometry_cpu_JOB/`. Le istruzioni EGL sotto restano come storico del primo tentativo.

Fonti consultate: [Pyrender, modalità offscreen](https://pyrender.readthedocs.io/en/latest/examples/offscreen.html), [installazione OSMesa e fork PyOpenGL](https://pyrender.readthedocs.io/en/latest/install/index.html), [ricetta Mesa e rimozione OSMesa](https://github.com/conda-forge/mesalib-feedstock/pull/123). La causa specifica dell'indisponibilità EGL sul cluster non è ancora accertata.

8 novembre 2026. Script preparati e sintassi controllata localmente; job non ancora inviato. Rendering, allineamento e punti vengono eseguiti sull'HPC, senza rieseguire Depth Anything o SuperFlex.

Il job usa mesh e pose P01_01, le tre profondità del job 744902 e le annotazioni originali. Riutilizza le funzioni originali Whareformer per posa, rendering e allineamento. Esclude dal fit i poligoni di tutti gli oggetti annotati e delle mani; ricrea le maschere con cv2.fillPoly e nearest neighbour come il codice originale, anziché assumere identità con la precedente rasterizzazione locale di anteprima.

**Scala diagnostica:** manca la scala effettiva della baseline. Il job usa esplicitamente scala 1, in unità della ricostruzione, non metri. Nessuna equivalenza baseline rivendicata. Conserva profondità grezza e scene depth, parametri del fit e punti camera/mondo, senza cambiare le feature Whareformer. La scala può essere fornita successivamente con `--scale-file`; la provenienza deve coincidere con la baseline. Non usa automaticamente il valore nel config.

Si mantiene la proiezione pinhole del codice originale, che non applica i coefficienti di distorsione presenti in EPIC-Fields. Il clipping originale 0.01–10 è nelle unità correnti e può cambiare copertura dopo una variazione di scala: l'equivalenza va verificata nuovamente, non dedotta solo da un fattore globale.

Output in `~/cv_project/runs/epic_geometry_JOB/geometry/`: mappe di scena e allineate, maschere, PLY camera/mondo, NPZ con coordinate/colori/pixel e report. Stop se mancano superfici statiche; nessuna nuvola per frame con fit degenere, coefficiente negativo o profondità dell'oggetto non positiva. Un fit numericamente valido non dimostra accuratezza: prima di SuperFlex occorre ispezionare le nuvole e i residui del fit.

## Trasferimento — PowerShell locale

```powershell
Set-Location '[LOCAL_HOME]\Desktop\2026\3rd semester DSBA\Computer Vision\lavoro di gruppo'
Dettagli personali di accesso HPC omessi dalla copia condivisa; configurazione conservata solo localmente.
```

## Invio — terminale HPC

```bash
cd "$HOME/cv_project"
sbatch --account="$USER" setup_epic_geometry.sbatch
```

Monitoraggio: `squeue -u "$USER"`. Con il numero ricevuto, leggere `epic_geometry_NUMERO.out` e `.err`. Il job installa le sole dipendenze di geometria nell'ambiente cv-epic-depth; l'ambiente SuperFlex resta separato. La disponibilità del rendering EGL sull'HPC deve ancora essere verificata dal job.

## Costo atteso

Questa prova elabora tre frame senza nuovi forward neurali; atteso carico contenuto, tempo effettivo da misurare. I 30 minuti richiesti sono un limite SLURM, non una previsione. Il primo carico consistente arriverà con profondità su molti frame e SuperFlex su molte osservazioni/oggetti. Il forward lampada di circa 0.79 s non misura caricamento, preprocessing, rendering o costo completo, e non basta per stimare il video intero. Prima di estendere, misurare il costo completo su un piccolo lotto e salvare le forme per riusarle negli esperimenti di associazione.
