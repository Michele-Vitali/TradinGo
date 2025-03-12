import time
import yfinance as yf
import pandas as pd
from datetime import datetime
import requests_cache
from tickers_controller import TickersController
from debug import Debug as db

dataFrame = pd.read_csv("tickers.csv", sep="|")
datiJson = dataFrame.to_dict(orient="records")

tickers_code = [ticker['Code'] for ticker in datiJson]
lista_test = tickers_code[20:22]

session = requests_cache.CachedSession('yfinance_cache')
session.headers['User-Agent'] = 'Mozilla/5.0'
tc = TickersController()

for t_code in lista_test:
    db.debug_print(t_code)

    ticker = tc.get_ticker(t_code)
    history = ticker.history(period="1y")
    #Volume medio
    db.debug_print(history['Volume'])
    avg_volume = round(history['Volume'].mean(), 4)
    db.debug_print(f"Volume medio: {avg_volume}")

    #Variazione percentuale
    start_price = history['Close'].iloc[0]
    end_price = history['Close'].iloc[-1]
    price_variation_pcg = round(((end_price - start_price) / start_price) * 100, 4)
    db.debug_print(f"Variazione percentuale: {price_variation_pcg}")

    #Volatilità
    history['Returns'] = history['Close'].pct_change()
    volatility = round(history['Returns'].std() * (252 ** 0.5), 4)
    db.debug_print(f"Volatilita': {volatility}")

    fast_info = ticker.get_fast_info()
    #VWAP
    last_price = round(fast_info['lastPrice'], 4)
    lastVolume = round(fast_info['lastVolume'], 4)
    vwap = round((history['Close'] * history['Volume']).sum() / history['Volume'].sum(), 4)
    db.debug_print(f"Prezzo attuale: {last_price}")
    db.debug_print(f"Volume odierno: {lastVolume}")
    db.debug_print(f"VWAP: {vwap}")
    db.debug_print("Indicatore 1:")
    if last_price > vwap:
        db.debug_print("Il titolo sta salendo!")
    else:
        db.debug_print("Il titolo sta scendendo!")

    earnings = ticker.get_earnings_history()
    avg_actual_eps = 0
    avg_expected_eps = 0
    avg_surprise = 0
    count = 0
    date = earnings.index
    for row in earnings.itertuples():
        date = earnings.index[count]
        actual_eps = round(row.epsActual, 4)
        avg_actual_eps += actual_eps
        expected_eps = round(row.epsEstimate, 4)
        avg_expected_eps += expected_eps
        surprise = round(((actual_eps - expected_eps) / expected_eps) * 100, 4)
        avg_surprise += surprise
        count += 1

        db.debug_print(f"Data: {date}, EPS Effettivo: {actual_eps}, EPS Atteso: {expected_eps}, Surprise: {surprise}")

    db.debug_print(f"EPS attuale medio: {avg_actual_eps}")
    db.debug_print(f"EPS atteso medio: {avg_expected_eps}")
    db.debug_print(f"Surprise medio: {avg_surprise}")
    if avg_actual_eps > avg_expected_eps: #Surprise > 0
        db.debug_print("L'azienda guadagna piu' di quanto atteso! Ottimo!")
    elif avg_actual_eps < avg_expected_eps: #Surprise < 0
        db.debug_print("L'azienda guadagna meno di quanto atteso! MMM!")
    else:
        db.debug_print("L'azienda guadagna come atteso... Normale.")

    reccomendation = ticker.get_recommendations_summary()
    upgrades = ticker.get_upgrades_downgrades()

    db.debug_print("Raccomandazioni analisti:")
    for rec in reccomendation.itertuples():
        rating = rec.strongBuy*2 + rec.buy - rec.hold*0.5 - rec.sell - rec.strongSell*2
        db.debug_print(f"Data: {rec.period}, Rating: {rating}")

    db.debug_print("\nAggiornamenti recenti:")
    for upgrade in upgrades.itertuples():
        db.debug_print(upgrade)
        db.debug_print(f"Data: {upgrade.date}, Azione: {upgrade.action}")
    
    news = ticker.news
    db.debug_print("Ultime notizie sul titolo:")
    for n in news[:5]:
        db.debug_print(n)
        db.debug_print(f"Data: {n['providerPublishTime']}, Titolo: {n['title']}, Fonte: {n['publisher']}")
        
    time.sleep(5)