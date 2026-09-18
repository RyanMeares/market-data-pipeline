import sqlite3
from pathlib import Path

import pandas as pd
import yfinance as yf

project_folder = Path(__file__).resolve().parent.parent
database_path = project_folder / "data" / "market_data.db"
universe_path = project_folder / "data" / "universe.csv"

universe = pd.read_csv(universe_path)
tickers = universe["ticker"].dropna().str.strip().tolist()

connection = sqlite3.connect(database_path)
cursor = connection.cursor()

for ticker in tickers:
    print(f"Downloading {ticker}...")

    prices = yf.download(
        ticker,
        start="2015-01-01",
        auto_adjust=False,
        progress=False
    )

    if prices.empty:
        print(f"No data found for {ticker}.")
        continue

    if isinstance(prices.columns, pd.MultiIndex):
        prices.columns = prices.columns.get_level_values(0)

    prices = prices.reset_index()

    rows = []

    for _, row in prices.iterrows():
        rows.append((
            ticker,
            row["Date"].strftime("%Y-%m-%d"),
            float(row["Open"]),
            float(row["High"]),
            float(row["Low"]),
            float(row["Close"]),
            float(row["Adj Close"]),
            int(row["Volume"])
        ))

    cursor.executemany("""
        INSERT OR REPLACE INTO prices
        (ticker, date, open, high, low, close, adj_close, volume)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, rows)

    print(f"Saved {len(rows)} rows for {ticker}.")

connection.commit()
connection.close()

print("Finished downloading and saving price data.")