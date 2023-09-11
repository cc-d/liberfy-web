# api/dependencies.py
import jwt
from typing import Union, Optional
from jwt import PyJWTError
from fastapi import Depends, HTTPException, Request
from sqlalchemy import select
from config import JWT_ALGORITHM, JWT_SECRET, JWT_EXPIRE_SECS
from db import AsyncSession, get_db, async_add_com_ref
from fastapi.security import OAuth2PasswordRequestForm
from models import User
from schemas import UserDB, UserCreate, Token, TokenLogin, UserOutToken
from auth import get_password_hash, oauth2_scheme, verify_password
from crud import user_from_email


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
) -> UserDB:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except PyJWTError as e:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid auth credentials JWT error: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )

    email: str = payload.get("sub", None)
    if email is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid auth credentials no email",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await user_from_email(email, db)
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid auth credentials no user",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return UserDB(**user.__dict__)


async def get_login_data(
    request: Request, db: AsyncSession = Depends(get_db)
) -> Union[TokenLogin, OAuth2PasswordRequestForm]:
    try:
        # Try to parse body as JSON
        return TokenLogin(**await request.json())
    except ValueError:
        # If error, parse body as form data
        form = await request.form()
        return OAuth2PasswordRequestForm(**form)


async def get_tokenlogin_user(
    data: Union[TokenLogin, OAuth2PasswordRequestForm] = Depends(
        get_login_data
    ),
    db: AsyncSession = Depends(get_db),
) -> UserDB:
    email, password = data.username, data.password
    print(f'email: {email}', data, data.username, data.password)
    user = await user_from_email(email, db)
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid auth credentials no user found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif not verify_password(password, user.hpassword):
        raise HTTPException(
            status_code=401,
            detail="Invalid auth credentials password mismatch",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return UserDB(**user.__dict__)
