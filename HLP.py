import random
import math
import DB       # Contiene gli articoli e i loro parametri
import UT       # Funzioni di supporto

def Legenda ():
    print("\nLEGENDA")
    print("\tw = n° della settimana")
    print("\tProd = articolo")
    print("\tHA = ore per produrre un articolo")
    print("\tHP = ore settimanali della Produzione. Possono essere variabili ogni settimana")
    print("")
    print("\tW/hse->Stock init = stock articoli disponibili a magazzino")
    print("\tSales Office->Bcklg init = backlog articoli richiesti precedentemente")
    print("\tSales Office->Arts ord = articoli richiesti in questo periodo")
    print("\tSales Office->Arts 2prd = articoli da produrre rapportando le ore disponibili per le ore per produrli")
    print("\tSales Office->Arts 2log = articoli richiesti, già presenti a stock, per la Logistica")
    print("\tSales Office->Hrs arts = ore necessarie alla Produzione per produrre gli articoli richiesti")
    print("\tSales Office->Hrs left = ore che la Produzione avanza nel produrre gli articoli richiesti")
    print("\tSales Office->Bcklg T1 = backlog degli articoli richiesti dopo analisi disponibilità produzione")
    print("\tW/hse->Stock T1 = stock articoli disponibili a magazzino dopo analisi backlog e ordini")
    print("")
    print("\tProduction->Arts made = articoli prodotti")
    print("\tProduction->Over stck = eventuali articoli prodotti a saturazione delle ore della Produzione")
    print("\tProduction->Arts 2CQ = articoli prodotti e overstock da far controllare dalla Qualità")
    print("")
    print("\tQuality->Arts scraps = articoli che non hanno superato il controllo qualità")
    print("\tQuality->Arts OK = articoli che hanno superato il controllo qualità")
    print("\tQuality->Over stT1 = overstock che hanno superato il controllo qualità")
    print("\tW/hse->Stock T2 = stock articoli disponibili a magazzino dopo analisi")
    print("")
    print("\tLogistics->Arts ready = articoli disponibili a essere spediti")
    print("\tLogistics->Cap = capacità della Logistica per la spedizione")
    print("\tLogistics->Arts sent = articoli effettivamente spediti")
    print("")
    print("\tSales->Blklg end = articoli richiesti, ma che non si sono potuti produrre")
    print("\tW/hse->Stock end = articoli presenti a stock")
    print("")
    print("\tck = la colonna fornisce un controllo sui dati di ogni riga. Se è 0, i dati sono corretti")

def Params ():
    print("\nPARAMETRI SIMULAZIONE")
    print(f"\n\t- N° di settimane per l'analisi: {DB.Weeks}")
    print(f"\t- N° di prodotti a catalogo: {DB.Products}")
    
    # MAGAZZINO - Stock iniziale
    if DB.flgStockInit == False: # Stock iniziale = 0 per tutti i prodotti
        for p in range(0,DB.Products): UT.SetValue (p, "StockInit", 0)
        print("\n\t- Warehouse - Nessun articolo ha uno stock iniziale")
    else:   # Generazione di uno stock casuale per ogni prodotto
        for p in range(0,DB.Products): UT.SetValue (p, "StockInit", random.randint(1,DB.Products*2))
        print("\t- Warehouse - Tutti gli articoli possono avere uno stock iniziale")
    
    # VENDITE - Backlog
    if DB.flgBacklogInit == False: # Backlog iniziale = 0 per tutti i prodotti
        for p in range(0,DB.Products): UT.SetValue (p, "BacklogInit", 0)
        print("\t- Sales Office - Backlog - Nessun articolo ha un backlog iniziale")
    else:   # Generazione di uno backlog casuale per ogni prodotto
        for p in range(0,DB.Products): UT.SetValue (p, "BacklogInit", random.randint(1,DB.Products*2))
        print("\t- Sales Office - Tutti gli articoli possono avere un backlog iniziale")
 
    # PRODUZIONE
    if DB.flgOverStock == False: print("\t- Produzione - Overstock non ammesso")
    else: print("\t- Produzione - Overstock ammesso")
    if DB.flgProdCap == False: print(f"\t- Produzione - Capacità produttiva: {DB.ProdCap}h")
    else: print(f"\t- Produzione - Capacità produttiva: {DB.ProdCap}h, variabile tra {DB.ProdCapMIN}/{DB.ProdCapMAX}h a seconda della settimana")
    
    # CONTROLLO QUALITA'
    if DB.flgCQprod == False: print(f'\t- Controllo Qualità - Articoli non soggetti a controllo qualità')
    else: print(f'\t- Controllo Qualità - Articoli soggetti a controllo qualità')
    
    # LOGISTICA
    if DB.flgLogCap == False: print(f'\t- Logistica - Capacità logistica non soggetta a variazioni')
    else: print(f'\t- Logistica - Capacità logistica variabile')

