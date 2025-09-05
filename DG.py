import random
import DB       # Contiene gli articoli e i loro parametri
import HLP      # Visualizza la legenda e i parametri dell'articolo e del programma
import UT       # Funzioni di supporto

def DataGenerator ():

    CSVheader = [  # Intestazione delle colonne del file CSV con solo i campi essenziali
        "Settimana", "Articolo", "Ore articolo", "Ore settimanali", "Stock", "Backlog", "Art. ordinati", "Art. da produrre", "Art. per Logistica", "Ore totali", "Ore disponibili",
        "Art. prodotti", "Overstock", "Art. per CQ", "Art. scartati", "Art. passed","Overstock t1", "Art. da spedire", "Art. spediti", "Backlog finale", "Stock finale"]
    CSVdata = []

    CSVheaderAI = [  # Intestazione delle colonne del file CSV con tutti i dati visualizzati
        "Settimana", "n", "Articolo", "Ore articolo", "Ore settimanali", "Stock", "Backlog", "Art. ordinati", "Art. da produrre", "Ore totali", "Art. per Logistica", "Ore disponibili",
        "Backlog t1", "Stock t1", "Art. prodotti", "Overstock", "Art. per CQ", "Art. scartati", "Art. passed","Overstock t1", "Stock t1", "Art. da spedire", "Art. spediti", "Backlog finale", "Stock finale"]
    CSVdataAI = []

    # Inizializzazione variabili prima del loop
    DB.Products = len (DB.ART)                                      # Numero prodotti presenti a catalogo
    HLP.SetShowInfo ()                                              # Visualizza i parametri usati del programma e l'intestazione della tabella

    for px in range(0, DB.Products):                                # Imposta i valori finali di stock e backlog che diventeranno quelli iniziali a inizio generazione dati
        UT.SetValue(px, "StockEnd", UT.RandomStockBacklog(px) if DB.flgStockInit else 0)
        UT.SetValue(px, "BacklogEnd", UT.RandomStockBacklog(px) if DB.flgBacklogInit else 0)

    for week in range(1, DB.Weeks + 1):                             # *** LOOP PER TUTTE LE SETTMANE
        if DB.flgProdCap == True: DB.ProdCap = UT.hProdCap()        # Determina la capacità produttiva della settimana
        for px in range(0, DB.Products):                            # *** LOOP PER OGNI PRODOTTO
            #*** WAREHOUSE ***
            # Set variabili iniziali
            Articolo = UT.GetValue (px, "articolo")
            StockInit = UT.GetValue(px, "StockEnd") if DB.flgStockInit else 0       # StockInit = 0 se DB.flgStockInit = False. StockInit = StockEnd se DB.flgStockInit = True
            BacklogInit = UT.GetValue(px, "BacklogEnd") if DB.flgBacklogInit else 0 # BacklogInit = 0 se DB.flgBacklogInit = False. BacklogInit = BacklogEnd se DB.flgBacklogInit = True
            StockEnd = BacklogEnd = 0

            #*** SALES OFFICE ***
            hArt = UT.GetValue (px, "ArtHours")                     # Tempo necessario per produrre l'articolo
            Orders = UT.RandomOrders (px)                           # Numero ordini "ricevuti"
            UT.SetValue (px, "Orders", Orders)                      # Memorizza il numero di ordini "ricevuti"

            # Analisi ordini (recenti e passati [orders e backlog]), stock e tempi per produrre un articolo e disponibilità temporale produzione
            Arts2prd, Arts2log, BacklogT1, StockT1, hLeft = UT.SALES (Orders, BacklogInit, StockInit, hArt, DB.ProdCap)
            hArts = Arts2prd * hArt                                 # Tempo necessario per produrre gli articoli ordinati

            #*** PRODUCTION ***
            ArtsMade = Arts2prd
            # Overstock
            if DB.flgOverStock == False: OverStk = 0; StockT2 = StockT1
            else: OverStk = UT.PROD_OVERSTOCK (hArt, hLeft, StockT1)
            Arts2CQ = ArtsMade + OverStk

            #*** QUALITY ***
            if DB.flgCQprod == False:   ArtsScraps = 0              # Nessun articolo viene scartato
            else: ArtsScraps = random.randint(0,px)                 # Scarto articoli generato casuale... potrebbe essere anche zero
            ArtsOK, OverStkT1, ArtsScraps, StockT2 = UT.QUALITY (ArtsMade, OverStk, ArtsScraps, StockT1)
            StockT2 = StockT2 + OverStkT1                           # L'overstock si aggiunge allo stock

            #*** LOGISTICS ***
            ArtsReady = ArtsOK + Arts2log
            if DB.flgLogCap == False: sLogCap = "fix"; LogCap = 0
            else: sLogCap = "flx"; LogCap = random.randint(0,px)   # Riduzione capacità logistica casuale... potrebbe essere anche zero
            if (ArtsReady - LogCap) < 0: sLogCap = "fix"; LogCap = 0
            ArtsSent = ArtsReady - LogCap

            #*** WAREHOUSE ***
            StockEnd = StockT2 + LogCap
            UT.SetValue (px, "StockEnd", StockEnd)

            #*** SALES ***
            BacklogEnd = BacklogT1 + LogCap
            UT.SetValue (px, "BacklogEnd", BacklogEnd)

            CK = (StockInit + ArtsMade + OverStk) - (ArtsSent + ArtsScraps + StockEnd)      # Verifica di coerenza dati per ordini e prodotti (valore atteso -> ck = 0)

            print(  # Stampa riga articolo
                f"{week:1d}|{Articolo:6}{hArt:2d}{DB.ProdCap:3d}|{StockInit:5d}|{BacklogInit:5d}{Orders:5d}{Arts2prd:5d}{Arts2log:5d}{hArts:5d}{hLeft:5d}{BacklogT1:5d}|{StockT1:5d}"
                f"|{ArtsMade:5d}{OverStk:5d}{Arts2CQ:5d}|{ArtsScraps:5d}{ArtsOK:5d}{OverStkT1:5d}|{StockT2:5d}|{ArtsReady:5d}{sLogCap:>4}{ArtsSent:5d}|{BacklogEnd:5d}|{StockEnd:5d}|{CK:2d}")

            CSVrow = [                      # Solo i campi essenziali
                week, Articolo, hArt, DB.ProdCap, StockInit, BacklogInit, Orders, Arts2prd, Arts2log, hArts, hLeft, ArtsMade, OverStk, Arts2CQ, ArtsScraps, ArtsOK, OverStkT1, ArtsReady, ArtsSent,
                BacklogEnd, StockEnd]
            CSVdata.append (CSVrow)         # Salvataggio dati in formato CSV

            CSVrowAI = [                    # Tutti i campi
                week, px+1, Articolo, hArt, DB.ProdCap, StockInit, BacklogInit, Orders, Arts2prd, Arts2log, hArts, hLeft, BacklogT1, StockT1, ArtsMade, OverStk, Arts2CQ, ArtsScraps, ArtsOK, OverStkT1,
                StockT2, ArtsReady, ArtsSent, BacklogEnd, StockEnd]
            CSVdataAI.append (CSVrowAI)     # Salvataggio dati in formato CSV

            if (px+1)%DB.Products == 0:
                HLP.ViewWeekInfo ()         # Visualizzazione info dati settimanali
                print("---------------------------------------------------------------------------------------------------------------------------------")
   
    UT.WriteCSV(DB.CSVfile, CSVheader, CSVdata, False)          # Scrittura file con i soli campi essenziali
    UT.WriteCSV(DB.CSVfileAI, CSVheaderAI, CSVdataAI, True)     # Scrittura file con tutti i dati visualizzati

# MAIN
if __name__ == "__main__": DataGenerator (); print("")