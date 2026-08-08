from typing import Any, Dict

from app.agents.base_agent import BaseAgent


class WritingAgent(BaseAgent):

    def __init__(self):
        super().__init__(
            name="Writing Agent",
            description="Creates and formats written content."
        )

    def can_handle(self, query: str) -> bool:

        keywords = [
            "write",
            "essay",
            "email",
            "letter",
            "blog",
            "story",
            "poem",
            "caption",
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
            "response": f"Writing request received: {query}",
            "memory_used": (
                context.get("memories", [])
                if context
                else []
            ),
        }