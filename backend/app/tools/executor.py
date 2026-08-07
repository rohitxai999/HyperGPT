from app.tools.selector import ToolSelector
from app.tools.logger import logger


class ToolExecutor:
    """
    Executes the appropriate tool based on the user's request.
    """

    def __init__(self):
        self.selector = ToolSelector()

    async def execute(self, user_input: str):
        tool = self.selector.select(user_input)

        if tool is None:
            result = {
                "success": False,
                "message": "No suitable tool found."
            }

            logger.log("none", user_input, result)
            return result

        # Calculator Tool
        if tool.name == "calculator":
            expression = (
                user_input.lower()
                .replace("calculate", "")
                .strip()
            )

            result = await tool.execute(expression=expression)

        # Date & Time Tool
        elif tool.name == "datetime":
            result = await tool.execute()

        # Unknown Tool
        else:
            result = {
                "success": False,
                "message": "Tool execution not implemented."
            }

        # Log every execution
        logger.log(tool.name, user_input, result)

        return result