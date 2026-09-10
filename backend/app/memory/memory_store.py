from sqlalchemy.orm import Session

from backend.app.database.database import SessionLocal
from backend.app.models.memory import Memory


class MemoryStore:
    """
    Persistent memory storage for HyperGPT.

    Handles:
    - Saving memories
    - Retrieving memories
    - Deleting memories
    """

    def __init__(self):
        self.db: Session = SessionLocal()

    def save_memory(
        self,
        content: str,
        user_id: str = "default",
        importance: float = 1.0,
    ):
        """
        Save a new memory to the database.
        """

        memory = Memory(
            user_id=user_id,
            content=content,
            importance=importance,
        )

        self.db.add(memory)
        self.db.commit()
        self.db.refresh(memory)

        return memory

    def get_all_memories(self):
        """
        Retrieve all memories, newest first.
        """

        return (
            self.db.query(Memory)
            .order_by(Memory.created_at.desc())
            .all()
        )

    def delete_all(self):
        """
        Delete all stored memories.
        """

        self.db.query(Memory).delete()
        self.db.commit()

    def close(self):
        """
        Close the database session.
        """

        self.db.close()