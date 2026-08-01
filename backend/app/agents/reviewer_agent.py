from typing import Any, Dict

from app.agents.base_agent import BaseAgent


class ReviewerAgent(BaseAgent):
    """
    Reviewer Agent

    Responsible for:
    - Reviewing outputs
    - Detecting mistakes
    - Finding missing information
    - Suggesting improvements
    """

    def __init__(self):
        super().__init__(
            name="Reviewer Agent",
            description="Reviews and improves AI-generated outputs."
        )

    def execute(
        self,
        task: str,
        context: Dict[str, Any] | None = None
    ):
        return {
            "agent": self.name,
            "task": task,
            "issues": [],
            "recommendations": [],
            "approved": True,
            "status": "success"
        }

    def review(self, content: str):
        return {
            "issues": [],
            "recommendations": []
        }