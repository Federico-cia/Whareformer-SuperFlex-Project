# Stato corrente del progetto

Consolidato il 22 novembre 2026 da documenti e ricevute locali; ultima osservazione HPC disponibile: **21:58:31 Europe/Rome**. Nessuna nuova interrogazione remota durante il riordino. Decisioni in [REGISTRO_DECISIONI](REGISTRO_DECISIONI.md), attività in [TODO](TODO.md).

## Obiettivo e organizzazione

Verificare se la forma SuperFlex e la memoria geometrica migliorano l'associazione delle identità di Whareformer, a parità degli altri input. Marco segue il punto 3 (memoria/ammissione) e P01_01; Federico il punto 2 (matcher) e P01_02. Punti 1 (confronto forme) e 4 (collocazione nella scena) restano da discutere dopo entrambi. Presentazione il 23 novembre; scadenza del progetto completo successiva, non precisata. Si prosegue con una sola chat.

## Implementato e disponibile

- **Memoria opzione A:** stati di posizione distinti dalla forma persistente; criterio C per riproiezione, verificatore per l'ammissione delle viste. Codice e test locali riportati nei resoconti; efficacia reale non validata. [Contratto corrente](MEMORIA_OPZIONE_A_E_SELEZIONE_20261122.md).
- **Dati allineati v2:** 8106 osservazioni, 2427 frame, 24 identità, 86 773 738 punti; 19 escluse e una fallita. Piena risoluzione, unità EPIC-Fields non certificate in metri. [Riepilogo](../evidence/aligned_20261122/summary.json), [provenienza](../evidence/aligned_20261122/PROVENIENZA.md). Alpha/beta: audit 783586 e job conclusi 786174/786275; riproduzione audit 40/40 esatta. v1 contenuta in v2, identica su 300 nuvole campionate secondo la verifica registrata.
- **Drive:** 15/216 blocchi P01_01 (7680 nuove osservazioni, più campione 446) archiviati e verificati; struttura video → run → tipo. Job 786129 concluso: zero blocchi falliti, 7 491 881 373 byte liberati sull'HPC dopo verifica; input della run caricati. [Ricevuta](../evidence/ASSET_ESTERNI.md#asset-4b23e54c0b27), [guida operativa](../evidence/ASSET_ESTERNI.md#asset-b16d1fb602da). Recuperate da Drive le mappe 0000–0003 rilasciate prematuramente, senza perdita documentata. Produzione restante non rilanciata.
- **Griglia end-to-end:** runner con W0, memoria, matcher e valutatore ufficiale; prova su prefisso diagnostico fino al frame 4300 (1321 frame annotati), peso matcher 0.1 segnaposto. Non è la selezione finale con il modello del compagno.
- **Consegne:** driver/pacchetti P01_02 pronti, pilota HPC non verificato ([resoconto](../archive/PACCHETTO_HPC_P01_02_20261122.md)); pacchetto 890 mesh compare200 pronto ([resoconto](../archive/PACCHETTO_MESH_SUPERFLEX_20261122.md)). Export CPU 785638 concluso e archivio 8126 geometrie scaricato: chiusura della consegna P01_01 ancora pendente.
- **Mappa e pubblicazione:** opzione A applicata il 22 novembre su conferma di Marco: 39 nodi/53 collegamenti, 20 schede di nodo e 22 di freccia aggiornate; 50 schede non modificate conservate. Layout e schede verificati nel browser, con copia offline e backup. [Esito](../evidence/map_20261122/ESITO_APPLICAZIONE.md), [mappa](../../mappa_interattiva/README.md). Ultimo consolidamento remoto documentato 5827c32; modifiche del 22 novembre locali, senza nuovo push.

- **Copia pubblicabile:** preparata una copia separata basata sul main baa2470 verificato, con codice/mappa/memoria/evidenze selezionati, contributi del collega preservati e controlli passati; commit e push autorizzati da Marco dopo controllo degli aggiornamenti remoti. [Preparazione](../evidence/clean_update_20261122/README.md).

## Job da ricontrollare

| Job | Ultimo stato osservato | Esiti, log e ripresa |
|---|---|---|
| 786252 — cv_mem_grid | RUNNING, gnode02, 21:58 del 22 novembre | [Ricevuta locale](../evidence/ASSET_ESTERNI.md#asset-c9ad72c1060d); remoto ~/cv_project/memory_grid_smoke_20261122_v1/, out_786252/, logs/grid_786252.*. W0: 15.4 s; c05_m025: 3108.3 s; c07_m025 ancora in corso. Controllo: strumenti_hpc/memory_grid/2_controlla_prova_griglia.bat. |
| 786329 — cv_sf_aligned | RUNNING, gnode01, stessa ricevuta | [Invio](../evidence/ASSET_ESTERNI.md#asset-d6afb5baa812); remoto ~/cv_project/superflex_aligned_p01_20261122_v1/, queries/, logs/sf_786329.out/.err e logs/worker_786329.log. SuperFlex delle osservazioni allineate FPS-4096, poi upload Drive; completamento/upload non ancora attestati. Controllo: strumenti_hpc/superflex_allineato/2_controlla_superflex_allineato.bat. |

Prova GPU della griglia preparata ma **non inviata** (4_invia_prova_gpu.bat). Gli altri job citati nei resoconti sono storia: non reinviarli senza leggere gli esiti.

## Evidenze e problemi aperti

- **Tracking:** campagna del 15 novembre, 29 configurazioni, assegnazioni identiche alla baseline: IDF1 73.269735%, mPCL 70.465504%. Nessun beneficio dimostrato. [Risultati](../archive/RISULTATI_CAMPAGNA_HPC_20261115.md).
- **Costo:** la prova CPU rallenta fortemente dopo il frame elaborato 1000 (circa 9 s/frame nella coda). L'estrapolazione al video intero è insostenibile; causa da profilare prima di GPU/griglia estesa.
- **Verificatore:** baseline addestrata su simulazioni; variante prudente con 30 errori fra 125 ammissioni (24%) su due identità sintetiche di valutazione. Non è stima su video reale. Proposta di dati prodotti dal registratore effettivo non adottata. [Report e varianti storiche](../archive/REPORT_PUNTO3_20261122.md).
- **Copertura e selezione:** geometria circa 7% di P01_01 più campione; modello finale del punto 2 non concluso; disponibile sul remoto una calibrazione preliminare b/w dello scoring oracle, distinta dal tracking completo. Parametri finali dipendono da entrambi e dai dati esportati dalla memoria. P01_01 è training Whareformer: risultati di sviluppo; test indipendente ancora da scegliere.

## Ripresa

Prima acquisire gli esiti dei due job tramite Marco e profilare la memoria. In parallelo chiarire con Federico il contratto del punto 2 e decidere il test indipendente; dipendenze e rinvii in [TODO](TODO.md). Accesso HPC tramite batch avviati da Marco; massimo due job attivi. Archivio di recupero locale outputs/hpc_storage_recovery_20261121 da non eliminare. [Archivio precedente al riordino](../archive/prima_consolidamento_20261122/README.md): cronologia, quote storiche, precedenti export e pubblicazioni.
