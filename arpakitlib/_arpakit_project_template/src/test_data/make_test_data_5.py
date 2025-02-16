import asyncio


def make_test_data_5():
    pass


async def async_make_test_data_5():
    pass


def __example():
    make_test_data_5()


async def __async_example():
    await async_make_test_data_5()


if __name__ == '__main__':
    __example()
    asyncio.run(__async_example())
