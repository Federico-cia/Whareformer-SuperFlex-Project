# Ripartenza controllata dell'arricchimento — 21 novembre 2026

## Mandato e accesso

Marco richiede esplicitamente «Fallo ripartire». Eseguita per questa ripartenza
diagnosi e ripresa tramite l'accesso SSH già configurato, con esecuzione
autorizzata fuori dall'ambiente che non poteva leggere la chiave. Nessuna chiave,
password, autorizzazione del server o configurazione di sicurezza modificata.
Non è una revisione generale delle modalità HPC di AGENTS: registra l'azione
specificamente richiesta da Marco e le verifiche necessarie alla ripresa.

## Diagnosi effettiva

783207/783208 e le riprese 783490/783491 sono falliti su gnode02 durante MoGE,
dopo DA completata. Nessun traceback Python esplicito; MaxRSS dei batch circa
3.0–3.6 GB a fronte di 16 GB richiesti, senza prova di causa da memoria.
MoGE aveva report parziali (47 nel blocco 8, 26 nel blocco 9), ma nessun indice
finale. Associazione col nodo osservata, guasto hardware non dimostrato.

Controller remoto SHA-256 invariato:
`0f73f716b6c1d61bbfb08e33d8880f3f2652fe969347a89955f4c84b2ce66e9f`.
Coda verificata vuota prima degli invii. Nessun job duplicato.

## Intervento operativo

- Conservati tutti gli otto blocchi conclusi e tutte le cache/parziali.
- Ripresa dei rami dai primi blocchi mancanti: **783750, ramo 0/blocco 8**;
  **783751, ramo 1/blocco 9**, inviati alle 23:20.
- Esclusione temporanea di gnode02 come intervento controllato. Applicata anche
  al batch corrente e propagata ai successori tramite `SBATCH_EXCLUDE`.
- Aggiunti tracing shell e diagnostica Python/C++ per eventuali nuovi errori.
  Nessun modello, dato, parametro scientifico o codice pipeline modificato.
- Backup remoto `geometry.sbatch.before_restart_20261121`, hash
  `06f1f808d14ca82a046d66ff27bbf55615648eb768085954a9d7c179cff9e029`;
  batch aggiornato hash
  `babf49cb53d359bb9ee75f0a61f490b76e598a5407a665b1877a7cdb89220276`.

Radice remota `~/cv_project/p01_full_enrichment_20261121_v1/`;
log `geometry_783750.out/.err`, `geometry_783751.out/.err`;
ricevute `submissions/restart_exclude_gnode02_0008_783750.json` e
`submissions/restart_exclude_gnode02_0009_783751.json`. Catena successori
gestita dal controller preesistente, a due rami.

## Verifica di avanzamento

Alle **23:23:51** entrambi **RUNNING su gnode03**, rispettivamente a 3m14s
e 3m08s: superato il precedente tempo di arresto.

**In entrambi i blocchi DA e MoGE hanno indice finale con 512/512 ready**;
nuvole in costruzione (86 report per sorgente nel blocco 8, 46 nel blocco 9).
Questa è evidenza di superamento dello stadio che si interrompeva, non soltanto
di accettazione dello scheduler. Ancora 8/216 blocchi conclusi a quel controllo;
SuperFlex dei nuovi blocchi e completamento della catena non ancora verificati.

File locali: `strumenti_hpc/diagnosi_ripartenza_20261121.txt`,
`preripresa_20261121.txt`, `esito_ripresa_controllata_20261121.txt`,
`stato_ripresa_controllata_20261121.txt`. Script di ripresa controllata e
monitoraggio salvati nella stessa cartella. Non eseguire nuovamente la ripresa
mentre esistono job della catena in coda.

## Ripresa della prossima sessione

Controllare i successori e numero di blocchi con lo script di controllo già
esistente prima di qualsiasi invio. Non dichiarare ancora la run completa o
garantita per tutta la notte. Nessuna sorveglianza permanente o automazione
creata. Audit 783586 resta concluso e non va rilanciato; punto 3 invariato.
