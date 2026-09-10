from datetime import datetime


class TimeTool:

    name = "time"

    def execute(self):

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return {
            "tool": self.name,
            "result": current_time
        }