# Roadmap operativa — progetto Computer Vision

**Condivisione conclusa, 11 novembre:** codice riusabile e memoria scientifica pubblicati su un ramo dedicato della repository comune; verifica di riservatezza e stato remoto in `STATO_LAVORO.md`. La pubblicazione non aggiunge evidenze scientifiche né modifica i prossimi passi approvati.

**Condivisione verificata, 11 novembre:** remoto comune collegato; prima di pubblicare, preparato un ramo separato con dieci file di utilità geometrica/analisi, testati contro gli output esistenti. Nessun upload, nuovo job o avanzamento del matcher. Dettagli `REVISIONE_CODICE_REPOSITORY.md`; gli esperimenti e i loro limiti restano quelli già registrati.

**Coordinamento dell'11 novembre:** usare la repository comune, senza predisporre un secondo remoto. Specifica tecnica per il collegamento delle osservazioni in `docs/INPUT_SUPERFLEX_PER_WHAREFORMER.md`: nuvola di superficie per oggetto distinta dalla posizione XYZ del tracker. Export e mapping alle detection reali restano da verificare; nessuna nuova inferenza.

**Passaggio organizzativo richiesto da Marco, 10 novembre:** prima dello scambio di asset con il collega, predisporre repository GitHub privata con inventario comprensibile del codice, risultati numerici essenziali e pacchetti dati esterni. Guide `docs/CODICE_PRODOTTO.md` e `docs/CONDIVISIONE.md`. Non è una nuova fase sperimentale né certifica la baseline del collega: prepara il collegamento previsto dal piano corrente.

**Direzione confermata da Marco, 10 novembre:** proseguire DA/MoGE in parallelo fino a convenienza chiara. Il primo test d'identità fa avanzare la verifica del segnale (fase 3 del piano storico), senza superarne ancora il criterio di validazione: campione limitato, metrica/memoria aperte, beneficio tracking assente. Raccordo osservazioni/identità con la baseline ancora parziale. Prossimi passi: ampliare/rafforzare identità entro categoria e collegare detection/feature/XYZ; preparare una sola interfaccia con sorgente configurabile, poi validare distanza/memoria e prototipo per entrambi. Mantenere il controllo sui punti. Decisione finale basata su utilità, affidabilità e costo, non sull'IoU 2D soltanto; nessuna necessità di scegliere una sorgente prima di preparare l'integrazione. Nessuna nuova esecuzione in questo chiarimento.

**Verifica conclusiva, 10 novembre, prevale sullo stato di avvio sotto:** 750536 COMPLETED/0:0 in 47m26s, 8797 coppie e analisi descrittiva recuperate/verificate. Nessun job attivo e nessun precalcolo da rilanciare. Risultati `RISULTATI_IDENTITA_DA_MOGE.md`: mantenere DA/MoGE e controllo sui punti, nessun vincitore generale. Prossimo passo: rafforzare/ampliare identità entro categoria e collegare le detection baseline, riusando le distanze esistenti.

**Ricognizione robotica successiva, sessione avviata il 9 novembre:** `RICOGNIZIONE_MEMORIA_GEOMETRICA_ROBOTICA.md` confronta i precedenti e propone un test circoscritto qualità–memoria–costo. Non cambia domanda, dataset, ruoli o priorità approvate. Un'eventuale validazione geometrica con GT indipendente richiede scelta separata di Marco; nessuna estensione robotica completa implicitamente aggiunta alla consegna.

**Aggiornamento operativo, 10 novembre:** esperimento appaiato DA/MoGE avviato sulle ricostruzioni esistenti: punti/SuperFlex, 8797 coppie. Preparazione e pilota conclusi; job CPU 750536 ancora RUNNING all'ultima verifica, controllarlo senza duplicarlo. Primo campione visivo 37 osservazioni/sette identità, non certificazione persistente; restano ampliamento dei negativi entro categoria e collegamento alle detection baseline. Protocollo e limiti in `ESPERIMENTO_IDENTITA_DA_MOGE.md`, stato/log in `STATO_LAVORO.md`. Nessun beneficio d'identità o tracking ancora concluso.

