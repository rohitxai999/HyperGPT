from typing import List

from backend.app.planner.task import Task
from backend.app.planner.task_manager import TaskManager


class AutonomousPlanner:
    """
    HyperGPT autonomous planner.

    Converts a user goal into structured executable tasks
    managed by the central TaskManager.
    """

    def __init__(self, task_manager: TaskManager | None = None):
        self.task_manager = task_manager or TaskManager()

    def create_plan(self, prompt: str) -> List[Task]:
        """
        Create a structured task plan from a user prompt.

        The current planner uses deterministic intent detection.
        The architecture is designed so an LLM-based planner can
        replace the intent detection layer later.
        """

        tasks: List[Task] = []
        prompt_lower = prompt.lower()

        # ----------------------------------------------------------
        # Calculation
        # ----------------------------------------------------------

        if "calculate" in prompt_lower or "calculation" in prompt_lower:
            task = self.task_manager.create_task(
                description="Perform calculation",
                tool="calculator",
                assigned_agent="Math Agent",
                metadata={
                    "source": "AutonomousPlanner",
                    "intent": "calculation",
                },
            )
            tasks.append(task)

        # ----------------------------------------------------------
        # Time
        # ----------------------------------------------------------

        if "time" in prompt_lower:
            dependencies = [tasks[-1].id] if tasks else []

            task = self.task_manager.create_task(
                description="Get current time",
                tool="time",
                assigned_agent="Tool Agent",
                dependencies=dependencies,
                metadata={
                    "source": "AutonomousPlanner",
                    "intent": "time",
                },
            )
            tasks.append(task)

        # ----------------------------------------------------------
        # Save / File Writing
        # ----------------------------------------------------------

        if "save" in prompt_lower or "write" in prompt_lower:
            dependencies = [tasks[-1].id] if tasks else []

            task = self.task_manager.create_task(
                description="Save report",
                tool="file_writer",
                assigned_agent="Writing Agent",
                dependencies=dependencies,
                metadata={
                    "source": "AutonomousPlanner",
                    "intent": "file_creation",
                },
            )
            tasks.append(task)

        # ----------------------------------------------------------
        # General Reasoning
        # ----------------------------------------------------------

        if not tasks:
            task = self.task_manager.create_task(
                description="General reasoning",
                tool="none",
                assigned_agent="Orchestrator",
                metadata={
                    "source": "AutonomousPlanner",
                    "intent": "general_reasoning",
                },
            )
            tasks.append(task)

        return tasks

    def get_execution_trace(self):
        """Return the planner's execution trace."""
        return self.task_manager.get_execution_trace()

    def get_execution_summary(self):
        """Return the current execution summary."""
        return self.task_manager.get_execution_summary()