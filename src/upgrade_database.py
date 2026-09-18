import sqlite3
from pathlib import Path

project_folder = Path(__file__).resolve().parent.parent
database_path = project_folder / "data" / "market_data.db"

connection = sqlite3.connect(database_path)
cursor = connection.cursor()

tables = ["prices", "securities", "macro"]

for table in tables:
    columns = cursor.execute(f"PRAGMA table_info({table})").fetchall()
    column_names = [column[1] for column in columns]

    if "last_updated" not in column_names:
        cursor.execute(
            f"ALTER TABLE {table} ADD COLUMN last_updated TEXT"
        )
        print(f"Added last_updated to {table}.")
    else:
        print(f"{table} already has last_updated.")

for table in tables:
    cursor.execute(f"""
        UPDATE {table}
        SET last_updated = datetime('now')
        WHERE last_updated IS NULL
    """)

connection.commit()
connection.close()

print("Database upgrade complete.")