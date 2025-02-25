import aiogram
from aiogram import Router

from tg_bot.transmitted_tg_data import TransmittedTgBotData

tg_bot_router = Router()


@tg_bot_router.error()
async def _(
        event: aiogram.types.ErrorEvent,
        transmitted_tg_bot_data: TransmittedTgBotData,
        **kwargs
):
    pass
