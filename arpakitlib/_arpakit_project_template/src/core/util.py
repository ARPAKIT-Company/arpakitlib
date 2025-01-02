import asyncio
import importlib
from contextlib import suppress
from functools import lru_cache

from arpakitlib.ar_file_storage_in_dir_util import FileStorageInDir
from arpakitlib.ar_logging_util import setup_normal_logging
from arpakitlib.ar_sqlalchemy_util import SQLAlchemyDB
from src.core.settings import get_cached_settings


def setup_logging():
    setup_normal_logging(log_filepath=get_cached_settings().log_filepath)


def create_cache_file_storage_in_dir() -> FileStorageInDir:
    return FileStorageInDir(dirpath=get_cached_settings().cache_dirpath)


@lru_cache()
def get_cached_cache_file_storage_in_dir() -> FileStorageInDir:
    return create_cache_file_storage_in_dir()


def create_media_file_storage_in_dir() -> FileStorageInDir:
    return FileStorageInDir(dirpath=get_cached_settings().media_dirpath)


@lru_cache()
def get_cached_media_file_storage_in_dir() -> FileStorageInDir:
    return create_media_file_storage_in_dir()


def create_dump_file_storage_in_dir() -> FileStorageInDir:
    return FileStorageInDir(dirpath=get_cached_settings().dump_dirpath)


@lru_cache()
def get_cached_dump_file_storage_in_dir() -> FileStorageInDir:
    return create_dump_file_storage_in_dir()


def create_sqlalchemy_db() -> SQLAlchemyDB:
    with suppress(Exception):
        importlib.import_module("src.db.sqlalchemy_model")

    return SQLAlchemyDB(
        db_url=get_cached_settings().sql_db_url,
        db_echo=get_cached_settings().sql_db_echo
    )


@lru_cache()
def get_cached_sqlalchemy_db() -> SQLAlchemyDB:
    return create_sqlalchemy_db()


def __example():
    pass


async def __async_example():
    pass


if __name__ == '__main__':
    __example()
    asyncio.run(__async_example())
