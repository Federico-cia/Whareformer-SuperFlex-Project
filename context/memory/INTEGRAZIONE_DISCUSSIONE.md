# Interfaccia geometrica e integrazione Whareformer

> Aggiornamento 12 novembre: parte autonoma consegnata; stato e limiti correnti in [CONSEGNA_RAMO_GEOMETRICO.md](CONSEGNA_RAMO_GEOMETRICO.md). Le attività autonome indicate come future nelle sezioni storiche sono superate; restano aperte integrazione e valutazione sulla baseline reale.


Consolidamento dell'11 novembre 2026. Stato operativo e piano esecutivo in `STATO_LAVORO.md` e `PIANO_CHIUSURA_RAMO_GEOMETRICO.md`; decisioni storiche nel registro.

## Vincoli approvati

La forma è un segnale aggiuntivo per l'identità; feature visive e XYZ Whareformer restano invariati. DA e MoGE sono opzioni della stessa interfaccia, con controllo geometrico sui punti. Forma corrente e forme della memoria devono essere stimate con SuperFlex nel ramo SuperFlex.

L'unità è l'osservazione di un oggetto. Input e convenzioni già verificati in `docs/INPUT_SUPERFLEX_PER_WHAREFORMER.md`: nuvola camera, non singolo XYZ, preprocessing SuperFlex distinto dalla normalizzazione per il confronto. Conservare provenienza e collegamento a video/frame/maschera. `annotation_index` non va dichiarato uguale a `detection_idx` prima della verifica sulla baseline.

## Componente autonomo da completare

Preparare export, caricamento, confronto e memoria configurabile senza dipendere dal codice modificato del tracker. Le verifiche su sequenze sintetiche/registrate dimostrano il comportamento del componente, non un beneficio tracking. Distinguere identità annotate usate per valutazione diagnostica e associazioni predette usate dal metodo.

La memoria legge soltanto forme precedenti e si aggiorna dopo l'associazione. Forme mancanti devono essere esplicite e consentire il comportamento della baseline. Una o poche ricostruzioni senza fusione sono il candidato iniziale; capacità, ammissione, sostituzione e aggregazione delle distanze restano da validare. Non mediare parametri di primitive non corrispondenti.

Confrontare superfici campionate o descrittori documentati, non vettori grezzi di primitive. Gestire scala e rotazione esplicitamente: RMS elimina la dimensione assoluta; l'allineamento dell'output non corregge la sensibilità del predittore all'orientamento dell'input. Non assumere scala metrica affidabile o posa canonica oracle.

## Candidato di collegamento, non metodo definitivo

Reti inizialmente congelate; correzione dei logits prima della softmax, mantenendo il matcher greedy originale. Candidato discusso:

`z(n,k) = zW(n,k) + lambda * m(n,k) * (tau - dS(n,k))`

`m=0` per forme mancanti; `dS` è una distanza dalla memoria da validare. Minimo fra forme passate, soglia neutra `tau` e peso `lambda` sono proposte, non valori già fissati. Il logit New Track resterebbe originale, ma la rinormalizzazione può cambiarne la probabilità. Peso zero deve recuperare la baseline. La concatenazione di una terza distanza nell'embedding richiederebbe invece adattamento del modello.

Calibrare sullo sviluppo includendo peso zero, congelare le scelte prima del test. Nella valutazione tracking usare associazioni predette, senza identità oracle o osservazioni future. Misurare metriche ufficiali, fusioni errate, frammentazione, copertura e costo. Contributo nullo o negativo della forma resta un risultato valido.

Fusione delle nuvole con nuova inferenza, SAM3 e memoria robotica non sono prerequisiti del lavoro approvato. Le esplorazioni concettuali restano in `OPZIONI_FORMA_E_MEMORIA_ROBOTICA.md` e `RICOGNIZIONE_MEMORIA_GEOMETRICA_ROBOTICA.md`, senza nuovo obiettivo adottato.
