import sqlite3
from pathlib import Path

project_folder = Path(__file__).resolve().parent.parent
database_path = project_folder / "data" / "market_data.db"

connection = sqlite3.connect(database_path)
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS prices (
    ticker TEXT NOT NULL,
    date TEXT NOT NULL,
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    adj_close REAL,
    volume INTEGER,
    PRIMARY KEY (ticker, date)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS securities (
    ticker TEXT PRIMARY KEY,
    company TEXT,
    sector TEXT,
    industry TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS macro (
    date TEXT NOT NULL,
    series_id TEXT NOT NULL,
    value REAL,
    PRIMARY KEY (date, series_id)
)
""")

connection.commit()
connection.close()

print("Database created successfully.")