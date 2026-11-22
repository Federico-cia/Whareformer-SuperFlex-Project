# Decisioni vigenti e storia delle revisioni

Consolidamento del 22 novembre 2026. Questo registro contiene le scelte, non il diario dei job. Stato di esecuzione in [STATO_LAVORO](STATO_LAVORO.md); dettagli di metodo nei documenti collegati.

## Storia completa

Le **92 voci numerate** e tutti gli aggiornamenti non numerati del registro precedente sono conservati nel [registro storico integrale](../archive/prima_consolidamento_20261122/REGISTRO_DECISIONI.md). Numeri e date originari restano invariati. L'[indice storico](../archive/prima_consolidamento_20261122/README.md) permette la ricerca per titolo; nessuna scelta precedente è cancellata né trasformata retrospettivamente in risultato.

## D01 — Domanda, confronto e risorse

**Approvato, 4–7 novembre.** Valutare il contributo delle forme SuperFlex al matching Whareformer su EPIC-KITCHENS, a parità degli altri input, con baseline, controllo punti e test separato. Robust preaddestrato come punto di partenza. Motivazione: isolare il contributo della forma entro il budget. Limite: novità generale e beneficio non dimostrati. [Origine: voci 1–4](../archive/prima_consolidamento_20261122/REGISTRO_DECISIONI.md#1-studiare-la-forma-come-informazione-aggiuntiva--confermata-il-4-novembre).

## D02 — Metodo originale, ciclo causale e primi risultati

**Approvato, 13–15 novembre.** Prima verificare il ciclo intero, poi affrontare sistematicamente le criticità; riusare i metodi dei paper applicabili, attribuendo gli adattamenti. Tutte le detection leggono la memoria precedente al frame; aggiornamenti solo dopo l'assegnazione, completamenti disponibili in futuro, conservazione dell'ultimo stato valido sui fallimenti. Prima run e campagna eseguite: integrazione verificata, nessun beneficio tracking. Conseguenza: non equiparare successo software e scientifico. [Prima run](../archive/PRIMA_RUN_COMPLETA_20261114.md), [campagna](../archive/RISULTATI_CAMPAGNA_HPC_20261115.md), [contratto](ROADMAP_CICLO_GEOMETRICO.md).

## D03 — Due integrazioni senza nuove etichette manuali

**Richieste, 16 novembre; scelta finale aperta.** Tentare fusione esterna appresa e adattamento del matcher con geometria, usando input/target originali e memoria strettamente passata. Motivazione: confrontare due modi di impiegare il segnale; track predette non diventano GT. Fine-tuning è raccomandazione, non decisione adottata. [Fattibilità](../archive/FATTIBILITA_DUE_INTEGRAZIONI_20261116.md), [questioni correnti](INTEGRAZIONE_DISCUSSIONE.md).

## D04 — Ruoli, ammissione appresa e revisione della memoria

**Approvato e poi rivisto, 21–22 novembre.** Marco segue punto 3/P01_01, Federico punto 2/P01_02; confronto forme e collocazione seguono. Il rinvio storico dei gate è superato: criterio appreso per conservare viste parziali valide, DA allineata alla scena, forma separata dalla collocazione e fusione anche dopo movimento come obiettivo. Abbandonata la prima vista fissa a favore di punti pesati.

Il 22 novembre autorizzato un prototipo con simulazioni e registrazione per vista, senza certificazione preventiva completa della staticità. La sua riduzione a una sola forma non realizzava il sistema multi-ipotesi originario: ripristino richiesto e autorizzato, poi precisato in D05. Export iniziale/prudente/multi-ipotesi restano confronti storici, non risultati dell'opzione A. Limite: baseline sintetica e test software non validano fusioni reali. [Confronto storico](../archive/CONFRONTO_MEMORIA_ORIGINARIA_20261122.md), [report del prototipo](../archive/REPORT_PUNTO3_20261122.md).

## D05 — Opzione A: stato di posizione distinto dall'ammissione

**Decisione di Marco, 22 novembre, sera.** Uno stato corrisponde a una posizione; criterio C di riproiezione sagoma/spazio libero per assegnare le viste. Una vista respinta dal verificatore rimane nello stato e non ne crea un altro; ritorno in una vecchia posizione apre un nuovo stato perché l'orientamento può cambiare. Nuvole a piena risoluzione; FPS-4096 solo all'ingresso SuperFlex. Motivazione: non scambiare parzialità o fallimento della registrazione per movimento. Limite: occlusioni e profondità condivisa non modellate; impostazioni operative non calibrate. [Metodo e scelte implementative](MEMORIA_OPZIONE_A_E_SELEZIONE_20261122.md).

## D06 — Parametri scelti sul sistema completo

**Decisione di Marco, 22 novembre, sera.** Soglia/margine del criterio C si selezionano con pipeline completa e IDF1/mPCL su P01_01, poi su entrambi i video quando P01_02 disponibile, senza ulteriori procedure approvate. Configurazione iniziale dichiarata per generare i dati del punto 2; un riaddestramento se la scelta cambia molto. Motivazione: utilità dipendente dal consumatore della memoria. Superati budget fisso 5% e utilità prequenziale come criterio finale; quest'ultima resta secondaria, fissata prima. Limiti: punto 2, copertura e costo GPU; P01_01 è sviluppo e il test indipendente resta aperto. [Procedura](MEMORIA_OPZIONE_A_E_SELEZIONE_20261122.md).

## D07 — Sorgenti, allineamento e produzione

**Decisione di Marco, 22 novembre.** DA per copertura completa, MoGE solo campione di confronto; non è superiorità generale dimostrata. P01_01 a Marco, P01_02 a Federico. Forme delle osservazioni calcolate su DA allineata con FPS-4096, come la memoria: alpha/beta cambia le proporzioni, forme su DA grezza solo confronto. Campione MoGE e test finale da definire. [Ruoli](../archive/RUOLI_DA_MOGE_E_CONSEGNA_P01_02_20261122.md), [driver pronto, pilota da validare](../archive/PACCHETTO_HPC_P01_02_20261122.md).

## D08 — Conservazione senza perdita e Drive

**Autorizzato ed eseguito sui blocchi esistenti, 22 novembre.** Rigenerazione CPU dei derivati con checksum originali; successivamente Drive con struttura video → run → tipo, copia/verifica prima del rilascio locale. Motivazione: quota HPC insufficiente alla campagna; mantenere dati e riproducibilità. Regola successiva: salvare alpha/beta e nuvole allineate prima di rilasciare mappe dense; recupero dei primi quattro blocchi ha risolto la violazione involontaria. Estensione automatica del driver ancora da fare. [Compattazione](../archive/COMPATTAZIONE_HPC_20261122.md), [piano Drive](../archive/ARCHIVIAZIONE_DRIVE_PIANO_20261122.md), [guida operativa](../evidence/ASSET_ESTERNI.md#asset-b16d1fb602da).

## D09 — Mappa e pubblicazione

**Approvato/applicato, 21 novembre.** Rami paralleli, 39 nodi/49 collegamenti; nuovi e vecchi commenti confermati, applicati e pubblicati. Nodi descrivono processi, frecce dipendenze; evitare dettagli di singole run nelle schede generali. Proposte di testo nuove richiedono conferma; nessuna autorizzazione automatica per ulteriori modifiche. README unico ingresso, preservare contributi del collega/storia ed escludere dati, pesi e accessi da Git. [Mappa](../../mappa_interattiva/README.md); applicazioni/pubblicazioni nel registro storico (voci 83–92 e successivi aggiornamenti non numerati).

## D10 — Memoria concisa con archivio separato

**Richiesta e attuata, 22 novembre.** Marco chiede di snellire la memoria senza perdere informazioni o storia: stato corrente sostituito in sede, TODO di sole attività aperte, registro di scelte, dettagli nei resoconti e storia nell'archivio. Motivazione: duplicazioni e checklist obsolete ostacolavano la ripresa. Archivio leggibile e originali integri conservati con hash; nessun esperimento o cambio scientifico implicito. [Regole](MANUTENZIONE_MEMORIA.md), [indice e conservazione](../archive/prima_consolidamento_20261122/README.md).

## D11 — Leggibilità della mappa: «less is more»

**Indicazione di Marco, 22 novembre.** Privilegiare leggibilità e sintesi nell'aggiornamento della mappa. Preparata una [proposta strutturale](../archive/STRUTTURA_PROPOSTA_MAPPA_20261122.md) che riusa i 39 riquadri e porta i collegamenti a 53; dettagli del ciclo nelle schede. La prima fase era proposta non approvata; successivamente Marco conferma struttura e testi e ne richiede l'applicazione preservando i commenti non modificati. **Esecuzione:** applicati testi/layout con backup, 50 schede conservate e controlli browser/offline; adattata la scheda per finestre strette. [Esito e verifiche](../evidence/map_20261122/ESITO_APPLICAZIONE.md). Nessuna nuova scelta metodologica, esecuzione HPC o pubblicazione GitHub.

## D12 — Copia separata per un aggiornamento pulito della repository

**Richiesta di Marco, 22 novembre.** Preparare sul PC una selezione sensata per il prossimo push. Creata una copia sul main baa2470 verificato, preservando contributi del collega e storia, con codice corrente, mappa, memoria concisa ed evidenze leggere; esclusi dati completi, pesi, accessi, backup e duplicati operativi. Controlli e perimetro nella [preparazione](../evidence/clean_update_20261122/README.md). Dopo la preparazione Marco autorizza commit e push, previa verifica di nuovi aggiornamenti di Federico; main risulta ancora baa2470 al controllo. La selezione non equivale a nuova validazione scientifica.
