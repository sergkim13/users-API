from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from users_app.schemas.schemas import (
    Payload,
    PrivateCreateUserModel,
    PrivateDetailUserResponseModel,
    PrivateUpdateUserModel,
    PrivateUsersListResponseModel,
    QueryParams
)
from users_app.services.helper import get_jwt_private
from users_app.services.users import UserService, get_user_service


router = APIRouter(
    prefix='/api/v1/private',
    tags=['admin'],
)


@router.get(
    path='/users',
    response_model=PrivateUsersListResponseModel,
    summary='Постраничное получение кратких данных обо всех пользователях',
)
async def private_user_list(
    query: QueryParams = Depends(),
    user_service: UserService = Depends(get_user_service),
    jwt: Payload = Depends(get_jwt_private),
) -> PrivateUsersListResponseModel:
    '''Shows user's info list with pagination.'''
    users_list = await user_service.get_list_private(query)
    return users_list


@router.post(
    path='/users',
    response_model=PrivateDetailUserResponseModel,
    summary='Создание пользователя',
)
async def private_user_create(
    data: PrivateCreateUserModel,
    user_service: UserService = Depends(get_user_service),
    jwt: Payload = Depends(get_jwt_private),
) -> PrivateDetailUserResponseModel:
    '''Creates a user.'''
    new_user = await user_service.create(data=data)
    return new_user


@router.get(
    path='/users/{pk}',
    response_model=PrivateDetailUserResponseModel,
    summary='Детальное получение информации о пользователе',
)
async def private_user_detail(
    pk: int,
    user_service: UserService = Depends(get_user_service),
    jwt: Payload = Depends(get_jwt_private),
) -> PrivateDetailUserResponseModel:
    '''Shows detail info about specific user.'''
    user = await user_service.get_detail(user_id=pk)
    return user


@router.patch(
    path='/users/{pk}',
    response_model=PrivateDetailUserResponseModel,
    summary='Изменение информации о пользователе',
)
async def private_user_update(
    pk: int,
    data: PrivateUpdateUserModel,
    user_service: UserService = Depends(get_user_service),
    jwt: Payload = Depends(get_jwt_private),
) -> PrivateDetailUserResponseModel:
    '''Update info about specific user.'''
    updated_user = await user_service.update(user_id=pk, data=data)
    return updated_user


@router.delete(
    path='/users/{pk}',
    summary='Удаление пользователя',
)
async def private_user_delete(
    pk: int,
    user_service: UserService = Depends(get_user_service),
    jwt: Payload = Depends(get_jwt_private),
) -> JSONResponse:
    '''Delete specific user.'''
    return await user_service.delete(user_id=pk)
