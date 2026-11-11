# Primo confronto di stabilità/discriminatività DA–MoGE

Verifica del 10 novembre 2026. Protocollo prefissato in `ESPERIMENTO_IDENTITA_DA_MOGE.md`; risultati e log in `outputs/shape_identity_v1/`. Analisi descrittiva di sviluppo, non valutazione del tracking o graduatoria generale delle sorgenti.

## Catena procedurale essenziale

Sintesi richiesta da Marco il 10 novembre; chiarimento del procedimento eseguito, non nuovo esperimento.

- **Domanda:** stabilità fra viste della stessa istanza e separazione fra istanze diverse; confronto DA/MoGE e contributo SuperFlex rispetto ai punti.
- **Input:** nuvole e superfici già disponibili nelle quattro condizioni della tabella sotto. Nessuna nuova inferenza. RGB/maschere/annotazioni servono a verificare corrispondenze e identità, non entrano nella distanza geometrica.
- **Preprocessing:** 1024 punti per rappresentazione, centratura e divisione per raggio RMS; confronto di forma senza posizione né dimensione assoluta.
- **D2:** per ciascuna rappresentazione, 16384 distanze interne fra coppie di punti. Fra due osservazioni si confrontano le distribuzioni ordinate mediante media delle differenze assolute (Wasserstein 1D empirica). Distanza piccola indica distribuzioni simili, non identità certa. Controlli distinti: spettro di covarianza e allineamento rigido multi-inizio con Chamfer.
- **Output e lettura:** tabella di distanze per coppia, non nuove mesh; etichette visive separate distinguono coppie della stessa identità e di identità diverse. L'AUC misura l'ordinamento fra questi due gruppi, non la percentuale di associazioni corrette del tracker. Copertura, risultati e limiti nelle sezioni successive; dettagli riproducibili nel protocollo collegato.

## Esito operativo verificato

Job **750536 COMPLETED/0:0 in 47m26s**, quattro CPU, nessuna GPU. Precalcolo misurato: 2766.5s (46m06.5s), inferiore alla proiezione iniziale di circa 1h19m. Tutte le **8797 coppie** completate, dieci riusate dal pilota; CSV con 35188 righe, quattro rappresentazioni per coppia incluse le indisponibilità. Valutatore completato, stderr vuoto e nessun job attivo nella successiva lettura della coda. Nessuna nuova inferenza o installazione.

Archivio `completed_results.tar.gz`, riepilogo e CSV recuperati con SHA-256 corrispondenti al remoto. Output remoti `~/cv_project/runs/shape_identity_v1/`; log `~/cv_project/shape_identity_750536.out/.err`, anche scaricati localmente. Controlli locali indipendenti in `local_verification.json`: chiavi/firme per coppia, completezza, valori finiti/non negativi e ricalcolo delle AUC mediante conteggio esplicito di confronti fra distanze, indipendente dal calcolo per ranghi del valutatore.

## Copertura dell'analisi etichettata

Campione revisionato visivamente prima di leggere le distanze: 37 osservazioni, sette identità, quattro video. Non è ground truth persistente certificata: caratteristiche e contesto visivo sostengono le corrispondenze, senza escludere sostituzioni con istanze indistinguibili fra frame campionati. Le altre 262 osservazioni restano non etichettate; le loro distanze sono disponibili per future revisioni.

158 coppie etichettate disponibili per punti DA, SuperFlex DA e punti MoGE; 149 per SuperFlex MoGE. Il confronto fra tutte le rappresentazioni usa **le stesse 149 coppie**: 79 della stessa identità, 30 di identità diverse della stessa categoria, 40 di categorie diverse. Le nove escluse dipendono dal fallimento SuperFlex MoGE già noto sul tagliere P08_09/frame_0000010781__a01, non da una nuova esclusione basata sui punteggi. Nell'intero precalcolo questo output mancante interessa 51 coppie; non imputare distanze favorevoli ai casi mancanti.

