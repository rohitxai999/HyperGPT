from app.memory.memory_retriever import MemoryRetriever
from app.rag.retriever import retrieve_documents


class ContextService:
    """
    Unified context service for HyperGPT.

    Combines:
    - long-term memory
    - semantic memory retrieval
    - RAG documents
    """

    def __init__(self):
        self.memory_retriever = MemoryRetriever()

    def get_memory_context(
        self,
        query: str,
        user_id: str = "default",
        limit: int = 5,
    ):
        """
        Retrieve memories relevant to the current query.
        """

        memories = self.memory_retriever.retrieve(
            query=query,
            limit=limit
        )

        return memories

    def get_full_context(
        self,
        query: str,
    ):
        """
        Build unified context for HyperGPT.
        """

        memories = self.get_memory_context(
            query=query
        )

        documents = retrieve_documents(query)

        return {
            "memories": memories,
            "documents": documents,
        }