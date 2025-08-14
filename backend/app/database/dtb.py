from pathlib import Path
import sqlite3

DB_PATH = Path(__file__).with_name("data") / "newsApp.db"

def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn