import aiogram.filters

from project.tg_bot.blank.client import get_cached_client_tg_bot_blank
from project.tg_bot.const import ClientTgBotCommands
from project.tg_bot.middleware.common import TgBotMiddlewareData

tg_bot_router = aiogram.Router()


@tg_bot_router.message(aiogram.filters.Command(ClientTgBotCommands.healthcheck))
async def _(
        m: aiogram.types.Message,
        tg_bot_middleware_data: TgBotMiddlewareData,
        **kwargs
):
    await m.answer(text=get_cached_client_tg_bot_blank().healthcheck())
