# Controllo della repository prima della pubblicazione

Richiesta di Marco: controllo complessivo e push su main. Copia di pubblicazione
basata su main 567321e, verificato tramite fetch; nessun nuovo contributo remoto
in conflitto. Contenuti del collega e storia preservati.

Verificati codice mantenuto, collegamenti, inventario SHA-256, mappa e coerenza
fra decisioni, implementazione e attività pendenti. Aggiornati ingressi e
istruzioni superate sul rinvio dei filtri. Il verificatore principale rimane da
addestrare e il problema di capacità HPC è rinviato alla prossima sessione.
Gli stati dei job sono datati, non un nuovo controllo live.

Suite della copia pubblicabile: 105 casi, 103 superati e due saltati per
motmetrics assente; tutti i 23 nuovi casi superati. Ambiente locale Python 3.13,
con dipendenze diverse dai requirements storici; nessuna nuova inferenza GPU.
Controllo iniziale: 635 collegamenti, 53 sorgenti Python e 219 hash, zero errori;
l'inventario finale include anche questa verifica e le evidenze di test.
Mappa: 39 riquadri, 49 collegamenti, 792 campi, copia offline e servizio verificati
in sola lettura. Le cinque schede del punto 3 hanno snapshot dei campi confermati
per rispettare le revisioni successive all'originale.

Scansione dei file modificati senza riscontri per chiavi private, token noti,
segreti assegnati, percorsi personali e account HPC. È un controllo per pattern,
non garanzia assoluta. Nessun nuovo archivio completo, dato grezzo o checkpoint
incluso. La copia verificata dei tracciati archiviati sul PC resta esclusa da Git.

Dettagli e log in [evidenze](../evidence/point3_20261121/README.md).
Questa nota descrive il controllo pre-push, non certifica ancora la pubblicazione.
