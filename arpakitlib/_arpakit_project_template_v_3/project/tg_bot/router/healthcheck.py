import aiogram.filters

from project.tg_bot.blank.blank import get_cached_tg_bot_blank
from project.tg_bot.const import TgBotCommands

tg_bot_router = aiogram.Router()


@tg_bot_router.message(aiogram.filters.Command(TgBotCommands.healthcheck))
async def _(m: aiogram.types.Message, **kwargs):
    await m.answer(text=get_cached_tg_bot_blank().healthcheck())
