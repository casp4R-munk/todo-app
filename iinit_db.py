import sqlite3

conn = sqlite3.connect("database.db")

conn.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL
)
""")

conn.close()

print("Database klar!")
