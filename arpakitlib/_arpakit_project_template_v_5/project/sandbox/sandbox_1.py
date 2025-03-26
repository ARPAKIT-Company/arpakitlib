import asyncio

from project.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db
from project.sqlalchemy_db_.sqlalchemy_model import OperationDBM, StoryLogDBM


def __sandbox():
    with get_cached_sqlalchemy_db().new_session() as s:
        o = StoryLogDBM()
        o.title = "hj;ll    "
        o.level = "info"
        o.extra_data = {}
        print(o.simple_dict_json())


async def __async_sandbox():
    pass


if __name__ == '__main__':
    __sandbox()
    asyncio.run(__async_sandbox())
