from datetime import datetime


class ToolLogger:
    """
    Logs tool executions in memory.
    """

    def __init__(self):
        self.history = []

    def log(self, tool_name: str, user_input: str, result: dict):
        self.history.append(
            {
                "timestamp": datetime.now().isoformat(),
                "tool": tool_name,
                "input": user_input,
                "result": result,
            }
        )

    def get_history(self):
        return self.history

    def clear(self):
        self.history.clear()


logger = ToolLogger()