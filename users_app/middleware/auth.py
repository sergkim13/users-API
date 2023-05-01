import re
from http import HTTPStatus
from typing import Callable

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from users_app.services.auth import AuthService, get_auth_service
from users_app.validation.schemas import CodelessErrorResponseModel


class AuthdMidddleware(BaseHTTPMiddleware):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.auth_service: AuthService = get_auth_service()
        self.user_routes_schema = r'^\/users.*'
        self.private_routes_schema = r'^\/private.*'

    async def dispatch(self, request: Request, call_next: Callable):
        try:
            if re.match(self.private_routes_schema, request.url.path):
                await self.auth_service.check_jwt_private(request)
            if re.match(self.user_routes_schema, request.url.path):
                await self.auth_service.check_jwt(request)
        except HTTPException as exc:
            if exc.status_code == HTTPStatus.UNAUTHORIZED:
                error_response = CodelessErrorResponseModel(message=exc.detail)
            if exc.status_code == HTTPStatus.FORBIDDEN:
                error_response = CodelessErrorResponseModel(message=exc.detail)
            return JSONResponse(content=error_response.dict(), status_code=exc.status_code)
        return await call_next(request)
