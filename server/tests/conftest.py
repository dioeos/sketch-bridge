import asyncio
from contextlib import ExitStack

import pytest
from fastapi.testclient import TestClient
from pytest_postgresql import factories
from pytest_postgresql.janitor import DatabaseJanitor

from src.main import init_app
from src.database import get_db, sessionmanager

import pytest_asyncio

test_db = factories.postgresql_proc(port=None, dbname="test_db")


@pytest.fixture(autouse=True)
def app():
    with ExitStack():
        yield init_app(init_db=False)


@pytest.fixture
def client(app):
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def connection_test(test_db):
    pg_host = test_db.host
    pg_port = test_db.port
    pg_user = test_db.user
    pg_db = test_db.dbname
    pg_password = test_db.password

    with DatabaseJanitor(
        user=pg_user,
        host=pg_host,
        port=pg_port,
        dbname=pg_db,
        password=pg_password,
        version=test_db.version,
    ):
        connection_str = (
            f"postgresql+psycopg://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}"
        )

        sessionmanager.init(connection_str)
        yield
        await sessionmanager.close()


@pytest.fixture(scope="function", autouse=True)
async def create_tables(connection_test):
    async with sessionmanager.connect() as connection:
        await sessionmanager.drop_all(connection)
        await sessionmanager.create_all(connection)


@pytest.fixture(scope="function", autouse=True)
async def session_override(app, connection_test):
    async def get_db_override():
        async with sessionmanager.session() as session:
            yield session

    app.dependency_overrides[get_db] = get_db_override


@pytest.fixture(scope="session")
def db_manager(connection_test):
    """Pytest fixture that gives initialized sessionmanager"""
    return sessionmanager


@pytest_asyncio.fixture
async def db_connection(db_manager):
    """Low level connection fixture using sessionmanager.connect()"""
    async with db_manager.connect() as conn:
        yield conn


@pytest_asyncio.fixture
async def db_session(db_manager):
    """Async session fixture using sessionmanager.session()"""
    async with db_manager.session() as session:
        yield session
