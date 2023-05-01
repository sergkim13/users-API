from http import HTTPStatus

from fastapi import APIRouter, Depends, Request

from users_app.api.v1.routers.constants import (
    USER_DETAIL,
    USER_LIST,
    USER_PREFIX,
    USER_UPDATE,
)
from users_app.exceptions.constants import E400_401, E400_401_404
from users_app.services.auth import AuthService, get_auth_service
from users_app.services.users import UserService, get_user_service
from users_app.validation.schemas import (
    CurrentUserResponseModel,
    QueryParams,
    UpdateUserModel,
    UpdateUserResponseModel,
    UsersListResponseModel,
)

router = APIRouter(
    prefix=USER_PREFIX,
    tags=['user'],
)


@router.get(
    path=USER_LIST,
    status_code=HTTPStatus.OK,
    response_model=UsersListResponseModel,
    summary='Постраничное получение кратких данных обо всех пользователях',
    responses=E400_401,
)
async def users_list(
    query: QueryParams = Depends(),
    user_service: UserService = Depends(get_user_service),
) -> UsersListResponseModel:
    '''Shows user's info list with pagination.'''
    users_list = await user_service.get_list(query)
    return users_list


@router.get(
    path=USER_DETAIL,
    status_code=HTTPStatus.OK,
    response_model=CurrentUserResponseModel,
    summary='Получение данных о текущем пользователе',
    responses=E400_401,
)
async def user_detail(
    request: Request,
    user_service: UserService = Depends(get_user_service),
    auth_service: AuthService = Depends(get_auth_service),
) -> CurrentUserResponseModel:
    '''Shows info about current logged in user.'''
    jwt = await auth_service.check_jwt(request)
    user_id = jwt['user_id']
    return await user_service.get_detail(user_id=user_id)


@router.patch(
    path=USER_UPDATE,
    status_code=HTTPStatus.OK,
    summary='Изменение данных пользователя',
    response_model=UpdateUserResponseModel,
    responses=E400_401_404,
)
async def user_update(
    request: Request,
    data: UpdateUserModel,
    user_service: UserService = Depends(get_user_service),
    auth_service: AuthService = Depends(get_auth_service),
) -> UpdateUserResponseModel:
    '''Update info about current logged in user.'''
    jwt = await auth_service.check_jwt(request)
    user_id = jwt['user_id']
    return await user_service.update(user_id=user_id, data=data)
