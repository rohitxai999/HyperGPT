from fastapi import FastAPI

from app.api.tools import router as tools_router

app = FastAPI(
    title="HyperGPT",
    version="1.0.0"
)

app.include_router(tools_router)


@app.get("/")
def root():
    return {
        "message": "HyperGPT Backend Running"
    }