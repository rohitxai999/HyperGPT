import uuid

from fastapi.testclient import TestClient

from app.api.chat import orchestrator
from app.database.database import SessionLocal
from app.main import app
from app.models.conversation import Conversation
from app.models.message import Message
from app.models.user import User


client = TestClient(app)


def unique_credentials():
    suffix = uuid.uuid4().hex[:12]

    return {
        "email": f"day29_{suffix}@example.com",
        "username": f"day29_{suffix}",
        "password": "Day29StrongPassword123!",
    }


def register_and_login():
    credentials = unique_credentials()

    register_response = client.post(
        "/auth/register",
        json=credentials,
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        json={
            "email": credentials["email"],
            "password": credentials["password"],
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    return credentials, {
        "Authorization": f"Bearer {token}",
    }


def cleanup_user(email: str):
    db = SessionLocal()

    try:
        user = (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

        if user:
            conversations = (
                db.query(Conversation)
                .filter(
                    Conversation.user_id == user.id
                )
                .all()
            )

            for conversation in conversations:
                db.query(Message).filter(
                    Message.conversation_id
                    == conversation.id
                ).delete()

            db.query(Conversation).filter(
                Conversation.user_id == user.id
            ).delete()

            db.delete(user)
            db.commit()

    finally:
        db.close()


def test_chat_requires_authentication():
    response = client.post(
        "/chat",
        json={
            "query": "Hello HyperGPT",
        },
    )

    assert response.status_code == 401


def test_chat_creates_persistent_conversation(monkeypatch):
    credentials, headers = register_and_login()

    def fake_run(query):
        return {
            "query": query,
            "responses": [],
            "final_response": "Mocked HyperGPT response.",
        }

    monkeypatch.setattr(
        orchestrator,
        "run",
        fake_run,
    )

    try:
        response = client.post(
            "/chat",
            json={
                "query": "Explain artificial intelligence.",
            },
            headers=headers,
        )

        assert response.status_code == 200

        data = response.json()

        assert data["conversation_id"] is not None
        assert data["user_message_id"] is not None
        assert data["assistant_message_id"] is not None
        assert (
            data["final_response"]
            == "Mocked HyperGPT response."
        )

        conversation_id = data["conversation_id"]

        conversation_response = client.get(
            f"/conversations/{conversation_id}",
            headers=headers,
        )

        assert conversation_response.status_code == 200

        conversation = conversation_response.json()

        assert conversation["id"] == conversation_id
        assert len(conversation["messages"]) == 2

        assert conversation["messages"][0]["role"] == "user"
        assert (
            conversation["messages"][0]["content"]
            == "Explain artificial intelligence."
        )

        assert conversation["messages"][1]["role"] == "assistant"
        assert (
            conversation["messages"][1]["content"]
            == "Mocked HyperGPT response."
        )

    finally:
        cleanup_user(credentials["email"])


def test_chat_reuses_existing_conversation(monkeypatch):
    credentials, headers = register_and_login()

    call_count = {"value": 0}

    def fake_run(query):
        call_count["value"] += 1

        return {
            "query": query,
            "responses": [],
            "final_response": f"Response {call_count['value']}",
        }

    monkeypatch.setattr(
        orchestrator,
        "run",
        fake_run,
    )

    try:
        first_response = client.post(
            "/chat",
            json={
                "query": "First question",
            },
            headers=headers,
        )

        assert first_response.status_code == 200

        conversation_id = first_response.json()[
            "conversation_id"
        ]

        second_response = client.post(
            "/chat",
            json={
                "query": "Second question",
                "conversation_id": conversation_id,
            },
            headers=headers,
        )

        assert second_response.status_code == 200

        assert (
            second_response.json()["conversation_id"]
            == conversation_id
        )

        conversation_response = client.get(
            f"/conversations/{conversation_id}",
            headers=headers,
        )

        assert conversation_response.status_code == 200

        messages = conversation_response.json()["messages"]

        assert len(messages) == 4

        assert messages[0]["content"] == "First question"
        assert messages[1]["content"] == "Response 1"
        assert messages[2]["content"] == "Second question"
        assert messages[3]["content"] == "Response 2"

    finally:
        cleanup_user(credentials["email"])


def test_user_cannot_access_another_users_conversation(
    monkeypatch,
):
    user1_credentials, user1_headers = register_and_login()
    user2_credentials, user2_headers = register_and_login()

    def fake_run(query):
        return {
            "query": query,
            "responses": [],
            "final_response": "Private response.",
        }

    monkeypatch.setattr(
        orchestrator,
        "run",
        fake_run,
    )

    try:
        response = client.post(
            "/chat",
            json={
                "query": "Private user 1 question",
            },
            headers=user1_headers,
        )

        assert response.status_code == 200

        conversation_id = response.json()[
            "conversation_id"
        ]

        forbidden_response = client.get(
            f"/conversations/{conversation_id}",
            headers=user2_headers,
        )

        assert forbidden_response.status_code == 404

        forbidden_chat = client.post(
            "/chat",
            json={
                "query": "Attempt to use another user's conversation",
                "conversation_id": conversation_id,
            },
            headers=user2_headers,
        )

        assert forbidden_chat.status_code == 404

    finally:
        cleanup_user(user1_credentials["email"])
        cleanup_user(user2_credentials["email"])
