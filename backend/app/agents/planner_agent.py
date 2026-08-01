from typing import Any, Dict

from app.agents.base_agent import BaseAgent


class PlannerAgent(BaseAgent):
    """
    Planner Agent

    Responsible for:
    - Breaking large tasks into steps
    - Creating execution plans
    - Managing priorities
    """

    def __init__(self):
        super().__init__(
            name="Planner Agent",
            description="Creates structured plans for complex tasks."
        )

    def execute(
        self,
        task: str,
        context: Dict[str, Any] | None = None
    ):
        return {
            "agent": self.name,
            "task": task,
            "plan": [
                "Understand the problem",
                "Break into smaller tasks",
                "Execute each task",
                "Verify the result"
            ],
            "status": "success"
        }

    def create_plan(self, goal: str):
        return []