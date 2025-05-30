import asyncio
import aiohttp
from services.reader import read_csv_file_in_batches
from services.sender import send_employee_record
import logging

logging.basicConfig(level=logging.INFO)

async def main():
    async with aiohttp.ClientSession() as session:
        batch_number = 1
        for batch in read_csv_file_in_batches():
            logging.info(f"Sending batch {batch_number} with {len(batch)} records...")
            tasks = [send_employee_record(session, emp) for emp in batch]
            await asyncio.gather(*tasks)
            batch_number += 1


if __name__ == "__main__":
    asyncio.run(main())
