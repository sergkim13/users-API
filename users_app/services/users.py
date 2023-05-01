from http import HTTPStatus

from fastapi import Depends, HTTPException
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from users_app.cache.abstract_cache import AbstractCache
from users_app.cache.module import get_cache
from users_app.database.crud.cities import CityCRUD
from users_app.database.crud.users import UserCRUD
from users_app.database.models import User
from users_app.database.settings import get_session
from users_app.validation.schemas import (
    CitiesHintModel,
    PaginatedMetaDataModel,
    PrivateCreateUserModel,
    PrivateDetailUserResponseModel,
    PrivateUpdateUserModel,
    PrivateUsersListHintMetaModel,
    PrivateUsersListMetaDataModel,
    PrivateUsersListResponseModel,
    QueryParams,
    UpdateUserModel,
    UsersListMetaDataModel,
    UsersListResponseModel,
)


class UserService:
    def __init__(
        self,
        cache: AbstractCache,
        user_crud: UserCRUD,
        city_crud: CityCRUD,
        pwd_context: CryptContext = CryptContext(schemes=['bcrypt'], deprecated='auto'),
    ) -> None:
        self.cache = cache
        self.user_crud = user_crud
        self.pwd_context = pwd_context
        self.city_crud = city_crud

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
            cities_list = [
                await self._get_city(city_id=getattr(user, 'city')) for user in users_list
            ]

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
        cache_key = f'user-{user_id}'
        user = await self.cache.get(cache_key)
        if not user:
            try:
                user = await self.user_crud.read(user_id=user_id)
                await self.cache.set(cache_key, user)
            except NoResultFound:
                raise HTTPException(
                    status_code=HTTPStatus.NOT_FOUND,
                    detail='User not found.'
                )
        return user

    async def create(self, data: PrivateCreateUserModel) -> PrivateDetailUserResponseModel:
        try:
            user = await self.user_crud.create(data=data)
            await self.cache.clear('all')
            return user
        except IntegrityError as e:
            if 'UniqueViolationError' in str(e.orig):
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail=f'User with email {data.email} already exists.'
                )
            elif 'ForeignKeyViolationError' in str(e.orig):
                raise HTTPException(
                    status_code=HTTPStatus.NOT_FOUND,
                    detail='City with given ID not found',
                )
            else:
                raise

    async def update(self, user_id: int,
                     data: UpdateUserModel | PrivateUpdateUserModel) -> User:
        try:
            user = await self.user_crud.read(user_id=user_id)
            updated_user = await self.user_crud.update(user=user, data=data)
            await self.cache.clear(f'user-{user_id}')
            await self.cache.clear('all')
        except NoResultFound:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='User not found.'
            )
        except IntegrityError as e:
            if 'UniqueViolationError' in str(e.orig):
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail=f'User with email {data.email} already exists.'
                )
            if 'ForeignKeyViolationError' in str(e.orig):
                raise HTTPException(
                    status_code=HTTPStatus.NOT_FOUND,
                    detail='City with given ID not found',
                )
        return updated_user

    async def delete(self, user_id: int) -> str:
        try:
            await self.user_crud.delete(user_id=user_id)
            await self.cache.clear(f'user-{user_id}')
            await self.cache.clear('all')
            return f'User {user_id} has been deleted.'
        except NoResultFound:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='User not found.'
            )

    async def _get_list(self, query: QueryParams) -> tuple[int, list[User | None]]:
        users_count = await self._count_users()
        max_pages = (users_count + query.size - 1) // query.size
        if query.page > max_pages:
            users_list = []
        else:
            cache_key = f'users-{query}'
            users_list = await self.cache.get(cache_key)
            if not users_list:
                users_list = await self.user_crud.read_all(query)
                await self.cache.set(cache_key, users_list)
        return (users_count, users_list)

    async def _get_city(self, city_id: int) -> CitiesHintModel | None:
        return await self.city_crud.read(city_id=city_id)

    async def _count_users(self):
        return await self.user_crud.count_all()


def get_user_service(
    session: AsyncSession = Depends(get_session),
    cache: AbstractCache = Depends(get_cache),
) -> UserService:
    user_crud = UserCRUD(session)
    city_crud = CityCRUD(session)
    return UserService(cache, user_crud, city_crud)
