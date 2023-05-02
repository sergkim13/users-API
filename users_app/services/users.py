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
from users_app.exceptions.constants import (
    MSG_CITY_NOT_FOUND,
    MSG_EMAIL_EXISTS,
    MSG_USER_NOT_FOUND,
)
from users_app.security.hasher import get_pwd_context
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
        pwd_context: CryptContext,
    ) -> None:
        '''Init `UserService` instance.'''
        self.cache = cache
        self.user_crud = user_crud
        self.pwd_context = pwd_context
        self.city_crud = city_crud

    async def get_list(self, query: QueryParams) -> UsersListResponseModel:
        '''Gets list of users and returns response serialized for `user` paths.'''
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
        '''Gets list of users and returns response serialized for `private` paths.'''
        users_count, users_list = await self._get_list(query)
        if users_list == []:
            cities_list = []
        else:
            cities_list = [
                await self._get_city(
                    city_id=getattr(user, 'city', None)) for user in users_list  # type: ignore
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
        '''Returns a specific `User`.'''
        cache_key = f'user-{user_id}'
        user = await self.cache.get(cache_key)
        if not user:
            try:
                user = await self.user_crud.read(user_id=user_id)
                await self.cache.set(cache_key, user)
            except NoResultFound:
                raise HTTPException(
                    status_code=HTTPStatus.NOT_FOUND,
                    detail=MSG_USER_NOT_FOUND
                )
        return user

    async def create(self, data: PrivateCreateUserModel) -> PrivateDetailUserResponseModel:
        '''Creates new `User`.'''
        try:
            user = await self.user_crud.create(data=data)
            await self.cache.clear('all')
            return user
        except IntegrityError as e:
            if 'UniqueViolationError' in str(e.orig):
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail=MSG_EMAIL_EXISTS.format(data.email)
                )
            elif 'ForeignKeyViolationError' in str(e.orig):
                raise HTTPException(
                    status_code=HTTPStatus.NOT_FOUND,
                    detail=MSG_CITY_NOT_FOUND,
                )
            else:
                raise

    async def update(self, user_id: int,
                     data: UpdateUserModel | PrivateUpdateUserModel) -> User:
        '''Updates specific `User`.'''
        try:
            user = await self.user_crud.read(user_id=user_id)
            updated_user = await self.user_crud.update(user=user, data=data)
            await self.cache.clear(f'user-{user_id}')
            await self.cache.clear('all')
            return updated_user
        except NoResultFound:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=MSG_USER_NOT_FOUND
            )
        except IntegrityError as e:
            if 'UniqueViolationError' in str(e.orig):
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail=MSG_EMAIL_EXISTS.format(data.email)
                )
            if 'ForeignKeyViolationError' in str(e.orig):
                raise HTTPException(
                    status_code=HTTPStatus.NOT_FOUND,
                    detail=MSG_CITY_NOT_FOUND,
                )
            else:
                raise

    async def delete(self, user_id: int) -> None:
        '''Delete `User`.'''
        try:
            await self.user_crud.delete(user_id=user_id)
            await self.cache.clear(f'user-{user_id}')
            await self.cache.clear('all')
        except NoResultFound:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=MSG_USER_NOT_FOUND,
            )

    async def _get_list(self, query: QueryParams) -> tuple[int, list[User | None]]:
        '''Gets list of users and returns it with quantity of all users.'''
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
        '''Gets a specific `City`.'''
        return await self.city_crud.read(city_id=city_id)

    async def _count_users(self):
        '''Counts all users.'''
        return await self.user_crud.count_all()


def get_user_service(
    session: AsyncSession = Depends(get_session),
    cache: AbstractCache = Depends(get_cache),
    pwd_context: CryptContext = Depends(get_pwd_context),
) -> UserService:
    '''Returns `UserService` instance for dependency injection.'''
    user_crud = UserCRUD(session)
    city_crud = CityCRUD(session)
    return UserService(cache, user_crud, city_crud, pwd_context)
