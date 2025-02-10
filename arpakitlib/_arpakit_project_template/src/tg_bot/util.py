from functools import lru_cache

from src.core.settings import get_cached_settings
from src.core.util import get_cached_media_file_storage_in_dir, get_cached_cache_file_storage_in_dir, \
    get_cached_dump_file_storage_in_dir
from src.json_db.util import get_json_db
from src.sqlalchemy_db.util import get_cached_sqlalchemy_db
from src.tg_bot.transmitted_tg_data import TransmittedTgData


def create_transmitted_tg_bot_data() -> TransmittedTgData:
    settings = get_cached_settings()

    sqlalchemy_db = get_cached_sqlalchemy_db() if settings.sqlalchemy_sync_db_url is not None else None

    json_db = get_json_db() if settings.json_db_dirpath is not None else None

    media_file_storage_in_dir = (
        get_cached_media_file_storage_in_dir() if settings.media_dirpath is not None else None
    )

    cache_file_storage_in_dir = (
        get_cached_cache_file_storage_in_dir() if settings.cache_dirpath is not None else None
    )

    dump_file_storage_in_dir = (
        get_cached_dump_file_storage_in_dir() if settings.dump_dirpath is not None else None
    )

    transmitted_api_data = TransmittedTgData(
        sqlalchemy_db=sqlalchemy_db,
        json_db=json_db,
        media_file_storage_in_dir=media_file_storage_in_dir,
        cache_file_storage_in_dir=cache_file_storage_in_dir,
        dump_file_storage_in_dir=dump_file_storage_in_dir,
        settings=settings
    )

    return transmitted_api_data


@lru_cache()
def get_transmitted_tg_bot_data() -> TransmittedTgData:
    return create_transmitted_tg_bot_data()
