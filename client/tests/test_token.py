from client.utils.jwt.token import generate_jwt_token
import jwt
from client.utils.jwt.config import JWT_SECRET, JWT_ALGORITHM


def test_generate_jwt_token():
    token = generate_jwt_token()
    decoded = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    assert decoded["user"] == "test_user"