def TableHeader ():
    print("")
    print("=================================================================================================================================")
    print("")
    print("Brand: "+DB.COMPANY+" - "+DB.TITLE+" per simulare un flusso produzionale aziendale\t\t\t\t  [v"+DB.VERSION+"]")
    print("")
    print("             ------------------------------------------------------------------------------------------------------------------")
    print("             |W/hse|Sales Office                       |W/hse|Production     |Quality        |W/hse|Logistics     |Sales|W/hse|")
    print("             |-----------------------------------------------------------------------------------------------------------------")
    print("-+-----------|Stock|Bcklg Arts Arts Arts Hrs  Hrs Bcklg|Stock| Arts Over Arts|Arts  Arts Over|Stock|Arts      Arts|Bcklg|Stock|--")
    print("w| Prod HA HP| init| init  ord 2prd 2log arts left   T1|   T1| made stck  2CQ|scrps   OK stT1|   T2|ready Cap sent|  end|  end|ck")
    print("---------------------------------------------------------------------------------------------------------------------------------")

def ViewWeekInfo ():
    if DB.flgProdCap == False: print (f"Capacità produttiva: {DB.ProdCap}h ore", end=' ')
    else: print (f"Capacità produttiva: {DB.ProdCap}h", end=' ')
    if DB.flgOverStock == False: print("- Overstock: NO", end=' ')
    else: print("- Overstock: SI", end=' ')
    if DB.flgCQprod == False: print('- Controllo Qualità: NO', end=' ')
    else: print(f'- Controllo Qualità: SI', end=' ')
    if DB.flgLogCap == False: print('- Capacità logistica variabile: NO')
    else: print(f'- Capacità logistica variabile: SI')

def SetShowInfo ():
    print("\n"+DB.TITLE+" by "+DB.AUTHOR)

    # Impostazioni
    if UT.Yes_No("\n- Si desidera impostare manualmente tutte le impostazioni?", default='N') == 'Y':                           # Definisce se le impostazioni siano generate manualmente o automaticamente
        # Impostazioni manuali
        DB.flgStockInit = UT.Yes_No("\n- Si desidera che i prodotti abbiano uno stock iniziale?", default='Y') == 'Y'           # Definisce un eventale stock iniziale
        DB.flgBacklogInit = UT.Yes_No("- Si desidera che i prodotti abbiano un backlog iniziale?", default='Y') == 'Y'          # Definisce un eventale backlog iniziale
        DB.flgOverStock = UT.Yes_No("- Si desidera produrre overstock, se possibile?", default='Y') == 'Y'                      # Definisce se sia possibile produrre overstock
        DB.flgProdCap = UT.Yes_No("- Si desidera una capacità produttiva oraria variabile?", default='Y') == 'Y'                # Definisce se la capacità produttiva possa essere variabile
        DB.flgCQprod = UT.Yes_No("- Si desidera abilitare il controllo qualità?", default='Y') == 'Y'                           # Imposta se la produzione sia soggetta a controllo qualità
        DB.flgLogCap = UT.Yes_No("- Si desidera una capacità logistica variabile?", default='Y') == 'Y'                         # Imposta se la capacità logistica possa essere variabile
    else:
        DB.flgStockInit = random.choice([True, False])      # Definisce un eventale stock iniziale
        DB.flgBacklogInit = random.choice([True, False])    # Definisce un eventale backlog iniziale
        DB.flgOverStock = random.choice([True, False])      # Definisce se sia possibile produrre overstock
        DB.flgProdCap = random.choice([True, False])        # Definisce se la capacità produttiva possa essere variabile
        DB.flgCQprod = random.choice([True, False])         # Imposta se la produzione sia soggetta a controllo qualità
        DB.flgLogCap = random.choice([True, False])         # Imposta se la capacità logistica possa essere variabile

    # Visualizzazioni info
    #if UT.Yes_No("\n- Si desidera visualizzare i parametri impostati?", default='Y') == 'Y': Params ()                      # Visualizzazione parametri della simulazione
    Params ()       # Visualizzazione parametri della simulazione
    if UT.Yes_No("\n- Si desidera visualizzare una legenda delle colonne della tabella?", default='N') == 'Y': Legenda ()   # Visualizzazione legenda colonne

    # Intestazione tabella
    TableHeader ()