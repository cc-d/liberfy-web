from fastapi import APIRouter, HTTPException, Depends

from auth import create_access_token
from crud import create_new_user, user_from_email
from dependencies import get_current_user, get_tokenlogin_user
from db import get_db, AsyncSession
from schemas import (
    UserDB,
    UserCreate,
    Token,
    TokenLogin,
    UserOutToken,
    UserOut,
    ProjectBase,
    ProjectCreate,
    ProjectOut,
    ProjectDB,
)

urouter = APIRouter(prefix='/user', tags=['user'])


@urouter.post("/create", response_model=UserOutToken)
async def register_user(data: UserCreate, db: AsyncSession = Depends(get_db)):
    email, password = data.email, data.password
    print(f'email: {email}')
    print(f'password: {password}')

    db_user = await user_from_email(email, db)

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    newuser = await create_new_user(
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
    current_user: UserDB = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> UserOut:
    return current_user
