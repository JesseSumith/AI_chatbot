import sqlite3
from datetime import datetime

DB_PATH = "logs/interactions.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_message TEXT NOT NULL,
            intent TEXT,
            bot_response TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_interaction(user_message, intent, bot_response):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO interactions (user_message, intent, bot_response, timestamp)
        VALUES (?, ?, ?, ?)
    """, (user_message, intent, bot_response, datetime.now().isoformat()))
    conn.commit()
    conn.close()
