import pytest


@pytest.mark.asyncio
async def test_create_vacancy(client, superuser_token):
    resp = await client.post(
        "/api/v1/vacancies/",
        json={"title": "Python Developer", "description": "We need a dev", "category": "DEV"},
        headers={"Authorization": f"Bearer {superuser_token}"},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "Python Developer"
    assert data["status"] == "OPEN"


@pytest.mark.asyncio
async def test_create_vacancy_forbidden(client, user_token):
    resp = await client.post(
        "/api/v1/vacancies/",
        json={"title": "Some Vacancy"},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_get_vacancies(client):
    resp = await client.get("/api/v1/vacancies/")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


@pytest.mark.asyncio
async def test_get_vacancy_by_id(client, superuser_token):
    create = await client.post(
        "/api/v1/vacancies/",
        json={"title": "QA Engineer"},
        headers={"Authorization": f"Bearer {superuser_token}"},
    )
    vac_id = create.json()["id"]
    resp = await client.get(f"/api/v1/vacancies/{vac_id}")
    assert resp.status_code == 200
    assert resp.json()["id"] == vac_id


@pytest.mark.asyncio
async def test_get_vacancy_not_found(client):
    resp = await client.get("/api/v1/vacancies/00000000-0000-0000-0000-000000000000")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_update_vacancy(client, superuser_token):
    create = await client.post(
        "/api/v1/vacancies/",
        json={"title": "Old Vacancy"},
        headers={"Authorization": f"Bearer {superuser_token}"},
    )
    vac_id = create.json()["id"]
    resp = await client.patch(
        f"/api/v1/vacancies/{vac_id}",
        json={"title": "Updated Vacancy", "description": "Updated desc"},
        headers={"Authorization": f"Bearer {superuser_token}"},
    )
    assert resp.status_code == 200
    assert resp.json()["title"] == "Updated Vacancy"


@pytest.mark.asyncio
async def test_close_vacancy(client, superuser_token):
    create = await client.post(
        "/api/v1/vacancies/",
        json={"title": "Vacancy To Close"},
        headers={"Authorization": f"Bearer {superuser_token}"},
    )
    vac_id = create.json()["id"]
    resp = await client.post(
        f"/api/v1/vacancies/{vac_id}/close",
        headers={"Authorization": f"Bearer {superuser_token}"},
    )
    assert resp.status_code == 200
    assert resp.json()["status"] == "CLOSED"


@pytest.mark.asyncio
async def test_delete_vacancy(client, superuser_token):
    create = await client.post(
        "/api/v1/vacancies/",
        json={"title": "Vacancy To Delete"},
        headers={"Authorization": f"Bearer {superuser_token}"},
    )
    vac_id = create.json()["id"]
    resp = await client.delete(f"/api/v1/vacancies/{vac_id}", headers={"Authorization": f"Bearer {superuser_token}"})
    assert resp.status_code == 200
    get_resp = await client.get(f"/api/v1/vacancies/{vac_id}")
    assert get_resp.status_code == 404


@pytest.mark.asyncio
async def test_filter_vacancies_by_status(client, superuser_token):
    await client.post(
        "/api/v1/vacancies/",
        json={"title": "Open Vac", "status": "OPEN"},
        headers={"Authorization": f"Bearer {superuser_token}"},
    )
    resp = await client.get("/api/v1/vacancies/?status=OPEN")
    assert resp.status_code == 200
    for v in resp.json():
        assert v["status"] == "OPEN"


@pytest.mark.asyncio
async def test_filter_vacancies_by_category(client, superuser_token):
    await client.post(
        "/api/v1/vacancies/",
        json={"title": "Dev Vac", "category": "DEV"},
        headers={"Authorization": f"Bearer {superuser_token}"},
    )
    resp = await client.get("/api/v1/vacancies/?category=DEV")
    assert resp.status_code == 200
    for v in resp.json():
        assert v["category"] == "DEV"


@pytest.mark.asyncio
async def test_vacancy_stats(client, superuser_token, user_token):
    vac_resp = await client.post(
        "/api/v1/vacancies/",
        json={"title": "Stats Vacancy"},
        headers={"Authorization": f"Bearer {superuser_token}"},
    )
    vac_id = vac_resp.json()["id"]
    await client.post(
        "/api/v1/resumes/",
        json={"applicant_name": "John Doe", "vacancy_id": vac_id, "status": "NEW"},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    resp = await client.get(
        f"/api/v1/vacancies/{vac_id}/stats",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["total_resumes"] >= 1
    assert "by_status" in data
