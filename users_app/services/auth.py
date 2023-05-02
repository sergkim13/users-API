from http import HTTPStatus

from fastapi import Depends, HTTPException, Request
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from users_app.database.crud.users import UserCRUD
from users_app.database.settings import get_session
from users_app.exceptions.constants import (
    MSG_INVALID_CREDS,
    MSG_NOT_AUTHENTICATED,
    MSG_NOT_AUTHORIZED,
)
from users_app.security.cifer import Cifer, get_cifer
from users_app.security.hasher import get_pwd_context
from users_app.validation.schemas import CurrentUserResponseModel, LoginModel, Payload


class AuthService:
    def __init__(self, user_crud: UserCRUD, pwd_context: CryptContext) -> None:
        '''Init `AuthService` instance.'''
        self.user_crud = user_crud
        self.pwd_context = pwd_context
        self.cifer: Cifer = get_cifer()

    async def authenticate_user(self, credentials: LoginModel) -> CurrentUserResponseModel:
        '''Checks recieved credentials.'''
        user = await self.user_crud.read_by_login(credentials.login)
        if not user or not self._verify_password(credentials.password, user.password):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=MSG_INVALID_CREDS,
            )
        return user

    async def encode_token(self, payload: Payload) -> str:
        '''Encodespayload to JWT.'''
        return self.cifer.encode(payload)

    async def check_jwt(self, request: Request) -> Payload:
        '''ChecksJWT in request's cookie.'''
        session_token = request.cookies.get('jwt_token')
        if not session_token:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail=MSG_NOT_AUTHENTICATED,
            )
        payload = self.cifer.decode(session_token)
        return payload

    async def check_jwt_private(self, request: Request) -> None:
        '''ChecksJWT in request's cookie and validate `is_admin` field in payload.'''
        payload = await self.check_jwt(request)
        if not payload.get('is_admin'):
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail=MSG_NOT_AUTHORIZED,
            )

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        '''Checkspassword in recieved credentialds and hashed password in database.'''
        return self.pwd_context.verify(plain_password, hashed_password)


def get_auth_service(
    session: AsyncSession = Depends(get_session),
    pwd_context: CryptContext = Depends(get_pwd_context)
):
    '''Returns `AuthService` instance for dependency injection.'''
    user_crud = UserCRUD(session)
    return AuthService(user_crud, pwd_context)
