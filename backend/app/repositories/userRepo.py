from database.dtb import get_connection
from typing import Optional, Dict

class UserRepo:
    def create_user(self, username: str, hashed_password: str) -> int:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (?,?)", (username, hashed_password))
        conn.commit()
        uid = cur.lastrowid
        conn.close()
        return uid

    def get_by_username(self, username: str) -> Optional[Dict]:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, username, password FROM users WHERE username=?", (username,))
        row = cur.fetchone()
        conn.close()
        if not row:
            return None
        return {"id": row["id"], "username": row["username"], "password": row["password"]}
