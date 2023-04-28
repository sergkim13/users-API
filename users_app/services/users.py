from http import HTTPStatus

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from users_app.database.crud.users import UserCRUD
from users_app.database.settings import get_session
from users_app.schemas.schemas import CurrentUserResponseModel, LoginModel, PrivateCreateUserModel, PrivateDetailUserResponseModel
from passlib.context import CryptContext


class UserService:
    def __init__(
        self,
        user_crud: UserCRUD,
        pwd_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto"),
    ) -> None:
        self.user_crud = user_crud
        self.pwd_context = pwd_context

    async def authenticate_user(self, credentials: LoginModel) -> CurrentUserResponseModel | None:
        user = await self.user_crud.read_by_login(credentials.login)
        if not user:
            return None
        if not await self._verify_password(credentials.password, user.password):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Invalid login or password',
            )
        return user

    async def create(self, user_data: PrivateCreateUserModel) -> PrivateDetailUserResponseModel:
        user = await self.user_crud.create(user_data)
        return user

    async def _verify_password(self, plain_password: str, hashed_password: str):
        return self.pwd_context.verify(plain_password, hashed_password)


def get_user_service(session: AsyncSession = Depends(get_session)) -> UserService:
    user_crud = UserCRUD(session)
    return UserService(user_crud)
