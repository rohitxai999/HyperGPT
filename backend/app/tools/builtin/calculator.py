class CalculatorTool:
    """
    Basic calculator tool.
    WARNING: eval() is only for development.
    We'll replace it with a safe math parser later.
    """

    def run(self, expression: str):
        try:
            return str(eval(expression))
        except Exception as e:
            return f"Calculation Error: {e}"