from contextlib import contextmanager
from datetime import datetime

import factory
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import event, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from testcontainers.postgres import PostgresContainer

from simple_todo.app import app
from simple_todo.database import get_session
from simple_todo.models import Category, Status, Todo, User, table_registry
from simple_todo.security import get_password_hash
from simple_todo.seeds import CATALOG_CATEGORIES, CATALOG_STATUSES
from simple_todo.settings import Settings


@pytest.fixture(scope='session')
def engine():
    with PostgresContainer('postgres:16', driver='psycopg') as postgres:
        _engine = create_async_engine(postgres.get_connection_url())

        yield _engine


@pytest.fixture
def client(session):
    def get_session_override():
        yield session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def session(engine):
    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        # Cadastros globais são dados de referência: sempre presentes.
        session.add_all(Status(**row) for row in CATALOG_STATUSES)
        session.add_all(Category(**row) for row in CATALOG_CATEGORIES)
        await session.commit()

        yield session

    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.drop_all)


@pytest_asyncio.fixture
async def status(session):
    """Status default do seed ('nao_iniciada')."""
    return await session.scalar(
        select(Status).where(Status.code == 'nao_iniciada')
    )


@pytest_asyncio.fixture
async def category(session):
    """Categoria de exemplo do seed ('feature')."""
    return await session.scalar(
        select(Category).where(Category.code == 'feature')
    )


@contextmanager
def _mock_db_time(*, model, time=datetime(2025, 5, 20)):
    def fake_time_hook(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time
        if hasattr(target, 'updated_at'):
            target.updated_at = time

    event.listen(model, 'before_insert', fake_time_hook)

    yield time

    event.remove(model, 'before_insert', fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@pytest_asyncio.fixture
async def user(session):
    password = 'test'

    user = UserFactory(password=get_password_hash(password))

    session.add(user)
    await session.commit()
    await session.refresh(user)

    user.clean_password = password

    return user


@pytest_asyncio.fixture
async def other_user(session):
    password = 'test'

    user = UserFactory(password=get_password_hash(password))

    session.add(user)
    await session.commit()
    await session.refresh(user)

    user.clean_password = password

    return user


@pytest.fixture
def token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    return response.json()['access_token']


@pytest.fixture
def settings():
    return Settings()


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'test{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')


class TodoFactory(factory.Factory):
    class Meta:
        model = Todo

    title = factory.Faker('text')
    description = factory.Faker('text')
    # 1 == 'nao_iniciada' (primeiro item do seed inserido no fixture session).
    status_id = 1
    user_id = 1
