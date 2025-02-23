from functools import lru_cache

import starlette.requests
from pydantic import BaseModel, ConfigDict

from arpakitlib.ar_file_storage_in_dir_util import FileStorageInDir
from arpakitlib.ar_json_db_util import BaseJSONDb
from arpakitlib.ar_sqlalchemy_util import SQLAlchemyDb
from core.cache_file_storage_in_dir import get_cached_cache_file_storage_in_dir
from core.dump_file_storage_in_dir import get_cached_dump_file_storage_in_dir
from core.media_file_storage_in_dir import get_cached_media_file_storage_in_dir
from core.settings import Settings
from core.settings import get_cached_settings
from json_db.util import get_json_db
from sqlalchemy_db.sqlalchemy_db import get_cached_sqlalchemy_db


class TransmittedAPIData(BaseModel):
    model_config = ConfigDict(extra="ignore", arbitrary_types_allowed=True, from_attributes=True)

    settings: Settings | None = None
    sqlalchemy_db: SQLAlchemyDb | None = None
    json_db: BaseJSONDb | None = None
    media_file_storage_in_dir: FileStorageInDir | None = None
    cache_file_storage_in_dir: FileStorageInDir | None = None
    dump_file_storage_in_dir: FileStorageInDir | None = None


def get_transmitted_api_data(request: starlette.requests.Request) -> TransmittedAPIData:
    return request.app.state.transmitted_api_data


def create_transmitted_api_data() -> TransmittedAPIData:
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

    transmitted_api_data = TransmittedAPIData(
        settings=settings,
        sqlalchemy_db=sqlalchemy_db,
        json_db=json_db,
        media_file_storage_in_dir=media_file_storage_in_dir,
        cache_file_storage_in_dir=cache_file_storage_in_dir,
        dump_file_storage_in_dir=dump_file_storage_in_dir
    )

    return transmitted_api_data


@lru_cache()
def get_cached_transmitted_api_data() -> TransmittedAPIData:
    return create_transmitted_api_data()
