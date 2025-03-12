import logging

import aiogram.filters
from aiogram.exceptions import AiogramError

from project.tg_bot.blank.client import get_cached_client_tg_bot_blank
from project.tg_bot.filter_.user_roles_has_client import UserRolesHasClientTgBotFilter
from project.tg_bot.middleware.common import MiddlewareDataTgBot

_logger = logging.getLogger(__name__)
tg_bot_router = aiogram.Router()


@tg_bot_router.callback_query(
    UserRolesHasClientTgBotFilter()

)
async def _(
        cq: aiogram.types.CallbackQuery,
        middleware_data_tg_bot: MiddlewareDataTgBot,
        **kwargs
):
    try:
        await cq.answer(
            text=get_cached_client_tg_bot_blank().keyboard_is_old(),
            show_alert=True
        )
    except AiogramError as exception:
        _logger.error(exception)

    try:
        await cq.message.edit_reply_markup(reply_markup=None)
    except AiogramError as e:
        _logger.error(e)
