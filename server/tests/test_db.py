# test_token/test_db.py

import pytest
from unittest.mock import patch, MagicMock
from mysql.connector import Error, IntegrityError
from server.models.models import Employee
from server.database import db


@pytest.fixture
def sample_employees():
    return [
        Employee(
            employee_id=1,
            name="Alice",
            email="alice@example.com",
            department="Engineering",
            designation="Engineer",
            salary=60000,
            date_of_joining="2023-01-01",
        ),
        Employee(
            employee_id=2,
            name="Bob",
            email="bob@example.com",
            department="Marketing",
            designation="Manager",
            salary=75000,
            date_of_joining="2022-05-10",
        ),
    ]


@patch("server.database.db.mysql.connector.connect")
def test_get_connection_success(mock_connect):
    mock_connect.return_value = MagicMock()
    conn = db.get_connection()
    assert conn is not None
    mock_connect.assert_called_once()


@patch(
    "server.database.db.mysql.connector.connect", side_effect=Error("connection failed")
)
def test_get_connection_failure(mock_connect):
    with pytest.raises(RuntimeError, match="Database connection failed"):
        db.get_connection()


@patch("server.database.db.get_connection")
def test_bulk_insert_employees_success(mock_conn, sample_employees):
    mock_cursor = MagicMock()
    mock_conn.return_value.cursor.return_value = mock_cursor
    db.bulk_insert_employees(sample_employees)
    assert mock_cursor.executemany.called
    assert mock_conn.return_value.commit.called


@patch("server.database.db.get_connection")
def test_bulk_insert_employees_integrity_error(mock_conn, sample_employees):
    mock_cursor = MagicMock()
    mock_cursor.executemany.side_effect = IntegrityError("Duplicate")
    mock_conn.return_value.cursor.return_value = mock_cursor
    with pytest.raises(ValueError, match="Duplicate or invalid data encountered"):
        db.bulk_insert_employees(sample_employees)


@patch("server.database.db.get_connection")
def test_bulk_insert_employees_mysql_error(mock_conn, sample_employees):
    mock_cursor = MagicMock()
    mock_cursor.executemany.side_effect = Error("MySQL error")
    mock_conn.return_value.cursor.return_value = mock_cursor
    with pytest.raises(RuntimeError, match="Database insert failed"):
        db.bulk_insert_employees(sample_employees)
