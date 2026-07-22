from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(
    title="HyperGPT API",
    version="1.0"
)


class ChatRequest(BaseModel):
    message: str



@app.get("/")
def home():

    return {
        "project": "HyperGPT",
        "version": "1.0",
        "message": "Welcome to HyperGPT 🚀"
    }



@app.post("/chat")
def chat(request: ChatRequest):

    user_message = request.message


    response = f"""
You asked:

{user_message}


HyperGPT response:

This is a test AI response.
Your backend connection is working successfully 🚀
"""


    return {
        "response": response
    }