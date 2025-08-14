from database.dtb import get_connection
from typing import List, Dict

class BookmarkRepo:
    def list(self, user_id: int) -> List[Dict]:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT id,title,url,source,published_at,description,image_url FROM bookmarks WHERE user_id=? ORDER BY id DESC",
            (user_id,),
        )
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()
        return rows

    def add(self, user_id: int, data: Dict) -> int:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT OR IGNORE INTO bookmarks (user_id,title,url,source,published_at,description,image_url)
            VALUES (?,?,?,?,?,?,?)
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
        bid = cur.lastrowid
        conn.close()
        return bid

    def delete(self, user_id: int, bookmark_id: int) -> int:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM bookmarks WHERE id=? AND user_id=?", (bookmark_id, user_id))
        changes = cur.rowcount
        conn.commit()
        conn.close()
        return changes