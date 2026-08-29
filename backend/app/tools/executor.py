from app.tools.selector import ToolSelector
from app.tools.registry import registry
from app.tools.logger import logger


class ToolExecutor:
    """
    Generic executor for HyperGPT tools.

    Supports explicit tool execution from AgentExecutor
    and automatic tool selection.
    """

    def __init__(self):
        self.selector = ToolSelector()

    async def execute(
        self,
        tool_or_input: str,
        arguments=None,
    ):
        """
        Execute a tool.

        Explicit mode:
            execute("calculator", {...})

        Automatic mode:
            execute("Multiply 25 by 4")
        """

        # ==================================================
        # EXPLICIT TOOL EXECUTION
        # ==================================================

        if arguments is not None:

            tool_name = tool_or_input

            tool = registry.get(tool_name)

            if tool is None:
                return {
                    "success": False,
                    "message": f"Tool not found: {tool_name}",
                }

            try:
                result = await tool.execute(
                    **arguments
                )

                if isinstance(result, dict):
                    result.setdefault(
                        "success",
                        True,
                    )
                    return result

                return {
                    "success": True,
                    "result": result,
                }

            except Exception as exc:

                return {
                    "success": False,
                    "tool": tool_name,
                    "message": "Tool execution failed.",
                    "error": str(exc),
                }

        # ==================================================
        # AUTOMATIC TOOL SELECTION
        # ==================================================

        user_input = tool_or_input

        selection = self.selector.select_with_explanation(
            user_input
        )

        selected_name = selection["selected_tool"]

        if selected_name is None:

            result = {
                "success": False,
                "message": "No suitable tool found.",
                "selection": selection,
            }

            logger.log(
                "none",
                user_input,
                result,
            )

            return result

        tool = registry.get(selected_name)

        if tool is None:

            result = {
                "success": False,
                "message": "Selected tool could not be loaded.",
                "selection": selection,
            }

            logger.log(
                "none",
                user_input,
                result,
            )

            return result

        try:

            tool_arguments = tool.prepare_arguments(
                user_input
            )

            result = await tool.execute(
                **tool_arguments
            )

            if isinstance(result, dict):
                result.setdefault(
                    "success",
                    True,
                )
                result["selection"] = selection

            else:
                result = {
                    "success": True,
                    "result": result,
                    "selection": selection,
                }

        except Exception as exc:

            result = {
                "success": False,
                "tool": tool.name,
                "message": "Tool execution failed.",
                "error": str(exc),
                "selection": selection,
            }

        logger.log(
            tool.name,
            user_input,
            result,
        )

        return result