from memory.models import Memory
from memory.memory_store import MemoryStore


class MemoryManager:
    def __init__(self):
        self.store = MemoryStore()

    def remember(
        self,
        memory_type: str,
        content: str,
        importance: int = 1,
        tags: str = "",
    ):
        """
        Save a new memory.
        """

        memory = Memory(
            memory_type=memory_type,
            content=content,
            importance=importance,
            tags=tags,
        )

        return self.store.add_memory(memory)

    def recall_all(self):
        """
        Return every stored memory.
        """

        return self.store.get_all_memories()

    def recall(self, memory_id: int):
        """
        Retrieve a memory by ID.
        """

        return self.store.get_memory(memory_id)

    def forget(self, memory_id: int):
        """
        Delete a memory.
        """

        self.store.delete_memory(memory_id)

    def close(self):
        self.store.close()