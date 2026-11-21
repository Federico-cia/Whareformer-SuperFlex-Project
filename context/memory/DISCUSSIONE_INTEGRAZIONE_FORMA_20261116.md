# Integrazione della forma: apprendimento e dati necessari

Discussione iniziale del 16 novembre 2026, conservata come storia. **Revisione successiva di Marco:** tentare entrambe le strade usando esclusivamente dati già etichettati; vietata nuova etichettatura manuale. La proposta storica di un campione manuale sotto è superata e non va eseguita. Direzione corrente e verifiche: [fattibilità delle due integrazioni](FATTIBILITA_DUE_INTEGRAZIONI_20261116.md), registro voce 81. Nessun nuovo protocollo dettagliato congelato o esperimento eseguito.

## Richiesta e criterio di Marco

Marco privilegia validità scientifica e coerenza con il trattamento degli altri input. Chiede una giustificazione concreta della stima del peso geometrico e dei dati necessari; in assenza di un metodo di stima convincente considera più sensato inserire il segnale nel modello e riaddestrarlo. Il costo computazionale è una sua preoccupazione, non una misura di fattibilità già acquisita. Scelta metodologica condivisa con il compagno ancora aperta.

## Trattamento originale verificato

Letti `Whareformer-repo/src/models/whareformer.py`, matcher originale, dataset/loss di training e configurazione EPIC. Riletto il [paper, §§3.2–3.7](https://arxiv.org/html/2607.08537).

- Aspetto: DINOv2 preaddestrato, normalizzazione/PCA/normalizzazione; configurazione EPIC a 256 dimensioni. Posizione: XYZ dalla pipeline geometrica. Estrattori distinti dal matcher addestrato.
- Per ogni coppia osservazione/track, il matcher seleziona separatamente i rappresentanti più vicini della memoria di aspetto e posizione. Il modello calcola distanza euclidea quadratica per aspetto ed euclidea per posizione.
- Due distanze concatenate alimentano `Linear(2, hidden_dim)`, ReLU, LayerNorm e dropout. Transformer, token Nuova track e classificatore producono i logits. Non esistono due coefficienti manuali globali che riassumano il contributo dei due input; combinazione e interazioni sono apprese.
- Il paper descrive teacher forcing con identità GT e memorie antecedenti all'osservazione; target = track corretta oppure Nuova track. Cross-entropy; il codice locale usa label smoothing 0.1.
- Configurazione EPIC locale: hidden_dim 64, depth 1. Non è dimostrato che adattare questo matcher richieda riaddestrare DINOv2/SuperFlex o sia computazionalmente impossibile. Tempo, dati e costo della generazione geometrica restano da stimare.

## Proposte di stima, non implementate

1. **Selezione sullo sviluppo:** griglia finita predefinita per peso e riferimento neutro; selezione mediante tracking completo con etichette, congelamento e valutazione separata. Basso sviluppo, costo di replay; un plateau non identifica un peso ottimo unico. Le 29 configurazioni già concluse sono un tale plateau, non una calibrazione riuscita.
2. **Fusione supervisionata minima:** logits proposti `z*_ij = zW_ij + m_ij (b - w d_ij)`, con `w >= 0`, indicatore di confronto valido `m`, nessuna correzione diretta a Nuova track. Imparare peso e intercetta mediante cross-entropy sulle associazioni corrette, con regolarizzazione. Baseline congelata e coefficiente fissato a uno: si stima una correzione relativa, non una percentuale di importanza. Per stati/memorie fissati, logits e distanze si possono precalcolare; l'ottimizzazione non richiede backpropagation nei due modelli. Il metodo è una proposta di fusione supervisionata, non mera calibrazione di probabilità né garanzia di beneficio. Disponibilità/mancanti e Nuova track vanno verificati. Rete completa non necessaria per questa stima.
3. **Ingresso geometrico nel matcher:** estendere l'embedding dalle due distanze a tre, con maschera di disponibilità. Possibile inizializzazione delle colonne originali dai pesi esistenti e colonna geometrica a zero; adattamento parziale o fine-tuning del matcher, con estrattori congelati. Non basta cambiare una dimensione per ottenere efficacia; costo e comportamento da verificare. Non adottato.

Il peso dipende dalla scala di distanza/logits e non misura il contributo intrinseco della forma. L'utilità aggiuntiva si valuta con confronto controllato rispetto alla baseline. Senza etichette affidabili la sola distribuzione delle distanze non identifica il peso utile all'associazione; riaddestrare richiede comunque supervisione o un diverso obiettivo da giustificare.

## Dati e limiti

Un esempio utile contiene osservazione corrente, memorie solo passate, logits originali per tutte le candidate inclusa Nuova track, distanze geometriche disponibili e associazione corretta. Servono corrispondenze d'identità, non mesh o distanze 3D ground truth e non un'etichetta numerica del peso. Includere alternative errate plausibili, ritorni dopo occlusione, nuove identità e geometria mancante; una sola categoria non certifica identità.

Il paper e il loader documentano manifest di training con target; disponibilità e join esatto fra tali target e le nostre osservazioni geometriche non sono stati verificati in questa discussione. Nel valutatore locale compaiono nomi oggetto: non assumerne senza verifica la granularità di identità fisica. Predizioni Whareformer/ID delle sue track non possono diventare automaticamente GT. Le 37 osservazioni/sette identità revisionate visivamente sono diagnostiche con limiti, non campione sufficiente dimostrato per apprendere e validare un peso generalizzabile. Le 446 osservazioni geometriche della campagna non sono 446 esempi indipendenti già etichettati per questo scopo.

Proposta: verificare prima i target originali e il join; se inadeguati, costruire un piccolo campione d'identità revisionato, scelto prima di leggere i punteggi e con casi ambigui espliciti. Separare stima, scelta delle opzioni e valutazione; nessuno split casuale di coppie che condividono osservazioni. Per conclusioni fuori scena separare scene/partecipanti; dichiarare eventuale esposizione del checkpoint originale ai dati di sviluppo. Non usare il test ufficiale per selezionare parametri.

Teacher forcing può servire per la prima stima, ma non prova utilità nel tracking: dopo divergenze le memorie predette cambiano, quindi serve replay causale completo su dati separati. Nessuna analisi quantitativa nuova, dataset aggiunto, run o modifica al metodo in questa discussione.
