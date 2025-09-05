import pandas as pd

df = pd.read_excel("data/latest_mandi_prices.csv.xlsx", sheet_name="Mandi_Pricee(1)")
df.to_csv("data/latest_mandi_prices.csv", index=False, encoding='utf-8')
print("Excel converted to clean CSV")
