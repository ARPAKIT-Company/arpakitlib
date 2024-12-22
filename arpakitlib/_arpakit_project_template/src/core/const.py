import asyncio
import os
import pathlib

BASE_DIRPATH: str = str(pathlib.Path(__file__).parent.parent.parent)

ENV_FILENAME: str = ".env"

ENV_FILEPATH: str = os.path.join(BASE_DIRPATH, ENV_FILENAME)

SRC_DIRNAME: str = "src"

SRC_DIRPATH: str = os.path.join(BASE_DIRPATH, SRC_DIRNAME)

MANAGE_DIRNAME: str = "manage"

MANAGE_DIRPATH: str = os.path.join(BASE_DIRPATH, MANAGE_DIRNAME)

RESOURCE_DIRNAME: str = "resource"

RESOURCE_DIRPATH: str = os.path.join(BASE_DIRPATH, RESOURCE_DIRNAME)

STATIC_DIRNAME: str = "static"

STATIC_DIRPATH: str = os.path.join(RESOURCE_DIRPATH, STATIC_DIRNAME)


def __example():
    print(f"BASE_DIRPATH: {BASE_DIRPATH}")
    print(f"ENV_FILENAME: {ENV_FILENAME}")
    print(f"ENV_FILEPATH: {ENV_FILEPATH}")
    print(f"SRC_DIRNAME: {SRC_DIRNAME}")
    print(f"SRC_DIRPATH: {SRC_DIRPATH}")
    print(f"MANAGE_DIRNAME: {MANAGE_DIRNAME}")
    print(f"MANAGE_DIRPATH: {MANAGE_DIRPATH}")
    print(f"RESOURCE_DIRNAME: {RESOURCE_DIRNAME}")
    print(f"RESOURCE_DIRPATH: {RESOURCE_DIRPATH}")
    print(f"STATIC_DIRNAME: {STATIC_DIRNAME}")
    print(f"STATIC_DIRPATH: {STATIC_DIRPATH}")


async def __async_example():
    pass


if __name__ == '__main__':
    __example()
    asyncio.run(__async_example())
