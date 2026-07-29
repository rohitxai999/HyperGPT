from app.database.database import SessionLocal
from app.database.memory_repository import MemoryRepository
from app.rag.retriever import retrieve_documents
from app.memory.ranking import MemoryRankingEngine


class ContextService:

    def __init__(self):

        self.ranking = MemoryRankingEngine()


    def get_memory_context(
        self,
        query: str,
        user_id: str = "default",
        limit: int = 5,
    ):

        db = SessionLocal()

        try:

            repo = MemoryRepository(db)

            memories = repo.get_by_user(user_id)

            ranked_memories = []

            for memory in memories:

                # Temporary similarity score
                # Later replaced by embedding similarity
                similarity = 0.8

                score = self.ranking.calculate_score(
                    similarity=similarity,
                    importance=memory.importance,
                    created_at=memory.created_at,
                )

                ranked_memories.append(
                    {
                        "content": memory.content,
                        "category": memory.category,
                        "importance": memory.importance,
                        "score": score["final_score"],
                    }
                )


            ranked_memories.sort(
                key=lambda x: x["score"],
                reverse=True
            )


            return ranked_memories[:limit]


        finally:
            db.close()



    def get_full_context(
        self,
        query: str,
    ):

        memories = self.get_memory_context(query)

        documents = retrieve_documents(query)


        return {
            "memories": memories,
            "documents": documents,
        }