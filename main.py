from fastapi import FastAPI

# Create the FastAPI application
app = FastAPI()

# Home route
@app.get("/")
def home():
    return {
        "project": "HyperGPT",
        "version": "1.0",
        "message": "Welcome to HyperGPT 🚀"
    }