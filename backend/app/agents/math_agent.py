from typing import Any, Dict

from app.agents.base_agent import BaseAgent


class MathAgent(BaseAgent):

    def __init__(self):
        super().__init__(
            name="Math Agent",
            description="Handles mathematical problems and calculations."
        )

    def can_handle(self, query: str) -> bool:

        keywords = [
            "calculate",
            "solve",
            "equation",
            "math",
            "algebra",
            "integral",
            "derivative",
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

        return self.run(
            task,
            context=context
        )

    def run(
        self,
        query: str,
        context: Dict[str, Any] | None = None
    ):

        return {
            "agent": self.name,
            "response": f"Solving math problem: {query}",
            "memory_used": (
                context.get("memories", [])
                if context
                else []
            ),
        }