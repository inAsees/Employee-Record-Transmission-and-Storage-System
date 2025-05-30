import pytest
from httpx import AsyncClient
from unittest.mock import patch, AsyncMock
from server.main import app
from datetime import datetime, timedelta, timezone
import jwt
from server.utils.jwt.config import JWT_SECRET, JWT_ALGORITHM


# Helper to generate valid JWT token for tests
def generate_test_jwt(expired=False):
    now = datetime.now(timezone.utc)
    payload = {
        "user": "test_user",
        "iat": now,
        "exp": now - timedelta(minutes=1) if expired else now + timedelta(minutes=5),
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


@pytest.mark.asyncio
async def test_upload_success():
    token = generate_test_jwt()
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "employee_id": 1,
        "name": "John Doe",
        "email": "john.doe@example.com",
        "department": "Engineering",
        "designation": "Developer",
        "salary": 100000,
        "date_of_joining": "2023-01-01",
    }

    with patch(
        "server.routes.employee.add_to_buffer", new_callable=AsyncMock
    ) as mock_add:
        mock_add.return_value = None

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post("/upload", json=payload, headers=headers)

        assert response.status_code == 200
        assert response.json() == {"message": "Record received"}
        mock_add.assert_awaited_once()


@pytest.mark.asyncio
async def test_upload_missing_authorization_header():
    payload = {
        "employee_id": 1,
        "name": "John Doe",
        "email": "john.doe@example.com",
        "department": "Engineering",
        "designation": "Developer",
        "salary": 100000,
        "date_of_joining": "2023-01-01",
    }

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/upload", json=payload)

    assert response.status_code == 401
    assert response.json()["detail"] == "Missing or invalid token"


@pytest.mark.asyncio
async def test_upload_expired_token():
    token = generate_test_jwt(expired=True)
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "employee_id": 1,
        "name": "John Doe",
        "email": "john.doe@example.com",
        "department": "Engineering",
        "designation": "Developer",
        "salary": 100000,
        "date_of_joining": "2023-01-01",
    }

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/upload", json=payload, headers=headers)

    assert response.status_code == 401
    assert response.json()["detail"] == "Token expired"


@pytest.mark.asyncio
async def test_upload_invalid_payload():
    token = generate_test_jwt()
    headers = {"Authorization": f"Bearer {token}"}
    # Missing required fields like name
    payload = {
        "employee_id": 1,
        "email": "john.doe@example.com",
        "department": "Engineering",
        "designation": "Developer",
        "salary": 100000,
        "date_of_joining": "2023-01-01",
    }

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/upload", json=payload, headers=headers)

    assert response.status_code == 400
    assert "Invalid record format" in response.json()["detail"]


@pytest.mark.asyncio
async def test_upload_internal_error(monkeypatch):
    token = generate_test_jwt()
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "employee_id": 1,
        "name": "John Doe",
        "email": "john.doe@example.com",
        "department": "Engineering",
        "designation": "Developer",
        "salary": 100000,
        "date_of_joining": "2023-01-01",
    }

    async def raise_exception(*args, **kwargs):
        raise Exception("DB error")

    monkeypatch.setattr("server.routes.employee.add_to_buffer", raise_exception)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/upload", json=payload, headers=headers)

    # Since your route catches Exception and raises HTTPException with 400:
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid record format"
