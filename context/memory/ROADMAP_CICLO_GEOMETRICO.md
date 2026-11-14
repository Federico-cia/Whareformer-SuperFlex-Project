# Ciclo geometrico approvato

Le due direzioni SuperFlex → Whareformer e Whareformer → SuperFlex sono parti di un ciclo unitario.

1. Estrarre la geometria dell'oggetto osservato nel frame e la sua rappresentazione di forma.
2. Confrontarla con la memoria geometrica delle track al termine del frame precedente. Tutte le detection del frame interrogano lo stesso stato precedente.
3. Correggere il matcher conservando aspetto/XYZ della baseline e lasciare a Whareformer l'assegnazione effettiva.
4. Per ogni assegnazione, proporre registrazione e accumulo dei soli punti osservati; registrare separatamente inizializzazione, fusione, rifiuto ed errore.
5. Dopo ogni aggiornamento ammesso, eseguire SuperFlex e pubblicare la forma per confronti nei frame successivi. Non usare completazioni come nuovi punti osservati.

DA e MoGE rimangono fonti separate. Distinguere coordinate camera della forma, coordinate scena/XYZ della baseline e normalizzazioni del confronto da quelle di ingresso a SuperFlex. Un nuovo video richiede nuove istanze e memorie. Il replay seriale con cache non è una ripresa generale da checkpoint.

Controlli: W0 baseline, G0 zero, forma separata, forma da accumulo e punti da accumulo; reti congelate, stesso budget geometrico dichiarato e tracker indipendenti. Gli esempi zero verificano la compatibilità del codice, non l'utilità del metodo.

Il protocollo originale IDF1/mPCL usa nomi oggetto e XYZ stimati: non certifica identità fisiche indipendenti. Mantenere scope, split e provenienza espliciti; non confrontare metriche del prefisso con il video completo.

Implementazione, risultati e prossime attività: [stato](STATO_LAVORO.md), [roadmap](ROADMAP.md), [codice](../../integration_prototype/README.md). Motivazioni e revisioni storiche: [registro](REGISTRO_DECISIONI.md) e [archivio](README.md). La revisione dei filtri resta esplicitamente rinviata da Marco.
