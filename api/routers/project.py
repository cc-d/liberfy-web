import asyncio
from fastapi import APIRouter, HTTPException, Depends
from logfunc import logf
from sqlalchemy import select
from auth import create_access_token
from crud import new_user, new_project
from dependencies import (
    user_from_email,
    get_curuser,
    get_curuser_id,
    get_tokenlogin_user,
    get_proj_from_id,
    get_user_projs,
)
from db import get_db, AsyncSession
from models import Project, User
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

prouter = APIRouter(prefix='/p', tags=['project'])


@prouter.post("/new", response_model=ProjectOut)
async def create_project(
    data: ProjectNew,
    user_id: str = Depends(get_curuser_id),
    db: AsyncSession = Depends(get_db),
) -> ProjectOut:
    project = await new_project(data.name, user_id, db)
    return project


@prouter.get("/all", response_model=list[ProjectOut])
async def get_all_projects(
    projects: list[Project] = Depends(get_user_projs),
) -> list[ProjectOut]:
    return projects


@prouter.get("/{project_id}", response_model=ProjectOut)
async def get_project(
    project: Project = Depends(get_proj_from_id),
) -> ProjectOut:
    return project
