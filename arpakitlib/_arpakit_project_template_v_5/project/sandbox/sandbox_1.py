import asyncio

import sqlalchemy

from project.sqlalchemy_db_.sqlalchemy_model import SimpleDBM


def __sandbox():
    a = sqlalchemy.inspect(SimpleDBM)
    print(a)


async def __async_sandbox():
    pass


if __name__ == '__main__':
    __sandbox()
    asyncio.run(__async_sandbox())
