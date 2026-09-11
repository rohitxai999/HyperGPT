import uuid
from unittest.mock import AsyncMock

from fastapi.testclient import TestClient

from backend.app.api import chat as chat_api
from backend.app.main import app


client = TestClient(app)


def _register_and_login():
    suffix = uuid.uuid4().hex[:8]
    user = {
        "email": f"chat_{suffix}@example.com",
        "username": f"chat_user_{suffix}",
        "password": "StrongPassword123!",
    }

    assert client.post("/auth/register", json=user).status_code == 201

    login = client.post(
        "/auth/login",
        json={"email": user["email"], "password": user["password"]},
    )
    assert login.status_code == 200

    return {"Authorization": f"Bearer {login.json()['access_token']}"}


def test_chat_awaits_orchestrator_and_persists_messages(monkeypatch):
    expected_result = {
        "query": "Calculate 21 plus 21",
        "final_response": "[Math Agent]\n\n42",
        "status": "success",
    }
    run = AsyncMock(return_value=expected_result)
    monkeypatch.setattr(chat_api.orchestrator, "run", run)

    headers = _register_and_login()
    response = client.post(
        "/chat",
        headers=headers,
        json={"query": "Calculate 21 plus 21"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["final_response"] == "[Math Agent]\n\n42"
    assert data["status"] == "success"
    assert data["conversation_id"]
    run.assert_awaited_once_with("Calculate 21 plus 21")

    conversation = client.get(
        f"/conversations/{data['conversation_id']}",
        headers=headers,
    )
    assert conversation.status_code == 200
    assert [message["content"] for message in conversation.json()["messages"]] == [
        "Calculate 21 plus 21",
        "[Math Agent]\n\n42",
    ]
