from datetime import datetime
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlmodel import Session
from starlette.status import HTTP_401_UNAUTHORIZED
from models.user import User
from utils.jwt import JWT_SECRET_KEY, ALGORITHM, TokenData
from db import get_session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

credentials_exception = HTTPException(
    status_code=HTTP_401_UNAUTHORIZED,
    detail="Could not validated credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

token_expires_exception = HTTPException(
    status_code=HTTP_401_UNAUTHORIZED,
    detail="Token Expired!!",
    headers={"WWW-Authenticate": "Bearer"},
)


def validate_token(token: TokenData):
    if token.expire <= datetime.now():
        print(
            f"---------------\n\ntoken expired - now => {datetime.now()} - token => {token.expire}\n\n--------------------"
        )
        raise token_expires_exception

    print(
        f"---------------\n\nvalid token - now => {datetime.now()} - token => {token.expire}\n\n--------------------"
    )


async def get_current_user(
    token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)
):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        data = TokenData.parse_obj(payload)
    except (JWTError, ValidationError):
        raise credentials_exception

    validate_token(data)
    print(f"----------\ntoken data => {data}\n----------")
    user = session.get(User, data.id)
    if not user:
        raise credentials_exception
    return user
