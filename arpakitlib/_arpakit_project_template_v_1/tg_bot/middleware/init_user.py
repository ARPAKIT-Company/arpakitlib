import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from tg_bot.transmitted_tg_data import TransmittedTgBotData

_logger = logging.getLogger(__name__)


class InitUserTgBotMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        _logger.info("start")
        transmitted_tg_bot_data: TransmittedTgBotData = data["transmitted_tg_bot_data"]
        # ...
        _logger.info("finish")
        return await handler(event, data)
