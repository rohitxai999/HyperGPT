import json

from sqlalchemy.orm import Session

from app.profile.models import UserProfile


class ProfileRepository:

    @staticmethod
    def get_profile(db: Session, user_id: str):

        profile = (
            db.query(UserProfile)
            .filter(UserProfile.user_id == user_id)
            .first()
        )

        if profile is None:

            profile = UserProfile(user_id=user_id)

            db.add(profile)

            db.commit()

            db.refresh(profile)

        return profile

    @staticmethod
    def update_list(profile, field_name, values):

        current = json.loads(getattr(profile, field_name))

        for value in values:

            if value not in current:
                current.append(value)

        setattr(profile, field_name, json.dumps(current))

    @staticmethod
    def save(db: Session, profile):

        db.add(profile)

        db.commit()

        db.refresh(profile)

        return profile