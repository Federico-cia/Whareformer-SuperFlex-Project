# Sviluppo senza HPC — 14 novembre 2026

## Valutatore e comando unico collegati — 14 novembre

Implementati export delle osservazioni/assegnazioni con hash, IDF1/mPCL originali con scope esplicito e comando input preparati → varianti → valutazione → tabella. 763498 COMPLETED/0:0 (33 s), otto test; 763530 COMPLETED/0:0 (45 s), 69 test tutti eseguiti, riprodotti IDF1 73.269735% e mPCL 70.465504% su predizioni registrate train. 763531 RUNNING a 10m50s nell’ultima osservazione: nove configurazioni zero, CPU e cache esistente; esito ancora da acquisire. [COMPLETAMENTO_PIPELINE_20261114.md](COMPLETAMENTO_PIPELINE_20261114.md).

**GPU concluso:** 763324 COMPLETED/0:0 (43m30s), sei ricostruzioni reali ready e controllo zero esatto, ma nessuna fusione multivista ammessa. Filtri invariati e revisione ancora rinviata. Mancano unificazione del frontend dati, copertura sufficiente e calibrazione/test; il comando attuale parte da input preparati. Le precedenti note di metriche non collegate e GPU ancora attivo sono storiche.

## Runner comune e misure implementati — 14 novembre

Disponibili W0/G0/S-separata/S-accumulo/P-accumulo, DA/MoGE, memorie e modelli indipendenti, controllo sui punti ammessi e report JSONL/JSON/CSV con copertura, fallimenti, byte di payload e costi dei replay. 58 test locali superati; esempio a peso zero, tracking metrics ancora non calcolate. Nessuna nuova run reale del runner comune né modifica dei job esistenti. [RUNNER_VARIANTI_20261114.md](RUNNER_VARIANTI_20261114.md). Prossimo: collegare valutatore tracking e protocollo/copertura di calibrazione-test.

**HPC verificato durante il lavoro:** 763322 COMPLETED/0:0 (9m56s), 763323 COMPLETED/0:0 (12m11s), zero esatto; nel secondo solo 12 inizializzazioni e 12 rifiuti, nessuna fusione, conteggi sulle quattro rappresentazioni. 763324 RUNNING a 29m19s con almeno un risultato neurale reale ready; esito complessivo ancora da acquisire. [Dettagli HPC](RIPRESA_HPC_20261114.md). Le indicazioni precedenti di job CPU attivi/GPU in attesa sono storiche.

**Stato del documento:** piano storico della fase senza HPC, conservato per i criteri software. Dopo la ripresa HPC e l'approvazione della selezione/calibrazione autonome, sequenza e priorità correnti sono in [ROADMAP_CICLO_GEOMETRICO.md](ROADMAP_CICLO_GEOMETRICO.md); le note sotto su esiti da recuperare e calibrazione ancora da approvare non sono lo stato attuale.

## HPC ripristinato, arretrati inviati — 14 novembre

SSH/accounting/coda accessibili. Recuperati 761899 (prefisso storico a peso zero esatto, 3398 frame/10264 detection, zero differenze dal collega) e 761905 (IDF1 73.2697% sulle predizioni registrate train, non test). Nuovi job: 763321 COMPLETED/0:0, 50 test ambiente passati; 763322 replica aggiornata e 763323 accumulo RUNNING nell’ultima osservazione; 763324 SuperFlex differita PENDING per dipendenza dai due CPU. Nessun nuovo esito sperimentale ancora dichiarato; prossima acquisizione dei risultati. [RIPRESA_HPC_20261114.md](RIPRESA_HPC_20261114.md). Le note precedenti sul blocco DNS e sui due esiti ancora da leggere sono storiche.

**Avanzamento SuperFlex:** interfaccia differita e ritorno alla memoria futura collegati, 43 controlli locali; worker GPU non eseguito. Prossimi punti 4–5 per varianti e misure. [SUPERFLEX_DIFFERITA_20261114.md](SUPERFLEX_DIFFERITA_20261114.md).

**Avanzamento accumulo:** candidato collegato al coordinatore e modalità runner predisposta; 35 test locali, nessuna nuova validazione reale. Prossimo: interfaccia SuperFlex differita. [COLLEGAMENTO_ACCUMULO_20261114.md](COLLEGAMENTO_ACCUMULO_20261114.md).

**Avanzamento del coordinatore:** implementazione e controlli locali completati; resta il collegamento del candidato di accumulo e successivamente SuperFlex differita. [COORDINATORE_FRAME_20261114.md](COORDINATORE_FRAME_20261114.md). Le voci numerate sotto restano i criteri del piano.

