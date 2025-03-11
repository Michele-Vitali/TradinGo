import time
import yfinance as yf
import pandas as pd
from datetime import datetime
import requests_cache

dataFrame = pd.read_csv("tickers.csv", sep="|")
datiJson = dataFrame.to_dict(orient="records")

tickers_code = [ticker['Code'] for ticker in datiJson]
lista_test = tickers_code[15:20]

session = requests_cache.CachedSession('yfinance_cache')
session.headers['User-Agent'] = 'Mozilla/5.0'

for t_code in lista_test:
    ticker = yf.Ticker(t_code)
    if ticker.history(period="1mo").empty:
        print(f"Questo ticker non è valido: {t_code}")
    else:
        end_date = datetime.now().strftime('%Y-%m-%d')

        history = ticker.history(start='2022-01-01', end=end_date)
        #Volume medio
        avg_volume = round(history['Volume'].mean(), 4)
        print(f"Volume medio: {avg_volume}")

        #Variazione percentuale
        start_price = history['Close'].iloc[0]
        end_price = history['Close'].iloc[-1]
        price_variation_pcg = round(((end_price - start_price) / start_price) * 100, 4)
        print(f"Variazione percentuale: {price_variation_pcg}")

        #Volatilità
        history['Returns'] = history['Close'].pct_change()
        volatility = round(history['Returns'].std() * (252 ** 0.5), 4)
        print(f"Volatilita': {volatility}")

        fast_info = ticker.get_fast_info()
        #VWAP
        last_price = round(fast_info['lastPrice'], 4)
        lastVolume = round(fast_info['lastVolume'], 4)
        vwap = round((history['Close'] * history['Volume']).sum() / history['Volume'].sum(), 4)
        print(f"Prezzo attuale: {last_price}")
        print(f"Volume odierno: {lastVolume}")
        print(f"VWAP: {vwap}")
        print("Indicatore 1:")
        if last_price > vwap:
            print("Il titolo sta salendo!")
        else:
            print("Il titolo sta scendendo!")

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

            print(f"Data: {date}, EPS Effettivo: {actual_eps}, EPS Atteso: {expected_eps}, Surprise: {surprise}")

        print(f"EPS attuale medio: {avg_actual_eps}")
        print(f"EPS atteso medio: {avg_expected_eps}")
        print(f"Surprise medio: {avg_surprise}")
        if avg_actual_eps > avg_expected_eps: #Surprise > 0
            print("L'azienda guadagna piu' di quanto atteso! Ottimo!")
        elif avg_actual_eps < avg_expected_eps: #Surprise < 0
            print("L'azienda guadagna meno di quanto atteso! MMM!")
        else:
            print("L'azienda guadagna come atteso... Normale.")

        reccomendation = ticker.get_recommendations_summary()
        upgrades = ticker.get_upgrades_downgrades()

        print("Raccomandazioni analisti:")
        for rec in reccomendation.itertuples():
            rating = rec.strongBuy*2 + rec.buy - rec.hold*0.5 - rec.sell - rec.strongSell*2
            print(f"Data: {rec.period}, Rating: {rating}")

        '''print("\nAggiornamenti recenti:")
        for upgrade in upgrades.itertuples():
            print(upgrade)
            print(f"Data: {upgrade.date}, Azione: {upgrade.action}")
        '''
        '''
        news = ticker.news
        print("Ultime notizie sul titolo:")
        for n in news[:5]:
            print(n)
            print(f"Data: {n['providerPublishTime']}, Titolo: {n['title']}, Fonte: {n['publisher']}")
        '''
    time.sleep(5)