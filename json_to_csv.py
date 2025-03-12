import pandas as pd

df = pd.read_json("exchanges.json")
csv_data = df.to_csv("exchanges.csv", index=False)
print("Finito!")