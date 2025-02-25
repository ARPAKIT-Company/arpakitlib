import aiogram.filters

from tg_bot.const import TgBotCommands

tg_bot_router = aiogram.Router()


@tg_bot_router.message(aiogram.filters.Command(TgBotCommands.arpakitlib))
async def _(m: aiogram.types.Message, **kwargs):
    await m.answer(text="arpakitlib")
