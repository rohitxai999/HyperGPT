import re

from app.tools.base_tool import BaseTool


class CalculatorTool(BaseTool):
    """
    Calculator tool for evaluating basic arithmetic expressions.

    Supports:
    - Natural-language arithmetic through prepare_arguments()
    - Structured arithmetic through operation/a/b arguments
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
            text = re.sub(pattern, replacement, text)

        expression = re.sub(
            r"[^0-9+\-*/().% ]",
            "",
            text,
        )

        expression = " ".join(expression.split())

        return {
            "expression": expression,
        }

    async def execute(self, **kwargs):
        """
        Execute either a structured arithmetic operation
        or a prepared mathematical expression.
        """

        operation = kwargs.get("operation")
        a = kwargs.get("a")
        b = kwargs.get("b")

        # ==================================================
        # STRUCTURED OPERATION MODE
        # ==================================================

        if operation is not None:
            try:
                if a is None or b is None:
                    return {
                        "success": False,
                        "error": "Both 'a' and 'b' are required.",
                    }

                operation = str(operation).lower().strip()

                if operation in {"add", "addition", "plus"}:
                    result = a + b

                elif operation in {
                    "subtract",
                    "subtraction",
                    "minus",
                }:
                    result = a - b

                elif operation in {
                    "multiply",
                    "multiplication",
                    "times",
                }:
                    result = a * b

                elif operation in {
                    "divide",
                    "division",
                }:
                    if b == 0:
                        return {
                            "success": False,
                            "error": "Division by zero is not allowed.",
                        }

                    result = a / b

                else:
                    return {
                        "success": False,
                        "error": f"Unsupported operation: {operation}",
                    }

                return {
                    "success": True,
                    "operation": operation,
                    "a": a,
                    "b": b,
                    "result": result,
                }

            except (TypeError, ValueError) as exc:
                return {
                    "success": False,
                    "operation": operation,
                    "error": str(exc),
                }

        # ==================================================
        # EXPRESSION MODE
        # ==================================================

        expression = kwargs.get("expression", "")

        expression = re.sub(
            r"[^0-9+\-*/().% ]",
            "",
            expression,
        ).strip()

        if not expression:
            return {
                "success": False,
                "error": "No valid mathematical expression provided.",
            }

        try:
            result = eval(
                expression,
                {"__builtins__": {}},
                {},
            )

            return {
                "success": True,
                "expression": expression,
                "result": result,
            }

        except Exception as exc:
            return {
                "success": False,
                "expression": expression,
                "error": str(exc),
            }