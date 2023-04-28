from http import HTTPStatus
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, Request

faske_users = [
    {'id': 1, 'username': 'potter', 'password': '112345', 'is_admin': False},
    {'id': 2, 'username': 'weasly', 'password': '12', 'is_admin': False},
    {'id': 3, 'username': 'grandger', 'password': '192', 'is_admin': True},
]

router = APIRouter(
    prefix="/api/v1",
    tags=["auth"],
)


class LoginSchema(BaseModel):
    login: str
    password: str


def check_user(creds: LoginSchema) -> dict | str:
    for user in faske_users:
        if user['username'] == creds.login and user['password'] == creds.password:
            return {'is_admin': user['is_admin']}
    return 'Unknown user'


@router.post('/login')
async def login(credentials: LoginSchema):
    '''Log in to the system.'''
    checking_result = check_user(credentials)
    if 'Unknown user' in checking_result:
        return JSONResponse({'message': 'Unknown user'})
    response = JSONResponse({'message': 'Successfully logged in'})
    response.set_cookie(key='is_logged_in', value='True')
    response.set_cookie(key='is_admin', value=checking_result['is_admin'])
    return response


@router.post('/logout')
async def logout():
    '''Log out of the system.'''
    pass
