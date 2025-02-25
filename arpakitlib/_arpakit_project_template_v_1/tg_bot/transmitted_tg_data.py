from functools import lru_cache

from pydantic import BaseModel

from arpakitlib.ar_file_storage_in_dir_util import FileStorageInDir
from arpakitlib.ar_json_db_util import BaseJSONDb
from arpakitlib.ar_sqlalchemy_util import SQLAlchemyDb
from core.cache_file_storage_in_dir import get_cached_cache_file_storage_in_dir
from core.dump_file_storage_in_dir import get_cached_dump_file_storage_in_dir
from core.media_file_storage_in_dir import get_cached_media_file_storage_in_dir
from core.settings import Settings, get_cached_settings
from json_db.json_db import get_cached_json_db
from sqlalchemy_db.sqlalchemy_db import get_cached_sqlalchemy_db


class TransmittedTgBotData(BaseModel):
    settings: Settings | None = None
    sqlalchemy_db: SQLAlchemyDb | None = None
    json_db: BaseJSONDb | None = None
    media_file_storage_in_dir: FileStorageInDir | None = None
    cache_file_storage_in_dir: FileStorageInDir | None = None
    dump_file_storage_in_dir: FileStorageInDir | None = None


def create_transmitted_tg_bot_data() -> TransmittedTgBotData:
    settings = get_cached_settings()

    sqlalchemy_db = get_cached_sqlalchemy_db() if settings.sqlalchemy_sync_db_url is not None else None

    json_db = get_cached_json_db() if settings.json_db_dirpath is not None else None

    media_file_storage_in_dir = (
        get_cached_media_file_storage_in_dir() if settings.media_dirpath is not None else None
    )

    cache_file_storage_in_dir = (
        get_cached_cache_file_storage_in_dir() if settings.cache_dirpath is not None else None
    )

    dump_file_storage_in_dir = (
        get_cached_dump_file_storage_in_dir() if settings.dump_dirpath is not None else None
    )

    transmitted_api_data = TransmittedTgBotData(
        settings=settings,
        sqlalchemy_db=sqlalchemy_db,
        json_db=json_db,
        media_file_storage_in_dir=media_file_storage_in_dir,
        cache_file_storage_in_dir=cache_file_storage_in_dir,
        dump_file_storage_in_dir=dump_file_storage_in_dir,
    )

    return transmitted_api_data


@lru_cache()
def get_cached_transmitted_tg_bot_data() -> TransmittedTgBotData:
    return create_transmitted_tg_bot_data()
