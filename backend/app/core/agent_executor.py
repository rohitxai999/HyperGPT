import inspect
from typing import Any


class AgentExecutor:
    """Executes HyperGPT agent plans using registered tools."""

    def __init__(self, tool_executor=None):
        self.tool_executor = tool_executor

    def execute_plan(self, plan):
        """
        Execute a plan.

        Supports both:
        - asynchronous real tool executors
        - synchronous legacy/mock executors
        """

        if self.tool_executor is not None:
            execute_method = self.tool_executor.execute

            if inspect.iscoroutinefunction(execute_method):
                return self._execute_plan_async(plan)

        return self._execute_plan_sync(plan)

    def _execute_plan_sync(self, plan):
        """Execute a plan using a synchronous tool executor."""

        for step in plan.steps:
            try:
                step.status = "running"

                if self.tool_executor is None:
                    result = step.parameters

                else:
                    execute_method = self.tool_executor.execute

                    parameter_count = len(
                        inspect.signature(execute_method).parameters
                    )

                    if parameter_count >= 2:
                        result = execute_method(
                            step.tool,
                            step.parameters,
                        )
                    else:
                        result = execute_method(
                            step.description
                        )

                    if inspect.isawaitable(result):
                        raise RuntimeError(
                            "Asynchronous tool executor requires "
                            "awaiting execute_plan()."
                        )

                    if (
                        isinstance(result, dict)
                        and result.get("success") is False
                    ):
                        raise RuntimeError(
                            result.get(
                                "error",
                                result.get(
                                    "message",
                                    "Tool execution failed.",
                                ),
                            )
                        )

                step.result = result
                step.status = "completed"

            except Exception as exc:
                step.status = "failed"
                step.result = {
                    "success": False,
                    "error": str(exc),
                }
                plan.status = "failed"
                return plan

        plan.status = "completed"
        return plan

    async def _execute_plan_async(self, plan):
        """Execute a plan using an asynchronous tool executor."""

        for step in plan.steps:
            try:
                step.status = "running"

                if self.tool_executor is None:
                    result = step.parameters

                else:
                    execute_method = self.tool_executor.execute

                    parameter_count = len(
                        inspect.signature(execute_method).parameters
                    )

                    if parameter_count >= 2:
                        result = execute_method(
                            step.tool,
                            step.parameters,
                        )
                    else:
                        result = execute_method(
                            step.description
                        )

                    if inspect.isawaitable(result):
                        result = await result

                    if (
                        isinstance(result, dict)
                        and result.get("success") is False
                    ):
                        raise RuntimeError(
                            result.get(
                                "error",
                                result.get(
                                    "message",
                                    "Tool execution failed.",
                                ),
                            )
                        )

                step.result = result
                step.status = "completed"

            except Exception as exc:
                step.status = "failed"
                step.result = {
                    "success": False,
                    "error": str(exc),
                }
                plan.status = "failed"
                return plan

        plan.status = "completed"
        return plan

    def execute(self, task: Any, context=None):
        """Synchronous compatibility method."""
        return {
            "task": task,
            "status": "completed",
            "result": task,
        }

    def run(self, task: Any, context=None):
        """Compatibility wrapper."""
        return self.execute(task, context)