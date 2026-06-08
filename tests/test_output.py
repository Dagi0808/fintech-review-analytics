import pandas as pd

df = pd.read_csv("../data/raw/reviews_raw.csv")

print(df.head())
print("\n--- COUNT PER BANK ---")
print(df.groupby("bank").size())