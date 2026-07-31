from collections import defaultdict
from datetime import datetime, timedelta


class TimelineService:
    """
    Groups memories into human-friendly time periods.
    """

    def __init__(self):
        pass

    @staticmethod
    def group_memories(memories):
        """
        Expects a list of memory objects with a `created_at` attribute.
        Returns a dictionary grouped by time period.
        """

        now = datetime.utcnow()
        timeline = defaultdict(list)

        for memory in memories:
            created = memory.created_at

            if created is None:
                timeline["Unknown"].append(memory)
                continue

            delta = now - created

            if delta < timedelta(days=1):
                timeline["Today"].append(memory)
            elif delta < timedelta(days=2):
                timeline["Yesterday"].append(memory)
            elif delta < timedelta(days=7):
                timeline["This Week"].append(memory)
            elif delta < timedelta(days=30):
                timeline["This Month"].append(memory)
            elif delta < timedelta(days=365):
                timeline["This Year"].append(memory)
            else:
                timeline["Older"].append(memory)

        return dict(timeline)

    @staticmethod
    def timeline_summary(grouped_memories):
        """
        Creates a readable timeline summary.
        """

        lines = []

        for period, memories in grouped_memories.items():
            lines.append(f"{period} ({len(memories)} memories)")

        return "\n".join(lines)