from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, HTTPException
from fastapi.responses import JSONResponse

from users_app.schemas.schemas import PrivateCreateUserModel, PrivateDetailUserResponseModel
from users_app.services.users import UserService, get_user_service

faske_users = [
    {'id': 1, 'username': 'potter', 'password': '112345', 'is_admin': False},
    {'id': 2, 'username': 'weasly', 'password': '12', 'is_admin': False},
    {'id': 3, 'username': 'grandger', 'password': '192', 'is_admin': True},
]

router = APIRouter(
    prefix='/api/v1/private',
    tags=['admin'],
)


@router.get('/users')
async def private_user_list(is_logged_in: Annotated[str | None, Cookie()] = None):
    '''Shows user's info list with pagination.'''
    if not is_logged_in:
        raise HTTPException(status_code=401, detail='Not authenticated')
    return JSONResponse({'is_logged_in': 'Yep'})


@router.post(
    path='/users',
    response_model=PrivateDetailUserResponseModel,
)
async def private_user_create(
    user_data: PrivateCreateUserModel,
    user_service: UserService = Depends(get_user_service),
) -> PrivateDetailUserResponseModel:
    '''Creates a user.'''
    new_user = await user_service.create(user_data)
    return new_user


@router.get('/users/{pk}')
async def private_user_detail():
    '''Shows detail info about specific user.'''
    pass


@router.patch('/users/{pk}')
async def private_user_update():
    '''Update info about specific user.'''
    pass


@router.delete('/users/{pk}')
async def private_user_delete():
    '''Delete specific user.'''
    pass
