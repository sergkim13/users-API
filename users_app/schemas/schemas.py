from datetime import date

from pydantic import BaseModel, validator


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
    birthday: date
    is_admin: bool

    class Config:
        orm_mode = True


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
    birthday: date


# Private detail
class PrivateDetailUserResponseModel(CurrentUserResponseModel):
    id: int
    city: int
    additional_info: str
    password: str

    @validator('city', pre=True)
    def city_default(cls, value):
        if value is None:
            return 0
        return value

    class Config:
        orm_mode = True


# Private list
class CitiesHintModel(BaseModel):
    id: int
    name: str


class PrivateUsersListHintMetaModel(BaseModel):
    city: CitiesHintModel


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
