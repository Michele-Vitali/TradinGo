import csv
import requests
from ticker import Ticker
from exchange import Exchange
import json
import chardet

class MarketController:

    def __init__(self, key):
        self.key = key
        #This is a list of dictionaries containing the exchanges
        self.exchanges_list = []
        self.tickers_list = []
        self.exchanges_file = "exchanges.json"
        self.tickers_file = "tickers.csv"
        self.get_exchanges()
        self.get_markets()

    def get_exchanges(self):
        '''exchanges_url = f"https://eodhd.com/api/exchanges-list/?api_token={self.key}&fmt=json"
        resp = self.make_call(exchanges_url)
        self.update_file(resp, self.exchanges_file)
        exchanges = [Exchange.from_dict(data) for data in resp]
        self.exchanges_list.extend(exchanges)'''
        #Carico i dati per testing, così non spreco le chiamate
        with open("exchanges.json", "r", encoding='utf-8') as f:
            self.exchanges_list = json.load(f)

    def get_markets(self):
        tickers_totali = []
        lista_test = self.exchanges_list[:1]
        first = True
        for exchange in lista_test:
            url = f"https://eodhd.com/api/exchange-symbol-list/{exchange['Code']}?api_token={self.key}&fmt=json"
            resp = self.make_call(url)
            resp_bytes = json.dumps(resp).encode('utf-8')
            if first:
                encoding = chardet.detect(resp_bytes)['encoding']
            decoded_data = resp_bytes.decode(encoding)
            fixed_data = decoded_data.encode('latin-1').decode('utf-8')
            resp = json.loads(fixed_data)
            tickers_totali.extend(resp)
            tickers = [Ticker.from_dict(data) for data in resp]
            self.tickers_list.extend(tickers)
        '''
        with open("tickers.json", "r", encoding='utf-8') as f:
            jsonData = json.load(f)
        
        tickers_totali.extend(jsonData)
        tickers = [Ticker.from_dict(data) for data in jsonData]
        self.tickers_list.extend(tickers)
        '''
        self.update_file(tickers_totali, self.tickers_file)

    def update_data(self):
        self.get_exchanges()
        self.get_markets()

    def update_file(self, arr, file, mode="w"):
        with open(file, mode=mode, encoding="utf-8") as f:
            #json.dump(arr, f, ensure_ascii=False, indent=4)
            writer = csv.DictWriter(f, fieldnames=arr[0].keys(), delimiter="|")
            writer.writeheader()
            writer.writerows(arr)
            print("Dati salvati!")

    def make_call(self, url):
        resp = requests.get(url)
        if resp.ok:
            resp = resp.json()
        else:
            print("Errore nella richiesta a: " + url)
            resp = None
        return resp