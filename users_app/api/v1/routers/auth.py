from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from users_app.schemas.schemas import (
    CurrentUserResponseModel,
    ErrorResponseModel,
    LoginModel,
)
from users_app.services.users import UserService, get_user_service

faske_users = [
    {'id': 1, 'username': 'potter', 'password': '112345', 'is_admin': False},
    {'id': 2, 'username': 'weasly', 'password': '12', 'is_admin': False},
    {'id': 3, 'username': 'grandger', 'password': '192', 'is_admin': True},
]

router = APIRouter(
    prefix='/api/v1',
    tags=['auth'],
)


@router.post(
    path='/login',
    response_model=CurrentUserResponseModel,
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


@router.post(path='/logout')
async def logout(response: JSONResponse) -> str:
    '''Log out of the system.'''
    response.delete_cookie('is_logged_in')
    response.delete_cookie('is_admin')
    return 'Logged out successfully.'
