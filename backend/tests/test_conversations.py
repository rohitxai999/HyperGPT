import uuid

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def unique_user():
    value = uuid.uuid4().hex[:8]

    return {
        "email": f"conversation_{value}@example.com",
        "username": f"conversation_user_{value}",
        "password": "StrongPassword123!",
    }


def register_and_login():
    user = unique_user()

    register = client.post(
        "/auth/register",
        json=user,
    )

    assert register.status_code == 201

    login = client.post(
        "/auth/login",
        json={
            "email": user["email"],
            "password": user["password"],
        },
    )

    assert login.status_code == 200

    token = login.json()["access_token"]

    return user, {
        "Authorization": f"Bearer {token}"
    }


def test_create_conversation():
    _, headers = register_and_login()

    response = client.post(
        "/conversations",
        headers=headers,
    )

    assert response.status_code == 201

    data = response.json()

    assert "id" in data
    assert data["title"] == "New Conversation"
    assert "created_at" in data
    assert "updated_at" in data


def test_list_conversations():
    _, headers = register_and_login()

    first = client.post(
        "/conversations",
        headers=headers,
    )

    second = client.post(
        "/conversations",
        headers=headers,
    )

    assert first.status_code == 201
    assert second.status_code == 201

    response = client.get(
        "/conversations",
        headers=headers,
    )

    assert response.status_code == 200

    conversations = response.json()

    assert len(conversations) >= 2

    ids = [conversation["id"] for conversation in conversations]

    assert first.json()["id"] in ids
    assert second.json()["id"] in ids


def test_get_conversation():
    _, headers = register_and_login()

    create = client.post(
        "/conversations",
        headers=headers,
    )

    assert create.status_code == 201

    conversation_id = create.json()["id"]

    response = client.get(
        f"/conversations/{conversation_id}",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == conversation_id
    assert data["title"] == "New Conversation"
    assert "messages" in data


def test_conversation_requires_authentication():
    response = client.get("/conversations")

    assert response.status_code == 401


def test_get_missing_conversation():
    _, headers = register_and_login()

    response = client.get(
        "/conversations/999999999",
        headers=headers,
    )

    assert response.status_code == 404


def test_delete_conversation():
    _, headers = register_and_login()

    create = client.post(
        "/conversations",
        headers=headers,
    )

    assert create.status_code == 201

    conversation_id = create.json()["id"]

    delete = client.delete(
        f"/conversations/{conversation_id}",
        headers=headers,
    )

    assert delete.status_code == 200

    assert (
        delete.json()["message"]
        == "Conversation deleted successfully"
    )

    get_deleted = client.get(
        f"/conversations/{conversation_id}",
        headers=headers,
    )

    assert get_deleted.status_code == 404


def test_user_cannot_access_another_users_conversation():
    _, user1_headers = register_and_login()

    create = client.post(
        "/conversations",
        headers=user1_headers,
    )

    assert create.status_code == 201

    conversation_id = create.json()["id"]

    _, user2_headers = register_and_login()

    response = client.get(
        f"/conversations/{conversation_id}",
        headers=user2_headers,
    )

    assert response.status_code == 404


def test_user_cannot_delete_another_users_conversation():
    _, user1_headers = register_and_login()

    create = client.post(
        "/conversations",
        headers=user1_headers,
    )

    assert create.status_code == 201

    conversation_id = create.json()["id"]

    _, user2_headers = register_and_login()

    response = client.delete(
        f"/conversations/{conversation_id}",
        headers=user2_headers,
    )

    assert response.status_code == 404