import pytest


# --- Categories ---

@pytest.mark.asyncio
async def test_create_category(client, superuser_token):
    resp = await client.post(
        "/api/v1/categories/",
        json={"name": "Development"},
        headers={"Authorization": f"Bearer {superuser_token}"},
    )
    assert resp.status_code == 201
    assert resp.json()["name"] == "Development"


@pytest.mark.asyncio
async def test_create_category_forbidden(client, user_token):
    resp = await client.post(
        "/api/v1/categories/",
        json={"name": "Sales"},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_get_categories(client):
    resp = await client.get("/api/v1/categories/")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


@pytest.mark.asyncio
async def test_get_category_by_id(client, superuser_token):
    create = await client.post(
        "/api/v1/categories/",
        json={"name": "Management"},
        headers={"Authorization": f"Bearer {superuser_token}"},
    )
    cat_id = create.json()["id"]
    resp = await client.get(f"/api/v1/categories/{cat_id}")
    assert resp.status_code == 200
    assert resp.json()["id"] == cat_id


@pytest.mark.asyncio
async def test_get_category_not_found(client):
    resp = await client.get("/api/v1/categories/00000000-0000-0000-0000-000000000000")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_update_category(client, superuser_token):
    create = await client.post(
        "/api/v1/categories/",
        json={"name": "OldName"},
        headers={"Authorization": f"Bearer {superuser_token}"},
    )
    cat_id = create.json()["id"]
    resp = await client.patch(
        f"/api/v1/categories/{cat_id}",
        json={"name": "NewName"},
        headers={"Authorization": f"Bearer {superuser_token}"},
    )
    assert resp.status_code == 200
    assert resp.json()["name"] == "NewName"


@pytest.mark.asyncio
async def test_delete_category(client, superuser_token):
    create = await client.post(
        "/api/v1/categories/",
        json={"name": "ToDelete"},
        headers={"Authorization": f"Bearer {superuser_token}"},
    )
    cat_id = create.json()["id"]
    resp = await client.delete(f"/api/v1/categories/{cat_id}", headers={"Authorization": f"Bearer {superuser_token}"})
    assert resp.status_code == 200
    get_resp = await client.get(f"/api/v1/categories/{cat_id}")
    assert get_resp.status_code == 404


# --- Jobs ---

@pytest.mark.asyncio
async def test_create_job(client, superuser_token):
    resp = await client.post(
        "/api/v1/jobs/",
        json={"title": "Backend Developer"},
        headers={"Authorization": f"Bearer {superuser_token}"},
    )
    assert resp.status_code == 201
    assert resp.json()["title"] == "Backend Developer"


@pytest.mark.asyncio
async def test_create_job_forbidden(client, user_token):
    resp = await client.post(
        "/api/v1/jobs/",
        json={"title": "Some Job"},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_get_jobs(client):
    resp = await client.get("/api/v1/jobs/")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


@pytest.mark.asyncio
async def test_get_job_by_id(client, superuser_token):
    create = await client.post(
        "/api/v1/jobs/",
        json={"title": "Frontend Developer"},
        headers={"Authorization": f"Bearer {superuser_token}"},
    )
    job_id = create.json()["id"]
    resp = await client.get(f"/api/v1/jobs/{job_id}")
    assert resp.status_code == 200
    assert resp.json()["id"] == job_id


@pytest.mark.asyncio
async def test_get_job_not_found(client):
    resp = await client.get("/api/v1/jobs/00000000-0000-0000-0000-000000000000")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_update_job(client, superuser_token):
    create = await client.post(
        "/api/v1/jobs/",
        json={"title": "Old Title"},
        headers={"Authorization": f"Bearer {superuser_token}"},
    )
    job_id = create.json()["id"]
    resp = await client.patch(
        f"/api/v1/jobs/{job_id}",
        json={"title": "New Title"},
        headers={"Authorization": f"Bearer {superuser_token}"},
    )
    assert resp.status_code == 200
    assert resp.json()["title"] == "New Title"


@pytest.mark.asyncio
async def test_delete_job(client, superuser_token):
    create = await client.post(
        "/api/v1/jobs/",
        json={"title": "Job To Delete"},
        headers={"Authorization": f"Bearer {superuser_token}"},
    )
    job_id = create.json()["id"]
    resp = await client.delete(f"/api/v1/jobs/{job_id}", headers={"Authorization": f"Bearer {superuser_token}"})
    assert resp.status_code == 200
    get_resp = await client.get(f"/api/v1/jobs/{job_id}")
    assert get_resp.status_code == 404


@pytest.mark.asyncio
async def test_job_with_category(client, superuser_token):
    cat = await client.post(
        "/api/v1/categories/",
        json={"name": "Tech"},
        headers={"Authorization": f"Bearer {superuser_token}"},
    )
    cat_id = cat.json()["id"]
    resp = await client.post(
        "/api/v1/jobs/",
        json={"title": "DevOps", "category_id": cat_id},
        headers={"Authorization": f"Bearer {superuser_token}"},
    )
    assert resp.status_code == 201
    assert resp.json()["category_id"] == cat_id
