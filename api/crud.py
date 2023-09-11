import jwt
from jwt import PyJWTError
from fastapi import Depends, HTTPException
from sqlalchemy import select
from logfunc import logf
from config import JWT_ALGORITHM, JWT_SECRET, JWT_EXPIRE_SECS, DEFAULTS as DEFS
from db import AsyncSession, get_db, async_add_com_ref
from dependencies import get_curuser, get_curuser_id
from models import User, Project, SyncDir, DirFile
from schemas import ProjectNew, ProjectDB, SyncDirDB, DirFileDB
from auth import get_password_hash, oauth2_scheme


@logf()
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


@logf()
async def new_project(
    name: str = DEFS.PROJECT_NAME,
    user_id: str = Depends(get_curuser_id),
    db: AsyncSession = Depends(get_db),
) -> ProjectDB:
    db_project = Project(name=name, user_id=user_id)
    db_project = await async_add_com_ref(db_project, db)
    return db_project


@logf()
async def new_syncdir(
    path: str,
    project_id: str,
    user_id: str = get_curuser_id,
    db: AsyncSession = Depends(get_db),
) -> SyncDir:
    sync_dir = SyncDir(path=path, project_id=project_id, user_id=user_id)
    sync_dir = await async_add_com_ref(sync_dir, db)
    return sync_dir


@logf()
async def get_proj_syncdirs(
    project_id: str, db: AsyncSession = Depends(get_db)
) -> list[SyncDir]:
    result = await db.execute(
        select(SyncDir).where(SyncDir.project_id == project_id)
    )
    return result.scalars().all()
