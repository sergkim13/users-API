from http import HTTPStatus

import pytest

# from tests.fixtures.users import test
from users_app.api.v1.routers.constants import (
    LOGIN,
    LOGOUT,
    PRIVATE_USER_CREATE_FULL,
    PRIVATE_USER_DELETE_FULL,
    PRIVATE_USER_DETAIL_FULL,
    PRIVATE_USER_UPDATE_FULL,
    PRIVATE_USERS_LIST_FULL,
    USER_DETAIL_FULL,
    USER_UPDATE_FULL,
    USERS_LIST_FULL,
)
from users_app.exceptions.constants import (
    MSG_INVALID_CREDS,
    MSG_NOT_AUTHENTICATED,
    MSG_NOT_AUTHORIZED,
)


@pytest.mark.asyncio
async def test_post_login(client, fixture_user, user_login_form):
    '''Checks normal response of `login` endpoint.'''
    response = await client.post(LOGIN, json=user_login_form)
    assert response.status_code == HTTPStatus.OK
    assert response.cookies.get('jwt_token')


@pytest.mark.asyncio
async def test_post_login_with_bad_request(client):
    '''Checks `Bad request` response of `login` endpoint with invalid credentials.'''
    response = await client.post(LOGIN, json={'login': 'fake', 'password': 'fake'})
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['message'] == MSG_INVALID_CREDS


@pytest.mark.asyncio
async def test_post_login_with_validation_error(client):
    '''Checks `Validation error` response of `login` endpoint with request without body.'''
    response = await client.post(LOGIN)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json()['detail'][0]['msg'] == 'field required'


@pytest.mark.asyncio
async def test_get_logout(client, fixture_user):
    '''Checks normal response of `logout` endpoint.'''
    response = await client.get(LOGOUT)
    assert response.status_code == HTTPStatus.OK
    assert not response.cookies.get('jwt_token')


@pytest.mark.asyncio
async def test_login_required_routes_without_login(client):
    '''Checks responses of endpoints without authentification.'''
    response_users_list = await client.get(USERS_LIST_FULL)
    response_user_detail = await client.get(USER_DETAIL_FULL)
    response_user_update = await client.patch(USER_UPDATE_FULL)
    response_private_users_list = await client.get(PRIVATE_USERS_LIST_FULL)
    response_private_user_create = await client.post(PRIVATE_USER_CREATE_FULL)
    response_private_user_detail = await client.get(PRIVATE_USER_DETAIL_FULL)
    response_private_user_update = await client.patch(PRIVATE_USER_UPDATE_FULL)
    response_private_user_delete = await client.get(PRIVATE_USER_DELETE_FULL)

    assert response_users_list.status_code == HTTPStatus.UNAUTHORIZED
    assert response_user_detail.status_code == HTTPStatus.UNAUTHORIZED
    assert response_user_update.status_code == HTTPStatus.UNAUTHORIZED
    assert response_private_users_list.status_code == HTTPStatus.UNAUTHORIZED
    assert response_private_user_create.status_code == HTTPStatus.UNAUTHORIZED
    assert response_private_user_detail.status_code == HTTPStatus.UNAUTHORIZED
    assert response_private_user_update.status_code == HTTPStatus.UNAUTHORIZED
    assert response_private_user_delete.status_code == HTTPStatus.UNAUTHORIZED
    assert response_users_list.json()['message'] == MSG_NOT_AUTHENTICATED
    assert response_user_detail.json()['message'] == MSG_NOT_AUTHENTICATED
    assert response_user_update.json()['message'] == MSG_NOT_AUTHENTICATED
    assert response_private_users_list.json()['message'] == MSG_NOT_AUTHENTICATED
    assert response_private_user_create.json()['message'] == MSG_NOT_AUTHENTICATED
    assert response_private_user_detail.json()['message'] == MSG_NOT_AUTHENTICATED
    assert response_private_user_update.json()['message'] == MSG_NOT_AUTHENTICATED
    assert response_private_user_delete.json()['message'] == MSG_NOT_AUTHENTICATED


@pytest.mark.asyncio
async def test_admin_required_routes_with_user(client, fixture_user, user_login_form, query_params):
    '''Checks responses of endpoints with authentification by not admin.'''
    await client.post(LOGIN, json=user_login_form)
    response_users_list = await client.get(USERS_LIST_FULL, params=query_params.dict())
    response_user_detail = await client.get(USER_DETAIL_FULL)
    response_user_update = await client.get(USER_UPDATE_FULL)
    response_private_users_list = await client.get(PRIVATE_USERS_LIST_FULL)
    response_private_user_create = await client.post(PRIVATE_USER_CREATE_FULL)
    response_private_user_detail = await client.get(PRIVATE_USER_DETAIL_FULL)
    response_private_user_update = await client.patch(PRIVATE_USER_UPDATE_FULL)
    response_private_user_delete = await client.get(PRIVATE_USER_DELETE_FULL)

    assert response_users_list.status_code == HTTPStatus.OK
    assert response_user_detail.status_code == HTTPStatus.OK
    assert response_user_update.status_code == HTTPStatus.OK
    assert response_private_users_list.status_code == HTTPStatus.FORBIDDEN
    assert response_private_user_create.status_code == HTTPStatus.FORBIDDEN
    assert response_private_user_detail.status_code == HTTPStatus.FORBIDDEN
    assert response_private_user_update.status_code == HTTPStatus.FORBIDDEN
    assert response_private_user_delete.status_code == HTTPStatus.FORBIDDEN
    assert response_private_users_list.json()['message'] == MSG_NOT_AUTHORIZED
    assert response_private_user_create.json()['message'] == MSG_NOT_AUTHORIZED
    assert response_private_user_detail.json()['message'] == MSG_NOT_AUTHORIZED
    assert response_private_user_update.json()['message'] == MSG_NOT_AUTHORIZED
    assert response_private_user_delete.json()['message'] == MSG_NOT_AUTHORIZED
