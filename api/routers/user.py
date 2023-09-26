from auth import create_access_token
from crud import new_user
from db import AsyncSession, get_db
from dependencies import get_curuser, get_tokenlogin_user, user_from_email
from fastapi import APIRouter, Depends, HTTPException
from models import User
from schemas import Token, UserDB, UserOut, UserOutToken

urouter = APIRouter(prefix='/u', tags=['user'])


@urouter.post("/new", response_model=UserOutToken)
async def create(*args, db: AsyncSession = Depends(get_db), **kwargs):
    email, password = kwargs.get('username'), kwargs.get('password')

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
