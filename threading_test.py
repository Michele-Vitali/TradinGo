import concurrent.futures
import threading
import queue
import requests
import time
import pandas as pd
import yfinance as yf
import colorama


#Configure
colorama.init()
df = pd.read_csv("tickers.csv", delimiter="|", usecols=['Code'])
symbols = df['Code'].tolist()
SYMBOLS_F = symbols[2020:2520]
MAX_WORKERS = 50
count = 0

def fetch_data(symbol):
    global count
    count += 1
    try:
        stock = yf.Ticker(symbol)
        history = stock.history(period="1y")
    except:
        pass

start_time = time.time()

with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as exc:
    exc.map(fetch_data, SYMBOLS_F)

elapsed_time = time.time() - start_time
print(colorama.Fore.CYAN, f"Simboli scaricati correttamente: {count}")
print(colorama.Fore.YELLOW, f"Tempo impiegato: {elapsed_time}")

'''
BATCH_TIME = 30
symbol_per_request = 30

#data_queue = queue.Queue()
downloaded_count = 0
#lock = threading.Lock()

#session = requests.Session()

def fetch_data(sym):
    global downloaded_count
    try:
        stock = yf.download(sym, period="1d")
        #data = stock.history(period="1d")
        if not stock.empty:
            downloaded_count += len(sym)
            #with lock:
            #    downloaded_count += 1
            #data_queue.put((sym, data)) 
        else:
            print(f"Nessun dato per {sym}")
    except Exception as e:
        print(f"Errore nella richiesta del titolo: {sym}")

def process_data():
    while not data_queue.empty():
        symbol, data = data_queue.get()
        
        #print(f"Simbolo ottenuto! ({symbol})")
  
#consumer = threading.Thread(target=process_data, daemon=True)
#consumer.start()

start_time = time.time()
symbol_batches = [SYMBOLS_F[i:i + symbol_per_request] for i in range(0, len(SYMBOLS_F), symbol_per_request)]

with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    executor.map(fetch_data, SYMBOLS_F)

elapsed_time = time.time() - start_time
print(f"Test finito in {elapsed_time} secondi!")
print(f"Simboli scaricati correttamente: {downloaded_count/len(SYMBOLS_F)}")'''