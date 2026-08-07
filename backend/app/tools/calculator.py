import re

from app.tools.base_tool import BaseTool


class CalculatorTool(BaseTool):
    """
    Calculator tool for evaluating basic arithmetic expressions.
    """

    name = "calculator"
    description = "Performs basic arithmetic calculations."

    async def execute(self, **kwargs):
        expression = kwargs.get("expression", "")

        # Extract only numbers, operators, parentheses and decimal points
        expression = expression.lower()
        expression = re.sub(r"[^0-9+\-*/().% ]", "", expression)
        expression = expression.strip()

        try:
            result = eval(expression)

            return {
                "success": True,
                "expression": expression,
                "result": result,
            }

        except Exception as e:
            return {
                "success": False,
                "expression": expression,
                "error": str(e),
            }