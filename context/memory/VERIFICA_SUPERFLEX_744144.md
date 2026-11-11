# Verifica della prima inferenza SuperFlex robust

7 novembre 2026. Job HPC **744144**, esempio degli autori `lamp.ply`. Risultati acquisiti localmente in `outputs/setup_744144/`.

## Controlli effettuati

- Presenti report JSON, input e predizioni NPZ, input e ricostruzione PLY, checksum, vincoli ed export dell'ambiente. Stdout/stderr completi e stato contabile SLURM non ancora acquisiti; i messaggi di completamento sono stati mostrati da Marco in screenshot.
- Report: PyTorch 2.6.0+cu124, istanza A100 MIG 4g.40gb, seed 42, 4096 punti e **7 primitive attive**. Il caricamento esatto delle chiavi, il forward e l'export hanno superato i controlli dello script.
- Verifica locale: array numerici finiti; punti nel PLY coerenti con quelli delle predizioni; mesh con 5848 vertici e 12194 triangoli, indici validi. Hash di checkpoint e configurazione nel report coerenti con l'inventario locale verificato prima del trasferimento.
- Confronto visivo in tre proiezioni ortografiche, usando coordinate e scala comuni. Figura: `outputs/setup_744144/confronto_lampada.png`; riepilogo tecnico: `outputs/setup_744144/verifica_locale.json`.

## Esito e limiti

La lampada resta riconoscibile: ingombro generale di base e paralume e collegamento centrale sono riprodotti. La decomposizione approssima i dettagli: base più arrotondata, collegamento sottile semplificato, paralume suddiviso in primitive con giunzioni visibili. I colori distinguono le primitive e non rappresentano categorie semantiche o materiali.

**Primo controllo funzionale e visivo del componente superato su questo esempio.** Non è una replica quantitativa del paper, una verifica su osservazioni EPIC o una dimostrazione di forma discriminativa per l'identità. Non sono state misurate accuratezza geometrica con un protocollo di benchmark o qualità del completamento delle parti non viste.

Il tempo di circa 0,787 s è quello di un singolo primo forward nel job; non comprende tutta la preparazione e non costituisce un benchmark di velocità. La memoria massima riportata da PyTorch non coincide con l'intera occupazione GPU del processo.

## Prossimo passo

Concordare col collega un piccolo insieme di osservazioni EPIC con identificatori comuni; verificare disponibilità congiunta di RGB, maschere, profondità e calibrazione. Le sole feature Whareformer e le posizioni 3D non bastano per ricostruire la superficie. Costruire e controllare prima le nuvole di punti, poi applicare l'ambiente SuperFlex già funzionante. Nessun bisogno di ripetere l'installazione.
