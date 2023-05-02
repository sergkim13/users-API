from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from users_app.database.models import City


class CityCRUD:
    '''`City` class which provides CRUD operations.'''
    def __init__(self, session: AsyncSession) -> None:
        '''Init `CityCRUD` instance with given session.'''
        self.session = session

    async def read(self, city_id: int):
        '''Read specific city by `id` field.'''
        query = select(City).where(City.id == city_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
