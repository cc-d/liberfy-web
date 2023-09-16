from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum
from config import DEFAULTS as DEFS


# Enum Definitions
class TokenType(str, Enum):
    bearer = "bearer"


class ChecksumType(str, Enum):
    md5 = "md5"


# Token
class Token(BaseModel):
    access_token: str
    token_type: TokenType = TokenType.bearer


class TokenLogin(BaseModel):
    username: str
    password: str = Field(..., min_length=8)
    grant_type: str = 'password'
    scope: str = ''
    client_id: str = ''
    client_secret: str = ''


# User
class UserBase(BaseModel):
    email: str


class UserNew(UserBase):
    password: str


class UserOut(UserBase):
    id: str


class UserDB(UserOut):
    hpassword: str
    projects: list['ProjectDB']

    class Config:
        orm_mode = True


class UserOutToken(UserOut):
    token: Token


# Project
class ProjectBase(BaseModel):
    pass


class ProjectNew(ProjectBase):
    name: str


class ProjectOut(ProjectNew):
    id: str
    user_id: str


class ProjectDB(ProjectOut):
    user: UserDB
    syncdirs: list['SyncDirDB'] = []

    class Config:
        orm_mode = True


# SyncDir / DirFile
class SyncDirBase(BaseModel):
    path: str


class SyncDirCreate(SyncDirBase):
    project_id: str


class DirFileBase(BaseModel):
    relpath: str
    content: Optional[str]
    last_updated: datetime = datetime.now


class DirFileCreate(DirFileBase):
    syncdir_id: str
    checksum: str
    checksum_type: ChecksumType


class DirFileOut(DirFileCreate):
    id: str


class SyncDirOut(SyncDirCreate):
    id: str
    user_id: str
    dirfiles: list[DirFileOut] = []


class SyncDirDB(SyncDirOut):
    project: ProjectDB

    class Config:
        orm_mode = True


class DirFileDB(DirFileOut):
    syncdir: SyncDirDB

    class Config:
        orm_mode = True
