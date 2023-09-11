# api/schemas.py
from pydantic import BaseModel, Field


# Token
class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class TokenLogin(BaseModel):
    username: str
    password: str
    grant_type: str = 'password'
    scope: str = ''
    client_id: str = ''
    client_secret: str = ''


# User
class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
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
    name: str


class ProjectCreate(ProjectBase):
    pass


class ProjectOut(ProjectBase):
    id: str
    user_id: str


class ProjectDB(ProjectOut):
    user: UserDB
    sync_dirs: list['SyncDirDB']

    class Config:
        orm_mode = True


# SyncDir
class SyncDirBase(BaseModel):
    path: str


class SyncDirCreate(SyncDirBase):
    project_id: str


class SyncDirOut(SyncDirCreate):
    id: str
    dirfiles: list['DirFileDB']


class SyncDirDB(SyncDirOut):
    project: ProjectDB

    class Config:
        orm_mode = True


# DirFile
class DirFileBase(BaseModel):
    relpath: str
    content: str | None


class DirFileCreate(DirFileBase):
    sync_dir_id: str
    checksum: str
    checksum_type: str = 'md5'


class DirFileOut(DirFileCreate):
    id: str


class DirFileDB(DirFileOut):
    sync_dir: SyncDirDB

    class Config:
        orm_mode = True
