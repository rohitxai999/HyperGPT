import re
from typing import Any, Dict

from app.agents.base_agent import BaseAgent
from app.core.planner import TaskPlanner
from app.core.agent_executor import AgentExecutor
from app.tools.executor import ToolExecutor


class MathAgent(BaseAgent):

    def __init__(self):
        super().__init__(
            name="Math Agent",
            description="Handles mathematical problems and calculations."
        )

        self.planner = TaskPlanner()
        self.tool_executor = ToolExecutor()
        self.agent_executor = AgentExecutor(
            self.tool_executor
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
            "multiply",
            "add",
            "subtract",
            "divide",
        ]

        return any(
            word in query.lower()
            for word in keywords
        )

    async def execute(
        self,
        task: str,
        context: Dict[str, Any] | None = None
    ):
        return await self.run(
            task,
            context=context
        )

    async def run(
        self,
        query: str,
        context: Dict[str, Any] | None = None
    ):

        plan = self.planner.create_plan(
            query
        )

        normalized_query = query.lower()

        # ---------------------------------
        # Extract numbers
        # ---------------------------------

        numbers = re.findall(
            r"-?\d+(?:\.\d+)?",
            query
        )

        # ---------------------------------
        # Create calculator plan
        # ---------------------------------

        if len(numbers) >= 2:

            a = float(numbers[0])
            b = float(numbers[1])

            if a.is_integer():
                a = int(a)

            if b.is_integer():
                b = int(b)

            if "multiply" in normalized_query:

                self.planner.add_step(
                    plan,
                    query,
                    "calculator",
                    {
                        "operation": "multiply",
                        "a": a,
                        "b": b,
                    },
                )

            elif "add" in normalized_query:

                self.planner.add_step(
                    plan,
                    query,
                    "calculator",
                    {
                        "operation": "add",
                        "a": a,
                        "b": b,
                    },
                )

            elif "subtract" in normalized_query:

                self.planner.add_step(
                    plan,
                    query,
                    "calculator",
                    {
                        "operation": "subtract",
                        "a": a,
                        "b": b,
                    },
                )

            elif "divide" in normalized_query:

                self.planner.add_step(
                    plan,
                    query,
                    "calculator",
                    {
                        "operation": "divide",
                        "a": a,
                        "b": b,
                    },
                )

        # ---------------------------------
        # No executable plan
        # ---------------------------------

        if not plan.steps:

            return {
                "agent": self.name,
                "response": (
                    f"Unable to create a calculator plan for: {query}"
                ),
                "memory_used": (
                    context.get("memories", [])
                    if context
                    else []
                ),
                "status": "failed",
            }

        # ---------------------------------
        # Execute asynchronously
        # ---------------------------------

        plan = await self.agent_executor.execute_plan(
            plan
        )

        # ---------------------------------
        # Find completed steps
        # ---------------------------------

        completed_steps = [
            step
            for step in plan.steps
            if step.status == "completed"
        ]

        # ---------------------------------
        # Execution failure
        # ---------------------------------

        if not completed_steps:

            return {
                "agent": self.name,
                "response": (
                    f"Math execution failed for: {query}"
                ),
                "memory_used": (
                    context.get("memories", [])
                    if context
                    else []
                ),
                "status": "failed",
                "plan_status": plan.status,
            }

        # ---------------------------------
        # Get final result
        # ---------------------------------

        result = completed_steps[-1].result

        if isinstance(result, dict):
            final_result = result.get(
                "result",
                result
            )
        else:
            final_result = result

        return {
            "agent": self.name,
            "response": str(final_result),
            "memory_used": (
                context.get("memories", [])
                if context
                else []
            ),
            "status": "success",
            "plan_status": plan.status,
            "execution_plan": plan,
        }