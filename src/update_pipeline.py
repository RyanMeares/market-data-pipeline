import os
import sqlite3
from pathlib import Path

import pandas as pd
import yfinance as yf
from dotenv import load_dotenv
from fredapi import Fred

SERIES_IDS = ["DGS10", "DGS2", "DGS3MO", "CPIAUCSL", "UNRATE"]

project_folder = Path(__file__).resolve().parent.parent
database_path = project_folder / "data" / "market_data.db"
universe_path = project_folder / "data" / "universe.csv"

load_dotenv(project_folder / ".env")
api_key = os.getenv("FRED_API_KEY")

if not api_key:
    raise ValueError("FRED_API_KEY was not found in the .env file.")

universe = pd.read_csv(universe_path)
tickers = universe["ticker"].dropna().str.strip().tolist()

fred = Fred(api_key=api_key)

connection = sqlite3.connect(database_path)
cursor = connection.cursor()

today = pd.Timestamp.today().normalize()

for ticker in tickers:
    latest_date = cursor.execute("""
        SELECT MAX(date)
        FROM prices
        WHERE ticker = ?
    """, (ticker,)).fetchone()[0]

    if latest_date:
        start_date = (
            pd.Timestamp(latest_date) + pd.Timedelta(days=1)
        ).strftime("%Y-%m-%d")
    else:
        start_date = "2015-01-01"

    if pd.Timestamp(start_date) > today:
        print(f"{ticker} is already up to date through {latest_date}.")
        continue

    print(f"Updating {ticker} from {start_date}...")

    prices = yf.download(
        ticker,
        start=start_date,
        auto_adjust=False,
        progress=False
    )

    if prices.empty:
        print(f"No new price data for {ticker}.")
        continue

    if isinstance(prices.columns, pd.MultiIndex):
        prices.columns = prices.columns.get_level_values(0)

    prices = prices.reset_index()

    rows = [
        (
            ticker,
            row["Date"].strftime("%Y-%m-%d"),
            float(row["Open"]),
            float(row["High"]),
            float(row["Low"]),
            float(row["Close"]),
            float(row["Adj Close"]),
            int(row["Volume"])
        )
        for _, row in prices.iterrows()
    ]

    cursor.executemany("""
        INSERT OR REPLACE INTO prices
        (ticker, date, open, high, low, close, adj_close, volume, last_updated)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
    """, rows)

    print(f"Saved {len(rows)} new rows for {ticker}.")

for series_id in SERIES_IDS:
    latest_date = cursor.execute("""
        SELECT MAX(date)
        FROM macro
        WHERE series_id = ?
    """, (series_id,)).fetchone()[0]

    if latest_date:
        start_date = (
            pd.Timestamp(latest_date) + pd.Timedelta(days=1)
        ).strftime("%Y-%m-%d")
    else:
        start_date = "2015-01-01"

    if pd.Timestamp(start_date) > today:
        print(f"{series_id} is already up to date through {latest_date}.")
        continue

    print(f"Updating {series_id} from {start_date}...")

    observations = fred.get_series(
        series_id,
        observation_start=start_date
    ).dropna()

    rows = [
        (date.strftime("%Y-%m-%d"), series_id, float(value))
        for date, value in observations.items()
    ]

    if not rows:
        print(f"No new macro data for {series_id}.")
        continue

    cursor.executemany("""
        INSERT OR REPLACE INTO macro
        (date, series_id, value, last_updated)
        VALUES (?, ?, ?, datetime('now'))
    """, rows)

    print(f"Saved {len(rows)} new rows for {series_id}.")

connection.commit()
connection.close()

print("Pipeline update complete.")