import logging

import aiogram
from aiogram import Router

_logger = logging.getLogger(__name__)

tg_bot_router = Router()


@tg_bot_router.error()
async def _(
        event: aiogram.types.ErrorEvent,
        **kwargs
):
    _logger.exception(event.exception)
