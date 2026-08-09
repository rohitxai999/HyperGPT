from app.tools.selector import ToolSelector
from app.tools.logger import logger


class ToolExecutor:
    """
    Generic executor for HyperGPT tools.

    Uses explainable tool selection and delegates
    argument preparation to the selected tool.
    """

    def __init__(self):
        self.selector = ToolSelector()

    async def execute(self, user_input: str):
        """
        Select and execute the appropriate tool.
        """

        selection = self.selector.select_with_explanation(
            user_input
        )

        selected_name = selection["selected_tool"]

        if selected_name is None:
            result = {
                "success": False,
                "message": "No suitable tool found.",
                "selection": selection
            }

            logger.log(
                "none",
                user_input,
                result
            )

            return result

        tool = self.selector.select(user_input)

        if tool is None:
            result = {
                "success": False,
                "message": "Selected tool could not be loaded.",
                "selection": selection
            }

            logger.log(
                "none",
                user_input,
                result
            )

            return result

        try:
            arguments = tool.prepare_arguments(
                user_input
            )

            result = await tool.execute(
                **arguments
            )

        except Exception as exc:

            result = {
                "success": False,
                "tool": tool.name,
                "message": "Tool execution failed.",
                "error": str(exc)
            }

        # Attach selection information to the result.
        if isinstance(result, dict):
            result["selection"] = selection

        logger.log(
            tool.name,
            user_input,
            result
        )

        return result
