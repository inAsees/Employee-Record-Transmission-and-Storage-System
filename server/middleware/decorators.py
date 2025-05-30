from datetime import datetime
import logging
import time
from functools import wraps
from typing import Callable, Awaitable
import jwt
from fastapi import Request, HTTPException
from pydantic import ValidationError
from models.models import EmployeeIn
from utils.jwt.config import JWT_SECRET, JWT_ALGORITHM


def log_execution(func: Callable[..., Awaitable]):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.time()
        result = await func(*args, **kwargs)
        duration = time.time() - start
        logging.info(f"{func.__name__} executed in {duration:.3f}s")
        return result

    return wrapper

def validate_jwt(func):
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        logging.info("Validating JWT token...")

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            logging.warning("Missing or malformed Authorization header.")
            raise HTTPException(status_code=401, detail="Missing or invalid token")

        token = auth_header.split(" ")[1]
        try:
            jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            logging.info("JWT token validated successfully.")
        except jwt.ExpiredSignatureError:
            logging.warning("JWT token expired.")
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            logging.warning("Invalid JWT token.")
            raise HTTPException(status_code=401, detail="Invalid token")

        return await func(request, *args, **kwargs)

    return wrapper


def log_errors(func: Callable[..., Awaitable]):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logging.exception(f"Exception in {func.__name__}: {e}")
            raise

    return wrapper
