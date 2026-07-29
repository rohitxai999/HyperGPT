from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models.memory import Memory


class MemoryRepository:

    def __init__(self, db: Session):
        self.db = db


    def save(
        self,
        user_id: str,
        content: str,
        importance: int,
        category: str,
    ):
        """
        Save memory only if duplicate does not exist.
        """

        existing = (
            self.db.query(Memory)
            .filter(
                Memory.user_id == user_id,
                Memory.content == content
            )
            .first()
        )

        # Prevent duplicate memory
        if existing:
            return existing


        memory = Memory(
            user_id=user_id,
            content=content,
            importance=importance,
            category=category,
        )

        self.db.add(memory)
        self.db.commit()
        self.db.refresh(memory)

        return memory


    def get_all(self):
        return self.db.query(Memory).all()


    def get_by_user(self, user_id: str):
        """
        Get all memories of a specific user.
        """

        return (
            self.db.query(Memory)
            .filter(Memory.user_id == user_id)
            .all()
        )


    def get_recent_memories(
        self,
        user_id: str = "default",
        limit: int = 10,
    ):
        """
        Get latest memories.
        """

        return (
            self.db.query(Memory)
            .filter(Memory.user_id == user_id)
            .order_by(desc(Memory.created_at))
            .limit(limit)
            .all()
        )


    def search_memories(
        self,
        keyword: str,
        user_id: str = "default",
    ):
        """
        Search memories by keyword.
        """

        return (
            self.db.query(Memory)
            .filter(
                Memory.user_id == user_id,
                Memory.content.ilike(f"%{keyword}%")
            )
            .all()
        )