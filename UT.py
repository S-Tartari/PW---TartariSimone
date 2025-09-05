import random
import sys
import os
import csv
import DB           # Contiene gli articoli e i loro parametri

def Yes_No(question, default):
    default = default.upper()
    
    while True:
        choices = f"[{'Y' if default == 'Y' else 'y'}/{'N' if default == 'N' else 'n'}]"
        ans = input(f"{question} {choices} ").strip().upper()
        
        if ans in ('Y', 'N'): 
            return ans
        elif ans == '': 
            sys.stdout.write(f"\033[1A\033[{len(question) + len(choices) + 1}C{default}\n")
            sys.stdout.flush()
            return default
        
        print("Risposta non valida. Usare 'Y', 'N' o 'enter'/'invio' per il default.", file=sys.stderr)

def SetValue (art, field, value):
    """
    Assegna al campo del prodotto indicato il valore specificato - Attenzione: il primo record ha indice 0
    Parametri
    - art = indice del prodotto (>=0)
    - field = nome del campo che deve esistere (!= "")
    - value = valore del campo
    Restituisce
    - nulla
    """
    DB.ART[art][field] = value
    return

def GetValue (art, field):
    """
    Recupera dal campo indicato il suo valore - Attenzione: il primo record ha indice 0
    Parametri
    - art = indice del prodotto (>=0)
    - field = nome del campo che deve esistere (!= "")
    Restituisce
    - value = il valore memorizzato nel campo
    """
    return DB.ART[art][field]

