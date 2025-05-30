import pytest
from httpx import AsyncClient
from datetime import datetime, timedelta
import jwt
from main import app
from server.utils.jwt.config import JWT_SECRET, JWT_ALGORITHM


def generate_token(expired=False):
    payload = {
        "sub": "test_user",
        "exp": datetime.utcnow() - timedelta(minutes=5)
        if expired
        else datetime.utcnow() + timedelta(minutes=10),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


@pytest.mark.asyncio
async def test_upload_valid_payload():
    token = generate_token()
    payload = {
        "employee_id": 1,
        "name": "John Doe",
        "email": "john.doe@example.com",
        "department": "Engineering",
        "designation": "Engineer",
        "salary": 80000,
        "date_of_joining": "2023-01-01",
    }

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/upload", json=payload, headers={"Authorization": f"Bearer {token}"}
        )
    assert response.status_code == 200
    assert response.json()["message"] == "Record received"


@pytest.mark.asyncio
async def test_upload_with_expired_token():
    token = generate_token(expired=True)
    payload = {
        "employee_id": 1,
        "name": "John Doe",
        "email": "john.doe@example.com",
        "department": "Engineering",
        "designation": "Engineer",
        "salary": 80000,
        "date_of_joining": "2023-01-01",
    }

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/upload", json=payload, headers={"Authorization": f"Bearer {token}"}
        )
    assert response.status_code == 401
    assert response.json()["detail"] == "Token expired"


@pytest.mark.asyncio
async def test_upload_with_invalid_token():
    token = "invalid.token.value"
    payload = {
        "employee_id": 1,
        "name": "John Doe",
        "email": "john.doe@example.com",
        "department": "Engineering",
        "designation": "Engineer",
        "salary": 80000,
        "date_of_joining": "2023-01-01",
    }

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/upload", json=payload, headers={"Authorization": f"Bearer {token}"}
        )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"


@pytest.mark.asyncio
async def test_upload_with_missing_fields():
    token = generate_token()
    payload = {
        # Missing required fields like email, department, etc.
        "employee_id": 2,
        "name": "Jane Doe",
        "salary": 75000,
        "date_of_joining": "2022-06-01",
    }

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/upload", json=payload, headers={"Authorization": f"Bearer {token}"}
        )
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid record format"


@pytest.mark.asyncio
async def test_upload_with_malformed_json():
    token = generate_token()
    # send as text instead of valid JSON
    malformed_payload = "not-a-valid-json"

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/upload",
            content=malformed_payload,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
        )
    assert response.status_code == 400
