# api/crud.py
from sqlalchemy import select
from db import AsyncSession

from models import User
from schemas import UserDB, UserCreate
from auth import get_password_hash


async def create_new_user(db: AsyncSession, userdata: UserCreate) -> UserDB:
    email = userdata.email
    st = select(User).where(User.email == email)
    result = await db.execute(st)

    if result.scalars().one_or_none() is not None:
        raise Exception('user already exists')

    hpass = get_password_hash(userdata.password)

    db_user = User(email=userdata.email, hpass=hpass)

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_user_with_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().one_or_none()
