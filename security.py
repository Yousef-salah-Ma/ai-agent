from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
import jwt

from fastapi import Depends ,Header

from fastapi.security import OAuth2PasswordBearer

from fastapi import HTTPException

password_hash = PasswordHash.recommended()

SECRET_KEY = "test123456"
ALGORITHM = "HS256"


def hash_password(password: str):
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str):
    return password_hash.verify(password, hashed_password)


def create_access_token(user_id: int):
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30)
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(Auth2PasswordBearer: str = Header()):

    try:
        payload = jwt.decode(
            Auth2PasswordBearer,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        return int(user_id)

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