**Passaggio alla prossima chat, 9 novembre:** obiettivo scientifico invariato e nessuna nuova fase approvata. Primo lavoro: verificare asset/corrispondenze e preparare osservazioni con identità fisiche controllate, poi valutare stabilità/discriminatività contro geometria semplice. Comprensione DA/MoGE, camera e interpretazione del test documentate in `COMPRENSIONE_DA_MOGE_SUPERFLEX.md`; confronto con camera nota per MoGE solo eventuale diagnostica, non prerequisito. Seguire `TODO.md`.
**Avanzamento corrente:** confronto 200 nuove immagini/cinque video concluso, 299 osservazioni e 890 mesh; esito in `RISULTATI_CONFRONTO_200.md`. DA grezzo raccomandato per il primo prototipo sulla base del vantaggio modesto di compatibilità 2D, non come scelta definitiva approvata né prova di accuratezza 3D. Seguono corrispondenze e identità/stabilità/discriminatività; baseline e interfaccia del collega da verificare. Non ripetere i test conclusi.

**Esito successivo del 9 novembre:** su richiesta di Marco, completato confronto esteso di 16 nuovi frame, 27 oggetti/11 categorie e 81 ricostruzioni con DA grezzo/allineato e MoGE. Nessun vantaggio visivo sistematico MoGE; alcune forme semplici riconoscibili. Dettagli `CONFRONTO_GEOMETRIA_ESTESO.md`. Prossimo passo: corrispondenze e identità verificate; nessuna scelta definitiva della sorgente geometrica.

**Ultimo aggiornamento del 9 novembre:** piano corrente in [TODO.md](TODO.md). Controllo MoGE-2 + VISOR → robust completato e ispezionato, senza miglioramento visivo sistematico (`VERIFICA_MOGE2_749539.md`); XYZ Whareformer invariati. Prossimo passo: corrispondenze e campione con identità verificate per stabilità/discriminatività, poi confronto/memoria e valutazione nel tracker. Baseline/interfaccia in parallelo; SAM3 opzionale. La sequenza datata sotto è il piano iniziale storico, non nuove scadenze concordate. Stato in `STATO_LAVORO.md`.

Stato: **piano di lavoro, 4 novembre 2026**. Marco ha approvato la domanda di ricerca riportata in `FASE_0.md` ed EPIC-KITCHENS come base comune degli esperimenti, con sviluppo e test finale separati. Metodo e protocollo dettagliato restano da decidere dopo le verifiche iniziali. Scadenza confermata da Marco: **23 novembre 2026**. Le date di presentazione (24 novembre) e poster (1 dicembre) nei materiali del corso sono provvisorie.

## Obiettivo e ipotesi di partenza

Studiare se una memoria esplicita della forma 3D degli oggetti, ottenuta con SuperFlex, aiuta Whareformer ad associare le osservazioni alle identità corrette nei video egocentrici. L'ipotesi **non è ancora verificata**. La forma è un segnale aggiuntivo rispetto a descrittori DINOv2 e posizione 3D; non sostituisce automaticamente il punto di localizzazione.

Le due condizioni decisive sono:

1. Ottenere dalle osservazioni del benchmark nuvole di punti degli oggetti abbastanza affidabili per SuperFlex.
2. Dimostrare che la forma stimata aggiunge informazione per l'identità oltre ad aspetto e posizione già usati da Whareformer.

## Sequenza di lavoro

