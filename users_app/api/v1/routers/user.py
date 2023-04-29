from fastapi import APIRouter, Depends

from users_app.schemas.schemas import (
    CurrentUserResponseModel,
    Payload,
    QueryParams,
    UpdateUserModel,
    UpdateUserResponseModel,
    UsersListResponseModel,
)
from users_app.services.helper import get_jwt
from users_app.services.users import UserService, get_user_service


router = APIRouter(
    prefix='/api/v1/users',
    tags=['user'],
)



@router.get(
    path='/',
    response_model=UsersListResponseModel,
    summary='Постраничное получение кратких данных обо всех пользователях',
)
async def user_list(
    query: QueryParams = Depends(),
    user_service: UserService = Depends(get_user_service),
    jwt: Payload = Depends(get_jwt),
) -> UsersListResponseModel:
    '''Shows user's info list with pagination.'''
    users_list = await user_service.get_list(query)
    return users_list


@router.get(
    path='/current',
    response_model=CurrentUserResponseModel,
    summary='Получение данных о текущем пользователе',
)
async def user_detail(
    user_service: UserService = Depends(get_user_service),
    jwt: Payload = Depends(get_jwt),
) -> CurrentUserResponseModel:
    '''Shows info about current logged in user.'''
    user_id = jwt['user_id']
    return await user_service.get_detail(user_id=user_id)


@router.patch(
    path='/current',
    summary='Изменение данных пользователя',
    response_model=UpdateUserResponseModel,
)
async def user_update(
    data: UpdateUserModel,
    user_service: UserService = Depends(get_user_service),
    jwt: Payload = Depends(get_jwt),
) -> UpdateUserResponseModel:
    '''Update info about current logged in user.'''
    user_id = jwt['user_id']
    return await user_service.update(user_id=user_id, data=data)
