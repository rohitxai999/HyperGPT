from fastapi import FastAPI

from app.api.tools import router as tools_router
from app.api.chat import router as chat_router


app = FastAPI(
    title="HyperGPT",
    version="1.0.0"
)


app.include_router(tools_router)
app.include_router(chat_router)


@app.get("/")
def root():
    return {
        "message": "HyperGPT Backend Running"
    }