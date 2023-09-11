import jwt
import logfunc
from fastapi.security import (
    OAuth2AuthorizationCodeBearer,
    OAuth2PasswordRequestForm,
    OAuth2PasswordBearer,
)
from fastapi import Depends, HTTPException
from datetime import datetime, timedelta
from typing import Optional
from jwt import PyJWTError
from passlib.context import CryptContext
from db import get_db, AsyncSession
from models import User
from config import JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRE_SECS

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/u/tokenlogin")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(email: str, exp_delta: int = JWT_EXPIRE_SECS) -> str:
    exp = timedelta(seconds=exp_delta)
    utcnow = datetime.utcnow()
    payload = {'exp': utcnow + exp, 'sub': email, 'iat': utcnow}
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token
