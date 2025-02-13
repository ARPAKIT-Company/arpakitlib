import aiogram
from aiogram.fsm.storage.memory import MemoryStorage

from src.tg_bot.event import get_tg_bot_events
from src.tg_bot.router.main_router import main_tg_bot_router
from src.tg_bot.transmitted_tg_data import get_cached_transmitted_tg_bot_data


def create_tg_bot_dispatcher() -> aiogram.Dispatcher:
    tg_bot_dp = aiogram.Dispatcher(
        storage=MemoryStorage(),
        transmitted_tg_bot_data=get_cached_transmitted_tg_bot_data()
    )

    for tg_bot_event in get_tg_bot_events():
        tg_bot_dp.startup.register(tg_bot_event)

    tg_bot_dp.include_router(router=main_tg_bot_router)

    return tg_bot_dp
