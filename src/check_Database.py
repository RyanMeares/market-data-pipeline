import sqlite3
from pathlib import Path

project_folder = Path(__file__).resolve().parent.parent
database_path = project_folder / "data" / "market_data.db"

connection = sqlite3.connect(database_path)
cursor = connection.cursor()

price_rows = cursor.execute(
    "SELECT COUNT(*) FROM prices"
).fetchone()[0]

ticker_count = cursor.execute(
    "SELECT COUNT(DISTINCT ticker) FROM prices"
).fetchone()[0]

duplicate_price_rows = cursor.execute("""
    SELECT COUNT(*)
    FROM (
        SELECT ticker, date
        FROM prices
        GROUP BY ticker, date
        HAVING COUNT(*) > 1
    )
""").fetchone()[0]

missing_adjusted_close = cursor.execute(
    "SELECT COUNT(*) FROM prices WHERE adj_close IS NULL"
).fetchone()[0]

macro_rows = cursor.execute(
    "SELECT COUNT(*) FROM macro"
).fetchone()[0]

macro_series_count = cursor.execute(
    "SELECT COUNT(DISTINCT series_id) FROM macro"
).fetchone()[0]

duplicate_macro_rows = cursor.execute("""
    SELECT COUNT(*)
    FROM (
        SELECT date, series_id
        FROM macro
        GROUP BY date, series_id
        HAVING COUNT(*) > 1
    )
""").fetchone()[0]

connection.close()

print(f"Total price rows: {price_rows}")
print(f"Unique tickers: {ticker_count}")
print(f"Duplicate ticker/date records: {duplicate_price_rows}")
print(f"Missing adjusted-close values: {missing_adjusted_close}")
print(f"Total macro rows: {macro_rows}")
print(f"Unique macro series: {macro_series_count}")
print(f"Duplicate date/series records: {duplicate_macro_rows}")