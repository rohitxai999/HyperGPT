from datetime import datetime

from app.memory.importance import MemoryImportanceScorer
from app.memory.categories import MemoryCategoryClassifier
from app.memory.ranking import MemoryRankingEngine

from app.database.database import SessionLocal
from app.database.memory_repository import MemoryRepository


class MemoryService:

    def __init__(self):
        self.importance = MemoryImportanceScorer()
        self.category = MemoryCategoryClassifier()
        self.ranking = MemoryRankingEngine()


    def analyze(self, text: str):

        importance = self.importance.score(text)
        category = self.category.classify(text)

        memory = {
            "text": text,
            "importance": importance["importance"],
            "category": category["category"],
            "reason": importance["reason"],
            "created_at": importance["created_at"],
        }

        return memory


    def save_memory(self, user_id: str, text: str):

        memory = self.analyze(text)

        db = SessionLocal()

        try:

            repo = MemoryRepository(db)

            repo.save(
                user_id=user_id,
                content=text,
                importance=memory["importance"],
                category=memory["category"],
            )

        finally:
            db.close()

        return memory


    def rank_memory(
        self,
        similarity: float,
        importance: int,
        created_at: datetime,
    ):

        """
        Calculate memory relevance score.
        """

        return self.ranking.calculate_score(
            similarity=similarity,
            importance=importance,
            created_at=created_at,
        )