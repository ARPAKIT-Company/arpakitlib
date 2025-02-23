import logging
from typing import Callable

from aiogram import Dispatcher

from tg_bot.transmitted_tg_data import get_cached_transmitted_tg_bot_data

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


async def on_shutdown(*args, **kwargs):
    _logger.info("start")
    _logger.info("finish")


def get_tg_bot_startup_events() -> list[Callable]:
    res = [on_startup]
    return res


def get_tg_bot_shutdown_events() -> list[Callable]:
    res = [on_shutdown]
    return res


def add_events_to_tg_bot_dispatcher(*, tg_bot_dispatcher: Dispatcher):
    for tg_bot_event in get_tg_bot_startup_events():
        tg_bot_dispatcher.startup.register(tg_bot_event)
    for tg_bot_event in get_tg_bot_shutdown_events():
        tg_bot_dispatcher.shutdown.register(tg_bot_event)
