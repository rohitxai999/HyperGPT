from typing import Any, Dict

from app.agents.base_agent import BaseAgent


class ResearchAgent(BaseAgent):

    def __init__(self):
        super().__init__(
            name="Research Agent",
            description="Finds relevant knowledge from memory and RAG."
        )

    def can_handle(self, query: str) -> bool:

        keywords = [
            "remember",
            "memory",
            "prefer",
            "preferred",
            "previous",
            "before",
            "earlier",
            "my",
            "what do i",
            "what did i",
            "do you know about me",
        ]

        query_lower = query.lower()

        return any(
            keyword in query_lower
            for keyword in keywords
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

        memories = context.get("memories", [])

        documents = context.get("documents", [])

        if memories:

            best_memory = memories[0]

            response = (
                f"Based on my memory, "
                f"{best_memory['content']}"
            )

        elif documents:

            response = (
                "I found relevant information "
                "in the knowledge base."
            )

        else:

            response = (
                "I don't have a relevant memory "
                "for this request."
            )

        return {
            "agent": self.name,
            "response": response,
            "memory_used": memories,
            "rag_used": documents,
        }