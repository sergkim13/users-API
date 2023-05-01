from http import HTTPStatus

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from users_app.api.v1.routers.constants import LOGIN, LOGOUT
from users_app.exceptions.constants import E400
from users_app.services.auth import AuthService, get_auth_service
from users_app.validation.schemas import CurrentUserResponseModel, LoginModel, Payload

router = APIRouter(
    prefix='',
    tags=['auth'],
)


@router.post(
    path=LOGIN,
    status_code=HTTPStatus.OK,
    response_model=CurrentUserResponseModel,
    summary='Вход в систему',
    responses=E400,
)
async def login(
    credentials: LoginModel,
    response: JSONResponse,
    auth_service: AuthService = Depends(get_auth_service),
) -> CurrentUserResponseModel:
    '''Log in to the system.'''

    user = await auth_service.authenticate_user(credentials)
    payload = Payload(user_id=user.id, is_admin=user.is_admin)
    session_token = await auth_service.encode_token(payload=payload)
    response.set_cookie(key='jwt_token', value=session_token, expires=3600, httponly=True)
    return user


@router.get(
    path=LOGOUT,
    status_code=HTTPStatus.OK,
    summary='Выход из системы',
)
async def logout(response: JSONResponse) -> JSONResponse:
    '''Log out of the system.'''
    response.delete_cookie('jwt_token')
    return 'Logged out successfully.'
