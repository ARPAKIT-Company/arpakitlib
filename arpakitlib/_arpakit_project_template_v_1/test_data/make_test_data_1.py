import asyncio


def make_test_data_1():
    pass


async def async_make_test_data_1():
    pass


def __example():
    make_test_data_1()


async def __async_example():
    await async_make_test_data_1()


if __name__ == '__main__':
    __example()
    asyncio.run(__async_example())
