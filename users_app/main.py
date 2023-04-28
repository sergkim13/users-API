from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from users_app.api.v1.routers.auth import router as auth_router
from users_app.api.v1.routers.user import router as user_router
from users_app.api.v1.routers.admin import router as admin_router
from config import SECRET_KEY

app = FastAPI(
    title='Users API',
    description='Users API, powered by FastAPI',
    version='0.1.0',
    docs_url='/doc',
    redoc_url='/redoc',
)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(admin_router)
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
