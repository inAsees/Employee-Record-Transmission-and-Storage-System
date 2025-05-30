from dataclasses import asdict
import aiohttp
from models.models import Employee
from config.config import SERVER_URL, RETRY_ATTEMPTS
from middleware.decorators import log_execution_time, retry_on_failure
from utils.jwt.token import generate_jwt_token

@log_execution_time
@retry_on_failure(retries=RETRY_ATTEMPTS)
async def send_employee_record(session: aiohttp.ClientSession, employee: Employee):
    token = generate_jwt_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    emp_data = asdict(employee)
    emp_data["date_of_joining"] = emp_data[
        "date_of_joining"
    ].isoformat()  # Convert to "YYYY-MM-DD"

    try:
        async with session.post(
            SERVER_URL, json=emp_data, headers=headers
        ) as response:
            if response.status == 200:
                print(f"Sent: {employee.name}")
            else:
                print(f"Failed ({response.status}) for: {employee.name}")
    except Exception as e:
        print(f"Error sending {employee.name}: {e}")
