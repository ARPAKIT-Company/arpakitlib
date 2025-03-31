import asyncio

from pydantic import BaseModel

from project.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db
from project.sqlalchemy_db_.sqlalchemy_model import ApiKeyDBM


def __sandbox():
    pass


async def __async_sandbox():
    pass


if __name__ == '__main__':
    __sandbox()
    asyncio.run(__async_sandbox())
