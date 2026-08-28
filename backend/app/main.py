from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.chat import router as chat_router
from app.api.tools import router as tools_router
from app.database.database import Base, engine
from app.models.memory import Memory
from app.models.session import UserSession
from app.models.user import User


# Make sure all registered models have their tables.
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="HyperGPT",
    version="1.0.0",
)


# Existing HyperGPT routes
app.include_router(tools_router)
app.include_router(chat_router)

# Day 27 authentication routes
app.include_router(auth_router)


@app.get("/")
def root():
    return {
        "message": "HyperGPT Backend Running"
    }