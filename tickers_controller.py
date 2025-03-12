import yfinance as yf
import debug as db
import pandas as pd

class TickersController:

    def __init__(self, df):
        self.tickers = df

    def get_ticker(self, t_code):
        ticker = yf.Ticker(t_code)
        try:
            if ticker.fast_info['lastPrice'] is not None:
                db.debug_print("Esiste!")
            else:
                db.debug_print("Non esiste!")
        except:
            db.debug_print("Non esiste!")
        
    #def get_avg_volume(self, ticker):