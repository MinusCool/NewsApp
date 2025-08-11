import sqlite3
from pathlib import Path

DB_DIR = Path(__file__).resolve().parent
DB_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DB_DIR / "news_app.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    print(f"[SQLite] Using DB at: {DB_PATH}")
    conn = get_connection()
    cur = conn.cursor()

    cur.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS bookmarks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            url TEXT UNIQUE NOT NULL,
            source TEXT,
            published_at TEXT,
            description TEXT,
            image_url TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
    """)
    try:
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("admin", "admin123"))
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("user", "user123"))
    except sqlite3.IntegrityError:
        pass

    conn.commit()
    conn.close()
