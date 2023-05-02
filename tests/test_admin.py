from http import HTTPStatus

import pytest

from users_app.api.v1.routers.constants import (
    LOGIN,
    PRIVATE_USER_CREATE_FULL,
    PRIVATE_USER_DELETE_FULL,
    PRIVATE_USER_DETAIL_FULL,
    PRIVATE_USER_UPDATE_FULL,
    PRIVATE_USERS_LIST_FULL,
)
from users_app.validation.schemas import (
    PrivateDetailUserResponseModel,
    PrivateUsersListResponseModel,
)


@pytest.mark.asyncio
async def test_get_list_private(client, fixture_admin, admin_login_form, query_params):
    '''Checksnormal response of `users_list_private` endpoint.'''
    await client.post(LOGIN, json=admin_login_form)
    response = await client.get(PRIVATE_USERS_LIST_FULL, params=query_params.dict())
    assert response.status_code == HTTPStatus.OK
    assert PrivateUsersListResponseModel.validate(response.json())
    assert len(response.json()['data']) == 1
    assert response.json()['data'][0]['email'] == fixture_admin.email
    assert response.json()['data'][0]['first_name'] == fixture_admin.first_name
    assert response.json()['data'][0]['last_name'] == fixture_admin.last_name
    assert response.json()['meta']['pagination']['total'] == 1
    assert response.json()['meta']['pagination']['page'] == query_params.page
    assert response.json()['meta']['pagination']['size'] == query_params.size


@pytest.mark.asyncio
async def test_create_private(client, fixture_admin, admin_login_form, user_data):
    '''Checksnormal response of `user_create_private` endpoint.'''
    await client.post(LOGIN, json=admin_login_form)
    response = await client.post(PRIVATE_USER_CREATE_FULL, json=user_data)
    assert response.status_code == HTTPStatus.CREATED
    assert PrivateDetailUserResponseModel.validate(response.json())
    assert response.json()['id']
    assert response.json()['first_name'] == user_data['first_name']
    assert response.json()['last_name'] == user_data['last_name']
    assert response.json()['other_name'] == ''
    assert response.json()['email'] == user_data['email']
    assert response.json()['phone'] == ''
    assert response.json()['birthday'] is None
    assert response.json()['city'] == 0
    assert response.json()['additional_info'] == ''
    assert response.json()['is_admin'] == user_data['is_admin']


@pytest.mark.asyncio
async def test_get_detail_private(client, fixture_admin, admin_login_form, fixture_user):
    '''Checksnormal response of `user_deatail_private` endpoint.'''
    await client.post(LOGIN, json=admin_login_form)
    response = await client.get(PRIVATE_USER_DETAIL_FULL.format(pk=fixture_user.id))
    assert response.status_code == HTTPStatus.OK
    assert PrivateDetailUserResponseModel.validate(response.json())
    assert response.json()['id'] == fixture_user.id
    assert response.json()['first_name'] == fixture_user.first_name
    assert response.json()['last_name'] == fixture_user.last_name
    assert response.json()['other_name'] == ''
    assert response.json()['email'] == fixture_user.email
    assert response.json()['phone'] == ''
    assert response.json()['birthday'] is None
    assert response.json()['city'] == 0
    assert response.json()['additional_info'] == ''
    assert response.json()['is_admin'] == fixture_user.is_admin


@pytest.mark.asyncio
async def test_update_private(client, fixture_admin, admin_login_form, fixture_user):
    '''Checksnormal response of `user_update_private` endpoint.'''
    await client.post(LOGIN, json=admin_login_form)
    response = await client.patch(
        PRIVATE_USER_UPDATE_FULL.format(pk=fixture_user.id),
        json={
            'id': fixture_user.id,
            'email': 'brad_pitt@example.com',
            'other_name': 'braddford',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert PrivateDetailUserResponseModel.validate(response.json())
    assert response.json()['email'] == 'brad_pitt@example.com'
    assert response.json()['other_name'] == 'braddford'
    assert response.json()['id'] == fixture_user.id
    assert response.json()['first_name'] == fixture_user.first_name
    assert response.json()['last_name'] == fixture_user.last_name
    assert response.json()['phone'] == ''
    assert response.json()['birthday'] is None
    assert response.json()['city'] == 0
    assert response.json()['additional_info'] == ''
    assert response.json()['is_admin'] == fixture_user.is_admin


@pytest.mark.asyncio
async def test_delete_private(client, fixture_admin, admin_login_form, fixture_user):
    '''Checksnormal response of `user_delete_private` endpoint.'''
    await client.post(LOGIN, json=admin_login_form)
    response = await client.delete(PRIVATE_USER_DELETE_FULL.format(pk=fixture_user.id))
    check_existance = await client.get(PRIVATE_USER_DETAIL_FULL.format(pk=fixture_user.id))
    assert response.status_code == HTTPStatus.NO_CONTENT
    assert check_existance.status_code == HTTPStatus.NOT_FOUND
