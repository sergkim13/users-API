import pytest
import pytest_asyncio

from users_app.database.crud.users import UserCRUD
from users_app.validation.schemas import LoginModel, PrivateCreateUserModel, QueryParams


# Fixture query
@pytest.fixture
def query_params():
    return QueryParams(page=1, size=3)


# Fixture user
@pytest.fixture
def user_data():
    return {
        'first_name': 'Brad',
        'last_name': 'Pitt',
        'email': 'pitt@example.com',
        'is_admin': False,
        'password': 'fight_club',
    }


@pytest.fixture
def user_login_form(user_data):
    return LoginModel(login=user_data['email'], password=user_data['password']).dict()


@pytest_asyncio.fixture
async def fixture_user(session, user_data):
    user_crud = UserCRUD(session)
    return await user_crud.create(PrivateCreateUserModel(**user_data))


# Fixture admin
@pytest.fixture
def admin_data():
    return {
        'first_name': 'Tom',
        'last_name': 'Hanks',
        'email': 'hanks@example.com',
        'is_admin': True,
        'password': 'forrest',
    }


@pytest_asyncio.fixture
async def fixture_admin(session, admin_data):
    user_crud = UserCRUD(session)
    return await user_crud.create(PrivateCreateUserModel(**admin_data))
