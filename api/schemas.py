# api/schemas.py
from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class UserDB(UserBase):
    id: int
    hpass: str

    class Config:
        orm_mode = True


class UserDBWithToken(UserDB):
    token: Token
