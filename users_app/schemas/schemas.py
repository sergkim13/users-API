from datetime import date
from fastapi import Cookie, Query

from pydantic import BaseModel, root_validator, validator


# Auth
class LoginModel(BaseModel):
    login: str
    password: str


# User detail
class CurrentUserResponseModel(BaseModel):
    first_name: str
    last_name: str
    other_name: str
    email: str
    phone: str
    birthday: date | None
    is_admin: bool

    class Config:
        orm_mode = True

    @root_validator(pre=True)
    def set_default(cls, values):
        new_values = dict(values)
        if not new_values.get('other_name'):
            new_values['other_name'] = ''
        if not new_values.get('phone'):
            new_values['phone'] = ''
        return new_values


# User list
class PaginatedMetaDataModel(BaseModel):
    total: int
    page: int
    size: int


class UsersListElementModel(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str

    class Config:
        orm_mode = True


class UsersListMetaDataModel(BaseModel):
    pagination: PaginatedMetaDataModel


class UsersListResponseModel(BaseModel):
    data: list[UsersListElementModel]
    meta: UsersListMetaDataModel


# User update
class UpdateUserModel(BaseModel):
    first_name: str | None
    last_name: str | None
    other_name: str | None
    email: str | None
    phone: str | None
    birthday: date | None


class UpdateUserResponseModel(BaseModel):
    id: int
    first_name: str
    last_name: str
    other_name: str
    email: str
    phone: str
    birthday: date | None

    @root_validator(pre=True)
    def set_default(cls, values):
        new_values = dict(values)
        if not new_values.get('other_name'):
            new_values['other_name'] = ''
        if not new_values.get('phone'):
            new_values['phone'] = ''
        return new_values

    class Config:
        orm_mode = True


# Private detail
class PrivateDetailUserResponseModel(CurrentUserResponseModel):
    id: int
    city: int
    additional_info: str

    @root_validator(pre=True)
    def set_defaults(cls, values):
        new_values = dict(values)
        if not new_values.get('city'):
            new_values['city'] = 0
        if not new_values.get('additional_info'):
            new_values['additional_info'] = ''
        return new_values

    class Config:
        orm_mode = True


# Private list
class CitiesHintModel(BaseModel):
    id: int
    name: str


class PrivateUsersListHintMetaModel(BaseModel):
    city: list[CitiesHintModel | None]


class PrivateUsersListMetaDataModel(UsersListMetaDataModel):
    hint: PrivateUsersListHintMetaModel


class PrivateUsersListResponseModel(UsersListResponseModel):
    meta: PrivateUsersListMetaDataModel


# Private create
class PrivateCreateUserModel(BaseModel):
    first_name: str
    last_name: str
    other_name: str | None
    email: str
    phone: str | None
    birthday: date | None
    city: int | None
    additional_info: str | None
    is_admin: bool
    password: str

    class Config:
        orm_mode = True


# Private update
class PrivateUpdateUserModel(UpdateUserModel):
    id: int
    city: int | None
    additional_info: str | None
    is_admin: bool | None


# Errors
class CodelessErrorResponseModel(BaseModel):
    message: str


class ErrorResponseModel(CodelessErrorResponseModel):
    code: str


# Query
class QueryParams(BaseModel):
    page: int = Query(ge=1)
    size: int = Query(ge=1)


# Security
class Payload(BaseModel):
    user_id: int
    is_admin: bool
