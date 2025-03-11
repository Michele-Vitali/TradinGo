import time
from apscheduler.schedulers.background import BackgroundScheduler
import json
from market_controller import MarketController
import traceback

def get_keys(file="config.json"):
    with open(file, 'r') as f:
        config = json.load(f)
    return config

file = "config.json"
keys = get_keys(file)
market_controller = None
try:
    market_controller = MarketController(keys['eodhd'])
except Exception as e:
    print(f"Eccezione: {e}")
    traceback.print_exc()
    print("MarketController non creato!")
#scheduler = BackgroundScheduler()
#scheduler.add_job(market_controller.update_data(), 'interval', weeks=1)
#scheduler.start()

try:
    while True:
        time.sleep(10)
        print("Sono nel while")
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
    print("Codice interrotto!")