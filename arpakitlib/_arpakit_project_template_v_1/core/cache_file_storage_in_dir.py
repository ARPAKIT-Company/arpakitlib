from functools import lru_cache

from arpakitlib.ar_file_storage_in_dir_util import FileStorageInDir
from core.settings import get_cached_settings


def create_cache_file_storage_in_dir() -> FileStorageInDir:
    return FileStorageInDir(dirpath=get_cached_settings().cache_dirpath)


@lru_cache()
def get_cached_cache_file_storage_in_dir() -> FileStorageInDir:
    return create_cache_file_storage_in_dir()


def __example():
    print(get_cached_cache_file_storage_in_dir().dirpath)


if __name__ == '__main__':
    __example()
