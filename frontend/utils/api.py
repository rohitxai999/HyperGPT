import time
import requests


API_BASE_URL = "http://127.0.0.1:8000"


# ============================================================
# AUTHENTICATION
# ============================================================

def register_user(
    email: str,
    username: str,
    password: str,
):
    """
    Register a new HyperGPT user.
    """

    try:
        response = requests.post(
            f"{API_BASE_URL}/auth/register",
            json={
                "email": email,
                "username": username,
                "password": password,
            },
            timeout=30,
        )

        if response.status_code == 201:
            return {
                "success": True,
                "data": response.json(),
            }

        try:
            detail = response.json().get(
                "detail",
                "Registration failed",
            )
        except Exception:
            detail = "Registration failed"

        return {
            "success": False,
            "error": detail,
        }

    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "error": "Cannot connect to FastAPI server. Is Uvicorn running?",
        }

    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "Request timed out. Please try again.",
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


def login_user(
    email: str,
    password: str,
):
    """
    Login to HyperGPT and receive JWT access token.
    """

    try:
        response = requests.post(
            f"{API_BASE_URL}/auth/login",
            json={
                "email": email,
                "password": password,
            },
            timeout=30,
        )

        if response.status_code == 200:
            data = response.json()

            return {
                "success": True,
                "access_token": data["access_token"],
                "token_type": data.get(
                    "token_type",
                    "bearer",
                ),
            }

        try:
            detail = response.json().get(
                "detail",
                "Login failed",
            )
        except Exception:
            detail = "Login failed"

        return {
            "success": False,
            "error": detail,
        }

    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "error": "Cannot connect to FastAPI server. Is Uvicorn running?",
        }

    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "Request timed out. Please try again.",
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


def get_current_user(
    token: str,
):
    """
    Get the currently authenticated HyperGPT user.
    """

    try:
        response = requests.get(
            f"{API_BASE_URL}/auth/me",
            headers={
                "Authorization": f"Bearer {token}",
            },
            timeout=30,
        )

        if response.status_code == 200:
            return {
                "success": True,
                "data": response.json(),
            }

        try:
            detail = response.json().get(
                "detail",
                "Authentication failed",
            )
        except Exception:
            detail = "Authentication failed"

        return {
            "success": False,
            "error": detail,
        }

    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "error": "Cannot connect to FastAPI server. Is Uvicorn running?",
        }

    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "Request timed out. Please try again.",
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


def logout_user(
    token: str,
):
    """
    Logout and revoke the current session.
    """

    try:
        response = requests.post(
            f"{API_BASE_URL}/auth/logout",
            headers={
                "Authorization": f"Bearer {token}",
            },
            timeout=30,
        )

        if response.status_code == 200:
            return {
                "success": True,
                "data": response.json(),
            }

        try:
            detail = response.json().get(
                "detail",
                "Logout failed",
            )
        except Exception:
            detail = "Logout failed"

        return {
            "success": False,
            "error": detail,
        }

    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "error": "Cannot connect to FastAPI server. Is Uvicorn running?",
        }

    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "Request timed out. Please try again.",
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


# ============================================================
# CHAT
# ============================================================

def chat_with_ai(
    message: str,
    chat_id: str = "default",
    model: str = "llama-3.3-70b-versatile",
    token: str | None = None,
):
    """
    Send a chat request to the HyperGPT backend.
    """

    try:

        headers = {}

        if token:
            headers["Authorization"] = (
                f"Bearer {token}"
            )

        response = requests.post(
            f"{API_BASE_URL}/chat",
            json={
                "message": message,
                "chat_id": chat_id,
                "model": model,
            },
            headers=headers,
            timeout=60,
        )

        response.raise_for_status()

        data = response.json()

        return data["response"]

    except requests.exceptions.ConnectionError:

        return (
            "Cannot connect to FastAPI server. "
            "Is Uvicorn running?"
        )

    except requests.exceptions.Timeout:

        return (
            "Request timed out. "
            "Please try again."
        )

    except Exception as e:

        return f"Error: {e}"


# ============================================================
# STREAMING EFFECT
# ============================================================

def stream_text(text):
    """
    Simulate streaming text in the Streamlit UI.
    """

    for word in text.split():

        yield word + " "

        time.sleep(0.04)