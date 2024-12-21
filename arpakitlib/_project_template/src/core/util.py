import asyncio
from functools import lru_cache

from arpakitlib.ar_file_storage_in_dir_util import FileStorageInDir
from arpakitlib.ar_logging_util import setup_normal_logging
from src.core.settings import get_cached_settings


def setup_logging():
    setup_normal_logging(log_filepath=get_cached_settings().log_filepath)


def create_cache_file_storage_in_dir() -> FileStorageInDir:
    return FileStorageInDir(dirpath=get_cached_settings().cache_dirpath)


@lru_cache()
def get_cache_file_storage_in_dir() -> FileStorageInDir:
    return create_cache_file_storage_in_dir()


def __example():
    pass


async def __async_example():
    pass


if __name__ == '__main__':
    __example()
    asyncio.run(__async_example())
