import aiogram
from aiogram.fsm.storage.memory import MemoryStorage

from tg_bot.event import add_events_to_tg_bot_dispatcher
from tg_bot.router.main_router import main_tg_bot_router
from tg_bot.transmitted_tg_data import get_cached_transmitted_tg_bot_data


def create_tg_bot_dispatcher() -> aiogram.Dispatcher:
    tg_bot_dispatcher = aiogram.Dispatcher(
        storage=MemoryStorage(),
        transmitted_tg_bot_data=get_cached_transmitted_tg_bot_data()
    )

    add_events_to_tg_bot_dispatcher(tg_bot_dispatcher=tg_bot_dispatcher)

    tg_bot_dispatcher.include_router(router=main_tg_bot_router)

    return tg_bot_dispatcher
