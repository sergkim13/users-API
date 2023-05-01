import asyncio

import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy_utils import create_database, database_exists

from config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME
from users_app.cache.settings import redis_client
from users_app.database.crud.users import UserCRUD
from users_app.database.settings import get_session
from users_app.database.models import Base
from users_app.main import app


pytest_plugins = [
    'tests.fixtures.users',
]

# Test database fixtures
SQLALCHEMY_TEST_DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/test_{DB_NAME}"


# Test database fixtures
@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def db_engine():
    engine = create_async_engine(SQLALCHEMY_TEST_DATABASE_URL)

    if not database_exists:
        create_database(engine.url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield engine


@pytest_asyncio.fixture(scope="function")
async def session(db_engine):
    connection = await db_engine.connect()
    transaction = await connection.begin()
    session = AsyncSession(bind=connection)

    yield session

    await transaction.rollback()
    await connection.close()


@pytest_asyncio.fixture(scope="function")
async def client(session):
    app.dependency_overrides[get_session] = lambda: session

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


# CRUD fixtures





# @pytest_asyncio.fixture
# async def fixture_submenu(db, fixture_menu):
#     submenu_crud = SubmenuCRUD(db)
#     menu = fixture_menu
#     submenu = await submenu_crud.create(
#         menu.id,
#         scheme.SubmenuCreate(**new_submenu),
#     )
#     return menu.id, await submenu_crud.read(menu.id, submenu.id)


# @pytest_asyncio.fixture
# async def fixture_dish(db, fixture_menu, fixture_submenu):
#     dish_crud = DishCRUD(db)
#     menu = fixture_menu
#     submenu = fixture_submenu[1]
#     dish = await dish_crud.create(submenu.id, scheme.DishCreate(**new_dish))
#     return menu.id, submenu.id, await dish_crud.read(menu.id, submenu.id, dish.id)


# Auto clearing cache fixture
@pytest_asyncio.fixture(scope="function", autouse=True)
async def clear_cache():
    await redis_client.flushdb()
