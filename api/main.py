# api/main.py
from typing import Union, Optional
from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import (
    OAuth2AuthorizationCodeBearer,
    OAuth2PasswordRequestForm,
    OAuth2PasswordBearer,
)

from fastapi.responses import Response

from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from typing import (
    List,
    Optional,
    Dict,
    Any,
    Union,
    TypeVar,
    Generic,
    Type,
    Callable,
)


from myfuncs import runcmd

from config import HOST, PORT
from crud import create_new_user, get_current_user, user_from_email
from dependencies import get_current_user, get_tokenlogin_user
from auth import verify_password, create_access_token
from schemas import UserDB, Token, UserOutToken, UserOut, UserCreate, TokenLogin
from db import get_db


# Content Security Policy Middleware
class CSPMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        csp_directives = (
            "default-src 'self'; "
            "img-src 'self' data: https://fastapi.tiangolo.com; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "worker-src 'self' blob:; "
        )
        response.headers["Content-Security-Policy"] = csp_directives
        return response


app = FastAPI(docs_url='/docs', redoc_url='/redoc')

# fuck CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow any origin
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,  # Allow credentials (cookies, authorization headers, etc.)
    expose_headers=["*"],
)

# CSP middleware
app.add_middleware(CSPMiddleware)

router = APIRouter()

print("loading routes")


@router.get("/")
async def hello():
    return {"status": "ok"}


@app.post("/user/create", response_model=UserOutToken)
async def register_user(data: UserCreate, db: AsyncSession = Depends(get_db)):
    email, password = data.email, data.password
    print(f'email: {email}')
    print(f'password: {password}')

    db_user = await user_from_email(email, db)

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    newuser = await create_new_user(
        email, password, db
    )  # Assuming your create_user function is asynchronous

    utoken = Token(access_token=create_access_token(newuser.email))

    userout = UserOutToken(**newuser.__dict__, token=utoken)

    print(userout)
    return userout


@app.post("/user/tokenlogin", response_model=Token)
async def token_from_login(
    tokuser: UserDB = Depends(get_tokenlogin_user),
    db: AsyncSession = Depends(get_db),
):
    access_token = create_access_token(tokuser.email)
    return Token(access_token=access_token)


@app.get("/user/me", response_model=UserOut)
async def read_users_me(
    current_user: UserDB = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return current_user


@router.get("/openapi.json")
async def get_openapi_schema():
    return get_openapi(
        title="API documentation", version="1.0.0", routes=app.routes
    )


app.include_router(router)


if (__name__) == "__main__":
    runcmd(
        f"uvicorn main:app --host {HOST} --port {PORT} --reload", output=False
    )
