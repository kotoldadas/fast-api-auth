from enum import Enum
import os
from datetime import datetime, timedelta
from fastapi import HTTPException
from jose import jwt
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

from models.user import User

ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")  # should be kept secret
JWT_REFRESH_SECRET_KEY = os.getenv("JWT_REFRESH_SECRET_KEY")  # should be kept secret


class TokenType(str, Enum):
    access = "access"
    refresh = "refresh"


class Token(BaseModel):
    access_token: str
    token_type: TokenType


class TokenData(BaseModel):
    id: int
    username: str
    expire: datetime

    @classmethod
    def from_user(
        cls,
        user: User,
        expire: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    ):
        if not user.id:
            raise HTTPException(status_code=500)
        return cls(id=user.id, username=user.username, expire=datetime.now() + expire)


def create_access_token(data: TokenData) -> str:
    to_encode = jsonable_encoder(data.dict())
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
