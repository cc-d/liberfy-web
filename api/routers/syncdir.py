# FILE: routers/syncdir.py

from fastapi import APIRouter, Depends
from crud import new_syncdir, get_proj_syncdirs
from schemas import SyncDirCreate, SyncDirOut
from models import SyncDir, DirFile
from dependencies import get_curuser_id, get_syncdir_from_id
from db import AsyncSession, get_db

srouter = APIRouter(prefix='/p/{project_id}/s', tags=['syncdir'])


@srouter.post("/new", response_model=SyncDirOut)
async def create_syncdir(
    data: SyncDirCreate,
    user_id: str = Depends(get_curuser_id),
    db: AsyncSession = Depends(get_db),
) -> SyncDirOut:
    sync_dir = await new_syncdir(data.path, data.project_id, db)
    return sync_dir


@srouter.get("/all", response_model=list[SyncDirOut])
async def get_all_syncdirs(
    project_id: str, db: AsyncSession = Depends(get_db)
) -> list[SyncDirOut]:
    syncdirs = await get_proj_syncdirs(project_id, db)
    return syncdirs


@srouter.get("/{syncdir_id}", response_model=SyncDirOut)
async def get_syncdir(
    syncdir: SyncDir = Depends(get_syncdir_from_id),
) -> list[SyncDirOut]:
    return syncdir
