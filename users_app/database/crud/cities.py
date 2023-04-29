from sqlalchemy import select
from users_app.database.crud.abstract_crud import AbstractCRUD
from users_app.database.models import City
from sqlalchemy.ext.asyncio import AsyncSession


class CityCRUD(AbstractCRUD):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def read(self, city_id: int):
        query = select(City).where(City.id == city_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create(self):
        pass

    async def read_all(self):
        pass

    async def update(self):
        pass

    async def delete(self):
        pass
