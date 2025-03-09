import aiogram.filters

from project.tg_bot.blank.general import get_cached_general_blank_tg_bot
from project.tg_bot.const import GeneralCommandsTgBot

tg_bot_router = aiogram.Router()


@tg_bot_router.message(aiogram.filters.Command(GeneralCommandsTgBot.healthcheck))
async def _(m: aiogram.types.Message, **kwargs):
    await m.answer(text=get_cached_general_blank_tg_bot().healthcheck())
