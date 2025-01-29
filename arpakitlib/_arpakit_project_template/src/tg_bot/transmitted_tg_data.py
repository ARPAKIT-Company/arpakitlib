from aiogram import Bot

from arpakitlib.ar_aiogram_util import BaseTransmittedTgBotData
from arpakitlib.ar_file_storage_in_dir_util import FileStorageInDir
from arpakitlib.ar_sqlalchemy_util import SQLAlchemyDB
from src.core.settings import Settings


class TransmittedTgData(BaseTransmittedTgBotData):
    settings: Settings
    sqlalchemy_db: SQLAlchemyDB | None = None
    media_file_storage_in_dir: FileStorageInDir | None = None
    cache_file_storage_in_dir: FileStorageInDir | None = None
    dump_file_storage_in_dir: FileStorageInDir | None = None
    tg_bot: Bot

    # ...
