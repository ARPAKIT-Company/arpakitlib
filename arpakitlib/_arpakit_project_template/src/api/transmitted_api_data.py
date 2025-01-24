from arpakitlib.ar_fastapi_util import BaseTransmittedAPIData
from arpakitlib.ar_file_storage_in_dir_util import FileStorageInDir
from arpakitlib.ar_sqlalchemy_util import SQLAlchemyDB

from src.core.settings import Settings


class TransmittedAPIData(BaseTransmittedAPIData):
    settings: Settings
    sqlalchemy_db: SQLAlchemyDB | None = None
    media_file_storage_in_dir: FileStorageInDir | None = None
    cache_file_storage_in_dir: FileStorageInDir | None = None
    dump_file_storage_in_dir: FileStorageInDir | None = None

    # ...
