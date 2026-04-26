import sqlite3
import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, db_path="streamguard.db"):
        appdata_dir = os.path.join(os.environ.get("APPDATA", ""), "StreamGuard")
        os.makedirs(appdata_dir, exist_ok=True)
        self.db_path = os.path.join(appdata_dir, db_path)
        self.init_db()

    def _get_conn(self):
        return sqlite3.connect(self.db_path)

    def init_db(self):
        """Initializes the SQLite database with the necessary tables."""
        try:
            with self._get_conn() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS viewers (
                        author_id TEXT PRIMARY KEY,
                        display_name TEXT,
                        message_count INTEGER DEFAULT 0,
                        first_seen TEXT,
                        is_vip BOOLEAN DEFAULT 0
                    )
                ''')
                conn.commit()
        except Exception as e:
            logger.error(f"Error initializing database: {e}")

    def record_message(self, author_id: str, display_name: str) -> tuple[int, bool]:
        """
        Records a message from a viewer. 
        Returns a tuple: (new_message_count, is_first_time)
        """
        try:
            with self._get_conn() as conn:
                cursor = conn.cursor()
                # Check if viewer exists
                cursor.execute('SELECT message_count, is_vip FROM viewers WHERE author_id = ?', (author_id,))
                result = cursor.fetchone()
                
                is_first_time = False
                now_str = datetime.now().isoformat()
                
                if result is None:
                    # New viewer
                    is_first_time = True
                    message_count = 1
                    cursor.execute('''
                        INSERT INTO viewers (author_id, display_name, message_count, first_seen, is_vip)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (author_id, display_name, message_count, now_str, False))
                else:
                    # Existing viewer
                    message_count = result[0] + 1
                    cursor.execute('''
                        UPDATE viewers SET message_count = ?, display_name = ? WHERE author_id = ?
                    ''', (message_count, display_name, author_id))
                
                conn.commit()
                return message_count, is_first_time
        except Exception as e:
            logger.error(f"Error recording message for {author_id}: {e}")
            return 1, False

    def toggle_vip(self, author_id: str, is_vip: bool):
        """Toggles VIP status for a specific viewer."""
        try:
            with self._get_conn() as conn:
                cursor = conn.cursor()
                cursor.execute('UPDATE viewers SET is_vip = ? WHERE author_id = ?', (is_vip, author_id))
                conn.commit()
        except Exception as e:
            logger.error(f"Error updating VIP status for {author_id}: {e}")

    def get_top_viewers(self, limit: int = 50) -> list[dict]:
        """Retrieves the top viewers by message count."""
        try:
            with self._get_conn() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT author_id, display_name, message_count, first_seen, is_vip 
                    FROM viewers 
                    ORDER BY message_count DESC, display_name ASC 
                    LIMIT ?
                ''', (limit,))
                rows = cursor.fetchall()
                
                return [
                    {
                        "author_id": r[0],
                        "display_name": r[1],
                        "message_count": r[2],
                        "first_seen": r[3],
                        "is_vip": bool(r[4])
                    }
                    for r in rows
                ]
        except Exception as e:
            logger.error(f"Error fetching top viewers: {e}")
            return []
