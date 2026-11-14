# Collegamento riutilizzabile Whareformer–geometria — 14 novembre 2026

## Risultato del punto 1

Implementati `integration_prototype/geometry_matcher.py` e configurazione JSON di esempio. Il componente avvolge un matcher Whareformer già costruito, senza ricaricare pesi o copiare inferenza, softmax e assegnazione. Un hook temporaneo sull'output della rete applica l'adattatore esistente prima della softmax originale. L'hook viene rimosso anche in caso di errore.

Modalità: `disabled` delega direttamente senza input geometrico; `diagnostic` misura le distanze e aggiorna la memoria dopo commit senza alterare i punteggi; `active` applica il contributo configurato. In diagnostica e in active con peso zero viene restituito lo stesso oggetto tensor originale, evitando conversioni numeriche nel percorso della baseline. New Track non riceve correzione diretta; la sua probabilità può cambiare per normalizzazione in active non nullo.

Quattro rappresentazioni ammesse: `da_raw_points`, `da_raw_superflex`, `moge_points`, `moge_superflex`. Capacità, metrica D2/spettro, aggregazione, peso e distanza neutra sono configurabili e serializzabili. I valori dell'esempio servono a usare l'interfaccia e non costituiscono calibrazione scientifica. Le feature devono essere preestratte dalla rappresentazione dichiarata: il wrapper non ne verifica autonomamente il file/hash; il caricatore e il manifest del runner conservano questa responsabilità.

## Utilizzo e confini

Creare un'istanza per video, con un modello non condiviso fra esecuzioni concorrenti. Per ogni frame abilitato: `set_frame(frame_index, observation_keys, features)` nell'ordine reale delle detection; `tracker.update(...)`; poi `commit` con chiavi di osservazione e ID effettivi delle track aggiornate/create. Le colonne vengono ricavate nell'ordine delle track passate al matcher, mai ordinate per ID. Per una nuova sequenza creare un nuovo wrapper e un nuovo tracker.

Il componente richiede il matcher originale con un solo forward del modello per chiamata quando esistono track; senza track conserva il ritorno anticipato originale e inizializza solo la transazione geometrica. I controlli di contesto/ripetizione e il commit impediscono un secondo confronto prima della chiusura del frame. `abort` annulla solo la transazione geometrica, non esegue rollback del tracker originale: coordinamento completo e gestione delle eccezioni di tracker sono materia del punto 2. Non sono implementati qui registrazione, accumulo o nuova inferenza SuperFlex.

`run_real_prefix.py` ora usa il componente comune al posto della classe locale duplicata; conserva intenzionalmente il controllo a peso zero e gli assert baseline. Ogni copia committa le proprie associazioni. La preparazione include il nuovo modulo e l'output del runner ne registra hash/configurazione. Non modificati bundle o risultati storici; il runner aggiornato non è stato eseguito su HPC in questa fase.

## Verifiche effettive e limiti

Passati **16 test locali**: sette dell'adattatore esistente (inclusi 120 casi controllati a peso zero) e nove del nuovo wrapper. Verificate delega disattivata, diagnostica e zero per tutte le quattro rappresentazioni, modifica attiva dell'assegnazione in un caso controllato, New Track e input preservati, ordine righe/colonne, geometria mancante, primo frame senza track, validazione configurazione, commit e pulizia su errori.

I nuovi test compilano i metodi match/greedy/validazione dal sorgente originale, usando un modello e un oggetto tensor controllati NumPy. Non sono un test PyTorch, un'inferenza neurale o una misura di tracking. Esiti e hash in `outputs/reusable_integration_20261114/verification.json`. Controllata inoltre la sintassi dei quattro Python interessati e la validità della configurazione JSON. Nessun job, tentativo di accesso HPC, training o push.

**Chiusura:** punto 1 completato come sviluppo software e contratto locale; verifica dell'hook con Torch/checkpoint reale rinviata. Prossimo lavoro: punto 2, coordinatore causale che colleghi il matcher alla memoria/versioni e ai candidati di aggiornamento geometrico. Restano invariati i risultati 2B (0/12 aggiornamenti reali ammessi) e gli esiti HPC pendenti.
