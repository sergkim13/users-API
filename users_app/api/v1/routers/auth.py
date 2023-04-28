from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from users_app.schemas.schemas import (
    CurrentUserResponseModel,
    ErrorResponseModel,
    LoginModel,
)
from users_app.services.users import UserService, get_user_service


router = APIRouter(
    prefix='/api/v1',
    tags=['auth'],
)


@router.post(
    path='/login',
    response_model=CurrentUserResponseModel,
    summary='Вход в систему',
)
async def login(
    credentials: LoginModel,
    response: JSONResponse,
    user_service: UserService = Depends(get_user_service),
) -> CurrentUserResponseModel:
    '''Log in to the system.'''
    user = await user_service.authenticate_user(credentials)
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='User not found',
        )
    response.set_cookie(key='is_logged_in', value='True')
    response.set_cookie(key='is_admin', value=user.is_admin)

    return user


@router.get(
    path='/logout',
    summary='Выход из системы',
)
async def logout(response: JSONResponse) -> JSONResponse:
    '''Log out of the system.'''
    response.delete_cookie('is_logged_in')
    response.delete_cookie('is_admin')
    return 'Logged out successfully.'