| Quando | Fase | Attività e risultato verificabile | Decisione |
|---|---|---|---|
| **4–5 nov** | 0. Definire il perimetro | Verificare numero di studenti, consegna e scadenze effettive, accesso a GPU/dati; creare e mantenere il repository Git richiesto dal corso. Scrivere una domanda candidata, ipotesi falsificabile, letteratura più vicina e tabella dei confronti necessari. Separare ciò che è noto da ciò che va misurato. | Marco approva la domanda candidata e il dataset pilota; il metodo resta aperto. |
| **6–8 nov** | 1. Riprodurre i componenti | Far girare Whareformer con checkpoint/evaluator ufficiali su pochi video; registrare versione del codice, configurazione, split e risultati. In parallelo eseguire SuperFlex *robust* su esempi forniti dagli autori. Verificare nel codice la strategia di risoluzione dei conflitti di Whareformer. | Sapere se pipeline, checkpoint, dati e hardware sono realmente utilizzabili. |
| **8–11 nov** | 2. Costruire gli input 3D | Su un piccolo campione di osservazioni reali: RGB + maschera + profondità per pixel + intrinseci → nuvola di punti parziale per oggetto. Controllare allineamento, scala, coordinate, bordi e superfici visibili. Salvare esempi di oggetti piccoli, occlusi e ripresi da più viste. | **Gate 1:** se i punti non sono affidabili, correggere l'input o restringere il caso di studio prima di integrare il tracker. |
| **11–13 nov** | 3. Testare il segnale di forma | Applicare SuperFlex alle nuvole del pilota. Confrontare ripetizioni dello stesso oggetto e oggetti diversi, anche simili; valutare stabilità fra viste, qualità con occlusioni e costo. Confrontare con geometria semplice (p.es. estensioni 3D) e con i segnali già disponibili. | **Gate 2:** fissare con Marco domanda finale, protocollo, rappresentazione/confronto delle forme e regola minima di aggiornamento della memoria. Se la forma non è discriminativa, studiare e documentare quel limite invece di assumere un guadagno. |
| **14–17 nov** | 4. Integrare il metodo minimo | Aggiungere alla track una memoria della forma e un termine di similarità geometrica per l'associazione. Partire da un aggiornamento semplice e controllabile; addestrare/calibrare soltanto sui dati consentiti dal protocollo. Mantenere maschere, feature visive, posizioni 3D e split identici nei confronti. | Versione eseguibile con configurazioni registrate, senza modificare il test in base ai primi risultati. |
| **18–20 nov** | 5. Valutare | Confrontare Whareformer originale, geometria semplice e SuperFlex a parità di input e procedura. Misurare soprattutto **IDF1**; riportare anche **mPCL** e costo dell'intera pipeline. Analizzare errori di associazione, occlusioni, oggetti simili e stabilità dei risultati in modo proporzionato al campione. | Concludere solo ciò che i dati sostengono, incluso un eventuale risultato negativo. |
| **21–23 nov** | 6. Comunicare | Chiudere report, figure, tabelle, limiti, riproducibilità e presentazione. Il poster può essere rifinito in vista della sessione indicata provvisoriamente per il 1 dicembre, dopo aver confermato il calendario. | Consegna entro la scadenza effettiva. |

La scrittura del report comincia già nella fase 0: introduzione, related work e metodo vengono aggiornati mentre maturano le evidenze, così gli ultimi giorni restano per risultati e revisione.

### Avanzamento fase 0 — 4 novembre 2026

Istruttoria in [FASE_0.md](FASE_0.md): **domanda ed EPIC-KITCHENS approvati**, ipotesi falsificabili, pilota proposto nel train, confronti e registro delle verifiche. Il confronto geometrico usa forme SuperFlex sia per l'osservazione corrente sia per la memoria delle track. Marco ha confermato **due componenti, scadenza del 23 novembre e accesso alle GPU Bocconi**; ha riportato nodi con A100 da 80 GB. Repository locale predisposto; Marco creerà quello condiviso. **Fase ancora aperta per i dettagli operativi:** consegna, eccezione al gruppo di tre previsto dal syllabus, limiti HPC e campione pilota. Nessun modello eseguito; metodo e protocollo dettagliato non ancora fissati.

