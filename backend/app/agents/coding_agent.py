import re
from typing import Any, Dict

from app.agents.base_agent import BaseAgent


class CodingAgent(BaseAgent):
    """
    Coding Agent

    Responsible for:
    - Code generation
    - Bug fixing
    - Code explanation
    - Code optimization
    """

    def __init__(self):
        super().__init__(
            name="Coding Agent",
            description="Generates, explains and improves code."
        )

    def execute(
        self,
        task: str,
        context: Dict[str, Any] | None = None
    ):
        """
        Main entry point for the Coding Agent.
        """

        task_lower = task.lower()

        # ---------------------------------
        # Code generation
        # ---------------------------------

        if any(
            keyword in task_lower
            for keyword in [
                "write code",
                "write python",
                "python code",
                "generate code",
                "create code",
                "code for",
                "function",
                "program",
                "script",
            ]
        ):
            generated_code = self.generate_code(task)

            return {
                "agent": self.name,
                "task": task,
                "generated_code": generated_code,
                "explanation": self._generate_explanation(
                    task,
                    generated_code
                ),
                "suggestions": [
                    "Test the generated code.",
                    "Add input validation for production use.",
                    "Add unit tests for important functions.",
                ],
                "status": "success",
            }

        # ---------------------------------
        # Code explanation
        # ---------------------------------

        if any(
            keyword in task_lower
            for keyword in [
                "explain code",
                "explain this code",
                "explain the code",
            ]
        ):
            return {
                "agent": self.name,
                "task": task,
                "generated_code": "",
                "explanation": (
                    "Please provide the code you want me "
                    "to explain."
                ),
                "suggestions": [],
                "status": "success",
            }

        # ---------------------------------
        # General coding request
        # ---------------------------------

        generated_code = self.generate_code(task)

        return {
            "agent": self.name,
            "task": task,
            "generated_code": generated_code,
            "explanation": self._generate_explanation(
                task,
                generated_code
            ),
            "suggestions": [],
            "status": "success",
        }

    def generate_code(self, prompt: str):
        """
        Generate code from a natural-language prompt.

        This version provides deterministic templates for
        common coding tasks and acts as the foundation for
        future LLM-based generation.
        """

        prompt_lower = prompt.lower()

        # ---------------------------------
        # Factorial
        # ---------------------------------

        if "factorial" in prompt_lower:

            return """def factorial(n):
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers.")

    result = 1

    for i in range(2, n + 1):
        result *= i

    return result


# Example
print(factorial(5))
"""

        # ---------------------------------
        # Fibonacci
        # ---------------------------------

        if "fibonacci" in prompt_lower:

            return """def fibonacci(n):
    if n < 0:
        raise ValueError("n must be non-negative.")

    a, b = 0, 1

    for _ in range(n):
        a, b = b, a + b

    return a


# Example
print(fibonacci(10))
"""

        # ---------------------------------
        # Prime number
        # ---------------------------------

        if (
            "prime number" in prompt_lower
            or "check prime" in prompt_lower
        ):

            return """def is_prime(n):
    if n < 2:
        return False

    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False

    return True


# Example
print(is_prime(17))
"""

        # ---------------------------------
        # Palindrome
        # ---------------------------------

        if "palindrome" in prompt_lower:

            return """def is_palindrome(text):
    cleaned = text.lower().replace(" ", "")

    return cleaned == cleaned[::-1]


# Example
print(is_palindrome("madam"))
"""

        # ---------------------------------
        # Calculator
        # ---------------------------------

        if (
            "calculator" in prompt_lower
            or "calculate" in prompt_lower
        ):

            return """def calculator(a, b, operation):
    if operation == "add":
        return a + b

    if operation == "subtract":
        return a - b

    if operation == "multiply":
        return a * b

    if operation == "divide":
        if b == 0:
            raise ValueError("Cannot divide by zero.")
        return a / b

    raise ValueError("Unknown operation.")


# Example
print(calculator(10, 5, "multiply"))
"""

        # ---------------------------------
        # Generic Python function
        # ---------------------------------

        if "python" in prompt_lower:

            return """def main():
    print("Hello from HyperGPT Coding Agent")


if __name__ == "__main__":
    main()
"""

        # ---------------------------------
        # Fallback
        # ---------------------------------

        return (
            "# HyperGPT Coding Agent\n"
            "# Code generation template created.\n"
            "# A future LLM generation engine can replace "
            "this fallback.\n"
        )

    def explain_code(self, code: str):
        """
        Provide a basic explanation of supplied code.
        """

        if not code.strip():
            return "No code was provided."

        lines = [
            line.strip()
            for line in code.splitlines()
            if line.strip()
        ]

        functions = re.findall(
            r"def\s+([a-zA-Z_]\w*)\s*\(",
            code
        )

        explanation = []

        if functions:
            explanation.append(
                "Functions found: "
                + ", ".join(functions)
            )

        explanation.append(
            f"The code contains approximately "
            f"{len(lines)} non-empty lines."
        )

        return " ".join(explanation)

    def optimize_code(self, code: str):
        """
        Placeholder optimization interface.
        """

        if not code.strip():
            return ""

        return code

    def debug_code(self, code: str):
        """
        Basic debugging interface.
        """

        if not code.strip():
            return {
                "status": "failed",
                "error": "No code provided."
            }

        return {
            "status": "success",
            "message": "No automatic syntax analysis performed yet.",
            "code": code,
        }

    def _generate_explanation(
        self,
        task: str,
        code: str
    ) -> str:
        """
        Generate a concise explanation for generated code.
        """

        if "factorial" in task.lower():
            return (
                "The function calculates the factorial of a "
                "non-negative integer using an iterative loop."
            )

        if "fibonacci" in task.lower():
            return (
                "The function generates the Fibonacci sequence "
                "iteratively using two variables."
            )

        if "prime" in task.lower():
            return (
                "The function checks whether a number is prime "
                "by testing divisibility up to its square root."
            )

        if "palindrome" in task.lower():
            return (
                "The function normalizes the text and checks "
                "whether it reads the same forwards and backwards."
            )

        return (
            "The Coding Agent generated a Python implementation "
            "based on the requested task."
        )