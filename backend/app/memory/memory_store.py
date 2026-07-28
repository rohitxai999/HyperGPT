from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.memory import Memory


class MemoryStore:

    def __init__(self):
        self.db: Session = SessionLocal()

    def save_memory(
        self,
        content: str,
        user_id: str = "default",
        importance: int = 1
    ):

        memory = Memory(
            user_id=user_id,
            content=content,
            importance=importance
        )

        self.db.add(memory)
        self.db.commit()
        self.db.refresh(memory)

        return memory

    def get_all_memories(self):

        return (
            self.db.query(Memory)
            .order_by(Memory.created_at.desc())
            .all()
        )

    def delete_all(self):

        self.db.query(Memory).delete()
        self.db.commit()