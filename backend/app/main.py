from fastapi import FastAPI

from app.api.tools import router as tools_router
from app.api.chat import router as chat_router
from app.api.auth import router as auth_router
from app.api.conversations import router as conversations_router


app = FastAPI(
    title="HyperGPT",
    version="1.0.0",
)


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