from fastapi import FastAPI
from pydantic import BaseModel

# API Routers
from app.api.routes import router
from app.api.chat_manager import router as chat_manager_router

# Database
from app.models.database import Base, engine

# Multi-Agent Orchestrator
from app.agents.orchestrator import Orchestrator

# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="HyperGPT",
    version="1.0.0",
    description="HyperGPT - AI Assistant powered by Groq"
)

# Initialize Orchestrator
orchestrator = Orchestrator()

# Register API Routers
app.include_router(router)
app.include_router(chat_manager_router)


# -----------------------------
# Chat Request Model
# -----------------------------
class ChatRequest(BaseModel):
    prompt: str


# -----------------------------
# Multi-Agent Chat Endpoint
# -----------------------------
@app.post("/chat")
def chat(request: ChatRequest):
    response = orchestrator.route(request.prompt)

    return {
        "success": True,
        "agent_response": response
    }


# -----------------------------
# Home Endpoint
# -----------------------------
@app.get("/")
def home():
    return {
        "message": "Welcome to HyperGPT 🚀",
        "status": "Running",
        "version": "1.0.0"
    }


# -----------------------------
# Health Check
# -----------------------------
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "database": "connected",
        "ai": "Groq",
        "service": "HyperGPT"
    }