from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.rag.retriever import retrieve_documents


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