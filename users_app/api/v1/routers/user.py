from fastapi import APIRouter

from users_app.schemas.schemas import (
    CurrentUserResponseModel,
    UpdateUserModel,
    UpdateUserResponseModel,
    UsersListResponseModel,
)


router = APIRouter(
    prefix='/api/v1/users',
    tags=['user'],
)


@router.get(
    path='/',
    response_model=UsersListResponseModel,
    summary='Постраничное получение кратких данных обо всех пользователях',
)
async def user_list():
    '''Shows user's info list with pagination.'''
    pass


@router.get(
    path='/current',
    response_model=CurrentUserResponseModel,
    summary='Получение данных о текущем пользователе',
)
async def user_detail():
    '''Shows info about current logged in user.'''
    pass


@router.patch(
    path='/current',
    summary='Изменение данных пользователя',
    response_model=UpdateUserResponseModel,
)
async def user_update(data: UpdateUserModel) -> UpdateUserResponseModel:
    '''Update info about current logged in user.'''
    pass
