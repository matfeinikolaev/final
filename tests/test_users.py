import pytest


@pytest.mark.asyncio
async def test_get_users_as_superuser(client, superuser_token):
    resp = await client.get("/api/v1/users/", headers={"Authorization": f"Bearer {superuser_token}"})
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


@pytest.mark.asyncio
async def test_get_users_forbidden_for_regular(client, user_token):
    resp = await client.get("/api/v1/users/", headers={"Authorization": f"Bearer {user_token}"})
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_create_user_as_superuser(client, superuser_token):
    resp = await client.post(
        "/api/v1/users/",
        json={"email": "created@test.com", "password": "pass123", "first_name": "Created"},
        headers={"Authorization": f"Bearer {superuser_token}"},
    )
    assert resp.status_code == 201
    assert resp.json()["email"] == "created@test.com"


@pytest.mark.asyncio
async def test_create_user_duplicate_email(client, superuser_token):
    payload = {"email": "dupuser@test.com", "password": "pass123"}
    await client.post("/api/v1/users/", json=payload, headers={"Authorization": f"Bearer {superuser_token}"})
    resp = await client.post("/api/v1/users/", json=payload, headers={"Authorization": f"Bearer {superuser_token}"})
    assert resp.status_code == 400


@pytest.mark.asyncio
async def test_update_me(client, user_token):
    resp = await client.patch(
        "/api/v1/users/me",
        json={"first_name": "Updated"},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert resp.status_code == 200
    assert resp.json()["first_name"] == "Updated"


@pytest.mark.asyncio
async def test_update_me_unauthorized(client):
    resp = await client.patch("/api/v1/users/me", json={"first_name": "X"})
    assert resp.status_code == 401
