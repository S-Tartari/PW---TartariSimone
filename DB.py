# COSTANTI
COMPANY = "Sempre piu' in Alto!"        # Nome azienda
TITLE = "DataGenerator"                 # Nome script
AUTHOR = "Simone Tartari"               # Autore
VERSION = "7"                           # Versione del programma
Weeks = 8                               # N° di settimane per la simulazione
CSVfile = "PRODOTTI.csv"                # Nome del file CSV
CSVfileAI = "PRODOTTI[all_info].csv"    # Nome del file CSV con tutti dati visualizzati a video
Products = None                         # N° di prodotti a catalogo
ProdCap = 40                            # N° di ore lavorative per settimana [default]
ProdCapMIN = 24                         # N° minimo di ore lavorative per settimana [3 giorni]
ProdCapMAX = 48                         # N° di ore lavorative per settimana [6 giorni]
CQprodMAX = 5                           # Percentuale massima di scarto pezzi


# FLAGS PER DATAGENERATOR
flgProdCap = None                       # [False] La capacita' produttiva NON PUO' subire variazioni - [True] La capacita' produttiva PUO' subire variazioni
flgOverStock = None                     # [False] NON PUO' essere prodotto overstock - [True] PUO' essere prodotto overstock
flgCQprod = None                        # [False] NON VIENE applicato casualmente uno scarto - [True] VIENE applicato casualmente uno scarto
flgLogCap = None                        # [False] La capacità logistica NON PUO' subire variazioni - [True] La capacita' logistica PUO' subire variazioni
flgStockInit = None                     # [False] Tutti i prodotti NON HANNO uno stock iniziale - [True] Tutti i prodotti HANNO uno stock iniziale casuale 
flgBacklogInit = None                   # [False] Tutti i prodotti NON HANNO un backlog iniziale - [True] Tutti i prodotti HANNO un backlog iniziale casuale 

Debug = False                           # il flag può essere usato a scopo di debug

ART = [ # DATABASE ARTICOLI
    {
    "id": 1,                            # Codice prodotto
    "articolo": "Tenda",                # Descrizione prodotto
    "ArtHours": 16,                     # Tempo di produzione in ore di un articolo
    "StockInit": None,                  # WAREHOUSE - Stock iniziale 
    "StockEnd": None,                   # WAREHOUSE - Stock finale
    "Orders": None                      # SALES - N° ordini ricevuti
    },
    {
    "id": 2,                            # Codice prodotto
    "articolo": "Zaino",                # Descrizione prodotto
    "ArtHours": 8,                      # Tempo di produzione in ore di un articolo
    "StockInit": None,                  # WAREHOUSE - Stock iniziale
    "StockEnd": None,                   # WAREHOUSE - Stock finale
    "Orders": None                      # SALES - N° ordini ricevuti 
    },
    {
    "id": 3,                            # Codice prodotto
    "articolo": "Sacco",                # Descrizione prodotto
    "ArtHours": 4,                      # Tempo di produzione in ore di un articolo
    "StockInit": None,                  # WAREHOUSE - Stock iniziale
    "StockEnd": None,                   # WAREHOUSE - Stock finale
    "Orders": None                      # SALES - N° ordini ricevuti 
    },
    {
    "id": 4,                            # Codice prodotto
    "articolo": "Pile",                 # Descrizione prodotto
    "ArtHours": 2,                      # Tempo di produzione in ore di un articolo
    "StockInit": None,                  # WAREHOUSE - Stock iniziale
    "StockEnd": None,                   # WAREHOUSE - Stock finale
    "Orders": None                      # SALES - N° ordini ricevuti 
    },
    {
    "id": 5,                            # Codice prodotto
    "articolo": "Guanti",               # Descrizione prodotto
    "ArtHours": 1,                      # Tempo di produzione in ore di un articolo
    "StockInit": None,                  # WAREHOUSE - Stock iniziale
    "StockEnd": None,                   # WAREHOUSE - Stock finale
    "Orders": None                      # SALES - N° ordini ricevuti 
    }
]