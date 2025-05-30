import pytest
from client.services.reader import read_csv_file_in_batches
from client.models.models import Employee


def test_read_csv_file_in_batches(monkeypatch):
    batches = list(read_csv_file_in_batches())
    assert len(batches) > 0
    for batch in batches:
        assert all(isinstance(emp, Employee) for emp in batch)
