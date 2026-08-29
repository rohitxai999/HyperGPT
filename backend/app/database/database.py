from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


DATABASE_URL = "sqlite:///hypergpt_memory.db"


engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


Base = declarative_base()


# --------------------------------------------------
# Import models so SQLAlchemy registers all tables
# --------------------------------------------------

# Existing memory model
try:
    from app.memory.models import Memory
except ImportError:
    try:
        from app.models.memory import Memory
    except ImportError:
        Memory = None


# Existing profile model
try:
    from app.profile.models import UserProfile
except ImportError:
    UserProfile = None


# Day 27 Authentication models
try:
    from app.models.user import User
except ImportError:
    User = None


try:
    from app.models.session import UserSession
except ImportError:
    UserSession = None


# Day 28 Conversation models
try:
    from app.models.conversation import Conversation
except ImportError:
    Conversation = None


try:
    from app.models.message import Message
except ImportError:
    Message = None


# --------------------------------------------------
# Create all registered tables
# --------------------------------------------------

Base.metadata.create_all(bind=engine)


# --------------------------------------------------
# Database dependency
# --------------------------------------------------

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()