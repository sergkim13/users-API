from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, HTTPException
from fastapi.responses import JSONResponse

from users_app.schemas.schemas import PrivateCreateUserModel, PrivateDetailUserResponseModel, PrivateUpdateUserModel, PrivateUsersListResponseModel
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
    page: int,
    size: int,
    is_logged_in: Annotated[str | None, Cookie()] = None,
) -> PrivateUsersListResponseModel:
    '''Shows user's info list with pagination.'''
    if not is_logged_in:
        raise HTTPException(status_code=401, detail='Not authenticated')
    return JSONResponse({'is_logged_in': 'Yep'})


@router.post(
    path='/users',
    response_model=PrivateDetailUserResponseModel,
    summary='Создание пользователя',
)
async def private_user_create(
    data: PrivateCreateUserModel,
    user_service: UserService = Depends(get_user_service),
) -> PrivateDetailUserResponseModel:
    '''Creates a user.'''
    new_user = await user_service.create(data)
    return new_user


@router.get(
    path='/users/{pk}',
    response_model=PrivateDetailUserResponseModel,
    summary='Детальное получение информации о пользователе',
)
async def private_user_detail(pk: int) -> PrivateDetailUserResponseModel:
    '''Shows detail info about specific user.'''
    pass


@router.patch(
    path='/users/{pk}',
    response_model=PrivateDetailUserResponseModel,
    summary='Изменение информации о пользователе',
)
async def private_user_update(
    pk: int,
    data: PrivateUpdateUserModel,
) -> PrivateDetailUserResponseModel:
    '''Update info about specific user.'''
    pass


@router.delete(
    path='/users/{pk}',
    summary='Удаление пользователя',
)
async def private_user_delete(pk: int) -> JSONResponse:
    '''Delete specific user.'''
    pass
