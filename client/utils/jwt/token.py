import jwt
from datetime import datetime, timedelta, timezone
from .config import JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRY_MINUTES


def generate_jwt_token() -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "user": "test_user",
        "exp": now + timedelta(minutes=JWT_EXPIRY_MINUTES),
        "iat": now,
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token
