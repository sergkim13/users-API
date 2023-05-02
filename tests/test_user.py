from http import HTTPStatus

import pytest

from users_app.api.v1.routers.constants import (
    LOGIN,
    USER_DETAIL_FULL,
    USER_UPDATE_FULL,
    USERS_LIST_FULL,
)
from users_app.validation.schemas import (
    CurrentUserResponseModel,
    UpdateUserResponseModel,
    UsersListResponseModel,
)


@pytest.mark.asyncio
async def test_get_list(client, fixture_user, user_login_form, query_params):
    '''Checksnormal response of `users_list` endpoint.'''
    await client.post(LOGIN, json=user_login_form)
    response = await client.get(USERS_LIST_FULL, params=query_params.dict())
    assert response.status_code == HTTPStatus.OK
    assert UsersListResponseModel.validate(response.json())
    assert len(response.json()['data']) == 1
    assert response.json()['data'][0]['email'] == fixture_user.email
    assert response.json()['data'][0]['first_name'] == fixture_user.first_name
    assert response.json()['data'][0]['last_name'] == fixture_user.last_name
    assert response.json()['meta']['pagination']['total'] == 1
    assert response.json()['meta']['pagination']['page'] == query_params.page
    assert response.json()['meta']['pagination']['size'] == query_params.size


@pytest.mark.asyncio
async def test_get_current(client, fixture_user, user_login_form):
    '''Checksnormal response of `user_current` endpoint.'''
    await client.post(LOGIN, json=user_login_form)
    response = await client.get(USER_DETAIL_FULL)
    assert response.status_code == HTTPStatus.OK
    assert CurrentUserResponseModel.validate(response.json())
    assert response.json()['email'] == fixture_user.email
    assert response.json()['first_name'] == fixture_user.first_name
    assert response.json()['last_name'] == fixture_user.last_name
    assert response.json()['is_admin'] == fixture_user.is_admin
    assert response.json()['other_name'] == ''
    assert response.json()['phone'] == ''
    assert response.json()['birthday'] is None


@pytest.mark.asyncio
async def test_update_current(client, fixture_user, user_login_form):
    '''Checksnormal response of `user_update` endpoint.'''
    await client.post(LOGIN, json=user_login_form)
    response = await client.patch(
        USER_UPDATE_FULL,
        json={
            'email': 'brad_pitt@example.com',
            'other_name': 'braddford'
        }
    )
    assert response.status_code == HTTPStatus.OK
    assert UpdateUserResponseModel.validate(response.json())
    assert response.json()['email'] == 'brad_pitt@example.com'
    assert response.json()['other_name'] == 'braddford'
    assert response.json()['id'] == fixture_user.id
    assert response.json()['first_name'] == fixture_user.first_name
    assert response.json()['last_name'] == fixture_user.last_name
    assert response.json()['phone'] == ''
    assert response.json()['birthday'] is None
