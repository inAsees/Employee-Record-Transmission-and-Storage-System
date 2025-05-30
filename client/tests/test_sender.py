import pytest
from unittest.mock import AsyncMock, patch
from client.models.models import Employee
from client.services.sender import send_employee_record
from datetime import date


@pytest.mark.asyncio
@patch("client.services.sender.generate_jwt_token", return_value="mocktoken")
@patch("aiohttp.ClientSession.post", new_callable=AsyncMock)
async def test_send_employee_record_success(mock_post, mock_token):
    employee = Employee(
        employee_id=1,
        name="John Doe",
        email="john@example.com",
        department="IT",
        designation="Engineer",
        salary=60000.0,
        date_of_joining=date.today(),
    )

    mock_response = AsyncMock()
    mock_response.status = 200
    mock_post.return_value.__aenter__.return_value = mock_response

    async with AsyncMock() as session:
        await send_employee_record(session, employee)

    mock_post.assert_called_once()
