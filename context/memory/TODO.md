# Attività aperte

Consolidate il 22 novembre 2026. Stato ed esiti conclusi in [STATO_LAVORO](STATO_LAVORO.md); decisioni in [REGISTRO_DECISIONI](REGISTRO_DECISIONI.md). Le caselle storiche non costituiscono nuovi incarichi.

## Ripresa immediata

- [ ] **T01 — Esiti HPC:** leggere 786252 e 786329 con i controlli indicati nello stato; verificare risultati SuperFlex, conteggi/fallimenti e upload Drive prima di attestare il completamento.
- [ ] **T02 — Prestazioni memoria:** profilare il rallentamento della prova CPU, identificare la causa e misurare il costo corretto. Prima della prova GPU della griglia e di qualsiasi estensione.
- [ ] **T03 — Drive:** aggiornare/ricaricare README e catalogo per DA allineato e SuperFlex allineato; verificare che descrivano gli artefatti effettivamente caricati. Rinnovare il collegamento Google (revoca + drive_5) quando nessun job usa Drive; accesso di Federico non prioritario.
- [ ] **T04 — Consegna punto 2:** chiarire stato del modello di Federico e formato d'ingresso; scegliere una configurazione iniziale esplicita dell'opzione A e generare l'export causale. Chiudere pacchetto P01_01: verifica 8126 geometrie/join, esempi/logits rispetto a riferimento446, manifest e istruzioni. Scarico 785638 già concluso. Ampliare esempi con Nuova track e mancanti: il campione 446 non è training completo.
- [ ] **T05 — Prova GPU:** dopo T01/T02, eseguire il collaudo completo con SuperFlex (4_invia_prova_gpu.bat), controllare contratti FPS/worker e misurare costo per configurazione. Il collaudo con peso segnaposto non seleziona i parametri finali.

## Decisioni scientifiche e validazione

- [ ] **T06 — Test indipendente, prioritario:** Marco e Federico scelgono video mai usati per training Whareformer o sviluppo/calibrazione 3D. Opzioni da valutare: sottoinsieme dei 54 video EPIC di test, test completo se sostenibile, IT3DEgo/HD-EPIC come generalizzazione. Fissare campionamento prima dei risultati, baseline, metriche e incertezza per video; verificare accesso/dimensione di feature e training LMDB prima dello scarico. P01_01 resta sviluppo; P01_02 entra nella selezione quando disponibile.
- [ ] **T07 — Punto 2 e confronto forme:** concordare uso e forza del segnale, due memorie (descrittori/punti), D2 o Chamfer dopo allineamento, scala/parzialità e superfici interne delle primitive. Restano richiesti i due percorsi (fusione esterna appresa e adattamento del matcher), con controllo senza geometria a pari training; fine-tuning è raccomandazione, non scelta fissata. [Discussione](INTEGRAZIONE_DISCUSSIONE.md).
- [ ] **T08 — Affidabilità punto 3:** validare ammissioni/rifiuti con evidenza indipendente, simmetrie, viste parziali, errori di scala, movimento, chiusura/ritorno degli stati e contaminazione da associazioni errate. Definire costo degli errori e target con il compagno. Valutare la proposta di simulazioni passate nel registratore effettivo prima di cambiare modello o soglia; nessun rilassamento automatico. [Criticità](REGISTRO_CRITICITA_PIPELINE.md).
- [ ] **T09 — Selezione e ablation:** griglia sul sistema completo con punto 2 addestrato e copertura sufficiente; IDF1/mPCL, criterio secondario prefissato, tempi/fallimenti/copertura. Confrontare W0, memoria senza influenza sul matching, forme separate, accumulo SuperFlex e controllo punti. Congelare le scelte prima del test; se la memoria cambia molto, un riaddestramento del punto 2. [Metodo](MEMORIA_OPZIONE_A_E_SELEZIONE_20261122.md).
- [ ] **T10 — Punto 4:** fattibilità di scala, orientamento e collocazione della forma nella scena rispetto all'XYZ, trasformazioni inverse e aggiornamento dopo movimento. L'XYZ non determina R e scala; descrittore invariante e memoria collocata sono risultati diversi. Dopo punti 2/3.

## Produzione e consegna successive

- [ ] **T11 — Capacità e produzione P01_01:** integrare nel driver allineamento → archivio/verifica Drive → rilascio locale, lettori con recupero selettivo e arresto su trasferimento fallito; ricalcolare budget DA completo/MoGE campione, compresi allineamento e inode. Riprendere i blocchi mancanti solo dopo questi controlli; nessuna nuova produzione autorizzata dal solo riordino.
- [ ] **T12 — P01_02:** acquisire/verificare input, ambiente/pesi/risorse/quota del secondo HPC, prova comune P01_01 e pilota GPU/allineamento P01_02 prima della produzione. Driver/pacchetti già pronti; niente assegnazioni duplicate. Definire campione MoGE; estensione agli altri 55 video dopo costo e disponibilità degli input.
- [ ] **T13 — Provenienza/frontend:** chiudere provenienza JPEG/alias temporali e verifica baseline sul prefisso; completare il frontend comune dai dati originali (DINOv2/PCA/scena), mantenendo invariati segmentatore e GT. Non presumere equivalenza del JPEG dalla sola corrispondenza temporale.
- [ ] **T14 — Condivisione:** passaggio manuale del pacchetto mesh pronto e pubblicazione della [copia pulita preparata](../evidence/clean_update_20261122/README.md) solo quando richiesta, senza dati/pesi/accessi e preservando contributi/storia. Mappa opzione A già confermata e applicata ([esito](../evidence/map_20261122/ESITO_APPLICAZIONE.md)); ulteriori testi/strutture prima proposti e poi confermati. Tenere evidenze delle run fuori dalle schede generali.

## Secondari e residui da non perdere

- [ ] **T15 — Letteratura/indizi esterni:** recuperare testo della ricerca Consensus e verificare fonti; valutare contatto mano-oggetto VISOR come indizio, senza assumerlo prova di staticità.
- [ ] **T16 — Esiti storici incompleti:** se servono per confronto/riproducibilità, recuperare risultati 761899/761905 e documentare eventuale chiusura già attestata altrove; non rilanciare. Trasferimento collaborativo della mappa in Space sospeso (editor bloccato nella prova storica): non sostituisce l'HTML funzionante e non è priorità corrente.

## Attività già assorbite

Acquisizione P01_01 (110580 abbinate, dieci mancanti, zero conflitti), audit, compattazione, archivio dei 15 blocchi, recupero 0000–0003, nuvole v2, mappa/commenti e campagne concluse non vanno ripetuti. La prima run ha già verificato fusioni e SuperFlex causale; resta da validare il percorso corrente. Le vecchie griglie/piloti e il rinvio dell'ammissione sono superati dalle revisioni successive. [Archivio precedente al riordino](../archive/prima_consolidamento_20261122/README.md) conserva integralmente checklist ed esiti precedenti.
