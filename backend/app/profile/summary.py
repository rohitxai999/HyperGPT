import json

from app.profile.profile_service import ProfileService


class ProfileSummaryService:
    """
    Generates a compact summary of the user's profile.
    """

    def __init__(self, db):
        self.profile_service = ProfileService(db)

    def generate_summary(self, user_id: str) -> str:
        profile = self.profile_service.get_profile(user_id)

        interests = json.loads(profile.interests)
        goals = json.loads(profile.goals)
        skills = json.loads(profile.skills)
        projects = json.loads(profile.projects)
        languages = json.loads(profile.favorite_languages)
        frameworks = json.loads(profile.favorite_frameworks)

        summary = []

        if profile.name:
            summary.append(f"Name: {profile.name}")

        if profile.profession:
            summary.append(f"Profession: {profile.profession}")

        if projects:
            summary.append(
                "Projects: " + ", ".join(projects)
            )

        if skills:
            summary.append(
                "Skills: " + ", ".join(skills)
            )

        if interests:
            summary.append(
                "Interests: " + ", ".join(interests)
            )

        if goals:
            summary.append(
                "Goals: " + ", ".join(goals)
            )

        if languages:
            summary.append(
                "Favorite Languages: " + ", ".join(languages)
            )

        if frameworks:
            summary.append(
                "Favorite Frameworks: " + ", ".join(frameworks)
            )

        final_summary = "\n".join(summary)

        self.profile_service.update_summary(
            user_id,
            final_summary
        )

        return final_summary