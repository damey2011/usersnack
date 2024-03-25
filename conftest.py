import asyncio
from asyncio import AbstractEventLoop
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from aerich import Command
from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient
from tortoise import Tortoise, connections

from fixture_utils import load_fixtures
from main import app as _app
from settings import TORTOISE_ORM


async def _delete_tables() -> None:
    # Remove all tables, so existing migration files are able to recreate the tables
    connection = connections.get("default")
    for _, value in Tortoise.apps.get("models").items():
        await connection.execute_query(
            f"DROP TABLE \"{value.describe()['table']}\" CASCADE;"
        )


async def _run_migrations() -> None:
    command = Command(tortoise_config=TORTOISE_ORM, app="models")
    await command.init()
    await command.upgrade(True)


@asynccontextmanager
async def _tortoise_init() -> AsyncGenerator[None, None]:
    await Tortoise.init(TORTOISE_ORM)
    yield
    await Tortoise.close_connections()


@pytest_asyncio.fixture()
async def setup_db() -> AsyncGenerator[None, None]:
    async with _tortoise_init():
        await _delete_tables()
        await _run_migrations()
        yield


@pytest_asyncio.fixture()
async def reset_db(setup_db) -> AsyncGenerator[None, None]:
    delete_coroutines = []

    for key, Model in Tortoise.apps.get("models").items():
        if key.lower() != "aerich":
            delete_coroutines.append(Model.all().delete())

    # Clear the DB and reload fixtures
    await asyncio.gather(*delete_coroutines)
    await load_fixtures()

    yield


@pytest_asyncio.fixture()
async def client(reset_db) -> AsyncGenerator[AsyncClient, None]:
    async with LifespanManager(_app) as manager:
        async with AsyncClient(
            transport=ASGITransport(app=manager.app), base_url="http://test"
        ) as _client:
            yield _client
