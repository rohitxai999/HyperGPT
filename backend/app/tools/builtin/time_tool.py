from datetime import datetime


class TimeTool:
    """
    Returns the current system date and time.
    """

    def run(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")