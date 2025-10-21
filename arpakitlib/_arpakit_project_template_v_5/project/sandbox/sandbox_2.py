import asyncio

from project.sqlalchemy_db_.sqlalchemy_model import UserDBM


def __sandbox():
    print(UserDBM.get_sd_property_names())


async def __async_sandbox():
    pass


if __name__ == '__main__':
    __sandbox()
    asyncio.run(__async_sandbox())
