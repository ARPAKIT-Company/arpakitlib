import logging

import aiogram
from aiogram import Router

from arpakitlib.ar_exception_util import exception_to_traceback_str
from project.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db
from project.sqlalchemy_db_.sqlalchemy_model import StoryLogDBM
from project.tg_bot.middleware.common import MiddlewareDataTgBot

_logger = logging.getLogger(__name__)

tg_bot_router = Router()


@tg_bot_router.error()
async def _(
        event: aiogram.types.ErrorEvent,
        middleware_data_tg_bot: MiddlewareDataTgBot,
        **kwargs
):
    _logger.exception(event.exception)

    if get_cached_sqlalchemy_db() is not None:
        async with get_cached_sqlalchemy_db().new_async_session() as session:
            story_log_dbm = StoryLogDBM(
                level=StoryLogDBM.Levels.error,
                type=StoryLogDBM.Types.error_in_tg_bot,
                title=f"{type(event.exception)}",
                data={
                    "exception_str": str(event.exception),
                    "exception_traceback_str": exception_to_traceback_str(exception=event.exception)
                }
            )
        session.add(story_log_dbm)
        await session.commit()
        await session.refresh(story_log_dbm)
