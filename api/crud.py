# api/crud.py
import jwt
from jwt import PyJWTError
from fastapi import Depends, HTTPException
from sqlalchemy import select
from config import JWT_ALGORITHM, JWT_SECRET, JWT_EXPIRE_SECS, DEFAULTS as DEFS
from db import AsyncSession, get_db, async_add_com_ref
from dependencies import get_curuser, get_curuser_id
from models import User, Project
from schemas import ProjectNew, ProjectDB
from auth import get_password_hash, oauth2_scheme


async def new_user(
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


async def new_project(
    name: str = DEFS.PROJECT_NAME,
    user_id: str = Depends(get_curuser_id),
    db: AsyncSession = Depends(get_db),
) -> ProjectDB:
    db_project = Project(name=name, user_id=user_id)
    db_project = await async_add_com_ref(db_project, db)
    return db_project
