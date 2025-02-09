from functools import lru_cache

from src.core.settings import get_cached_settings
from src.json_db.json_db import JSONDb


def create_json_db() -> JSONDb:
    return JSONDb(
        dirpath=get_cached_settings().json_db_dirpath
    )


@lru_cache()
def get_json_db() -> JSONDb:
    return JSONDb(
        dirpath=get_cached_settings().json_db_dirpath
    )
