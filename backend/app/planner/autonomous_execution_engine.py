from typing import Any, Dict, Optional

from backend.app.planner.task import Task
from backend.app.planner.task_manager import TaskManager
from backend.app.tools.registry import ToolRegistry


class AutonomousExecutionEngine:
    """
    Executes autonomous HyperGPT plans using the unified ToolRegistry.

    Pipeline:

        TaskManager
             ↓
        AutonomousExecutionEngine
             ↓
        ToolRegistry
             ↓
        Tool
             ↓
        Result
    """

    def __init__(
        self,
        task_manager: TaskManager,
        tool_registry: Optional[ToolRegistry] = None,
    ):
        self.task_manager = task_manager

        if tool_registry is None:
            from backend.app.tools.registry import registry

            self.tool_registry = registry

            if not self.tool_registry.tools:
                self.tool_registry.auto_register()
        else:
            self.tool_registry = tool_registry

    async def execute_task(self, task: Task) -> Any:
        """
        Execute one task through the unified ToolRegistry.
        """

        tool = self.tool_registry.get(task.tool)

        if tool is None:
            raise RuntimeError(
                f"No tool registered for '{task.tool}'."
            )

        parameters = task.metadata.get("parameters", {})

        result = tool.execute(**parameters)

        if hasattr(result, "__await__"):
            result = await result

        if isinstance(result, dict):
            if result.get("success") is False:
                raise RuntimeError(
                    result.get(
                        "error",
                        result.get(
                            "message",
                            "Tool execution failed.",
                        ),
                    )
                )

        return result

    async def execute_plan(self) -> Dict[str, Any]:
        """
        Execute all tasks while respecting dependencies.
        """

        tasks = self.task_manager.get_all_tasks()

        execution_results = []

        for task in tasks:

            if task.status == "COMPLETED":
                execution_results.append(
                    {
                        "task_id": task.id,
                        "status": "COMPLETED",
                        "result": task.result,
                    }
                )
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

            success = await self._execute_with_retry(task)

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
            "summary": (
                self.task_manager
                .get_execution_summary()
            ),
            "trace": (
                self.task_manager
                .get_execution_trace()
            ),
        }

    async def _execute_with_retry(
        self,
        task: Task,
    ) -> bool:

        while True:

            try:

                self.task_manager.start_task(task.id)

                result = await self.execute_task(task)

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

                if not self.task_manager.retry_task(
                    task.id
                ):
                    return False

    def _overall_status(self) -> str:

        tasks = self.task_manager.get_all_tasks()

        if not tasks:
            return "EMPTY"

        if any(
            task.status == "FAILED"
            for task in tasks
        ):
            return "FAILED"

        if all(
            task.status == "COMPLETED"
            for task in tasks
        ):
            return "COMPLETED"

        return "PARTIAL"