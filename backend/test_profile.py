from app.database.database import SessionLocal
from app.profile.profile_service import ProfileService

db = SessionLocal()

service = ProfileService(db)

service.update_basic_info(
    user_id="default",
    name="Rohit",
    profession="AI Engineer"
)

service.add_project("default", "HyperGPT")
service.add_project("default", "JARVIS AI")
service.add_interest("default", "Artificial Intelligence")

print(service.profile_as_dict("default"))

db.close()