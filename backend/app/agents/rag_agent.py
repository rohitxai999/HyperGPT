from typing import Any, Dict

from app.agents.base_agent import BaseAgent


class RAGAgent(BaseAgent):

    def __init__(self):
        super().__init__(
            name="RAG Agent",
            description="Retrieves relevant information from the knowledge base."
        )

    def can_handle(self, query: str) -> bool:
        keywords = [
            "document",
            "pdf",
            "file",
            "knowledge",
            "rag",
            "retrieve",
        ]

        return any(
            word in query.lower()
            for word in keywords
        )

    def execute(
        self,
        task: str,
        context: Dict[str, Any] | None = None
    ):
        return self.run(task, context=context)

    def run(
        self,
        query: str,
        context: Dict[str, Any] | None = None
    ):
        context = context or {}

        return {
            "agent": self.name,
            "response": f"Searching knowledge base for: {query}",
            "memory_used": context.get("memories", []),
            "rag_used": context.get("documents", []),
        }