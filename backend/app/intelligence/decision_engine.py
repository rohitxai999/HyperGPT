from app.profile.profile_service import ProfileService
from app.profile.summary import ProfileSummaryService
from app.timeline.timeline_service import TimelineService


class DecisionEngine:
    """
    Builds personalized context for HyperGPT.

    Future versions will integrate:
    - Long-term memory
    - Vector search
    - Memory ranking
    - Multi-agent reasoning
    """

    def __init__(self, db):
        self.profile_service = ProfileService(db)
        self.summary_service = ProfileSummaryService(db)
        self.timeline_service = TimelineService()

    def build_context(self, user_id: str, memories: list):
        """
        Returns everything the AI should know before answering.
        """

        profile = self.profile_service.profile_as_dict(user_id)

        summary = self.summary_service.generate_summary(user_id)

        grouped = self.timeline_service.group_memories(memories)

        timeline = self.timeline_service.timeline_summary(grouped)

        return {
            "profile": profile,
            "profile_summary": summary,
            "timeline": timeline,
            "recent_memories": memories[:10],
        }