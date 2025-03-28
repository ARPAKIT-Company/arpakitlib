import aiogram.filters

from project.tg_bot.blank.client import get_cached_client_tg_bot_blank
from project.tg_bot.const import GeneralTgBotCommands
from project.tg_bot.middleware.common import MiddlewareDataTgBot

tg_bot_router = aiogram.Router()


@tg_bot_router.message(
    aiogram.filters.Command(GeneralTgBotCommands.healthcheck),
)
async def _(
        m: aiogram.types.Message,
        middleware_data_tg_bot: MiddlewareDataTgBot,
        **kwargs
):
    await m.answer(text=get_cached_client_tg_bot_blank().healthcheck())
