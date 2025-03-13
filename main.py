import time
from apscheduler.schedulers.background import BackgroundScheduler
import json
from market_controller import MarketController
from tickers_controller import TickersController
from my_ticker import MyTicker
import debug as db
import pandas as pd
import threading

def get_keys(file="config.json"):
    with open(file, 'r') as f:
        config = json.load(f)
    return config

def get_moved_tickers(tickers):
    test_df = tickers.iloc[2020:2050]
    final_df = pd.DataFrame()
    for row_t in test_df.itertuples():
        start = time.perf_counter()
        t = MyTicker(row_t.Code)
        if t is not None:
            t.calc_mov("1y")
            if t.avg_volume > 100000:
                data = [vars(t)]
                data[0]['ticker'] = t.ticker.ticker
                end = time.perf_counter()
                print(f"Tempo impiegato: {end-start:.6f} secondi")
                df = pd.DataFrame(data)
                final_df = pd.concat([final_df, df], ignore_index=True)
        
    final_df = final_df.sort_values(
        by=['avg_volume', 'price_var_pcg', 'volatility'],
        ascending=[False, False, True]
    )
    print(final_df)

file = "config.json"
keys = get_keys(file)
market_controller = None
try:
    market_controller = MarketController(keys['eodhd'])
    tickers_controller = TickersController(market_controller.tickers)
    mov = get_moved_tickers(tickers_controller.tickers)
except Exception as e:
    db.debug_print(f"Eccezione: {e}")
#scheduler = BackgroundScheduler()
#scheduler.add_job(market_controller.update_data(), 'interval', weeks=1)
#scheduler.start()

'''try:
    while True:
        time.sleep(10)
        db.debug_print("Sono nel while")
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
    db.debug_print("Codice interrotto!")
'''