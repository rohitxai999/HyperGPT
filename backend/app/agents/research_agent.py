from typing import Any, Dict

from app.agents.base_agent import BaseAgent


class ResearchAgent(BaseAgent):
    """
    Research Agent

    Responsible for:
    - Memory lookup
    - RAG retrieval
    - Fact gathering
    """

    def __init__(self):
        super().__init__(
            name="Research Agent",
            description="Finds relevant knowledge from memory and RAG."
        )

    def execute(
        self,
        task: str,
        context: Dict[str, Any] | None = None
    ):
        return {
            "agent": self.name,
            "task": task,
            "memory": [],
            "rag_results": [],
            "facts": [],
            "status": "success"
        }