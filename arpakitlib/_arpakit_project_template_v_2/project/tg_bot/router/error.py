import aiogram
from aiogram import Router

tg_bot_router = Router()


@tg_bot_router.error()
async def _(
        event: aiogram.types.ErrorEvent,
        **kwargs
):
    pass
