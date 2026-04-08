import sqlite3
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class Storage:
    def __init__(self, db_path: str = None):
        if db_path is None:
            base_path = Path(__file__).resolve().parent.parent
            db_path = base_path / "data" / "bot.db"

        self.db_path = str(db_path)
        self._initialize_db()

    def _initialize_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Posts procesados
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS processed_posts (
                id TEXT PRIMARY KEY,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Keywords dinámicas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS keywords (
                keyword TEXT PRIMARY KEY
            )
        """)

        conn.commit()
        conn.close()

    # =========================
    # POSTS
    # =========================
    def save_post_id(self, post_id: str):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            "INSERT OR IGNORE INTO processed_posts (id) VALUES (?)",
            (post_id,)
        )

        conn.commit()
        conn.close()

    def exists_post_id(self, post_id: str) -> bool:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT 1 FROM processed_posts WHERE id = ?",
            (post_id,)
        )

        result = cursor.fetchone()
        conn.close()

        return result is not None

    # =========================
    # KEYWORDS
    # =========================
    def add_keyword(self, keyword: str):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            "INSERT OR IGNORE INTO keywords (keyword) VALUES (?)",
            (keyword.lower(),)
        )

        conn.commit()
        conn.close()

    def remove_keyword(self, keyword: str):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM keywords WHERE keyword = ?",
            (keyword.lower(),)
        )

        conn.commit()
        conn.close()

    def get_keywords(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT keyword FROM keywords")
        rows = cursor.fetchall()

        conn.close()

        return [row[0] for row in rows]