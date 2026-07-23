import requests
import time

API_URL = "http://127.0.0.1:8000/chat"


def chat_with_ai(
    message: str,
    chat_id: str = "default",
    model: str = "llama-3.3-70b-versatile"
):

    try:

        response = requests.post(
            API_URL,
            json={
                "message": message,
                "chat_id": chat_id,
                "model": model
            },
            timeout=60
        )

        response.raise_for_status()

        data = response.json()

        return data["response"]

    except requests.exceptions.ConnectionError:

        return "❌ Cannot connect to FastAPI server. Is Uvicorn running?"

    except Exception as e:

        return f"❌ {e}"


def stream_text(text):

    for word in text.split():

        yield word + " "

        time.sleep(0.04)