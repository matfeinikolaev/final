import pytest


@pytest.mark.asyncio
async def test_register_success(client):
    resp = await client.post("/api/v1/auth/register", json={
        "email": "newuser@test.com",
        "password": "password123",
        "first_name": "New",
        "last_name": "User",
    })
    assert resp.status_code == 201
    data = resp.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_register_duplicate_email(client):
    payload = {"email": "dup@test.com", "password": "pass123"}
    await client.post("/api/v1/auth/register", json=payload)
    resp = await client.post("/api/v1/auth/register", json=payload)
    assert resp.status_code == 400
    assert "already registered" in resp.json()["detail"]


@pytest.mark.asyncio
async def test_login_success(client):
    await client.post("/api/v1/auth/register", json={"email": "login@test.com", "password": "pass123"})
    resp = await client.post("/api/v1/auth/login", data={"username": "login@test.com", "password": "pass123"})
    assert resp.status_code == 200
    assert "access_token" in resp.json()


@pytest.mark.asyncio
async def test_login_wrong_password(client):
    await client.post("/api/v1/auth/register", json={"email": "wrongpass@test.com", "password": "correct"})
    resp = await client.post("/api/v1/auth/login", data={"username": "wrongpass@test.com", "password": "wrong"})
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_login_nonexistent_user(client):
    resp = await client.post("/api/v1/auth/login", data={"username": "ghost@test.com", "password": "pass"})
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_get_me(client, user_token):
    resp = await client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {user_token}"})
    assert resp.status_code == 200
    assert resp.json()["email"] == "user@test.com"


@pytest.mark.asyncio
async def test_get_me_unauthorized(client):
    resp = await client.get("/api/v1/auth/me")
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_refresh_token(client):
    reg = await client.post("/api/v1/auth/register", json={"email": "refresh@test.com", "password": "pass123"})
    refresh_token = reg.json()["refresh_token"]
    resp = await client.post(f"/api/v1/auth/refresh?refresh_token={refresh_token}")
    assert resp.status_code == 200
    assert "access_token" in resp.json()


@pytest.mark.asyncio
async def test_refresh_invalid_token(client):
    resp = await client.post("/api/v1/auth/refresh?refresh_token=invalid.token.here")
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_change_password(client):
    await client.post("/api/v1/auth/register", json={"email": "chpass@test.com", "password": "oldpass"})
    login = await client.post("/api/v1/auth/login", data={"username": "chpass@test.com", "password": "oldpass"})
    token = login.json()["access_token"]
    resp = await client.post(
        "/api/v1/auth/change-password",
        json={"old_password": "oldpass", "new_password": "newpass"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    login2 = await client.post("/api/v1/auth/login", data={"username": "chpass@test.com", "password": "newpass"})
    assert login2.status_code == 200


@pytest.mark.asyncio
async def test_change_password_wrong_old(client):
    await client.post("/api/v1/auth/register", json={"email": "chpass2@test.com", "password": "correct"})
    login = await client.post("/api/v1/auth/login", data={"username": "chpass2@test.com", "password": "correct"})
    token = login.json()["access_token"]
    resp = await client.post(
        "/api/v1/auth/change-password",
        json={"old_password": "wrong", "new_password": "newpass"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 400
