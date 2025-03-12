import asyncio


def __sandbox():
    a = {1, 2, 3}
    a += [1, 2]
    print(a)


async def __async_sandbox():
    pass


if __name__ == '__main__':
    __sandbox()
    asyncio.run(__async_sandbox())