I confronti fra istanze diverse della stessa categoria riguardano **soltanto due piatti di P22_01**, 11 osservazioni: sei di un piatto bianco con bordo scanalato, cinque di un piatto verde chiaro con bordo liscio. Ci sono 25 coppie positive e 30 negative. Il numero di coppie non equivale a 55 osservazioni o identità indipendenti.

## Risultato prioritario entro categoria: P22_01

L'AUC è qui la frazione di confronti in cui una distanza fra identità diverse supera una distanza della stessa identità, con mezzo punto ai pareggi: 25 distanze positive × 30 negative = 750 confronti, dipendenti e non nuove osservazioni. 0.5 corrisponde all'assenza di ordinamento nel campione. Non è accuratezza di tracking. Misure già definite nel protocollo, nessuna selezionata a posteriori come nuova metrica primaria.

| Rappresentazione | D2, primaria | Spettro di covarianza, semplice | Registrazione multi-inizio + Chamfer |
|---|---:|---:|---:|
| Punti DA grezzo | 0.612 | 0.744 | 0.615 |
| SuperFlex da DA grezzo | 0.627 | 0.729 | 0.717 |
| Punti MoGE | 0.701 | 0.763 | 0.681 |
| SuperFlex da MoGE | 0.768 | 0.752 | 0.728 |

Con D2, le mediane intra/inter-identità sono rispettivamente 0.0693/0.0936 per punti DA, 0.0400/0.0607 per SuperFlex DA, 0.0989/0.1226 per punti MoGE e 0.0602/0.1117 per SuperFlex MoGE. Le scale delle distanze dipendono dalla rappresentazione: una mediana assoluta inferiore non dimostra automaticamente maggiore stabilità utile o separabilità.

Nel recupero del vicino più simile fra frame diversi e nella stessa categoria, la media fra le due identità con D2 è 81.7% per punti DA, 43.3% per SuperFlex DA, 71.7% per punti MoGE e 91.7% per SuperFlex MoGE. Ogni query confronta una piccola galleria, potenzialmente con frame futuri; non è memoria causale o IDF1. Le percentuali derivano soltanto da 11 query dipendenti e non sono stime robuste della prestazione.

## Lettura scientifica e prossimo passo

1. **MoGE non va scartato sulla sola IoU 2D.** Nel piccolo controllo di identità entro categoria, MoGE+SuperFlex è migliore di DA+SuperFlex con D2. È evidenza specifica di questo campione, non superiorità generale di MoGE e non misura dell'effetto isolato della profondità.
2. **Il beneficio di SuperFlex rispetto ai punti non è sistematico.** Con D2 il vantaggio è soprattutto nel ramo MoGE; lo spettro semplice dei punti è competitivo o superiore alle rispettive superfici. La registrazione migliora l'AUC delle superfici rispetto ai punti in entrambi i rami, ma nel campione non supera lo spettro semplice dei punti. Non fissare il confronto più costoso come necessario al matcher.
3. **Il risultato cambia con la distanza e con il criterio di lettura.** Nel ramo DA, un piccolo aumento dell'AUC D2 convive con un peggior recupero top-1: non riassumere tutto come miglioramento della forma. Completamento, parzialità e normalizzazione possono alterare i vicini più prossimi.
4. Il riepilogo globale di retrieval su sette identità è secondario: P01_01 ha una sola identità revisionata e rende il recupero entro categoria triviale; altri video separano categorie diverse. Non usare quel numero per dimostrare discriminazione tra istanze simili.

**Raccomandazione:** mantenere entrambi i rami e il controllo sui punti; ampliare e rafforzare le identità, soprattutto con più istanze della stessa categoria in più video, sfruttando prima le distanze già precalcolate. DA rimane un candidato operativo per il riuso dell'infrastruttura; questo esito non sostiene l'adozione definitiva o l'abbandono di MoGE. Collegare le osservazioni a `detection_idx`, feature e XYZ reali della baseline prima del prototipo nel tracker. Nessun nuovo job richiesto da questa verifica.

Non introdurre nuovi dataset, soglie, training o memoria fusa sulla base di queste sole evidenze. Conclusioni su utilità per Whareformer richiedono il successivo confronto con aspetto/posizione e valutazione originale del tracking.
