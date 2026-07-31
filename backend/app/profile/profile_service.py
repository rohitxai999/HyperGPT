import json
from sqlalchemy.orm import Session

from app.profile.repository import ProfileRepository


class ProfileService:
    """
    Handles creation, retrieval, and updating of a user's
    long-term profile.
    """

    def __init__(self, db: Session):
        self.db = db
        self.repo = ProfileRepository()

    def get_profile(self, user_id: str):
        """
        Return the user's profile.
        Creates one automatically if it doesn't exist.
        """
        return self.repo.get_profile(self.db, user_id)

    def add_interest(self, user_id: str, interest: str):
        profile = self.get_profile(user_id)
        self.repo.update_list(profile, "interests", [interest])
        return self.repo.save(self.db, profile)

    def add_goal(self, user_id: str, goal: str):
        profile = self.get_profile(user_id)
        self.repo.update_list(profile, "goals", [goal])
        return self.repo.save(self.db, profile)

    def add_skill(self, user_id: str, skill: str):
        profile = self.get_profile(user_id)
        self.repo.update_list(profile, "skills", [skill])
        return self.repo.save(self.db, profile)

    def add_project(self, user_id: str, project: str):
        profile = self.get_profile(user_id)
        self.repo.update_list(profile, "projects", [project])
        return self.repo.save(self.db, profile)

    def add_language(self, user_id: str, language: str):
        profile = self.get_profile(user_id)
        self.repo.update_list(profile, "favorite_languages", [language])
        return self.repo.save(self.db, profile)

    def add_framework(self, user_id: str, framework: str):
        profile = self.get_profile(user_id)
        self.repo.update_list(profile, "favorite_frameworks", [framework])
        return self.repo.save(self.db, profile)

    def update_basic_info(
        self,
        user_id: str,
        name: str = None,
        profession: str = None,
    ):
        profile = self.get_profile(user_id)

        if name:
            profile.name = name

        if profession:
            profile.profession = profession

        return self.repo.save(self.db, profile)

    def update_summary(self, user_id: str, summary: str):
        profile = self.get_profile(user_id)
        profile.summary = summary
        return self.repo.save(self.db, profile)

    def profile_as_dict(self, user_id: str):
        profile = self.get_profile(user_id)

        return {
            "user_id": profile.user_id,
            "name": profile.name,
            "profession": profile.profession,
            "interests": json.loads(profile.interests),
            "goals": json.loads(profile.goals),
            "skills": json.loads(profile.skills),
            "favorite_languages": json.loads(profile.favorite_languages),
            "favorite_frameworks": json.loads(profile.favorite_frameworks),
            "projects": json.loads(profile.projects),
            "preferred_response_length": profile.preferred_response_length,
            "preferred_ui_style": profile.preferred_ui_style,
            "personality": profile.personality,
            "summary": profile.summary,
        }