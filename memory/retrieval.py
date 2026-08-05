from memory.memory_store import MemoryStore


class MemoryRetrieval:
    def __init__(self):
        self.store = MemoryStore()

    def search(self, query: str):
        """
        Search memories by content, tags, or memory type.
        """
        cursor = self.store.conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM memories
            WHERE
                content LIKE ?
                OR tags LIKE ?
                OR memory_type LIKE ?
            ORDER BY importance DESC, created_at DESC
            """,
            (
                f"%{query}%",
                f"%{query}%",
                f"%{query}%",
            ),
        )

        return cursor.fetchall()

    def search_by_type(self, memory_type: str):
        """
        Retrieve all memories of a given type.
        """
        cursor = self.store.conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM memories
            WHERE memory_type = ?
            ORDER BY created_at DESC
            """,
            (memory_type,),
        )

        return cursor.fetchall()

    def close(self):
        self.store.close()