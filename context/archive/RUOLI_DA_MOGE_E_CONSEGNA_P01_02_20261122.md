# Ruoli DA/MoGE e preparazione P01_02 — 22 novembre 2026

Aggiornamento esecutivo: [driver e pacchetti P01_02 implementati e verificati localmente](PACCHETTO_HPC_P01_02_20261122.md). Restano acquisizione dati e pilota HPC; le note sotto di implementazione assente sono storiche.

## Decisione approvata

Marco approva DA per la generazione completa e MoGE soltanto come confronto su un campione. Per la memoria geometrica resta valida la precedente scelta DA allineato alla mesh della scena con pose EPIC-Fields; il fallimento dell'allineamento impedisce la fusione. Distinguere sempre DA grezzo e allineato negli output. La nuova scelta supera le indicazioni storiche di eseguire entrambe le sorgenti su tutta la copertura; non autorizza la cancellazione dei risultati MoGE già prodotti.

Motivazione: concentrare le risorse sulla pipeline principale. Evidenze già raccolte: vantaggio modesto DA grezzo nella sagoma 2D, segnale favorevole a MoGE nel piccolo controllo d'identità, nessun vincitore nel tracking integrato. Non è dimostrata superiorità generale DA né equivalenza fra sorgenti. Riferimenti: [200 immagini](RISULTATI_CONFRONTO_200.md), [identità](RISULTATI_IDENTITA_DA_MOGE.md), [tracking](RISULTATI_CAMPAGNA_HPC_20261115.md).

Il compagno elaborerà P01_02; Marco mantiene P01_01. Non dividere le osservazioni dello stesso video fra i due account. P01_02 non diventa automaticamente test indipendente: condivide il partecipante P01; ruolo nello split da fissare prima di tuning/valutazione.

## Consegna concreta da preparare

1. Runtime effettivo congelato: shape_tools, backend DA, SuperFlex e dipendenze realmente usate; revisioni/hash, checkpoint DA e SuperFlex, configurazione effettiva. Ambiente con versioni bloccate e istruzioni per estensioni C++/Ninja. MoGE separato e opzionale per il campione.
2. Input ufficiali P01_02: lista originale frame/osservazioni e ordine detection, RGB, annotazioni/maschere VISOR, mapping temporale, intrinseci/risoluzione, pose e mesh EPIC-Fields necessarie all'allineamento. Verificare disponibilità e copertura; non copiare metadati o geometrie pregresse P01_01. Le feature DINO/PCA/XYZ e il checkpoint Whareformer non sono prerequisiti della sola generazione geometrica; serviranno al collegamento/valutazione del tracker.
3. Manifest portabile con video/frame/detection_idx/annotation_id/observation_key, percorsi relativi o radice configurabile, RGB/maschera e checksum, camera/pose, alias temporali, mancanti e conflitti espliciti. Nessuna identità fisica inventata dall'annotation_id.
4. Driver parametrico per video, radice dati, runtime, ambienti e risorse Slurm. Eliminare dipendenze implicite dalla campagna P01_01 e dal suo indice delle 446 geometrie; aggregazione limitata a P01_02. Configurare sources=[da] e saltare MoGE; verificare che cache, export e controlli non richiedano artefatti MoGE. Congelare esplicitamente pixel_policy: nel campione appaiato pixel comuni DA/MoGE; nella produzione DA nessuna dipendenza occulta dalla validità MoGE. Questa differenza va tracciata, senza presentarla come confronto appaiato.
5. Contratto di consegna: nuvole osservate DA con colori/pixel/provenienza, parametri e trasformazioni SuperFlex, riferimenti scena, stato di ogni rappresentazione e degli allineamenti; indice globale, checksum, log e riepilogo copertura. Forme completate distinte dai punti osservati. Politica PLY/intermedi coerente con i lettori e verificata prima della compattazione.
6. Script HPC del compagno: account/partizione/GPU, RAM, durata, quota byte/inode e guard; esecuzione per blocchi, ripresa e ricevute. Stima del costo totale da un blocco pilota: ridurre a DA non dimostra automaticamente il rientro nella quota.
7. Validazione prima della produzione: poche osservazioni P01_01 note per verificare l'ambiente (tolleranze numeriche dichiarate); piccolo lotto P01_02 per join, riproiezione, allineamento scena, stati e ripresa. Poi elaborazione completa DA.
8. Campione MoGE: sfruttare i confronti esistenti; se esteso a P01_02, fissare selezione e denominatore prima di osservare gli output, stesse osservazioni/configurazioni appaiate e fallimenti espliciti. Dimensione/composizione ancora non definite; nessun obbligo di MoGE completo.

## Stato effettivo

Documentazione aggiornata e dipendenze del driver locale lette. Il driver full_p01_enrichment.py contiene video P01_01, URL/percorsi e campagna pregressa fissi, ambienti personali e stadio MoGE nella sequenza: non è pronto per la consegna P01_02. La configurabilità delle sorgenti è presente nella copia locale di shape_tools.pipeline, ma la revisione effettiva da consegnare e il comportamento DA-only devono essere verificati. Input e capacità HPC del compagno non verificati. Nessun nuovo codice operativo, archivio di consegna, trasferimento, job, cancellazione o pubblicazione in questa fase; nessuna modifica della mappa.
