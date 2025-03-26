import asyncio

from project.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db
from project.sqlalchemy_db_.sqlalchemy_model import StoryLogDBM


def __sandbox():
    with get_cached_sqlalchemy_db().new_session() as s:
        o = StoryLogDBM()
        o.title = None
        print(o.simple_dict_json())


async def __async_sandbox():
    pass


if __name__ == '__main__':
    __sandbox()
    asyncio.run(__async_sandbox())
