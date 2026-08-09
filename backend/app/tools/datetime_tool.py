from datetime import datetime

from app.tools.base_tool import BaseTool


class DateTimeTool(BaseTool):
    """
    Returns the current date and time.
    """

    name = "datetime"
    description = "Returns the current date and time."

    keywords = [
        "time",
        "date",
        "day",
        "today",
        "todays",
        "clock",
        "current time",
        "current date",
        "what time",
        "what date",
    ]

    async def execute(self, **kwargs):
        now = datetime.now()

        return {
            "success": True,
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M:%S"),
            "datetime": now.isoformat()
        }
