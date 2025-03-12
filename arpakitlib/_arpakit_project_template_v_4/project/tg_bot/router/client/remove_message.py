import logging

from aiogram import Router, types
from aiogram.exceptions import AiogramError

from project.tg_bot.callback.client import RemoveMessageCD
from project.tg_bot.filter_.user_roles_has_client import UserRolesHasClientTgBotFilter
from project.tg_bot.middleware.common import MiddlewareDataTgBot

_logger = logging.getLogger(__name__)
tg_bot_router = Router()


@tg_bot_router.callback_query(
    RemoveMessageCD.filter(),
    UserRolesHasClientTgBotFilter()

)
async def _(
        cq: types.CallbackQuery,
        middleware_data_tg_bot: MiddlewareDataTgBot,
        **kwargs
):
    try:
        await cq.message.delete()
    except AiogramError as exception:
        _logger.error(exception)
        try:
            await cq.answer()
        except AiogramError as exception:
            _logger.error(exception)
