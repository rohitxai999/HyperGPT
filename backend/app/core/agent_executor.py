import asyncio
import inspect
from typing import Any

from app.core.planner import ExecutionPlan, TaskPlanner


class AgentExecutor:
    """
    Executes HyperGPT plans.

    Supports:
    1. Existing synchronous tool executors.
    2. Real asynchronous ToolExecutor.
    """

    def __init__(self, tool_executor):
        self.tool_executor = tool_executor
        self.planner = TaskPlanner()

    def _build_user_input(
        self,
        tool_name: str,
        arguments: dict[str, Any],
    ) -> str:
        """
        Convert structured planner arguments into
        natural-language input for the real ToolExecutor.
        """

        if tool_name == "calculator":

            operation = arguments.get("operation")

            if operation == "add":
                return (
                    f"calculate "
                    f"{arguments['a']} plus {arguments['b']}"
                )

            if operation == "subtract":
                return (
                    f"calculate "
                    f"{arguments['a']} minus {arguments['b']}"
                )

            if operation == "multiply":
                return (
                    f"calculate "
                    f"{arguments['a']} times {arguments['b']}"
                )

            if operation == "divide":
                return (
                    f"calculate "
                    f"{arguments['a']} divided by {arguments['b']}"
                )

        return arguments.get(
            "user_input",
            ""
        )

    def _execute_sync(
        self,
        tool_name: str,
        arguments: dict[str, Any],
    ):
        """
        Execute against the legacy synchronous executor.
        """

        return self.tool_executor.execute(
            tool_name,
            arguments
        )

    async def _execute_async(
        self,
        tool_name: str,
        arguments: dict[str, Any],
    ):
        """
        Execute against the real asynchronous ToolExecutor.
        """

        user_input = self._build_user_input(
            tool_name,
            arguments
        )

        result = self.tool_executor.execute(
            user_input
        )

        if inspect.isawaitable(result):
            return await result

        return result

    def _is_real_async_executor(self) -> bool:
        """
        Detect whether the supplied executor exposes
        an asynchronous execute() method.
        """

        execute_method = getattr(
            self.tool_executor,
            "execute",
            None
        )

        return (
            execute_method is not None
            and inspect.iscoroutinefunction(
                execute_method
            )
        )

    def execute_plan(
        self,
        plan: ExecutionPlan,
    ):
        """
        Public synchronous API.

        Preserves compatibility with the original
        AgentExecutor tests.
        """

        if self._is_real_async_executor():

            return self._execute_real_async_plan(
                plan
            )

        return self._execute_sync_plan(
            plan
        )

    def _execute_sync_plan(
        self,
        plan: ExecutionPlan,
    ) -> ExecutionPlan:
        """
        Execute plans using synchronous executors.
        """

        self.planner.start(plan)

        for step in plan.steps:

            try:

                result = self._execute_sync(
                    step.tool,
                    step.arguments
                )

                self.planner.complete_step(
                    step,
                    result
                )

            except Exception as exc:

                self.planner.fail_step(
                    step,
                    str(exc)
                )

                self.planner.fail_plan(
                    plan
                )

                return plan

        self.planner.complete_plan(
            plan
        )

        return plan

    async def _execute_real_async_plan(
        self,
        plan: ExecutionPlan,
    ) -> ExecutionPlan:
        """
        Execute plans using the real asynchronous
        HyperGPT ToolExecutor.
        """

        self.planner.start(plan)

        for step in plan.steps:

            try:

                result = await self._execute_async(
                    step.tool,
                    step.arguments
                )

                if isinstance(result, dict):

                    success = result.get(
                        "success",
                        True
                    )

                    if not success:

                        self.planner.fail_step(
                            step,
                            result
                        )

                        self.planner.fail_plan(
                            plan
                        )

                        return plan

                self.planner.complete_step(
                    step,
                    result
                )

            except Exception as exc:

                self.planner.fail_step(
                    step,
                    str(exc)
                )

                self.planner.fail_plan(
                    plan
                )

                return plan

        self.planner.complete_plan(
            plan
        )

        return plan