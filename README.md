# Project Work - “Sempre più in Alto!”

## 📌 Descrizione del progetto

Questo repository contiene un'applicazione in Python che simula il flusso produttivo di un'azienda del settore secondario attraverso l'elaborazione settimanale di ordini, produzione, stock, backlog, controllo qualità e logistica. Il progetto ha, inoltre, una **dashboard interattiva** sviluppata in Streamlit per l’analisi dei risultati generati.


## 👤 Autore

- **Nome e Cognome**: Simone Tartari
- **Matricola**: 0312201761
- **Corso di Laurea**: Informatica per le Aziende Digitali (L-31)  
- **Anno Accademico**: 2024/2025

## 📓 Tema

- **Titolo del tema**: La digitalizzazione dell’impresa
- **Titolo della traccia**: Sviluppo di un codice Python per simulare un processo produttivo nel settore secondario
- **Traccia del project work**: Traccia n.1.5
- **Titolo dell'elaborato**: “Sempre più in Alto!”

## 🗂️ Struttura del repository

- `DB.py`  
  Definisce le costanti di simulazione e il catalogo dei prodotti.
- `DG.py`  
  Contiene la funzione `DataGenerator` per generare i dati settimanali.
- `UT.py`  
  Raccolta di funzioni ausiliarie (gestione ordini, scarti, stock, CSV, ecc.)
- `HLP.py`  
  Visualizzazione dei parametri e legenda da grafica terminale durante l’esecuzione.
- `Dashboard.py`  
  Dashboard per l’analisi grafica.
- `PRODOTTI.csv`  
  Output sintetico della simulazione.
- `PRODOTTI[all_info].csv`  
  Output completo con tutte le variabili generate.

## 🛠 Tecnologie Utilizzate

- **Python 3.x**
- **Streamlit** – per l'interfaccia web interattiva
- **Pandas** – per la manipolazione dei dati
- **Plotly Express** – per i grafici dinamici
- **Librerie standard**: `os`, `random`, `csv`, `math`, `sys`

## ⚙️ Come utilizzare il progetto (WindowsOS)

### 1. Esecuzione della simulazione
Eseguire il file `DG.py` per generare i dati simulati su più settimane:
```bash
python .\DG.py
```
Verranno creati i file `PRODOTTI.csv` e `PRODOTTI[all_info].csv`.

### 2. Avvio della dashboard interattiva
Per avviare la dashboard con i dati generati:
```bash
python -m streamlit run .\Dashboard.py
```
Una volta avviata, sarà possibile:
- Filtrare i dati per settimana e articolo
- Visualizzare KPI come stock, backlog, spedizioni, scarti
- Analizzare l’efficienza produttiva per articolo
- Consultare la tabella dati completa

## 🔎 Funzionalità principali

- ✅ Simulazione completa delle fasi aziendali: Magazzino, Vendite, Produzione, Qualità, Logistica
- 🧠 Gestione automatica di ordini, stock iniziali, backlog e scarti
- 🔁 Parametri configurabili: capacità produttiva e logistica variabile, overstock, controllo qualità
- 📊 Dashboard Streamlit con grafici, filtri e indicatori chiave
- 🧪 Verifica settimanale della coerenza dei dati (check `ck = 0`)
- 📁 Output esportabile in CSV per ulteriori analisi

## 📈 Esempio di flusso simulato

Ogni settimana, per ogni prodotto:
1. Ricezione ordini
2. Calcolo della produzione possibile
3. Simulazione del controllo qualità
4. Spedizione dei prodotti disponibili
5. Calcolo finale di backlog e stock

## 🧩 Requisiti

- Python ≥ 3.8
- Streamlit installato (`pip install streamlit`)
- Pandas e Plotly installati (`pip install pandas plotly`)

## 📄 Licenza

Progetto realizzato a fini didattici. Tutti i diritti sono riservati all’autore.
