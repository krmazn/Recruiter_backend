from typing import AsyncGenerator

import pytest
from fastapi_pagination import add_pagination
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession, AsyncTransaction

from app.api.deps import get_async_session
from app.db import async_session_factory, engine
from app.main import app


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(scope="session")
async def connection(anyio_backend: str) -> AsyncGenerator[AsyncConnection, None]:  # noqa
    async with engine.connect() as connection:
        yield connection


@pytest.fixture()
async def transaction(
    connection: AsyncConnection,
) -> AsyncGenerator[AsyncTransaction, None]:
    async with connection.begin() as transaction:
        yield transaction


@pytest.fixture(scope="session")
async def persistent_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session


@pytest.fixture()
async def session(
    connection: AsyncConnection, transaction: AsyncTransaction
) -> AsyncGenerator[AsyncSession, None]:
    """
    Фикстура с сессией SQLAlchemy, которая откатывает все внесённые изменения
    после выхода из функции-теста
    """
    async_session = AsyncSession(
        bind=connection,
        join_transaction_mode="create_savepoint",
        expire_on_commit=False,
    )

    yield async_session

    await transaction.rollback()


@pytest.fixture()
async def client(
    connection: AsyncConnection, transaction: AsyncTransaction
) -> AsyncGenerator[AsyncClient, None]:
    """
    Клиент для тестирования API.
    Переопределено получение сессии SQLAlchemy для того, чтобы откатывать
    изменения в БД после каждой функции теста.
    """

    async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
        async_session = AsyncSession(
            bind=connection,
            join_transaction_mode="create_savepoint",
            expire_on_commit=False,
        )
        async with async_session:
            yield async_session

    app.dependency_overrides[get_async_session] = override_get_async_session
    add_pagination(app)
    yield AsyncClient(app=app, base_url="http://test")
    del app.dependency_overrides[get_async_session]

    await transaction.rollback()
