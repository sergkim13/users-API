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
    prefix="/api/v1/users",
    tags=["user"],
)


@router.get('/')
async def user_list():
    '''Shows user's info list with pagination.'''
    pass


@router.get('/current')
async def user_detail():
    '''Shows info about current logged in user.'''
    pass


@router.patch('/current')
async def user_update():
    '''Update info about current logged in user.'''
    pass
