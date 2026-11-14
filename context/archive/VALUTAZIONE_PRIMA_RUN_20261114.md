# Valutazione della prima run e direzioni successive — 14 novembre 2026

Analisi richiesta da Marco dopo il completamento; raccomandazioni, non approvazione di nuovi metodi, job o modifica dei filtri. Evidenze di riferimento nel [resoconto](../evidence/full_video_20261114/REPORT.md) e nell'[audit](../evidence/full_video_20261114/audit.json).

## Giudizio

Il ciclo causale funziona da ingressi preparati fino alle predizioni e ai report finali su tutto il protocollo ufficiale. Sette fusioni ammesse, 25 nuove SuperFlex, 76 confronti successivi con ricostruzioni da fusioni dimostrano il ritorno effettivo della memoria al matcher. Restano distinti frontend rigenerato dalle immagini, accuratezza fisica delle fusioni, generalizzazione e miglioramento del tracking: questi risultati non sono ancora dimostrati.

## Criticità prioritarie

1. **Copertura:** 71 geometrie/110590 osservazioni (0.0642%); il risultato aggregato è dominato dal percorso aspetto/XYZ. Non inferire inutilità della geometria dalle metriche invariate.
2. **Validità delle fusioni:** sette ammissioni concentrate in due track predette, sei sulla track 35 e una sulla 4. Su 53 tentativi successivi, sette ammessi e 46 respinti; sette rifiuti dipendono soltanto dall'ambiguità. Il tasso di rifiuto non prova da solo che i gate siano errati: rumore, scala, viste parziali e associazioni rimangono possibili cause. La provenienza dei punti è verificata, la posa fisica no.
3. **Calibrazione del ponte geometrico:** nel codice la correzione è peso × (distanza neutra − distanza). Con peso 0.1 e distanza neutra 0 tutte le 695 correzioni osservate sono negative; mediana assoluta 0.00629963, massimo 0.03434743. Nuova track e coppie senza geometria non ricevono correzione diretta. Rischio di penalizzazione dovuta alla sola disponibilità della geometria; effetto sulle decisioni non osservato nella run. I margini dei punteggi originali non sono nel report: il valore assoluto delle correzioni non basta a stabilire perché le assegnazioni siano invariate. Verificare margini, ordinamento corretto/errato e comportamento quando la geometria manca prima di aumentare il peso.
4. **Utilità specifica di SuperFlex:** manca ancora un confronto attivo appaiato fra forme separate, punti accumulati e SuperFlex accumulato con stessi input/regole. D2 è un descrittore globale; discriminatività e beneficio della completion su EPIC sono ipotesi da misurare, non risultati della riuscita delle inferenze.
5. **Frontend e valutazione:** cache verificate ma nessuna nuova estrazione completa RGB; identità DINOv2/PCA/scena ancora da stabilire per rigenerare. P01_01 è sviluppo/train, nomi/XYZ seguono l'evaluator originale e non sono nuova GT fisica. Test separato necessario per conclusioni di efficacia generale.

## Approcci e compromessi

| Approccio | Vantaggio | Limite/costo | Raccomandazione |
|---|---|---|---|
| Diagnosi mirata con artefatti esistenti | Basso nuovo costo neurale; distingue validità geometrica, discriminatività e scala dei punteggi | Pochi casi, nessuna generalizzazione; la sola analisi visiva non certifica accuratezza | Primo passo consigliato |
| Estendere copertura e confrontare varianti appaiate | Più opportunità di misurare effetto; isola il contributo SuperFlex dai punti e dalla fusione | Nuove profondità/ricostruzioni e provenienza; errori possono propagarsi | Dopo i controlli essenziali, campione definito prima dei risultati e con casi facili/difficili |
| Completare prima il frontend RGB | Migliora riproducibilità e capacità di partire dagli ingressi dichiarati | Dipendenze originali/PCA/scena e costo; non risponde da solo all'utilità di SuperFlex | Necessario per il traguardo dalle immagini, separato dalla diagnosi scientifica |
| Rivedere registrazione e gate | Potenziale recupero di viste legittime respinte per simmetria/parzialità | Rischio di contaminare memoria con fusioni errate; più ammissioni non equivalgono a maggiore qualità | Rinvio esplicito ancora valido; nessuna esecuzione finché Marco non lo riattiva |

Sequenza proposta: verificare le sette fusioni e rifiuti rappresentativi con evidenze escluse dal fitting; diagnosticare distanze/margini e neutralità dei mancanti; ampliare copertura mantenendo storia completa; confrontare W0, forme separate, punti accumulati e SuperFlex accumulato; calibrare finitamente sullo sviluppo, congelare e verificare separatamente. Maschere, riferimento di valutazione e budget comuni; non scegliere soltanto casi in cui la geometria sembra riuscire. Rigenerazione del frontend come filone distinto, senza introdurre nuova PCA o modelli sostitutivi impliciti.

Una vista esclusa dal fitting offre un controllo utile ma non diventa automaticamente GT indipendente; quando posa/scala di riferimento non sono affidabili, dichiarare che la misura combina errore di posa e di forma. Nessuna nuova run avviata per questa analisi; configurazione e filtri della prima esecuzione restano congelati.
