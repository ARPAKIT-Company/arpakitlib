import logging
from typing import Callable

from src.tg_bot.transmitted_tg_data import get_cached_transmitted_tg_bot_data

_logger = logging.getLogger(__name__)


async def on_startup():
    _logger.info("start")

    if get_cached_transmitted_tg_bot_data().media_file_storage_in_dir is not None:
        get_cached_transmitted_tg_bot_data().media_file_storage_in_dir.init()

    if get_cached_transmitted_tg_bot_data().cache_file_storage_in_dir is not None:
        get_cached_transmitted_tg_bot_data().cache_file_storage_in_dir.init()

    if get_cached_transmitted_tg_bot_data().dump_file_storage_in_dir is not None:
        get_cached_transmitted_tg_bot_data().dump_file_storage_in_dir.init()

    if get_cached_transmitted_tg_bot_data().settings.api_init_sqlalchemy_db:
        get_cached_transmitted_tg_bot_data().sqlalchemy_db.init()

    if get_cached_transmitted_tg_bot_data().settings.api_init_json_db:
        get_cached_transmitted_tg_bot_data().json_db.init()

    _logger.info("finish")


async def on_shutdown(self, *args, **kwargs):
    self._logger.info("on_shutdown start")
    self._logger.info("on_shutdown was done")


def get_tg_bot_events() -> list[Callable]:
    res = []
    res.append(on_startup)
    res.append(TgBotShutdownEvent(transmitted_tg_bot_data=get_cached_transmitted_tg_bot_data()).on_shutdown)
    return res
