from sqlalchemy import func, select
from users_app.database.crud.abstract_crud import AbstractCRUD
from users_app.database.models import User
from users_app.schemas.schemas import PrivateCreateUserModel
from sqlalchemy.ext.asyncio import AsyncSession


class UserCRUD(AbstractCRUD):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def read_all(
        self,
        page: int,
        size: int,
    ):
        users_count = await self._count_all()
        max_pages = (users_count + size - 1) // size
        if page > max_pages:
            return []
        else:
            offset = (page - 1) * size
            query = select(User).order_by(User.id).offset(offset).limit(size)
            result = await self.session.execute(query)
            return result.scalars().all()

    async def _count_all(self):
        query = select(func.count()).select_from(User)
        result = await self.session.execute(query)
        return result.scalar_one()

    async def read_by_login(self, login: str):
        query = select(User).where(User.email == login)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create(self, data: PrivateCreateUserModel):
        new_user = User(**data.dict())
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user

    async def read(self):
        pass

    async def update(self):
        pass

    async def delete(self):
        pass
