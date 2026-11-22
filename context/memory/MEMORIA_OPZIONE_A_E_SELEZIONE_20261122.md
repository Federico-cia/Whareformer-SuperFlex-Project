# Memoria geometrica: opzione A e scelta dei parametri sul sistema completo

*Metodo consolidato il 22 novembre 2026. Decisioni in REGISTRO_DECISIONI.md; stato e attività correnti nei documenti omonimi. La cronologia precedente è conservata nell’archivio.*

## In breve

- Ogni traccia ha più **stati**; uno stato = una **posizione** dell'oggetto. Un nuovo stato nasce solo quando l'oggetto viene messo in una nuova posizione.
- La posizione si decide con il **criterio C** (riproiezione: sagoma e spazio vuoto visti dalle camere). Il verificatore decide **solo** se una vista entra nella forma.
- I due parametri del criterio (soglia di coerenza e margine di profondità) **si scelgono sul sistema completo**, guardando le metriche ufficiali di tracking, non su una misura sostitutiva.
- Oggi questa scelta non è ancora possibile: manca il modello del compagno (punto 2) e la geometria copre circa il 7% di P01_01. Si prepara tutto il necessario e si parte da una configurazione iniziale **dichiarata come tale**.

## Decisioni di Marco

| Decisione | Contenuto |
|---|---|
| Opzione A | Stato = posizione; una vista non ammessa resta nello stato e non ne apre uno nuovo. |
| Criterio C | Test di posizione per riproiezione (sagoma + spazio libero), nelle due direzioni. |
| Ritorno nella stessa posizione | Apre un nuovo stato (l'orientamento può essere cambiato). |
| Dati | Tutte le nuvole P01_01 allineabili (campione 446 + 7680 nuove), a **piena risoluzione**. |
| P01_02 | Quando disponibile, si rifà la selezione su entrambi i video, senza procedure aggiuntive. |
| Criterio di scelta | **Sistema completo**: metriche ufficiali di tracking con la memoria collegata al resto della pipeline. Nessuna soluzione provvisoria come risultato finale. |

## Come funziona ora la memoria

1. Una vista nuova viene confrontata con gli stati attivi (prima i confermati, poi i deboli) con il criterio C.
2. Se è compatibile con uno stato, vi entra; altrimenti nasce un nuovo stato debole.
3. Uno stato diventa confermato con almeno due viste e supporto sufficiente; quando l'oggetto è confermato in un posto, gli altri stati confermati si chiudono.
4. Dentro uno stato confermato il verificatore valuta ogni vista: se ammessa entra nella forma persistente, altrimenti resta nello stato senza riprovare.
5. Il primo stato confermato inizializza la forma; uno stato dopo uno spostamento viene registrato sulla forma.

Codice: `integration_prototype/position_state_memory.py`, test `test_position_state_memory.py`.

Impostazioni operative dell’assistente, non ottimi calibrati: minimo tra test diretto e inverso; fattore silhouette 2; minimo 32 punti proiettati; tre viste di riferimento. Verifica di fusione per singola vista senza ripetere le respinte a posa fissata. Risoluzione relativa per traccia: voxel 0.04 R e densità 0.1 R del primo raggio valido.
Collegamenti: export (`--policy position --position-config`) e pipeline (`position_config=...`).

## Come verranno scelti i parametri

1. Si prepara una **griglia** di configurazioni della memoria (soglia × margine).
2. Per ogni configurazione si esegue la **pipeline intera**: Whareformer con il modello del compagno, memoria geometrica, SuperFlex sulle forme della memoria, sui video di sviluppo (P01_01, poi anche P01_02).
3. Si sceglie con le **metriche ufficiali** (IDF1, mPCL) usate per la baseline.
4. Se più configurazioni differiscono di pochi eventi (rumore su uno-due video), decide un **criterio secondario fissato prima**: la capacità della memoria di prevedere dove si trova l'oggetto e com'è fatto.
5. Dipendenza circolare: il modello del compagno si addestra sui dati prodotti dalla memoria. Si parte da una configurazione iniziale; se la scelta finale cambia molto, il compagno riaddestra una volta.

## Perché non si può fare subito

- **Punto 2 non concluso.** Con l'adattatore geometrico attuale le 29 configurazioni della campagna del 15 novembre hanno dato assegnazioni identiche alla baseline (IDF1 73.269735%, mPCL 70.465504%): ogni soglia darebbe la stessa metrica.
- **Copertura geometrica.** 15 blocchi su 216 di P01_01 (circa 75 s contigui, frame ~937–5500) più il campione sparso; il resto è bloccato dalla capacità HPC.
- **Dipendenza memoria ↔ punto 2**, descritta sopra.

## Costo da pianificare: SuperFlex nel ciclo

La mappa approvata del 21 novembre (`mappa_interattiva/`, nodi R14–R15 e R35–R37) prevede che il confronto usi le **forme SuperFlex**: una per l'osservazione corrente e una per la memoria dopo ogni aggiornamento ammesso; la distanza fra forme corregge dall'esterno i punteggi di Whareformer (R20–R21). Marco conferma che il modello del compagno userà le forme SuperFlex.

Conseguenza: ogni configurazione della griglia produce versioni di forma diverse, ciascuna da ricostruire con SuperFlex su GPU. Costo da misurare prima di fissare la griglia. Riduzioni possibili: riuso delle ricostruzioni per forme identiche fra configurazioni (stesso hash della nuvola), ricostruzione differita già implementata, griglia piccola.

## Stato e attività

Consultare [STATO_LAVORO](STATO_LAVORO.md) per dati v2, job e prestazioni; [TODO](TODO.md) (T01–T09) per collaudo, export, punto 2 e selezione. Questa specifica non mantiene una seconda checklist.

## Proposte superate

- Budget fisso del 5% di falsi «nuova posizione»: era un test, non un ottimo.
- Utilità prequenziale come criterio **finale**: resta solo come criterio secondario e come aiuto per la configurazione iniziale.
- Pseudo-etichette di spostamento (traiettorie XYZ ufficiali, annotazioni EPIC-100): non affidabili per «fermo»; solo controllo indipendente.
- Sottocampionamento a 2048 punti: sostituito dalla piena risoluzione.

## Limiti da dichiarare

- Scelta su uno o due video di training di Whareformer: risultati di sviluppo, non prova di generalizzazione; il test indipendente resta il TODO prioritario del 21 novembre.
- L'ottimo dipende dal verificatore e dal modello del compagno: se cambiano, la scelta va rifatta sullo sviluppo.
- Occlusioni ed errori di profondità condivisi non sono modellati dal criterio C (producono stati in più, non contaminano la forma).
