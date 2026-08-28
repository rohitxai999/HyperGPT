import uuid

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def unique_user():
    value = uuid.uuid4().hex[:8]

    return {
        "email": f"test_{value}@example.com",
        "username": f"user_{value}",
        "password": "StrongPassword123!",
    }


def test_register_user():
    user = unique_user()

    response = client.post(
        "/auth/register",
        json=user,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["email"] == user["email"]
    assert data["username"] == user["username"]
    assert "hashed_password" not in data


def test_duplicate_email_rejected():
    user = unique_user()

    first = client.post(
        "/auth/register",
        json=user,
    )

    assert first.status_code == 201

    duplicate = client.post(
        "/auth/register",
        json={
            **user,
            "username": user["username"] + "_2",
        },
    )

    assert duplicate.status_code == 409


def test_login_and_me():
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

    me = client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert me.status_code == 200
    assert me.json()["email"] == user["email"]


def test_invalid_login_rejected():
    user = unique_user()

    client.post(
        "/auth/register",
        json=user,
    )

    response = client.post(
        "/auth/login",
        json={
            "email": user["email"],
            "password": "WrongPassword123!",
        },
    )

    assert response.status_code == 401


def test_protected_endpoint_requires_auth():
    response = client.get("/auth/me")

    assert response.status_code == 401


def test_logout_revokes_session():
    user = unique_user()

    client.post(
        "/auth/register",
        json=user,
    )

    login = client.post(
        "/auth/login",
        json={
            "email": user["email"],
            "password": user["password"],
        },
    )

    assert login.status_code == 200

    token = login.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    before_logout = client.get(
        "/auth/me",
        headers=headers,
    )

    assert before_logout.status_code == 200

    logout = client.post(
        "/auth/logout",
        headers=headers,
    )

    assert logout.status_code == 200

    after_logout = client.get(
        "/auth/me",
        headers=headers,
    )

    assert after_logout.status_code == 401