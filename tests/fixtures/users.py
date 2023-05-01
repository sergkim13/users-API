import pytest_asyncio

from users_app.database.crud.users import UserCRUD
from users_app.validation.schemas import PrivateCreateUserModel

fake_user = {
    'first_name': 'Brad',
    'last_name': 'Pitt',
    'email': 'pitt@example.com',
    'is_admin': True,
    'password': 'fight_club',
}


@pytest_asyncio.fixture
async def fixture_user(session):
    user_crud = UserCRUD(session)
    return await user_crud.create(PrivateCreateUserModel(**fake_user))
