# api/schemas.py
from pydantic import BaseModel, Field


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


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int


class UserDB(UserOut):
    hpassword: str

    class Config:
        orm_mode = True


class UserOutToken(UserOut):
    token: Token
