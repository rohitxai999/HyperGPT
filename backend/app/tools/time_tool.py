from datetime import datetime

from backend.app.tools.base_tool import BaseTool


class TimeTool(BaseTool):
    """
    Returns the current local time.
    """

    name = "time"
    description = "Returns the current local time."

    keywords = [
        "time",
        "current time",
        "clock",
        "what time",
        "right now",
    ]

    async def execute(self, **kwargs):
        current_time = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        return {
            "success": True,
            "tool": self.name,
            "result": current_time,
        }