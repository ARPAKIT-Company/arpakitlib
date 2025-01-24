import asyncio


def _sandbox():
    pass


async def _async_sandbox():
    pass


if __name__ == '__main__':
    _sandbox()
    asyncio.run(_async_sandbox())
