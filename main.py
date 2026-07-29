from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.rag.retriever import retrieve_documents

# Database Imports
from app.models.database import Base, engine

# Import models so SQLAlchemy registers all tables
from app.models.chat import Chat
from app.models.memory import Memory


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="HyperGPT API",
    version="1.0"
)


# -----------------------------
# CORS Configuration
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------
# Request Model
# -----------------------------
class ChatRequest(BaseModel):
    message: str


# -----------------------------
# Home Route
# -----------------------------
@app.get("/")
def home():

    return {
        "project": "HyperGPT",
        "version": "1.0",
        "status": "running",
        "message": "Welcome to HyperGPT 🚀"
    }


# -----------------------------
# Chat Route with RAG
# -----------------------------
@app.post("/chat")
def chat(request: ChatRequest):

    documents = retrieve_documents(
        request.message
    )

    context = "\n".join(documents)

    return {
        "query": request.message,
        "retrieved_context": context,
        "status": "RAG connected successfully 🚀"
    }


# -----------------------------
# RAG Health Check
# -----------------------------
@app.get("/rag-test")
def rag_test():

    return {
        "rag": "ready",
        "status": "Retriever connected 🚀"
    }


# -----------------------------
# Memory Health Check
# -----------------------------
@app.get("/memory-test")
def memory_test():

    return {
        "memory": "ready",
        "status": "Memory Engine connected 🚀"
    }