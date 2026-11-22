# Prima run completa Whareformer–SuperFlex — P01_01

Esecuzione terminata sul protocollo completo delle feature ufficiali; ciclo geometricamente attivo e ritorno delle ricostruzioni da fusioni ai confronti successivi verificati. Nessun miglioramento del tracking con questa configurazione. Risultati del 14 novembre 2026, video di sviluppo/train.

## 1. Estensione effettivamente elaborata

Tutti i **33310 frame con feature e 110590 osservazioni** ufficiali, nello stesso ordine della baseline; primo frame 937, ultimo 98099, nessun arresto al vecchio limite 7508. Il CSV originale riporta **99135 frame** a 59.94005994 fps, convertiti a 60 dalla convenzione originale. Anche il tracker originale visita soltanto i frame presenti nelle feature: questa è una run completa del suo protocollo, non l'elaborazione RGB di ogni fotogramma del file video. Orizzonte finale di valutazione 99135.

Geometria disponibile su **71 osservazioni in 38 frame**: 0.0642011% delle osservazioni e 0.11408% dei frame del protocollo. Nei restanti 110519 casi l'aggiornamento geometrico è dichiarato mancante e resta il percorso aspetto/XYZ; due join con alias non certificati rimangono esclusi. Questa limitazione impedisce di rivendicare geometria attiva su ogni frame o copertura adeguata a conclusioni generali.

## 2. Componenti eseguiti e provenienza

| Componente | Operazione effettiva |
|---|---|
| Frontend delle osservazioni | Riusati feature ufficiali DINOv2/PCA 256d e XYZ allineati alla scena; non rigenerati dalle immagini |
| Geometria delle osservazioni | Riusati punti camera DA e forme SuperFlex precedentemente prodotte; join esatti e hash verificati |
| Whareformer | Nuova inferenza del checkpoint originale congelato, softmax e assegnazione greedy degli autori |
| Confronto geometrico | D2, memoria precedente a tutte le query del frame; peso 0.1, distanza neutra 0, capacità forme separate 2 |
| Aggiornamento | Nuove proposte dalle associazioni effettive; registrazione rigida e filtri precedenti invariati; massimo 4 viste, 2048 punti/vista, osservazione limitata a 12000 punti |
| SuperFlex della memoria | **25 nuove inferenze reali**, checkpoint robust verificato, dopo ciascuna ammissione; nessun risultato neurale storico importato nella nuova cache |
| Valutazione e consegna | IDF1/mPCL originali, JSONL completi, memoria finale, parametri/mesh e audit verificati |

Nessun nuovo training, fit PCA, segmentatore, ricostruzione MVS o ottimizzazione dei filtri. Configurazione provvisoria per dimostrazione operativa, non calibrata per efficacia. DA come primo ramo già disponibile; nessuna superiorità su MoGE dedotta.

**Fedeltà e adattamenti.** Riletti PDF Whareformer §§3.2–3.7 (pp. 5–8) e SuperFlex §§4.1–4.3/5.3 (pp. 5–8 e 12), confrontati con codice originale. Riusati reti/checkpoint, matcher, gestione aspetto/posizione, inferenza robust, normalizzazione e inversa. Il campionamento casuale a 4096 punti segue la demo degli autori; il benchmark canonico usa invece FPS. Il ponte D2, la correzione dei logits, la registrazione temporale e la memoria limitata sono adattamenti nostri. Non applicata l'ottimizzazione test-time che nel paper usa anche occupazione completa. Le coordinate camera della forma, quelle scena degli XYZ e le normalizzazioni restano distinte; scala inter-vista e orientamento canonico non certificati.

## 3. Aggiornamenti, fusioni e ritorno al matcher

| Esito | Conteggio |
|---|---:|
| Inizializzazioni geometriche | 18 |
| Fusioni successive ammesse | 7 |
| Aggiornamenti rifiutati | 46 |
| Errori di aggiornamento / ricostruzione | 0 / 0 |
| Ricostruzioni SuperFlex riuscite | 25 |
| Richieste rimaste pendenti | 0 |
| Memorie geometriche finali | 18 track, 38732 punti osservati |

Le sette fusioni riguardano track predette, non identità fisiche certificate: track 4 (annotazione «chopping board») al frame 23269; track 35 (annotazione «pan») ai frame 57932, 65241, 77312, 81277, 86858 e 91092. Track 4 termina alla versione 2 con due viste; track 35 alla versione 7 con ancora e tre viste recenti conservate dalla politica FIFO. Le osservazioni provengono da frame distinti e i punti finali sono ricostruibili dalle osservazioni originali e dalle trasformazioni rigide salvate.

