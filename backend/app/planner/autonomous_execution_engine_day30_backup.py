from typing import Any, Callable, Dict, Optional

from backend.app.planner.task import Task
from backend.app.planner.task_manager import TaskManager


class AutonomousExecutionEngine:
    """
    Executes HyperGPT tasks according to their dependency graph.

    Responsibilities:
    - Respect task dependencies
    - Start tasks
    - Execute task handlers
    - Capture results
    - Handle failures
    - Retry failed tasks
    - Record execution trace
    """

    def __init__(
        self,
        task_manager: TaskManager,
        handlers: Optional[Dict[str, Callable[..., Any]]] = None,
    ):
        self.task_manager = task_manager
        self.handlers = handlers or {}

    def register_handler(
        self,
        tool_name: str,
        handler: Callable[..., Any],
    ) -> None:
        """Register a function capable of executing a tool."""
        self.handlers[tool_name] = handler

    def execute_task(self, task: Task) -> Any:
        """
        Execute a single task using its registered handler.
        """

        handler = self.handlers.get(task.tool)

        if handler is None:
            raise RuntimeError(
                f"No execution handler registered for tool "
                f"'{task.tool}'."
            )

        return handler(task)

    def execute_plan(self) -> Dict[str, Any]:
        """
        Execute all tasks while respecting dependencies.
        """

        tasks = self.task_manager.get_all_tasks()

        execution_results = []

        for task in tasks:

            if task.status == "COMPLETED":
                continue

            if not self.task_manager.dependencies_completed(task):
                execution_results.append(
                    {
                        "task_id": task.id,
                        "status": "BLOCKED",
                        "reason": "Dependencies not completed",
                    }
                )
                continue

            success = self._execute_with_retry(task)

            execution_results.append(
                {
                    "task_id": task.id,
                    "status": (
                        "COMPLETED"
                        if success
                        else "FAILED"
                    ),
                    "result": task.result,
                    "error": task.error,
                }
            )

        return {
            "status": self._overall_status(),
            "results": execution_results,
            "summary": self.task_manager.get_execution_summary(),
            "trace": self.task_manager.get_execution_trace(),
        }

    def _execute_with_retry(self, task: Task) -> bool:
        """Execute a task and retry when execution fails."""

        while True:

            try:
                self.task_manager.start_task(task.id)

                result = self.execute_task(task)

                self.task_manager.complete_task(
                    task.id,
                    result,
                )

                return True

            except Exception as exc:

                self.task_manager.fail_task(
                    task.id,
                    str(exc),
                )

                if not self.task_manager.retry_task(task.id):
                    return False

    def _overall_status(self) -> str:
        """Determine the overall execution status."""

        tasks = self.task_manager.get_all_tasks()

        if not tasks:
            return "EMPTY"

        if any(task.status == "FAILED" for task in tasks):
            return "FAILED"

        if all(task.status == "COMPLETED" for task in tasks):
            return "COMPLETED"

        return "PARTIAL"