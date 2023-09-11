# api/main.py
from datetime import timedelta
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    List,
    Optional,
    Type,
    TypeVar,
    Union,
)

from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import Response
from fastapi.security import (
    OAuth2AuthorizationCodeBearer,
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
)
from logfunc import logf
from myfuncs import runcmd
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.types import ASGIApp

from auth import create_access_token, verify_password
from config import HOST, PORT
from crud import new_user, get_curuser
from db import get_db
from dependencies import user_from_email, get_curuser, get_tokenlogin_user
from schemas import Token, TokenLogin, UserNew, UserDB, UserOut, UserOutToken


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


@router.get("/openapi.json")
async def get_openapi_schema():
    return get_openapi(
        title="API documentation", version="1.0.0", routes=app.routes
    )


app.include_router(router)

from routers import urouter, prouter

for rter in (urouter, prouter):
    app.include_router(rter)


if (__name__) == "__main__":
    runcmd(
        f"uvicorn main:app --host {HOST} --port {PORT} --reload", output=False
    )
