import sqlite3
from pathlib import Path

DB_PATH = Path("market_data.db")

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ticks (
            timestamp TEXT,
            symbol TEXT,
            price REAL,
            qty REAL
        )
    """)
    conn.commit()
    conn.close()

def insert_tick(ts, symbol, price, qty):
    conn = get_connection()
    conn.execute(
        "INSERT INTO ticks VALUES (?, ?, ?, ?)",
        (ts, symbol, price, qty)
    )
    conn.commit()
    conn.close()

def get_all_ticks():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM ticks").fetchall()
    conn.close()
    return rows
