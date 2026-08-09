import re

from app.tools.base_tool import BaseTool


class CalculatorTool(BaseTool):
    """
    Calculator tool for evaluating basic arithmetic expressions.
    """

    name = "calculator"
    description = "Performs basic arithmetic calculations."

    keywords = [
        "calculate",
        "calculation",
        "compute",
        "solve",
        "add",
        "addition",
        "subtract",
        "subtraction",
        "multiply",
        "multiplication",
        "divide",
        "division",
        "plus",
        "minus",
        "times",
        "percent",
    ]

    def prepare_arguments(self, user_input: str):
        """
        Convert natural-language arithmetic into
        a basic mathematical expression.
        """

        text = user_input.lower().strip()

        replacements = [
            (r"\bwhat is\b", ""),
            (r"\bwhat's\b", ""),
            (r"\bcalculate\b", ""),
            (r"\bcompute\b", ""),
            (r"\bsolve\b", ""),

            (r"\bdivided by\b", "/"),
            (r"\bdivide by\b", "/"),
            (r"\bdivision by\b", "/"),

            (r"\bmultiply by\b", "*"),
            (r"\btimes\b", "*"),
            (r"\bmultiplied by\b", "*"),

            (r"\bplus\b", "+"),
            (r"\badded to\b", "+"),
            (r"\badd\b", "+"),

            (r"\bminus\b", "-"),
            (r"\bsubtracted from\b", "-"),
            (r"\bsubtract\b", "-"),

            (r"\bpercent\b", "%"),
        ]

        for pattern, replacement in replacements:
            text = re.sub(
                pattern,
                replacement,
                text
            )

        expression = re.sub(
            r"[^0-9+\-*/().% ]",
            "",
            text
        )

        expression = " ".join(
            expression.split()
        )

        return {
            "expression": expression
        }

    async def execute(self, **kwargs):
        expression = kwargs.get(
            "expression",
            ""
        )

        expression = re.sub(
            r"[^0-9+\-*/().% ]",
            "",
            expression
        ).strip()

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
