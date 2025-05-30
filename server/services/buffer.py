import asyncio
from typing import List
from models.models import Employee
from database.db import bulk_insert_employees
import logging

BUFFER: List[Employee] = []
BATCH_SIZE = 100
LOCK = asyncio.Lock()


async def add_to_buffer(record: Employee):
    async with LOCK:
        BUFFER.append(record)
        if len(BUFFER) >= BATCH_SIZE:
            await flush_buffer()


async def flush_buffer():
    if not BUFFER:
        return
    try:
        logging.info(f"Flushing {len(BUFFER)} records to the database.")
        # Copy to avoid mutation during DB operation
        records_to_insert = BUFFER.copy()
        bulk_insert_employees(records_to_insert)
        BUFFER.clear()
    except Exception as e:
        logging.error(f"Failed to flush buffer: {e}")
        raise
