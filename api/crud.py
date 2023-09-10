# api/crud.py
import jwt
from jwt import PyJWTError
from fastapi import Depends, HTTPException
from sqlalchemy import select
from config import JWT_ALGORITHM, JWT_SECRET, JWT_EXPIRE_SECS
from db import AsyncSession, get_db, async_add_com_ref

from models import User
from schemas import UserDB, UserCreate
from auth import get_password_hash, oauth2_scheme


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


async def create_new_user(
    email: str, password: str, db: AsyncSession = Depends(get_db)
) -> User:
    st = select(User).where(User.email == email)
    result = await db.execute(st)

    if result.scalars().one_or_none() is not None:
        raise Exception('user already exists')

    hpass = get_password_hash(password)

    db_user = User(email=email, hpassword=hpass)
    db_user = await async_add_com_ref(db_user, db)
    return db_user


async def user_from_email(
    email: str, db: AsyncSession = Depends(get_db)
) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().one_or_none()
