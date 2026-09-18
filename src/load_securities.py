import sqlite3
from pathlib import Path

import pandas as pd
import yfinance as yf

project_folder = Path(__file__).resolve().parent.parent
database_path = project_folder / "data" / "market_data.db"
universe_path = project_folder / "data" / "universe.csv"

universe = pd.read_csv(universe_path)

connection = sqlite3.connect(database_path)
cursor = connection.cursor()

for _, company in universe.iterrows():
    ticker = company["ticker"]
    company_name = company["company"]
    sector = company["sector"]

    print(f"Getting industry data for {ticker}...")

    try:
        info = yf.Ticker(ticker).get_info()
        industry = info.get("industry")
    except Exception:
        industry = None
        print(f"Could not retrieve industry for {ticker}.")

    cursor.execute("""
        INSERT OR REPLACE INTO securities
        (ticker, company, sector, industry)
        VALUES (?, ?, ?, ?)
    """, (ticker, company_name, sector, industry))

connection.commit()
connection.close()

print("Finished saving company information.")