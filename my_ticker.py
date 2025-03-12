import yfinance as yf
import debug as db

class MyTicker:

    def __init__(self, sym):
        try:
            self.ticker = yf.Ticker(sym)
            self.avg_volume = "Non analizzato"
            self.price_var_pcg = "Non analizzato"
            self.volatility = "Non analizzato"
            if self.ticker.fast_info['lastPrice'] is None:
                raise Exception()
        except Exception as e:
            db.debug_print("Ticker non valido!")
            self.ticker = None

    def calc_mov(self, period):
        #db.debug_print(f"Simbolo: {self.ticker.ticker}")
        history = self.get_history(period)
        self.avg_volume = self.get_avg_volume(history)
        if self.avg_volume > 100000:
            #db.debug_print(f"Volume medio: {self.avg_volume}")
            self.price_var_pcg = self.get_price_var_pcg(history)
            #db.debug_print(f"Variazione percentuale del prezzo: {self.price_var_pcg}")
            self.volatility = self.get_volatility(history)
            #db.debug_print(f"Volatilita': {self.volatility}")
            

    def get_history(self, period):
        return self.ticker.history(period=period)
    
    def get_avg_volume(self, history):
        avg_volume = round(history['Volume'].mean(), 4)
        return avg_volume
    
    def get_price_var_pcg(self, history):
        start_price = history['Close'].iloc[0]
        end_price = history['Close'].iloc[-1]
        price_var_pcg = 0
        if start_price != 0:
            price_var_pcg = round(((end_price - start_price) / start_price) * 100, 4)
        else:
            price_var_pcg = f"Prezzo iniziale: 0 -> Variazione solo in valore assoluto: {round(end_price - start_price, 4): +}"
        return price_var_pcg
    
    def get_volatility(self, history):
        history['Returns'] = history['Close'].pct_change()
        volatility = round(history['Returns'].std() * (252 ** 0.5), 4)
        return volatility