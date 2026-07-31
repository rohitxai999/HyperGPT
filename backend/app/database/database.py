from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///hypergpt_memory.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

# Import models so SQLAlchemy knows about them
# Add new models here as HyperGPT grows
try:
    from app.memory.models import Memory  # Existing memory model
except ImportError:
    pass

try:
    from app.profile.models import UserProfile  # Day 13 profile model
except ImportError:
    pass

# Create all registered tables
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()