**Avanzamento:** punto 1 completato come sviluppo e contratto locale (16 test); conferma Torch/frame reali rinviata. Prossimo punto 2. [INTEGRAZIONE_RIUTILIZZABILE_20261114.md](INTEGRAZIONE_RIUTILIZZABILE_20261114.md).

## Mandato e perimetro

Marco dispone di proseguire lo sviluppo e rimandare gli esperimenti, poiché oggi HPC non disponibile. Sospesi i tentativi di accesso come attività prioritaria. Non cambia la domanda sul tracking o il ciclo unitario approvato; non sono adottati nuovi split, soglie o metodi di registrazione. Questo piano ordina il lavoro da fare, non descrive componenti già completati.

Disponibili adattatore logits/memoria, registrazione/accumulo candidati, asset originali verificati e runner a peso zero. Esiti HPC 761899/761905 ancora da recuperare; 2B non validato (0/12 aggiornamenti reali ammessi). Non attendere questi esiti per costruire le interfacce; restano necessari prima di rivendicare equivalenza reale o beneficio.

## Sequenza operativa

1. **Unificare il collegamento Whareformer–geometria.** Estrarre dal runner diagnostico un componente riutilizzabile con configurazione per modalità disattivata/diagnostica/contributo attivo, sorgente DA/MoGE e rappresentazione punti/SuperFlex. Conservare ordine detection/track e New Track; peso zero deve preservare esattamente il calcolo baseline. Nessun peso non nullo scelto come scientificamente valido. Uscita: integrazione richiamabile dal runner senza duplicare il tracker per ogni variante.

2. **Implementare il coordinatore causale del frame.** Stato precedente comune a tutte le detection; confronto, associazione, poi aggiornamento di forme separate oppure proposta di registrazione/accumulo. Stato geometrico con versione, trasformazioni/provenienza e ultima forma valida. Un aggiornamento rifiutato o una ricostruzione fallita non cancella quella forma; nessuna riscrittura retroattiva delle associazioni. Tenere espliciti nuvola aggiornata e versione dei punti da cui deriva la forma corrente. Uscita: percorso completo verificabile localmente, con inizializzazione/reset e mancanti gestiti.

3. **Preparare l'interfaccia di ricostruzione SuperFlex differita.** Riusare il nucleo esistente; esportare richieste con punti osservati, hash/versione, normalizzazione inversa e configurazione. Importare soltanto risultati con provenienza corrispondente; completamenti predetti esclusi dall'accumulo osservato. In locale un sostituto controllato verifica il flusso, senza essere una vera ricostruzione. Nel replay seriale il frame resta in attesa del risultato necessario, oppure si riparte dallo stato salvato prima dei frame successivi: non inserire oggi una forma calcolata domani fingendo che fosse disponibile ieri. Un'eventuale politica asincrona richiederebbe regole esplicite e valutazione dedicata. Uscita: pacchetto eseguibile su HPC senza ridisegnare il ciclo.

4. **Costruire il runner comune e i controlli locali mirati.** Predisporre le modalità W0, G0, forme separate, SuperFlex su accumulo e controllo punti già previste dalla roadmap. Ogni variante ricostruisce la propria memoria dalle proprie associazioni; associazioni registrate usate soltanto nel diagnostico dichiarato. Controlli nuovi: causalità fra detection/frame, mancanti, rifiuti, errore di associazione e contaminazione osservabile, risultato SuperFlex incompatibile/obsoleto, salvataggio/ripresa. Riutilizzare i test già conclusi. Uscita: esecuzione locale con dati disponibili e sostituti dichiarati; non valutazione di efficacia né correzione automatica di contaminazioni.

5. **Preparare il pacchetto sperimentale e il report.** Configurazioni, inventario input/output, dipendenze isolate, script di lancio/ripresa e aggregatore di metriche/costi/copertura/fallimenti. Predisporre il piano di calibrazione e test separato, lasciando esplicite le scelte ancora da approvare. Tabelle dei risultati vuote dove non misurate. Alla ripresa HPC prima recuperare 761899/761905; poi verifica reale a peso zero e piccolo pilota, quindi eventuale calibrazione e valutazione. Non rigenerare asset esistenti.

## Criterio di completamento della fase software

Ciclo implementato, modalità configurabili, provenienza/versioni verificabili, controlli locali mirati superati e pacchetto eseguibile pronto. Sono esiti diversi da registrazione reale valida, equivalenza sull'intero prefisso e miglioramento tracking: questi restano sperimentali. Nessuna garanzia che la registrazione attuale basti; la sua diagnosi resta una dipendenza scientifica del ramo accumulativo.
