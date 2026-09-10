import re
from typing import Any, Dict, Optional

from backend.app.agents.base_agent import BaseAgent
from backend.app.tools.registry import ToolRegistry


class MathAgent(BaseAgent):
    """
    HyperGPT Math Agent.

    Converts natural-language arithmetic requests into
    calculator-tool executions.
    """

    def __init__(self):
        super().__init__(
            name="Math Agent",
            description="Handles mathematical problems and calculations.",
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
            "multiplied",
            "times",
            "add",
            "plus",
            "subtract",
            "minus",
            "divide",
            "divided",
        ]

        normalized = query.lower()
        return any(keyword in normalized for keyword in keywords)

    async def execute(
        self,
        task: str,
        context: Optional[Dict[str, Any]] = None,
    ):
        return await self.run(task, context=context)

    async def run(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None,
    ):
        context = context or {}
        normalized_query = query.lower()

        numbers = re.findall(
            r"-?\d+(?:\.\d+)?",
            query,
        )

        if len(numbers) < 2:
            return {
                "agent": self.name,
                "response": (
                    f"Unable to create a calculator plan for: {query}"
                ),
                "memory_used": context.get("memories", []),
                "status": "failed",
            }

        a = float(numbers[0])
        b = float(numbers[1])

        if a.is_integer():
            a = int(a)

        if b.is_integer():
            b = int(b)

        operation = None

        if any(
            word in normalized_query
            for word in ["multiply", "multiplied", "times"]
        ):
            operation = "multiply"

        elif any(
            word in normalized_query
            for word in ["add", "plus"]
        ):
            operation = "add"

        elif any(
            word in normalized_query
            for word in ["subtract", "minus"]
        ):
            operation = "subtract"

        elif any(
            word in normalized_query
            for word in ["divide", "divided"]
        ):
            operation = "divide"

        if operation is None:
            return {
                "agent": self.name,
                "response": (
                    f"Unable to determine the mathematical operation "
                    f"for: {query}"
                ),
                "memory_used": context.get("memories", []),
                "status": "failed",
            }

        registry = ToolRegistry()

        # Use the existing registry API.
        if hasattr(registry, "auto_register"):
            registry.auto_register()

        tool = registry.get("calculator")

        if tool is None:
            return {
                "agent": self.name,
                "response": "Calculator tool is unavailable.",
                "memory_used": context.get("memories", []),
                "status": "failed",
            }

        result = tool.execute(
            operation=operation,
            a=a,
            b=b,
        )

        if hasattr(result, "__await__"):
            result = await result

        if isinstance(result, dict):
            if result.get("success") is False:
                return {
                    "agent": self.name,
                    "response": str(result),
                    "memory_used": context.get("memories", []),
                    "status": "failed",
                    "error": result,
                }

            final_result = result.get("result", result)

        else:
            final_result = result

        return {
            "agent": self.name,
            "response": str(final_result),
            "memory_used": context.get("memories", []),
            "status": "success",
            "operation": operation,
            "inputs": {
                "a": a,
                "b": b,
            },
            "result": final_result,
        }