from app.tools.registry import registry


class ToolSelector:
    """
    Selects the most appropriate tool based on the user's request.
    """

    def __init__(self):
        registry.auto_register()

    def select(self, user_input: str):
        """
        Select the appropriate tool.
        """

        text = user_input.lower()

        # Calculator keywords
        calculator_keywords = [
            "+", "-", "*", "/", "%",
            "calculate", "add", "subtract",
            "multiply", "divide"
        ]

        if any(keyword in text for keyword in calculator_keywords):
            return registry.get("calculator")

        # Date & Time keywords
        datetime_keywords = [
            "time",
            "date",
            "day",
            "today",
            "clock"
        ]

        if any(keyword in text for keyword in datetime_keywords):
            return registry.get("datetime")

        return None