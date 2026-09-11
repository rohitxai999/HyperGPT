from fastapi import FastAPI

from backend.app.api.tools import router as tools_router
from backend.app.api.chat import router as chat_router
from backend.app.api.auth import router as auth_router
from backend.app.api.conversations import router as conversations_router
from backend.app.database.database import init_db


app = FastAPI(
    title="HyperGPT",
    version="1.0.0",
)


# Ensure the persistence used by authenticated chat is ready before
# requests are served, including deployments started via this module.
init_db()


# --------------------------------------------------
# API Routers
# --------------------------------------------------

app.include_router(tools_router)
app.include_router(chat_router)
app.include_router(auth_router)
app.include_router(conversations_router)


# --------------------------------------------------
# Root Endpoint
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "HyperGPT Backend Running",
    }