def SALES (orders, backlog, stock, hours4art, hours4prod):
    """
    In base agli ordini (recenti e passati) e allo stock determina, in funzione del tempo necessario per produrre un articolo:
    - quanti articoli siano già disponibili a magazzino e quindi spedibili dalla logistica [Art2log]. Questi articoli disponibili a stock
      saranno detratti dagli articoli da produrre [orders+backlog]
    - quanti articoli possano essere prodotti [Art2prd], valutando gli ordini recenti e passati [orders+backlog], valutando le ore necessarie
      per produrre ciascuno [hours4art] e quante ore la produzione ha a disposizione per produrli [hours4prod]
    Parametri
    - orders: quantità di articoli ordinati (>=0)
    - backlog: quantità di articoli ordinati in precedenza (>=0)
    - stock: quantità di articoli disponibili a magazzino per orders e backlog (>=0)
    - hours4art: ore necessarie a produrre un articolo (>0)
    - hours4prod: ore disponibili in produzione per produrre gli articoli (>0 e hours4prod > hours4art)
    Restituisce
    - arts2prod: quantità di articoli che si possono produrre (>=0)
    - arts2log: quantità di articoli già pronti che possono essere spediti dalla logistica (>=0) perchè già presenti a stock
    - new_backlog: quantità di articoli che non possono essere spediti per mancanza di stock o articoli che non possono essere prodotti per mancanza di tempo da parte della produzione (>=0)
    - new_stock: pezzi rimasti in magazzino dopo che sono stati soddisfatti order e backlog (>=0)
    - hr_left: ore rimaste inutilizzate per la la produzione degli articoli, o perchè gli ordini sono stati soddisfatti tutti o perchè non c'è abbastanza tempo per produrne uno in più
    """
    # Calcolo della domanda totale (ordini + backlog)
    total_demand = orders + backlog

    # Articoli che possono essere spediti dalla logistica (minimo tra stock e domanda totale)
    arts2log = min(stock, total_demand)

    # Calcolo del nuovo stock dopo aver soddisfatto parte della domanda
    new_stock = stock - arts2log

    # Calcolo degli articoli che devono ancora essere prodotti (domanda residua)
    remaining_demand = total_demand - arts2log

    # Calcolo del massimo numero di articoli che possono essere prodotti con le ore disponibili
    max_prod = int(hours4prod // hours4art)
    arts2prod = min(max_prod, remaining_demand)

    # Calcolo del nuovo backlog (domanda non soddisfatta)
    new_backlog = remaining_demand - arts2prod

    # Calcolo delle ore di produzione non utilizzate
    hr_left = hours4prod - (arts2prod * hours4art)

    return (arts2prod, arts2log, new_backlog, new_stock, hr_left)

def PROD_OVERSTOCK (h_art, h_left, p_stock):
    """
    Calcola se sia possibile produrre overstock, ovvero dei pezzi, valutando la capacità oraria rimasta.
    Se ci sono ore a sufficienza per produrre dei pezzi, i pezzi prodotti si sommano a quelli presenti a magazzino
    Parametri
    - h_art: indica quante ore sono necessarie per produrre un pezzo (>0)
    - h_left: indica quante ore sono rimaste per poter produrre un pezzo (>=0)
    - p_stock: indica quanti pezzi ci sono a magazzino (>=0)
    Restituisce
    - p_made: quanti pezzi è stato possibile produrre (>=0)
    - p_newstock: quanti pezzi ci sono ora a stock, dopo che si è provato a produrne (>=0)
    """
    return (h_left // h_art)    # Divisione intera per ottenere il numero di pezzi prodotti

def QUALITY (items, overstock, scraps, stock):
    """
    Calcola quanti pezzi superano il controllo qualità valutando i pezzi prodotti.
    Scraps decrementa i pezzi da controllare [items e overstock] se >0
    Quindi con i pezzi a stock cerca di ripristinare il valore iniziale di items e di overstock.
    Se items = 0 e overstock = 0: new_items = 0; new_overstock = 0; new_scraps = 0; new_stock = stock
    Se scraps =0: new_items = items; new_overstock = overstock; new-scraps = 0; new_stock = stock
    Se scraps > (items+overstock): new_items = 0; new_overstock = 0; new_scraps = items+overstock; new_stock = stock
    Parametri
    - items: pezzi da controllare (>=0)
    - overstock: pezzi da controllare (>=0)
    - scraps: pezzi da scartare (>=0)
    - stock: pezzi a magazzino (>=0)
    Restituisce
    - new_items: pezzi rimasti dopo il controllo e la compensazione dello stock, se possibile (>=0). new_items <= items
    - new_overstock: pezzi rimasti dopo il controllo e la compensazione dello stock, se possibile (>=0). new_overstock <= overstock
    - new_scraps = pezzi effettivamente scartati (>=0). news_scraps <= scraps
    - new_stock = pezzi rimasti dopo la compensazione dei pezzi scartati per items e overstock (>=0). new_stock <= stock
    """
    new_items = items
    new_overstock = overstock
    new_scraps = 0
    new_stock = stock

    # Caso 1: Se items = 0 e overstock = 0
    if items == 0 and overstock == 0:
        return 0, 0, 0, stock

    # Caso 2: Se scraps = 0
    if scraps == 0:
        return items, overstock, 0, stock

    # Calcola il totale dei pezzi da controllare
    total_to_check = items + overstock

    # Caso 3: Se scraps > (items + overstock)
    if scraps >= total_to_check:
        new_scraps = total_to_check
        # I pezzi items e overstock sono completamente scartati
        new_items = 0
        new_overstock = 0
        return new_items, new_overstock, new_scraps, new_stock

    # Gestione degli 'scraps': se scraps è minore o uguale a total_to_check, decrementa i pezzi da controllare con 'scraps'
    remaining_scraps = scraps

    # Prima si scartano da 'items'
    if remaining_scraps > 0:
        if remaining_scraps >= new_items:
            new_scraps += new_items
            remaining_scraps -= new_items
            new_items = 0
        else:
            new_items -= remaining_scraps
            new_scraps += remaining_scraps
            remaining_scraps = 0

    # Poi si scartano da 'overstock', se ci sono ancora 'remaining_scraps'
    if remaining_scraps > 0:
        if remaining_scraps >= new_overstock:
            new_scraps += new_overstock
            remaining_scraps -= new_overstock
            new_overstock = 0
        else:
            new_overstock -= remaining_scraps
            new_scraps += remaining_scraps
            remaining_scraps = 0

    # Si prova a ripristinare i valori iniziali di 'items' e 'overstock' usando 'stock', se possibile

    # Pezzi che mancano da 'items' rispetto al valore iniziale
    items_needed = items - new_items
    if items_needed > 0:
        if new_stock >= items_needed:
            new_items += items_needed
            new_stock -= items_needed
        else:
            new_items += new_stock
            new_stock = 0

    # Pezzi che mancano da 'overstock' rispetto al valore iniziale
    overstock_needed = overstock - new_overstock
    if overstock_needed > 0:
        if new_stock >= overstock_needed:
            new_overstock += overstock_needed
            new_stock -= overstock_needed
        else:
            new_overstock += new_stock
            new_stock = 0

    return new_items, new_overstock, new_scraps, new_stock


def hProdCap ():
    """
    Genera le ore settimanali disponibili per la produzione
    # Parametri
    # - nessuno
    # Restituisce
    # - hours = ore settimanali calcolate in modo pseudo casuale
    """
    return random.choice([24, 32, 40, 44, 48])

def RandomOrders (px):
    """
    Genera un numero di ordini casuali in funzione dell'articolo. Il numero restituito può essere nullo.
    Parametri
    - px = codice dell'articolo (>0)
    Restituisce quanti prodotti sono stati ordinati (>=0)
    """
    hours = GetValue (px, "ArtHours")
    base_value = 20 - hours                 # Funzione del tempo impiegato per produrre l'articolo. Gli articoli che necessitano di più tempo, generano numeri più piccoli
    return random.randint(0, base_value)

def RandomStockBacklog (px):
    """
    Genera un numero casuale in funzione dell'articolo. Il numero restituito non può essere zero.
    Parametri
    - px = codice dell'articolo (>0)
    Restituisce quanti prodotti sono a stock/backlog (>0)
    """
    hours = GetValue (px, "ArtHours")
    base_value = 20 - hours                 # Funzione del tempo impiegato per produrre l'articolo. Gli articoli che necessitano di più tempo, generano numeri più piccoli
    return random.randint(1, base_value)

def WriteCSV(file_path, headers, data, _2nd=False):
    """
    Scrive i dati in un file CSV.
    Parametri
    - file_path: path del file CSV da creare (str!="")
    - headers: lista delle intestazioni delle colonne (list !="")
    - data: lista di liste contenenti i dati da scrivere (list !="")
    - _2nd: gestisce messaggi diversi (bool)
    """
    # Gestione percorso per Windows
    if os.name == "nt": script_dir = os.path.dirname(os.path.abspath(__file__)); file_path = os.path.join(script_dir, file_path)
    
    with open(file_path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(headers)
        writer.writerows(data)
    
    if _2nd == False: print(f"Dati salvati per Dashboard in: '{file_path}'", end=' ')
    else: print(f"e dati completi per verifica in: '{file_path}'")
