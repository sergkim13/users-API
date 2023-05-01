from fastapi import FastAPI, HTTPException
from starlette.middleware.sessions import SessionMiddleware

from config import SECRET_KEY
from users_app.api.v1.routers.admin import router as admin_router
from users_app.api.v1.routers.auth import router as auth_router
from users_app.api.v1.routers.user import router as user_router
from users_app.exceptions.handlers import (
    ClientExceptionHandler,
    InternalExceptionHandler,
)
from users_app.middleware.auth import AuthdMidddleware

app = FastAPI(
    title='Users API',
    description='Users API, powered by FastAPI',
    version='0.1.0',
    docs_url='/docs',
    redoc_url='/redoc',
)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(admin_router)
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
app.add_middleware(AuthdMidddleware)
app.add_exception_handler(500, InternalExceptionHandler())
app.add_exception_handler(HTTPException, ClientExceptionHandler())
