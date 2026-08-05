import sqlite3
from pathlib import Path

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Database paths
DB_DIR = BASE_DIR / "database"
DB_PATH = DB_DIR / "hypergpt.db"
SCHEMA_PATH = DB_DIR / "schema.sql"


class MemoryStore:
    def __init__(self):
        DB_DIR.mkdir(exist_ok=True)
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row
        self._initialize_database()

    def _initialize_database(self):
        with open(SCHEMA_PATH, "r", encoding="utf-8") as file:
            schema = file.read()
        self.conn.executescript(schema)
        self.conn.commit()

    def add_memory(self, memory):
        cursor = self.conn.cursor()

        cursor.execute(
            """
            INSERT INTO memories
            (memory_type, content, importance, tags)
            VALUES (?, ?, ?, ?)
            """,
            (
                memory.memory_type,
                memory.content,
                memory.importance,
                memory.tags,
            ),
        )

        self.conn.commit()
        return cursor.lastrowid

    def get_all_memories(self):
        cursor = self.conn.cursor()

        cursor.execute(
            """
            SELECT * FROM memories
            ORDER BY created_at DESC
            """
        )

        return cursor.fetchall()

    def get_memory(self, memory_id):
        cursor = self.conn.cursor()

        cursor.execute(
            """
            SELECT * FROM memories
            WHERE id=?
            """,
            (memory_id,),
        )

        return cursor.fetchone()

    def delete_memory(self, memory_id):
        cursor = self.conn.cursor()

        cursor.execute(
            """
            DELETE FROM memories
            WHERE id=?
            """,
            (memory_id,),
        )

        self.conn.commit()

    def close(self):
        self.conn.close()