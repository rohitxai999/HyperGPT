from fastapi import FastAPI

from app.routes.rag import router as rag_router


app = FastAPI(
    title="HyperGPT API",
    version="1.0.0",
    description="HyperGPT AI Assistant"
)


@app.get("/")
def home():
    return {
        "project": "HyperGPT",
        "status": "Running",
        "version": "1.0.0"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# RAG API
app.include_router(
    rag_router,
    prefix="/rag",
    tags=["RAG"]
)