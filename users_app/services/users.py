from http import HTTPStatus

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from users_app.database.crud.cities import CityCRUD

from users_app.database.crud.users import UserCRUD
from users_app.database.models import User
from users_app.database.settings import get_session
from users_app.schemas.schemas import CitiesHintModel, CurrentUserResponseModel, LoginModel, PaginatedMetaDataModel, PrivateCreateUserModel, PrivateDetailUserResponseModel, PrivateUpdateUserModel, PrivateUsersListHintMetaModel, PrivateUsersListMetaDataModel, PrivateUsersListResponseModel, QueryParams, UpdateUserModel, UsersListMetaDataModel, UsersListResponseModel
from passlib.context import CryptContext


class UserService:
    def __init__(
        self,
        user_crud: UserCRUD,
        city_crud: CityCRUD,
        pwd_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto"),
    ) -> None:
        self.user_crud = user_crud
        self.pwd_context = pwd_context
        self.city_crud = city_crud

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

    async def get_list(self, query: QueryParams) -> UsersListResponseModel:
        users_count, users_list = await self._get_list(query)
        return UsersListResponseModel(
            data=users_list,
            meta=UsersListMetaDataModel(
                pagination=PaginatedMetaDataModel(
                    total=users_count,
                    page=query.page,
                    size=query.size
                )
            )
        )

    async def get_list_private(self, query: QueryParams) -> PrivateUsersListResponseModel:
        users_count, users_list = await self._get_list(query)
        if users_list == []:
            cities_list = []
        else:
            cities_list = [await self._get_city(city_id=user.city) for user in users_list]

        return PrivateUsersListResponseModel(
            data=users_list,
            meta=PrivateUsersListMetaDataModel(
                pagination=PaginatedMetaDataModel(
                    total=users_count,
                    page=query.page,
                    size=query.size
                ),
                hint=PrivateUsersListHintMetaModel(city=cities_list),
            )
        )

    async def get_detail(self, user_id: int) -> User:
        user = await self.user_crud.read(user_id=user_id)
        return user

    async def create(self, data: PrivateCreateUserModel) -> PrivateDetailUserResponseModel:
        user = await self.user_crud.create(data=data)
        return user

    async def update(self, user_id: int,
                     data:  UpdateUserModel | PrivateUpdateUserModel) -> User:
        user = await self.user_crud.update(user_id=user_id, data=data)
        return user

    async def delete(self, user_id: int) -> str:
        await self.user_crud.delete(user_id=user_id)
        return f'User {user_id} has been deleted.'
    
    async def _get_list(self, query: QueryParams) -> tuple[int, list[User | None]]:
        users_count = await self._count_users()
        max_pages = (users_count + query.size - 1) // query.size
        if query.page > max_pages:
            users_list = []
        else:
            users_list = await self.user_crud.read_all(query)
        return (users_count, users_list)

    async def _get_city(self, city_id: int) -> CitiesHintModel:
        return await self.city_crud.read(city_id=city_id)

    async def _verify_password(self, plain_password: str, hashed_password: str):
        return self.pwd_context.verify(plain_password, hashed_password)

    async def _count_users(self):
        return await self.user_crud.count_all()


def get_user_service(session: AsyncSession = Depends(get_session)) -> UserService:
    user_crud = UserCRUD(session)
    city_crud = CityCRUD(session)
    return UserService(user_crud, city_crud)
