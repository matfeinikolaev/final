import pytest


@pytest.mark.asyncio
async def test_create_resume(client, user_token):
    resp = await client.post(
        "/api/v1/resumes/",
        json={"applicant_name": "Alice Smith", "applicant_email": "alice@test.com", "category": "DEV"},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["applicant_name"] == "Alice Smith"
    assert data["status"] == "NEW"


@pytest.mark.asyncio
async def test_create_resume_unauthorized(client):
    resp = await client.post(
        "/api/v1/resumes/",
        json={"applicant_name": "Bob"},
    )
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_get_resumes(client, user_token):
    resp = await client.get("/api/v1/resumes/", headers={"Authorization": f"Bearer {user_token}"})
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


@pytest.mark.asyncio
async def test_get_resume_by_id(client, user_token):
    create = await client.post(
        "/api/v1/resumes/",
        json={"applicant_name": "Bob Jones"},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    res_id = create.json()["id"]
    resp = await client.get(f"/api/v1/resumes/{res_id}", headers={"Authorization": f"Bearer {user_token}"})
    assert resp.status_code == 200
    assert resp.json()["id"] == res_id


@pytest.mark.asyncio
async def test_get_resume_not_found(client, user_token):
    resp = await client.get(
        "/api/v1/resumes/00000000-0000-0000-0000-000000000000",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_update_resume(client, user_token):
    create = await client.post(
        "/api/v1/resumes/",
        json={"applicant_name": "Old Name"},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    res_id = create.json()["id"]
    resp = await client.patch(
        f"/api/v1/resumes/{res_id}",
        json={"applicant_name": "New Name", "status": "REVIEWING"},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert resp.status_code == 200
    assert resp.json()["applicant_name"] == "New Name"
    assert resp.json()["status"] == "REVIEWING"


@pytest.mark.asyncio
async def test_delete_resume(client, user_token):
    create = await client.post(
        "/api/v1/resumes/",
        json={"applicant_name": "To Delete"},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    res_id = create.json()["id"]
    resp = await client.delete(f"/api/v1/resumes/{res_id}", headers={"Authorization": f"Bearer {user_token}"})
    assert resp.status_code == 200
    get_resp = await client.get(f"/api/v1/resumes/{res_id}", headers={"Authorization": f"Bearer {user_token}"})
    assert get_resp.status_code == 404


@pytest.mark.asyncio
async def test_filter_resumes_by_category(client, user_token):
    await client.post(
        "/api/v1/resumes/",
        json={"applicant_name": "Dev Person", "category": "DEV"},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    resp = await client.get("/api/v1/resumes/?category=DEV", headers={"Authorization": f"Bearer {user_token}"})
    assert resp.status_code == 200
    for r in resp.json():
        assert r["category"] == "DEV"


@pytest.mark.asyncio
async def test_filter_resumes_by_status(client, user_token):
    create = await client.post(
        "/api/v1/resumes/",
        json={"applicant_name": "Status Person"},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    res_id = create.json()["id"]
    await client.patch(
        f"/api/v1/resumes/{res_id}",
        json={"status": "ACCEPTED"},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    resp = await client.get("/api/v1/resumes/?status=ACCEPTED", headers={"Authorization": f"Bearer {user_token}"})
    assert resp.status_code == 200
    for r in resp.json():
        assert r["status"] == "ACCEPTED"


@pytest.mark.asyncio
async def test_resume_with_job(client, user_token, superuser_token):
    job_resp = await client.post(
        "/api/v1/jobs/",
        json={"title": "Resume Job"},
        headers={"Authorization": f"Bearer {superuser_token}"},
    )
    job_id = job_resp.json()["id"]
    vac_resp = await client.post(
        "/api/v1/vacancies/",
        json={"title": "Resume Vacancy", "job_id": job_id},
        headers={"Authorization": f"Bearer {superuser_token}"},
    )
    vac_id = vac_resp.json()["id"]
    resp = await client.post(
        "/api/v1/resumes/",
        json={"applicant_name": "Linked Person", "vacancy_id": vac_id},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert resp.status_code == 201
    assert resp.json()["vacancy_id"] == vac_id
