from backend.app.tools.calculator_tool import CalculatorTool
from backend.app.tools.time_tool import TimeTool
from backend.app.tools.file_writer_tool import FileWriterTool


class ToolRegistry:

    def __init__(self):

        self.tools = {
            "calculator": CalculatorTool(),
            "time": TimeTool(),
            "file_writer": FileWriterTool()
        }

    def get(self, tool_name: str):
        return self.tools.get(tool_name)
