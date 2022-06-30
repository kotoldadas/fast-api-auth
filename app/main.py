from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session, select
from services.auth import get_current_user
from utils.hashing import get_hashed_password, verify_password
from models import *
from utils.jwt import Token, TokenData, TokenType, create_access_token
from db import create_db_and_tables, get_session


app = FastAPI()


@app.on_event("startup")
def on_start():
    create_db_and_tables()


@app.get("/users/", response_model=list[UserRead])
async def get_all_users(session: Session = Depends(get_session)):
    statement = select(User)
    a = session.exec(statement).all()
    return a


@app.get("/users/me/")
async def get_current_users(user: User = Depends(get_current_user)):
    return user


@app.post("/register/", response_model=Token)
async def register(user: UserCreate, session: Session = Depends(get_session)):
    user.password = get_hashed_password(user.password)
    new_user = User.from_orm(user)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    tokenData = TokenData.from_user(new_user)
    token = create_access_token(tokenData)
    return Token(access_token=token, token_type=TokenType.access)


@app.post("/login/", response_model=Token)
async def login(user: UserLogin, session: Session = Depends(get_session)):
    statement = select(User).where(User.username == user.username)
    users = session.exec(statement).all()
    for u in users:
        if verify_password(user.password, u.password):
            tokenData = TokenData.from_user(u)
            token = create_access_token(tokenData)
            return Token(access_token=token, token_type=TokenType.access)

    raise HTTPException(status_code=404, detail="Not Found Custom")
