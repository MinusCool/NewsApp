from typing import List, Optional, Dict, Any
from db.database import get_connection
import sqlite3

class BookmarkRepository:
    def list_by_user(self, user_id: int) -> List[dict]:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT id, title, url, source, published_at, description, image_url FROM bookmarks WHERE user_id=? ORDER BY id DESC",
            (user_id,),
        )
        rows = cur.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def add(self, user_id: int, data: Dict[str, Any]) -> int:
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                """
                INSERT INTO bookmarks (user_id, title, url, source, published_at, description, image_url)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    user_id,
                    data.get("title"),
                    data.get("url"),
                    data.get("source"),
                    data.get("published_at"),
                    data.get("description"),
                    data.get("image_url"),
                ),
            )
            conn.commit()
            return cur.lastrowid
        except sqlite3.IntegrityError:
            raise ValueError("Bookmark already exists")
        finally:
            conn.close()

    def remove(self, user_id: int, bookmark_id: int) -> None:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM bookmarks WHERE id=? AND user_id=?", (bookmark_id, user_id))
        conn.commit()
        conn.close()
