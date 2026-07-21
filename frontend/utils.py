import requests

API_URL = "http://127.0.0.1:8000/chat"


def chat_with_ai(message: str):
    try:
        response = requests.post(
            API_URL,
            json={"message": message},
            timeout=60
        )

        response.raise_for_status()

        data = response.json()

        return data["response"]

    except requests.exceptions.ConnectionError:
        return "❌ Cannot connect to FastAPI server. Is Uvicorn running?"

    except Exception as e:
        return f"❌ {e}"