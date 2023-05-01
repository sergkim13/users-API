from http import HTTPStatus
import pytest

from tests.fixtures.users import fake_user
from users_app.api.v1.routers.constants import LOGIN, LOGOUT


@pytest.mark.asyncio
async def test_post_login(client, fixture_user):
    '''Check normal response of `login` endpoint.'''
    response = await client.post(LOGIN, json={'login': fake_user['email'], 'password': fake_user['password']})
    assert response.status_code == HTTPStatus.OK.value
    assert response.cookies.get('jwt_token')


@pytest.mark.asyncio
async def test_post_login_with_bad_request(client):
    '''Check `Bad request` response of `login` endpoint with invalid credentials.'''
    response = await client.post(LOGIN, json={'login': 'test', 'password': 'test'})
    assert response.status_code == HTTPStatus.BAD_REQUEST.value
    assert response.json()['message'] == 'Invalid login or password.'


@pytest.mark.asyncio
async def test_post_login_with_validation_error(client):
    '''Check `Validation error` response of `login` endpoint with request without body.'''
    response = await client.post(LOGIN)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY.value
    assert response.json()['detail'][0]['msg'] == 'field required'


@pytest.mark.asyncio
async def test_get_logout(client, fixture_user):
    '''Check normal response of `logout` endpoint.'''
    response = await client.get(LOGOUT)
    assert response.status_code == HTTPStatus.OK.value
    assert not response.cookies.get('jwt_token')
