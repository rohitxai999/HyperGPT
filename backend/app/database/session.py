from backend.app.database.database import Base, engine

# Import all models so SQLAlchemy registers them
from backend.app.models.memory import Memory


def init_database():
    Base.metadata.create_all(bind=engine)
