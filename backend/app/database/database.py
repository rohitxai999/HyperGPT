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


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize all HyperGPT database models.

    Imports are intentionally performed inside this function
    to avoid circular imports during Base initialization.
    """

    from backend.app.models.memory import Memory
    from backend.app.models.user import User
    from backend.app.models.session import UserSession

    try:
        from backend.app.models.conversation import Conversation
    except ImportError:
        Conversation = None

    try:
        from backend.app.models.message import Message
    except ImportError:
        Message = None

    # Keep references alive so SQLAlchemy registers the models.
    _ = (
        Memory,
        User,
        UserSession,
        Conversation,
        Message,
    )

    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()