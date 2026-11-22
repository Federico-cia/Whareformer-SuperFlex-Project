# Regole di manutenzione della memoria

Richieste da Marco e consolidate il 22 novembre 2026. Valgono insieme agli AGENTS e alle istruzioni scientifiche; il perimetro esplicito di Marco prevale. Conservare solo contenuti scientifici/operativi, mai credenziali o conversazione informale.

## Una sede per ciascuna informazione

| Documento | Contenuto autorevole | Da evitare |
|---|---|---|
| STATO_LAVORO | Fotografia corrente, evidenze essenziali, limiti, job ancora da seguire, prossimo passo | Successione di bollettini e stati superati |
| TODO | Sole attività aperte con ID stabile, dipendenza e responsabile quando noto | Resoconti, checklist duplicate o completate lasciate aperte |
| REGISTRO_DECISIONI | Scelta, stato (proposta/approvata/rivista), data nota, motivo, limite e conseguenza | Log di invii, test e trasferimenti senza decisione |
| Resoconto tecnico | Configurazioni, metodi, job/log/output, hash, prove, esiti/fallimenti e limiti | Copia integrale negli altri file |
| Roadmap e discussione | Dipendenze, contratti e questioni architetturali specifiche | Seconda copia di stato e TODO |
| README e passaggio AI | Orientamento e collegamenti | Cronologia e nuovi riepiloghi numerici |
| Archivio | Versioni storiche e revisioni superate, marcate come tali | Uso come stato corrente o lettura completa a ogni avvio |

## Come aggiornare

1. Aggiornare autonomamente dopo decisioni, risultati, cambi di piano o blocchi rilevanti; toccare **solo i file interessati**, non tutti a ogni messaggio. Nessun aggiornamento senza novità.
2. Modificare la sezione corrente in sede, anziché aggiungere un nuovo blocco sopra. Un esito verificato sostituisce l'attesa in stato/TODO; il passaggio intermedio resta nel resoconto. Non ripetere controlli conclusi.
3. Per una decisione nuova creare una voce breve, con ID stabile e collegamento al dettaglio. Se rivista, esplicitare quale scelta sostituisce e perché; conservare la precedente nell'archivio o nel registro. Mai inventare motivazioni retrospettive, date o risultati del collega.
4. Per i job mantenere in stato ID, ultimo stato/data osservati, percorsi di log/output, verifiche fatte e controllo successivo. I job conclusi passano al resoconto, salvo esito essenziale. RUNNING datato non significa attualmente attivo. Non salvare credenziali.
5. Chiudere o rimuovere dal TODO le attività concluse dopo aver collegato l'evidenza; non mantenere versioni duplicate. Proposte non approvate non diventano incarichi esecutivi. Conservare esplicitamente dipendenze e temi rinviati ancora validi.
6. Quando serve consolidare una storia senza resoconto, archiviarla una volta con indice, data e collegamenti corretti; conservare gli originali prima di riscritture sostanziali. Non creare snapshot completi a ogni aggiornamento ordinario. Identificativi storici e numerazione restano rintracciabili.
7. Aggiornare collegamenti e ancore quando si sposta una sezione. I link generali puntano al documento corrente; quelli a una voce storica puntano all'archivio. Non riscrivere pacchetti di consegna, backup o contenuti scientifici approvati solo per allinearli allo stato.
8. Prima di consegnare, verificare coerenza stato/TODO/decisioni, percorsi e riferimenti modificati, distinguendo verifiche nuove da quelle già riportate. Separare funzionamento software, validità geometrica e beneficio tracking.

## Dimensione e criterio di sintesi

Obiettivi orientativi: stato 1–2 pagine, TODO 1–2 pagine, passaggio AI circa 20–30 righe, singola decisione un paragrafo breve (due se è una revisione sostanziale). Il registro può crescere con **vere decisioni**, consultando solo la sintesi vigente e le revisioni pertinenti. Se una sezione supera questi limiti, spostare il dettaglio nel resoconto e collegarlo; non tagliare limiti scientifici o dipendenze per rispettare una quota rigida.

Controllo pratico: una nuova chat deve capire cosa è valido, cosa manca e dove riprendere senza ricostruire la cronologia. Le evidenze necessarie a riproducibilità e storia devono rimanere raggiungibili, non tutte caricate all'avvio.
