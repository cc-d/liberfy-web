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

prouter = APIRouter(prefix='/project', tags=['project'])


@prouter.post("/create", response_model=ProjectOut)
async def create_project(
    data: ProjectCreate,
    current_user: UserDB = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ProjectOut:
    project = await create_new_project(data.name, current_user.id, db)
    return project
