from fastapi import APIRouter, HTTPException, Depends

from auth import create_access_token
from crud import new_user
from dependencies import user_from_email, get_curuser, get_tokenlogin_user
from db import get_db, AsyncSession
from schemas import (
    UserDB,
    UserNew,
    Token,
    TokenLogin,
    UserOutToken,
    UserOut,
    ProjectBase,
    ProjectNew,
    ProjectOut,
    ProjectDB,
)
from models import User

urouter = APIRouter(prefix='/u', tags=['user'])


@urouter.post("/new", response_model=UserOutToken)
async def create_user(data: UserNew, db: AsyncSession = Depends(get_db)):
    email, password = data.email, data.password
    print(f'email: {email}')
    print(f'password: {password}')

    db_user = await user_from_email(email, db)

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    newuser = await new_user(
        email, password, db
    )  # Assuming your create_user function is asynchronous

    utoken = Token(access_token=create_access_token(newuser.email))

    userout = UserOutToken(**newuser.__dict__, token=utoken)

    return userout


@urouter.post("/tokenlogin", response_model=Token)
async def token_from_login(
    tokuser: UserDB = Depends(get_tokenlogin_user),
    db: AsyncSession = Depends(get_db),
):
    access_token = create_access_token(tokuser.email)
    return Token(access_token=access_token)


@urouter.get("/me", response_model=UserOut)
async def read_users_me(
    current_user: UserDB = Depends(get_curuser),
    db: AsyncSession = Depends(get_db),
) -> UserOut:
    return current_user
