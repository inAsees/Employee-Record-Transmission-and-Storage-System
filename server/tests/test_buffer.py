import pytest
from unittest.mock import patch, MagicMock
from server.services.buffer.buffer import (
    add_to_buffer,
    flush_buffer,
    BUFFER,
    BATCH_SIZE,
)
from server.models.models import Employee
from datetime import date


@pytest.fixture(autouse=True)
def clear_buffer():
    BUFFER.clear()
    yield
    BUFFER.clear()


def mock_employee(i=1):
    return Employee(
        employee_id=i,
        name=f"Test User {i}",
        email=f"test{i}@example.com",
        department="Engineering",
        designation="Developer",
        salary=100000,
        date_of_joining=date(2020, 1, 1),
    )


def test_buffer_flush_on_batch_limit():
    with patch(
        "server.services.buffer.buffer.bulk_insert_employees"
    ) as mock_bulk_insert:
        for i in range(BATCH_SIZE):
            asyncio_run(add_to_buffer(mock_employee(i)))
        mock_bulk_insert.assert_called_once()
        assert len(BUFFER) == 0


def test_buffer_flush_failure():
    with patch(
        "server.services.buffer.buffer.bulk_insert_employees",
        side_effect=Exception("DB Error"),
    ):
        for i in range(BATCH_SIZE):
            try:
                asyncio_run(add_to_buffer(mock_employee(i)))
            except Exception:
                pass
        assert len(BUFFER) == BATCH_SIZE


def test_flush_empty_buffer():
    with patch(
        "server.services.buffer.buffer.bulk_insert_employees"
    ) as mock_bulk_insert:
        asyncio_run(flush_buffer())
        mock_bulk_insert.assert_not_called()


def asyncio_run(coro):
    import asyncio

    return asyncio.get_event_loop().run_until_complete(coro)
