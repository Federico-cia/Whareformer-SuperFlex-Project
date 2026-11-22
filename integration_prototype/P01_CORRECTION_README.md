# P01_01: lavoro autonomo sulla correzione di Whareformer

Questa consegna serve a costruire esempi supervisionati e sviluppare la correzione
dei punteggi di Whareformer usando la geometria. Non esegue training di una nuova
architettura scelta implicitamente. P01_01 è sviluppo, non test indipendente.

## Due componenti della consegna

1. **Core**: questo codice, input numerici e annotazioni originali completi del
   video (33310 frame/110590 osservazioni), checkpoint Whareformer congelato e
   codice originale necessario. Include il riferimento numerico di 446 esempi
   già verificati. Non servono estrazione DINO/PCA, GPU o nuova inferenza SuperFlex.
2. **Geometrie**: archivio separato con 8126 osservazioni (446 precedenti + 7680
   nuove), ciascuna con nuvola DA osservata, colori/pixel, superficie e parametri
   SuperFlex, RGB/maschera, camera e indice di provenienza. Non sono 8126 frame
   distinti. Il numero esatto di frame e nel geometry_receipt.json verificato.

La geometria consegnata è DA **grezza**, non un insieme dichiarato interamente
allineato alla scena. E sufficiente per sperimentare il confronto di forma e la
correzione del matching. La memoria accumulata del punto 3 è una rappresentazione
distinta: il suo export verificato su 446 osservazioni non va spacciato per
memoria accumulata pronta su tutte le 8126.

## Avvio

Su Linux con Python 3.11 disponibile, oppure in un ambiente gia usato per
Whareformer:

```bash
bash setup.sh
.venv/bin/python verify_delivery.py
```

Per i comandi successivi fissare anche i thread di calcolo:

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
```

`bash check.sh` esegue controlli dei checksum, test del lettore e verifica degli
esempi eventualmente gia inclusi. Per un'installazione solo CPU si puo installare
prima `torch==2.6.0` dall'indice ufficiale `https://download.pytorch.org/whl/cpu`.

Le versioni sono fissate per l'ambiente proposto; le verifiche locali possono
usare un'altra versione di Torch. Non e garantita uguaglianza bit per bit su
qualsiasi sistema. In Windows usare un ambiente Python compatibile e gli stessi
comandi senza il prefisso `.venv/bin/`.

Se le geometrie sono fornite ancora nell'archivio originale:

```bash
.venv/bin/python finalize_p01_correction.py /percorso/geometry_received.tar.gz --root .
.venv/bin/python p01_correction_data.py verify-geometry --geometry data/geometry
```

L'importazione rifiuta sovrascritture, percorsi fuori dalla cartella, checksum
errati e conteggi diversi da 8126. Conservare gli archivi originali fino alla
verifica del destinatario. Non caricare in Git le cartelle dati/checkpoint.

## Preparare gli esempi per la correzione

```bash
.venv/bin/python p01_correction_data.py build --root . --geometry data/geometry --examples data/examples
.venv/bin/python p01_correction_data.py logits --root . --examples data/examples
.venv/bin/python verify_p01_correction_examples.py --root . --geometry data/geometry --examples data/examples
```

Il primo comando ripercorre **tutta** la storia del video con tracker, DenStream,
memorie d'aspetto/posizione e oracle degli autori. Esporta solo le osservazioni
con geometria disponibile, mantenendo il contesto dei frame senza geometria.
Ogni esempio contiene:

- input originale `(1+T,259)`: prima la query, poi T candidate, 256 dimensioni
  d'aspetto e tre di posizione, nello stesso ordine del modello;
- target one-hot: classe 0 Nuova track, classi 1..T candidate;
- chiavi di geometria della query e di tutte le viste precedenti per candidata.

Le geometrie precedenti sono indicizzate in modo compatto con prefissi per
traccia: nessuna copia quadratica delle liste, nessuna nuova politica di fusione.
Tutte le detection di un frame vedono solo geometrie di frame **precedenti**.
Target e identita oracle sono supervisione, non ingressi del modello operativo.
I nomi seguono il benchmark: non sono nuove identita fisiche certificate.

Il secondo comando calcola i logits del checkpoint Whareformer originale in
modalita eval congelata, sugli input oracle supervisionati. Questo e un dataset
di sviluppo, **non** un replay di tracking libero: dopo il training della
correzione bisogna valutarla nel tracker con le sue associazioni predette.

Il pacchetto completo include esempi/logits gia calcolati e verificati:
leggerli direttamente, senza rigenerarli o sovrascriverli. I comandi sopra servono
per riprodurli in una cartella nuova. La verifica estesa confronta anche tutti
i 446 esempi storici, input numerici e target, senza limitarsi al conteggio.

## Dal codice del collega

```python
from p01_correction_data import CorrectionData
data = CorrectionData('.', 'data/geometry', 'data/examples')
sample = data.example('P01_01/frame_0000002893__d0')
x = sample['numerical_input']
y = sample['label']
query = sample['query']
candidate_views = sample['candidate_views']
data.close()
```

`data.geometry_features(chiave, kind="surface")` applica gli estrattori D2 e
spettro gia usati dal progetto (campionamento 1024 punti, seed fissato). Usare
`kind="points"` per la superficie osservata. Restituisce punti normalizzati,
D2 e spettro; non sceglie quali viste della candidata confrontare o fondere.
Il campionamento serve al descrittore: i punti originali rimangono integri.

Ogni geometria indica percorsi relativi e SHA-256 di points.npz,
shape_parameters.npz e reconstruction.ply. I punti osservati sono in coordinate
camera X destra/Y basso/Z avanti; la scala stimata non certifica accuratezza
metrica. La mesh SuperFlex completa la forma e non sostituisce i punti osservati.
Le trasformazioni camera sono conservate. Alias temporali VISOR/RGB espliciti:
non affermare identita con il JPEG delle feature ufficiali per i casi con alias.

`p01_correction_hook.apply_correction` e il contratto minimo di integrazione:
logits originali + correzione esterna sulle sole classi con geometria disponibile.
Peso zero restituisce gli stessi logits; geometria mancante significa contributo
neutro, non distanza zero favorevole. Non e una scelta di architettura o training:
il collega puo apprendere il modulo concordato partendo da questi input/target.

Il riferimento `data/reference446/` permette di confrontare gli input e i target
gia validati con quelli ricostruiti. Il vecchio campione non conteneva Nuova track;
non eliminare gli eventuali nuovi casi dall'insieme esteso.

## Come condividerlo

Codice, questa guida, configurazione di installazione e manifest degli archivi
vanno nella repo comune, per esempio `tools/p01_01_correction/`. Input, geometrie,
checkpoint e archivi completi restano fuori dalla storia Git (gia ignorati).
Condividere i dati con cartella Drive/OneDrive ad accesso limitato al gruppo e
inserire nella guida della repo link, versione e SHA-256. Alternativa: asset di
una release GitHub per parti sotto 2 GiB, se il perimetro di accesso e adeguato.
Nessun upload, push o cambio delle autorizzazioni avviene automaticamente.

Rispettare le condizioni originali EPIC-KITCHENS/VISOR, dei dati Whareformer e
dei checkpoint. Non rendere pubblici i dati solo perche il codice e su GitHub.
Separazione training/calibrazione/test ancora da fissare: non usare le stesse
osservazioni per apprendere e dichiarare prestazioni indipendenti.
