# Coordinatore causale del frame — 14 novembre 2026

## Implementazione e comportamento

Implementato `integration_prototype/frame_coordinator.py`, con `FrameCoordinator`, `UpdateContext` e `GeometryDecision`. Riceve un tracker nuovo con il wrapper geometrico e lo possiede per una sequenza. Non ricopia Whareformer e non usa nomi di oggetto o identità GT per associare.

Per ogni frame:

1. Valida ordine temporale strettamente crescente, chiavi osservazione, indici/frame delle detection e corrispondenza dei dati geometrici.
2. Apre una sola transazione geometrica e chiama il tracker originale: tutte le detection interrogano la stessa memoria precedente.
3. Ricava le associazioni dagli incrementi effettivi delle history, inclusi i nuovi ID. Non usa soltanto `time_since_update==0`, non forza l'export del collega. Verifica copertura completa e associazioni uno-a-uno.
4. Committa le forme separate secondo queste associazioni. Una forma mancante non cancella quelle valide. Registra versione, osservazione e frame dell'ultimo aggiornamento per track.
5. Se configurato, invoca un aggiornatore geometrico puro per ciascuna osservazione con input disponibile. Ogni proposta riceve una copia dello stato precedente; le proposte accettate diventano visibili insieme dopo la loro valutazione. Rifiuto, errore o input mancante lasciano invariato il precedente stato geometrico valido.

Memoria delle forme separate e stato geometrico opzionale hanno versioni distinte: accettare una nuova forma osservata non implica accettare una fusione dei punti. Il valore generico dell'aggiornatore non sostituisce automaticamente il descrittore usato dal matcher. La provenienza contenuta nel payload deve essere fornita/validata dal futuro aggiornatore; il coordinatore ne garantisce passaggio e isolamento, non la correttezza fisica.

`snapshot` e risultati prima/dopo sono copie, per evitare modifiche retroattive dall'esterno. Il risultato include associazioni e stato di ciascuna proposta (`not_requested`, `missing`, `accepted`, `rejected`, `error`). Nessun salvataggio/ripristino persistente implementato qui: gli snapshot sono diagnostici in memoria, non checkpoint completi del tracker.

## Fallimenti e frame vuoti

Un errore del nucleo tracker/commit blocca il coordinatore: annullare la transazione geometrica non annulla mutazioni già avvenute in Whareformer. Non è permesso proseguire o riprovare su quella istanza; occorre ricostruire e ripercorrere la sequenza. Nessun rollback completo promesso. Gli errori del solo aggiornatore sono invece registrati per osservazione e preservano lo stato precedente, senza riscrivere l'associazione.

Per frame senza detection si aggiornano soltanto le età delle track e l'avanzamento temporale, conservando la geometria. Aggiunto percorso vuoto esplicito nel wrapper geometrico abilitato; in modalità disattivata il coordinatore aggiorna le età senza invocare la costruzione di input del modello originale, che presuppone detection presenti. Nessuna inferenza necessaria. Il coordinatore rifiuta elaborazione rientrante; uso previsto seriale.

## Collegamento e verifiche

`run_real_prefix.py` ora usa un coordinatore per variante e registra le versioni prima/dopo nei frame diagnostici; il preparatore include il nuovo modulo nei futuri bundle e il runner ne registra l'hash. Pacchetti e output storici non modificati. Nessuna run reale ripetuta.

**27 test locali superati:** 7 adapter, 9 wrapper e 11 nuovi coordinatore. Controllati ID reali nuovi, lettura comune dello stato precedente, callback solo dopo tutte le associazioni, isolamento delle proposte, versioni, mancanti/rifiuti/errori, frame vuoti nelle tre modalità, ordine temporale, associazione corrotta, blocco dopo errore del tracker e impossibilità di cambiare risultati passati con input futuri. Test compilano i metodi originali del tracker e matcher, usando track/modello/tensor controllati NumPy. Non costituiscono verifica Torch/checkpoint o efficacia reale.

Log, esito e hash: `outputs/frame_coordinator_20261114/tests.txt` e `verification.json`. Verificata sintassi dei cinque Python modificati/aggiunti. Nessun accesso HPC, nuovo esperimento, training o push.

## Stato e dipendenze successive

Coordinamento del frame completato come componente software verificato localmente. Nel runner corrente l'aggiornatore opzionale non è collegato: aggiorna solo forme separate. Prossimo lavoro: collegare esplicitamente il candidato esistente di registrazione/accumulo all'interfaccia di proposta, poi l'inferenza SuperFlex differita con corrispondenza di versione/provenienza. Non introdotti nuovo metodo o soglie scientifiche. Nessuna fusione reale certificata: resta 0/12 aggiornamenti reali ammessi nei piloti 2B. Esiti HPC 761899/761905 ancora da recuperare.
