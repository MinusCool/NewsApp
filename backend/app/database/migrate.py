from database.dtb import get_connection
import sqlite3

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS bookmarks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            url TEXT NOT NULL,
            source TEXT,
            published_at TEXT,
            description TEXT,
            image_url TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
    ''')

    cur.execute('''
        CREATE UNIQUE INDEX IF NOT EXISTS idx_bookmarks_user_url
        ON bookmarks(user_id, url);
    ''')

    try:
        cur.execute("PRAGMA index_list(bookmarks)")
        indexes = cur.fetchall()
        unique_url_index = None
        for row in indexes:
            name = row["name"]
            unique = row["unique"]
            if unique:
                cur.execute(f"PRAGMA index_info({name})")
                cols = [r["name"] for r in cur.fetchall()]
                if cols == ["url"]:
                    unique_url_index = name
                    break
        if unique_url_index:
            conn.executescript('''
                PRAGMA foreign_keys=off;
                BEGIN TRANSACTION;
                CREATE TABLE IF NOT EXISTS bookmarks_new (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    url TEXT NOT NULL,
                    source TEXT,
                    published_at TEXT,
                    description TEXT,
                    image_url TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                );
                INSERT OR IGNORE INTO bookmarks_new (id,user_id,title,url,source,published_at,description,image_url)
                    SELECT id,user_id,title,url,source,published_at,description,image_url FROM bookmarks;
                DROP TABLE bookmarks;
                ALTER TABLE bookmarks_new RENAME TO bookmarks;
                CREATE UNIQUE INDEX IF NOT EXISTS idx_bookmarks_user_url ON bookmarks(user_id, url);
                COMMIT;
                PRAGMA foreign_keys=on;
            ''')
    except sqlite3.Error:
        pass

    conn.commit()
    conn.close()
