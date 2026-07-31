from sqlalchemy.orm import Session

from app.profile.profile_service import ProfileService


class ProfileUpdater:
    """
    Updates the user's profile based on extracted information
    from conversations.
    """

    def __init__(self, db: Session):
        self.profile_service = ProfileService(db)

    def update_from_extracted_data(self, user_id: str, data: dict):
        """
        Expected data format:

        {
            "name": "...",
            "profession": "...",
            "projects": [...],
            "skills": [...],
            "interests": [...],
            "goals": [...],
            "favorite_languages": [...],
            "favorite_frameworks": [...]
        }
        """

        if not data:
            return

        self.profile_service.update_basic_info(
            user_id=user_id,
            name=data.get("name"),
            profession=data.get("profession"),
        )

        for project in data.get("projects", []):
            self.profile_service.add_project(user_id, project)

        for skill in data.get("skills", []):
            self.profile_service.add_skill(user_id, skill)

        for interest in data.get("interests", []):
            self.profile_service.add_interest(user_id, interest)

        for goal in data.get("goals", []):
            self.profile_service.add_goal(user_id, goal)

        for language in data.get("favorite_languages", []):
            self.profile_service.add_language(user_id, language)

        for framework in data.get("favorite_frameworks", []):
            self.profile_service.add_framework(user_id, framework)

    def update_summary(self, user_id: str, summary: str):
        self.profile_service.update_summary(user_id, summary)