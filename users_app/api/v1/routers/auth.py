from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from users_app.schemas.schemas import (
    CurrentUserResponseModel,
    LoginModel,
    Payload,
)
from users_app.security.cifer import Cifer, get_cifer
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
    cifer: Cifer = Depends(get_cifer),
) -> CurrentUserResponseModel:
    '''Log in to the system.'''

    user = await user_service.authenticate_user(credentials)
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='User not found',
        )
    payload = Payload(user_id=user.id, is_admin=user.is_admin)
    session_token = cifer.encode(payload=payload)
    response.set_cookie(key='jwt_token', value=session_token, expires=3600, httponly=True)
    return user


@router.get(
    path='/logout',
    summary='Выход из системы',
)
async def logout(response: JSONResponse) -> JSONResponse:
    '''Log out of the system.'''
    response.delete_cookie('jwt_token')
    return 'Logged out successfully.'
