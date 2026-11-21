# Risultati dell'audit del punto 3 — 21 novembre 2026

## Esito e provenienza

Marco ha eseguito controllo e scarico predisposti. Audit **783586 COMPLETED 0:0**,
durata **16m53s**; accounting scaricato alle 23:06, log `AUDIT_OK`. Verificati
localmente tutti i sette SHA-256 riportati dal server: summary, coppie, osservazioni,
log, nuvole e stdout/stderr. Nessun accesso HPC diretto dell'assistente.

Originali in `strumenti_hpc/audit_risultati/audit_783586_3577_5954/`;
[interpretazione numerica](../evidence/point3_20261121/audit_interpretation.json),
accounting/hash (`outputs/audit_ammissione_20261121_interpretation/audit_accounting_hashes.txt`, risorsa locale non pubblicata)
e stato arricchimento (`outputs/audit_ammissione_20261121_interpretation/enrichment_status.txt`, risorsa locale non pubblicata).
Nessun output originale modificato e nessun nuovo training o job.

## Risultati ricalcolati

- 446 osservazioni elaborate senza errori, su 247 frame; allineamento valido
  in 438/446 (98.2%), distribuite su 242 frame. Le otto non valide riguardano
  cinque frame e hanno tutte coefficiente affine alpha negativo: non fonderle.
- 438 nuvole allineate scaricate, 790502 punti, array tutti finiti e chiavi
  corrispondenti esattamente alle osservazioni valide. Questo verifica integrità
  e disponibilità, non accuratezza fisica.
- Maschere da tutti gli oggetti reperite per 422 osservazioni; per 24 lo script
  ha ripiegato sulle sole maschere del catalogo. Queste 24 hanno fit numericamente
  valido ma esclusione dello sfondo dinamico meno garantita.
- 429 coppie consecutive per identità benchmark, 415 confrontabili sia grezze
  sia allineate. Le 17 identità sono sbilanciate (pan: 183/415 coppie); le coppie
  condividono osservazioni e non sono esperimenti indipendenti.

| Sovrapposizione minima nelle due direzioni, stesse coppie | DA grezza | DA allineata |
|---|---:|---:|
| Mediana sulle 415 coppie | 3.27% | 22.80% |
| Mediana nel terzile di minore spostamento XYZ (139 coppie) | 28.08% | 68.16% |
| Mediana sulle 384 coppie con maschere complete in entrambe le viste | 4.45% | 24.88% |

Tolleranza NN descrittiva: 0.1 volte il raggio medio delle nuvole di ciascun ramo,
come nell'audit; non è una nuova soglia di ammissione. Sul confronto appaiato di
415 coppie: aumento in 254, parità in 71, diminuzione in 90. Non è uniformemente
migliore. Il terzile è definito dai dati, non una classe di staticità certificata;
XYZ e scala condividono dipendenze con la geometria valutata.

Il vecchio registratore/gate ammette 178/415 confronti allineati e ne respinge 237;
43 rifiuti sono dovuti alla sola ambiguità. Non chiamarli falsi rifiuti senza
riferimento indipendente: il fatto che l'identità oracle coincida non certifica
la posa né l'opportunità della fusione. Il riferimento relativo dalle camere
vale solo per oggetto fermo.

## Interpretazione e limiti

L'allineamento alla scena mostra un aumento descrittivo della coerenza spaziale
sulle stesse coppie; è coerente con la direzione già approvata, senza riaprire la
scelta della sorgente. Non dimostra da solo superiorità fisica o generalizzazione.
La variabilità del raggio delle nuvole parziali non risulta eliminata; visibilità,
campionamento e rumore del fit impediscono di interpretarla come solo errore di scala.

Non sono ancora disponibili etichette reali certificate di fusione corretta:
lo script stratifica il movimento del centroide ma non esclude rotazioni sul
posto o manipolazioni. `reg_*_surface_err_R` misura spostamento degli stessi
punti, non distanza fra superfici equivalente sotto simmetria. Le pose degli
altri candidati del registratore non sono esportate. Quindi non addestrare
automaticamente il verificatore su accettazioni/gate o su quei numeri come GT.

Le nuvole scaricate consentono ora di sviluppare localmente preparazione dei
dati e perturbazioni con trasformazioni note, senza aspettare l'arricchimento
completo. Rimangono da fissare/validare split, perturbazioni realistiche, evidenze
di staticità, parametri sullo sviluppo e protocollo indipendente.

## Arricchimento completo: arresto confermato

Controllo effettuato da Marco alle **23:01:50**: coda vuota, **8/216 blocchi**
completati, `final_status.json` assente. Riprese **783490 FAILED 1:0 (2m34s)** e
**783491 FAILED 1:0 (2m21s)**, entrambe su gnode02. Gli otto blocchi completati
riportano ciascuno 1024 SuperFlex ready e zero failed (due sorgenti per 512
osservazioni); i blocchi 8/9 non hanno ancora SuperFlex ready. Conservare i
parziali: l'assenza di SuperFlex non significa assenza di profondità già calcolate.

Acquisizione 782990 resta conclusa: 110580/110590 osservazioni abbinate, dieci
mancanti esplicite, 9656 alias temporali. Non dichiarare il dataset completo.

I log correnti mostrano caricamento pesi senza traceback visibile; non bastano
per attribuire i fallimenti al nodo o al codice. La precedente diagnosi di
evento del nodo era un'ipotesi, non causa confermata della nuova interruzione.
Aggiornati `diagnosi_remota.sh` e `esegui_diagnosi_hpc.bat` per includere i due
job di ripresa, accounting degli step, indici/report dei singoli stadi e script
batch remoto. Script di sola lettura, da avviare da Marco; nessuna ripresa inviata.

## Prossimo passo

Marco esegue `strumenti_hpc/esegui_diagnosi_hpc.bat`; leggere `esito_diagnosi.txt`
prima di preparare una correzione/ripresa. In parallelo, proseguire la preparazione
del verificatore con le nuvole ormai locali e target da trasformazioni note,
senza spacciare le coppie reali dell'audit per supervisione certificata.
