import csv
import requests
from my_ticker import MyTicker
from exchange import Exchange
import json
import chardet
import debug as db
import pandas as pd

class MarketController:

    def __init__(self, key):
        self.key = key
        #This is a list of dictionaries containing the exchanges
        self.exchanges = pd.DataFrame()
        self.tickers = pd.DataFrame()
        self.exchanges_file = "exchanges.csv"
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
        self.exchanges = pd.read_csv(self.exchanges_file, delimiter="|")

    def get_markets(self):
        '''for exchange in lista_test:
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
        self.tickers = pd.read_csv("tickers.csv", delimiter="|")
        

        #tickers_totali.extend(jsonData)
        #for row in self.tickers.itertuples():
        #    print(f"Codice: {row.Code}")
        self.update_file(self.tickers, self.tickers_file)

    def update_data(self):
        self.get_exchanges()
        self.get_markets()

    def update_file(self, df, file, mode="w"):
        df.to_csv(file, index=False, sep="|")
        db.debug_print("Dati salvati!")

    def make_call(self, url):
        resp = requests.get(url)
        if resp.ok:
            resp = resp.json()
        else:
            db.debug_print("Errore nella richiesta a: " + url)
            resp = None
        return resp