**695 coppie** hanno logits realmente modificati, variazione assoluta massima 0.03434743. Tutte interrogano ricostruzioni reali precedenti; **76 coppie in 28 frame** usano ricostruzioni successive a fusioni. Esempio verificato: inizializzazione track 4 al 2893 → fusione al 23269/versione 2 → nuova SuperFlex → confronto del 25902, distanza D2 0.04683498 e correzione effettiva −0.00468350. Il ciclo supera quindi il solo replay del tracking e le sole inizializzazioni.

Nei 46 rifiuti: supporto insufficiente in 39, residui eccessivi in 33, ambiguità in 34; motivi non mutuamente esclusivi. Non modificate soglie o registratore per ottenere le fusioni. L'ammissione software e la ricostruibilità dei punti dimostrano accumulo multivista eseguito; non sono verifica indipendente della correttezza fisica delle pose o dell'identità.

## 4. Metriche, controlli e costi

**52 track, zero differenze nelle 110590 assegnazioni rispetto alla baseline registrata.** IDF1 **73.2697350574193%**, mPCL originale **70.46550449586454%**: nessun miglioramento con il peso 0.1. Non è un test held-out né prova che ogni altra configurazione non possa migliorare. Convenzione originale per nomi e XYZ stimati, non nuova GT fisica; mPCL sulle 145 scale originali, incluse quelle non supportate secondo il protocollo.

Job **764454 COMPLETED 0:0, 8m40s**, gnode02: 72 test tutti eseguiti e passati, inferenza completa, worker reali, valutazione e confronto. Tempo interno del ciclo circa 412.59 s; worker 46.80 s incluso nel ciclo; registrazione 93.33 s inclusa nel coordinatore. Non sommare tempi annidati. Preparazione, vecchie estrazioni delle cache e trasferimenti esclusi da questi tempi. Picco allocato PyTorch SuperFlex riportato circa 43.47 MB, non misura della memoria totale GPU/processo.

Job **764474 COMPLETED 0:0, 53s**: audit e valutazione finale. La prima valutazione automatica usava erroneamente 98099 come orizzonte; è conservata come intermedia e superata da `final_evaluation/` e `final_comparison/`, calcolati a 99135 senza rifare l'inferenza. L'esempio corrente è corretto.

Audit: tutti i frame/chiavi in ordine, hash validi, evidenze delle query strettamente precedenti al frame, richieste legate a versioni/stati, una ricostruzione per ammissione, memoria finale uguale al cloud dell'ultima richiesta. Verifica indipendente locale: punti ricostruiti dalle sole osservazioni ammesse e trasformazioni; scarto massimo **2.22e−16**, entro il limite di verifica derivato dall’aritmetica float64 `32 epsilon × max(1, max|cloud|)`. Il primo controllo con uguaglianza bit a bit falliva solo per questa differenza di moltiplicazione matriciale fra piattaforme; nessun gate geometrico cambiato. Restano validi gli hash byte a byte dei file originali e l'uguaglianza memoria↔richiesta.

## 5. Output e criticità residue

- [Diagnostica temporale e nuvole](../evidence/ASSET_ESTERNI.md#asset-6acd7e9b18f9).
- [Audit esteso con eventi di fusione](../evidence/ASSET_ESTERNI.md#asset-58ff1da039d5).
- [Tutti i risultati, incluse tracce/memoria/ricostruzioni](../evidence/ASSET_ESTERNI.md#asset-b45b48fe3117).
- [Tabella finale](../evidence/ASSET_ESTERNI.md#asset-ac7e70020c10) e [riepilogo valutazione](../evidence/ASSET_ESTERNI.md#asset-c2f4a7600dc2).
- [Bundle di ingresso verificato](../evidence/ASSET_ESTERNI.md#asset-7f314a0c87f2); [archivio risultati](../evidence/ASSET_ESTERNI.md#asset-9cc362b332d5).

Directory HPC: `~/cv_project/full_video_20261114_v1/`; pipeline `run_764454/`, richieste/mesh/primitive `cache_764454/`, valutazione autorevole `final_evaluation/`, confronto `final_comparison/`, audit `audit/`. Localmente l'audit esteso è in `results/audit_extended/`. Tutti gli output completi scaricati; pesi e input grandi esclusi dalla pubblicazione GitHub.

Restano: frontend rigenerato da RGB e provenienza DINOv2/PCA/scena; copertura geometrica molto ridotta; accuratezza fisica e utilità delle fusioni da valutare con evidenze indipendenti; simmetrie, scala inter-vista e pose; revisione dei filtri ancora esplicitamente rinviata; calibrazione del contributo geometrico e successivo test separato. Non occorre negare le fusioni ora eseguite, ma non attribuire loro accuratezza o beneficio non misurati. Nessun job di questa esecuzione rimane attivo o in attesa.
