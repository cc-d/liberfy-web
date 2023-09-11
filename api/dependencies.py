# api/dependencies.py
import jwt
from typing import Union, Optional
from jwt import PyJWTError
from logfunc import logf
from fastapi import Depends, HTTPException, Request
from sqlalchemy import select
from config import JWT_ALGORITHM, JWT_SECRET, JWT_EXPIRE_SECS
from db import AsyncSession, get_db, async_add_com_ref
from fastapi.security import OAuth2PasswordRequestForm
from models import User, Project, SyncDir, DirFile
from schemas import (
    UserDB,
    UserNew,
    Token,
    TokenLogin,
    UserOutToken,
    UserOut,
    ProjectNew,
    ProjectDB,
    ProjectOut,
    SyncDirDB,
    DirFileDB,
)
from auth import get_password_hash, oauth2_scheme, verify_password


@logf()
async def user_from_email(
    email: str, db: AsyncSession = Depends(get_db)
) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().one_or_none()


@logf()
async def get_curuser(
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
    return user


@logf()
async def get_curuser_id(curuser: UserDB = Depends(get_curuser)) -> str:
    return curuser.id


@logf()
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


@logf()
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
    return user


@logf()
async def get_user_projs(
    user_id: str = Depends(get_curuser_id), db: AsyncSession = Depends(get_db)
) -> list[Project]:
    projects = await db.execute(
        select(Project).where(Project.user_id == user_id)
    )
    projects = projects.scalars().all()
    return projects


@logf()
async def get_proj_from_id(
    project_id: str,
    user_id: str = Depends(get_curuser_id),
    db: AsyncSession = Depends(get_db),
) -> Project:
    project = await db.execute(select(Project).where(Project.id == project_id))
    project = project.scalars().one_or_none()
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    elif project.user_id != user_id:
        raise HTTPException(status_code=401, detail="Not authorized")
    return project
