import aiogram.filters

from project.tg_bot.blank.general import get_cached_general_blank_tg_bot
from project.tg_bot.callback.general import HelloWorldGeneralCD
from project.tg_bot.const import GeneralCommandsTgBot
from project.tg_bot.kb.static_.general.hello_world import hello_world_general_static_tg_bot_kb

tg_bot_router = aiogram.Router()


@tg_bot_router.message(aiogram.filters.Command(GeneralCommandsTgBot.hello_world))
async def _(m: aiogram.types.Message, **kwargs):
    await m.answer(
        text=get_cached_general_blank_tg_bot().hello_world(),
        reply_markup=hello_world_general_static_tg_bot_kb()
    )


@tg_bot_router.callback_query(HelloWorldGeneralCD.filter())
async def _(m: aiogram.types.Message, **kwargs):
    await m.answer(text=get_cached_general_blank_tg_bot().hello_world())
