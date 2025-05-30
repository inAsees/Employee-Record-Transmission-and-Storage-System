from datetime import datetime
from http.client import HTTPException
import logging
from fastapi import Request, APIRouter
from services.buffer import add_to_buffer
from middleware.decorators import log_execution, validate_jwt, log_errors
from models.models import Employee


router = APIRouter()

@router.post("/upload", status_code=200)
@validate_jwt
@log_execution
@log_errors
async def upload_employee(request: Request):
    try:
        record = await request.json()
        record["date_of_joining"] = datetime.strptime(
            record["date_of_joining"], "%Y-%m-%d"
        ).date()
        employee = Employee(**record)
        await add_to_buffer(employee)
        return {"message": "Record received"}
    except Exception as e:
        logging.error(f"Invalid record: {e}")
        raise HTTPException(status_code=400, detail="Invalid record format")
