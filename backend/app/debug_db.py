from db.database import get_connection, DB_PATH

print(f"DB file: {DB_PATH}")
conn = get_connection()
names = [r["name"] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
print("Tables:", names)
for t in ("users", "bookmarks"):
    exists = bool(conn.execute(
        "SELECT COUNT(*) c FROM sqlite_master WHERE type='table' AND name=?", (t,)
    ).fetchone()["c"])
    print(f"Has table '{t}':", exists)
conn.close()
