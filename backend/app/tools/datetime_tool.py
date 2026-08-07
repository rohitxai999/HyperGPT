from datetime import datetime

from app.tools.base_tool import BaseTool


class DateTimeTool(BaseTool):
    """
    Returns the current date and time.
    """

    name = "datetime"
    description = "Returns the current date and time."

    async def execute(self, **kwargs):
        return {
            "success": True,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M:%S"),
            "datetime": datetime.now().isoformat()
        }