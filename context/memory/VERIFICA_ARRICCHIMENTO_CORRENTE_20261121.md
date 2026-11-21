# Verifica operativa dell'arricchimento

## Spazio recuperato e nuova ripresa — 21 novembre 2026

**Verifica successiva delle 23:51:38:** 783790/783791 entrambi RUNNING a 3m56s su gnode03; superato l'arresto precedente nelle nuvole, ora blocco 8 con 309/312 report DA/MoGE e blocco 9 con 286/288. Quota 41.19/46.56 GiB (circa 5.37 GiB liberi), otto blocchi ancora conclusi; SuperFlex dei nuovi blocchi non ancora verificata.

Marco autorizza pulizia e, esplicitamente, copia/archiviazione dei tracciati conclusi sul PC. Verificati due volte 377 file (5.47 GiB) e conservati in archivio locale di 636594519 byte con ledger/hash, prima di rimuovere le sole copie remote. Runtime, geometrie e input attuali preservati. Quota scesa da 46.35 a 40.88 GiB su 46.56; archivio da NON eliminare. [Operazioni, percorsi e ripristino](PULIZIA_E_RIPRESA_HPC_20261121.md).

**Job correnti:** 783790/783791, rami 0/1 dai blocchi 8/9, RUNNING su gnode03 al controllo 23:49:54 (2m11s). Preflight quota positivo anche sul nodo di calcolo. Otto blocchi conclusi a quel controllo. I tentativi 783750/751 sono falliti dopo MoGE anche su nodo diverso; 783782/783783 fermati prima delle inferenze per helper quota assente, poi corretto. Nessun precedente tentativo va considerato attivo.

Guard di quota a ogni blocco: riserva operativa 2 GiB/12000 file, stop esplicito codice 75 quando insufficiente; fallback nativo BeeGFS verificato. Tolta l'esclusione del nodo che non risolveva. Nessuna modifica scientifica. **Capacità ancora aperta:** costo misurato 0.64 GiB/blocco, estrapolazione circa 138 GiB/216 blocchi; la pulizia non basta a garantire completamento nella quota di 50 GB. Occorre compattare la conservazione senza perdere informazione necessaria o reperire capacità. Nessuna riduzione di copertura o sorgenti approvata in questa fase. Non promettere funzionamento ininterrotto notturno.


## HPC riavviato su richiesta di Marco — 21 novembre 2026, 23:23

Marco richiede «Fallo ripartire». Diagnosi e ripresa eseguite con accesso esistente autorizzato per l'azione: **783750 e 783751 RUNNING su gnode03**, rami 0/1 dai blocchi 8/9. **MoGE superato: 512/512 ready in entrambi**, DA già pronta, nuvole in costruzione. Ultimo controllo 23:23:51, rispettivamente 3m14s/3m08s; 8/216 blocchi ancora conclusi a quel momento. Catena automatica preesistente preservata, nessun duplicato o reset delle cache.

Escluso gnode02 dai job e successori come intervento controllato dopo quattro arresti osservati durante MoGE, senza pretendere diagnosi hardware conclusiva. Batch remoto salvato in backup e arricchito di log; dati/modelli/codice scientifico invariati. [Intervento, hash, log e ricevute](RIPARTENZA_HPC_20261121.md). Non reinviare mentre i rami sono in coda. SuperFlex dei nuovi blocchi e completamento integrale ancora da verificare; nessuna sorveglianza permanente avviata. Questo stato supera le precedenti note di coda vuota/run ferma. Audit e sviluppo punto 3 restano nello stato documentato.


## Audit acquisito; arricchimento fermo — 21 novembre 2026, esiti 23:01–23:06

Marco esegue gli script: **783586 COMPLETED 0:0, 16m53s**, sette hash verificati; 446 osservazioni, 438 allineamenti validi e nuvole locali finite, otto fit con alpha negativo. Confronto appaiato su 415 coppie: sovrapposizione mediana 3.27% grezza → 22.80% allineata (28.08% → 68.16% nel terzile di minore spostamento, non staticità certificata). 24 osservazioni con sole maschere del catalogo. Nessuna etichetta di fusione corretta ancora certificata: mantenere limiti di staticità, simmetrie ed errori condivisi. [Risultati, provenienza e interpretazione](RISULTATI_AUDIT_AMMISSIONE_20261121.md).

**Arricchimento:** coda vuota, 8/216 blocchi, nessun riepilogo finale; riprese 783490 e 783491 entrambe FAILED 1:0. Causa non identificata dai log disponibili. Aggiornata la diagnosi di sola lettura per questi job e per gli stadi parziali; prossimo intervento di Marco: `strumenti_hpc/esegui_diagnosi_hpc.bat`, poi leggere `esito_diagnosi.txt` prima di riprendere. Nessun accesso diretto HPC, invio o training dell'assistente. Le nuvole locali consentono di proseguire la preparazione dei dati da trasformazioni note senza attendere la run completa. Decisioni metodologiche approvate invariate.


## Evidenze acquisite

L'acquisizione 782990 è COMPLETED 0:0 in 41m10s. Archivio RGB 1716787200 byte, SHA-256 `f15f64717fd8f6a0190764e9b6011835f803b5e0325d7f9e0f2388dba115384e`; maschere sorgenti con hash originale `c848514f4586ac451373c0b0ea0af26029b4149a0d3863b27ecd020246ca2d6c`. Copertura: 110580/110590 osservazioni abbinate, dieci mancanti, zero conflitti, 9656 alias temporali. 32125 RGB verificati, 216 blocchi, 446 geometrie riusate e 110134 osservazioni nuove da inferire. Gli alias non certificano il JPEG che generò le feature originali.

I primi job 782968/782969 erano falliti per Ninja non disponibile; questo è un problema storico già affrontato dal rilancio, non la diagnosi dell'eventuale arresto corrente. `strumenti_hpc/esito_hpc.txt` delle 20:30 documenta otto blocchi completati, ciascuno con 1024 SuperFlex riuscite e zero fallimenti individuali (512 osservazioni, due sorgenti), poi arresto dei blocchi 8/9. `esito_ripresa.txt` delle 21:10 documenta successiva ripresa 783490/783491 RUNNING; `esito_audit_invio.txt` delle 21:45 documenta audit 783586 RUNNING all'invio.

Una prima interrogazione diretta in questa verifica non ha restituito job in squeue; sono stati acquisiti accounting iniziale e coverage, non accounting/log dei job successivi. Non dedurre completamento, né attribuire una causa corrente ai vecchi errori. Numero aggiornato di blocchi e stato dei successori da acquisire.

## Vincolo e azione predisposta

Il vincolo aggiornato in `lavoro di gruppo/AGENTS.md` riserva a Marco l'avvio degli script HPC. L'interrogazione iniziale ha preceduto la lettura di questa revisione; nessun ulteriore accesso diretto dopo averla letta. Aggiornato `strumenti_hpc/controllo_remoto.sh` per includere copertura, eventuale riepilogo finale e ultime sei ricevute dei rami, oltre ad accounting/stati/log/esiti SuperFlex già previsti.

Prossimo passo necessario: Marco esegue `strumenti_hpc/esegui_controllo_hpc.bat`; leggere quindi `esito_hpc.txt` aggiornato prima di ripresa o diagnosi. Nessun nuovo job, modifica di modello o rilancio effettuato in questa verifica. Le decisioni scientifiche del punto 3 restano invariate.
