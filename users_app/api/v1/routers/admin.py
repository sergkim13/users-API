from http import HTTPStatus

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from users_app.api.v1.routers.constants import (
    PRIVATE_PREFIX,
    PRIVATE_USER_CREATE,
    PRIVATE_USER_DELETE,
    PRIVATE_USER_DETAIL,
    PRIVATE_USER_UPDATE,
    PRIVATE_USERS_LIST,
)
from users_app.exceptions.constants import E400_401_403, E400_401_403_404, E401_403
from users_app.services.users import UserService, get_user_service
from users_app.validation.schemas import (
    PrivateCreateUserModel,
    PrivateDetailUserResponseModel,
    PrivateUpdateUserModel,
    PrivateUsersListResponseModel,
    QueryParams,
)

router = APIRouter(
    prefix=PRIVATE_PREFIX,
    tags=['admin'],
)


@router.get(
    path=PRIVATE_USERS_LIST,
    status_code=HTTPStatus.OK,
    response_model=PrivateUsersListResponseModel,
    summary='Постраничное получение кратких данных обо всех пользователях',
    responses=E400_401_403,
)
async def private_user_list(
    query: QueryParams = Depends(),
    user_service: UserService = Depends(get_user_service),
) -> PrivateUsersListResponseModel:
    '''Shows user's info list with pagination.'''
    users_list = await user_service.get_list_private(query)
    return users_list


@router.post(
    path=PRIVATE_USER_CREATE,
    status_code=HTTPStatus.CREATED,
    response_model=PrivateDetailUserResponseModel,
    summary='Создание пользователя',
    responses=E400_401_403,
)
async def private_user_create(
    data: PrivateCreateUserModel,
    user_service: UserService = Depends(get_user_service),
) -> PrivateDetailUserResponseModel:
    '''Creates a user.'''
    new_user = await user_service.create(data=data)
    return new_user


@router.get(
    path=PRIVATE_USER_DETAIL,
    status_code=HTTPStatus.OK,
    response_model=PrivateDetailUserResponseModel,
    summary='Детальное получение информации о пользователе',
    responses=E400_401_403_404,
)
async def private_user_detail(
    pk: int,
    user_service: UserService = Depends(get_user_service),
) -> PrivateDetailUserResponseModel:
    '''Shows detail info about specific user.'''
    user = await user_service.get_detail(user_id=pk)
    return user


@router.patch(
    path=PRIVATE_USER_UPDATE,
    status_code=HTTPStatus.OK,
    response_model=PrivateDetailUserResponseModel,
    summary='Изменение информации о пользователе',
    responses=E400_401_403_404,
)
async def private_user_update(
    pk: int,
    data: PrivateUpdateUserModel,
    user_service: UserService = Depends(get_user_service),
) -> PrivateDetailUserResponseModel:
    '''Update info about specific user.'''
    updated_user = await user_service.update(user_id=pk, data=data)
    return updated_user


@router.delete(
    path=PRIVATE_USER_DELETE,
    status_code=HTTPStatus.NO_CONTENT,
    summary='Удаление пользователя',
    responses=E401_403,
)
async def private_user_delete(
    pk: int,
    user_service: UserService = Depends(get_user_service),
) -> JSONResponse:
    '''Delete specific user.'''
    return await user_service.delete(user_id=pk)
