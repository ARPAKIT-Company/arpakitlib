from src.core.settings import get_cached_settings
from src.json_db.json_db import JSONDb


def get_json_db() -> JSONDb:
    return JSONDb(
        dirpath=get_cached_settings().json_db_dirpath
    )
