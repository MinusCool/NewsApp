from typing import Optional, Dict, Any
from database.dtb import get_connection
import sqlite3

class UserRepository:
    def create_user(self, username: str, password: str) -> int:
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password),
            )
            conn.commit()
            return cur.lastrowid
        except sqlite3.IntegrityError:
            raise ValueError("Username already exists")
        finally:
            conn.close()

    def get_user_by_credentials(self, username: str, password: str) -> Optional[dict]:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT id, username FROM users WHERE username=? AND password=?",
            (username, password),
        )
        row = cur.fetchone()
        conn.close()
        return dict(row) if row else None

    def get_user_by_id(self, user_id: int) -> Optional[dict]:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, username FROM users WHERE id=?", (user_id,))
        row = cur.fetchone()
        conn.close()
        return dict(row) if row else None
