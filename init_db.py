import sqlite3

conn = sqlite3.connect("database.db")

conn.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)
""")

conn.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT,
    user_id INTEGER
)
""")

conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("admin", "alphaadmin"))

conn.commit()
conn.close()

print("Database klar!")
