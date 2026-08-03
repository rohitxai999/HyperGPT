from app.tools.builtin.calculator import CalculatorTool
from app.tools.builtin.time_tool import TimeTool


class ToolRegistry:
    def __init__(self):
        self.tools = {
            "calculator": CalculatorTool(),
            "time": TimeTool(),
        }

    def get(self, tool_name: str):
        return self.tools.get(tool_name)

    def list_tools(self):
        return list(self.tools.keys())