import asyncio


def __sandbox():
    all_realization_term_ids = [1,2,3,4]
    chunk_size = 3
    chunked_list = [
        all_realization_term_ids[i:i + chunk_size]
        for i in range(0, len(all_realization_term_ids), chunk_size)
    ]
    print(chunked_list)


async def __async_sandbox():
    pass


if __name__ == '__main__':
    __sandbox()
    asyncio.run(__async_sandbox())
