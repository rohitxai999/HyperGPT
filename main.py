from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


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
# Chat Route
# -----------------------------
@app.post("/chat")
def chat(request: ChatRequest):

    return {
        "response": f"""
HyperGPT AI Assistant 🤖

Your message:
{request.message}

Backend Status:
Connected successfully 🚀
"""
    }


# -----------------------------
# Test RAG Connection
# -----------------------------
@app.get("/rag-test")
def rag_test():
    return {
        "rag": "ready",
        "status": "RAG module will be connected next 🚀"
    }