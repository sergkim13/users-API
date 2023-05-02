from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from users_app.database.models import User
from users_app.validation.schemas import (
    PrivateCreateUserModel,
    PrivateUpdateUserModel,
    QueryParams,
    UpdateUserModel,
)


class UserCRUD:
    '''`User` class which provides CRUD operations.'''

    def __init__(self, session: AsyncSession) -> None:
        '''Init `UserCRUD` instance with given session.'''
        self.session = session

    async def read_all(self, query: QueryParams) -> list[User | None]:
        '''Read all users with pagination.'''
        offset = (query.page - 1) * query.size
        query = select(User).order_by(User.id).offset(offset).limit(query.size)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def read(self, user_id=int) -> User:
        '''Read specific user by `id` field.'''
        query = select(User).where(User.id == user_id)
        result = await self.session.execute(query)
        return result.scalar_one()

    async def read_by_login(self, login: str):
        '''Read specific user by `email` field.'''
        query = select(User).where(User.email == login)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create(self, data: PrivateCreateUserModel):
        '''Create new user.'''
        new_user = User(**data.dict())
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user

    async def update(self, user: User, data: UpdateUserModel | PrivateUpdateUserModel) -> User:
        '''Update specific user.'''
        values = data.dict(exclude_unset=True)
        stmt = update(User).where(User.id == user.id).values(**values)
        await self.session.execute(stmt)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def delete(self, user_id: int):
        '''Delete specific user.'''
        user = await self.read(user_id)
        await self.session.delete(user)
        await self.session.commit()

    async def count_all(self):
        '''Count all users.'''
        query = select(func.count()).select_from(User)
        result = await self.session.execute(query)
        return result.scalar_one()
