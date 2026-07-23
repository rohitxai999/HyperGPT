from fastapi import FastAPI

# API Routers
from app.api.routes import router
from app.api.chat_manager import router as chat_manager_router

# Database
from app.models.database import Base, engine

# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="HyperGPT",
    version="1.0.0",
    description="HyperGPT - AI Assistant powered by Groq"
)

# Register API Routers
app.include_router(router)
app.include_router(chat_manager_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to HyperGPT 🚀",
        "status": "Running",
        "version": "1.0.0"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "database": "connected",
        "ai": "Groq",
        "service": "HyperGPT"
    }