## Controlli sperimentali indispensabili

Preparazione della fase 1 avviata il 4 novembre: [PRIMA_ESECUZIONE.md](PRIMA_ESECUZIONE.md) descrive la prima prova senza training; `scripts/prepare_baseline.py` controlla input e genera la configurazione di un singolo video del train. Confermati nell'ispezione locale matcher greedy e nome `object_annotations.json`. Restano necessari accesso concreto al cluster, download degli asset e installazione dell'ambiente; nessuna inferenza è stata eseguita.

Archivio ufficiale fornito da Marco in `Whareformer-repo/`: verificati tutti i 75 file rispetto agli hash dell'inventario GitHub già salvato per il commit fissato. CSV dei video già incluso. Feature per osservazione e checkpoint ancora da ottenere; manifest della verifica in `manifests/whareformer_archive.json`.

- Stesse osservazioni, maschere, feature DINOv2, posizioni 3D, split ed evaluator per i sistemi confrontati.
- Separazione fra dati usati per sviluppo/calibrazione e test. Niente scelta dei pesi sul test.
- Una baseline geometrica semplice, ottenuta dagli stessi input, per verificare se SuperFlex apporta qualcosa oltre a una misura grossolana della forma.
- IDF1 per l'associazione; mPCL per la localizzazione. Una forma ricostruita meglio non implica automaticamente un tracking migliore.
- Registrare versione del codice, checkpoint, configurazioni, provenienza dei dati, tempo di estrazione della geometria e di inferenza.

## Organizzazione del gruppo

**Avanzamento persona B, 7 novembre:** installazione SuperFlex robust e prima inferenza sull'esempio lamp.ply riuscite nel job HPC 744144, secondo il log condiviso; 7 primitive attive. File da recuperare e controllo visivo ancora pendente. Nessun esperimento EPIC o miglioramento di tracking misurato. Dettagli in `PRIMA_ESECUZIONE_SUPERFLEX.md` e stato corrente in `STATO_LAVORO.md`.

La tabella sintetica è in [roadmap separata per ruolo.md](<roadmap separata per ruolo.md>): **ruoli confermati il 7 novembre**, dettagli e date intermedie ancora da discutere. Per il punto di ripresa aggiornato vedere [STATO_LAVORO.md](STATO_LAVORO.md). Il completamento dei download Whareformer non è ancora verificato. Installazione ed esecuzione dei modelli avverranno sull'HPC Bocconi.

Il gruppo è di **due persone**. Assegnazione confermata da Marco il 7 novembre: **Marco segue dati/geometria e SuperFlex (persona B); l'altro membro segue Whareformer, integrazione e valutazione (persona A)**. Report e revisione degli esperimenti sono condivisi. Ciascuno deve capire la pipeline completa. Fare un breve controllo quotidiano su risultato, blocco, prossima prova e decisione necessaria. Limitare inizialmente il lavoro a un dataset, una variante minima di memoria e i tre confronti principali. Il syllabus parla di gruppi di tre: l'eventuale autorizzazione al gruppo di due resta da verificare con il corso.

## Fuori dallo scope iniziale

Reasoning semantico aggiuntivo sullo stato dell'oggetto, training da zero di SuperFlex, memoria geometrica complessa e validazione su robot. Si considerano solo dopo che le due verifiche decisive e i confronti principali sono stati completati.

## Materiali di continuità

- `Starting_point.md`: obiettivo e vincoli concordati.
- `LETTURA_E_BASE_SCIENTIFICA.md`: lettura dei paper, evidenze e questioni tecniche.
- `ISTRUZIONI_SUPERVISORE_SCIENTIFICO.md`: metodo di collaborazione e standard scientifici.
- Questa roadmap: stato operativo; aggiornarla dopo ogni gate e decisione di Marco.
