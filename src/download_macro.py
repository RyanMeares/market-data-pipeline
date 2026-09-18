import os
import sqlite3
from pathlib import Path

from dotenv import load_dotenv
from fredapi import Fred

SERIES_IDS = ["DGS10", "DGS2", "DGS3MO", "CPIAUCSL", "UNRATE"]

project_folder = Path(__file__).resolve().parent.parent
database_path = project_folder / "data" / "market_data.db"

load_dotenv(project_folder / ".env")
api_key = os.getenv("FRED_API_KEY")

if not api_key:
    raise ValueError("FRED_API_KEY was not found in the .env file.")

fred = Fred(api_key=api_key)

connection = sqlite3.connect(database_path)
cursor = connection.cursor()

for series_id in SERIES_IDS:
    print(f"Downloading {series_id}...")

    observations = fred.get_series(
        series_id,
        observation_start="2015-01-01"
    ).dropna()

    rows = [
        (date.strftime("%Y-%m-%d"), series_id, float(value))
        for date, value in observations.items()
    ]

    cursor.executemany("""
        INSERT OR REPLACE INTO macro (date, series_id, value)
        VALUES (?, ?, ?)
    """, rows)

    print(f"Saved {len(rows)} rows for {series_id}.")

connection.commit()
connection.close()

print("Finished downloading and saving macro data.")