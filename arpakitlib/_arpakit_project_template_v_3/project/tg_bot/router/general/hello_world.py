import aiogram.filters
from aiogram.filters import or_f

from arpakitlib.ar_str_util import remove_html
from project.tg_bot.blank.general import get_cached_general_blank_tg_bot
from project.tg_bot.callback.general import HelloWorldGeneralCD
from project.tg_bot.const import GeneralCommandsTgBot
from project.tg_bot.filter_.message_text import MessageTextTgBotFilter
from project.tg_bot.kb.inline_.general.hello_world import hello_world_general_inline_kb_tg_bot
from project.tg_bot.kb.static_.general.hello_world import hello_world_general_static_kb_tg_bot

tg_bot_router = aiogram.Router()


@tg_bot_router.message(
    or_f(
        aiogram.filters.Command(GeneralCommandsTgBot.hello_world),
        MessageTextTgBotFilter(get_cached_general_blank_tg_bot().but_hello_world())
    )
)
async def _(m: aiogram.types.Message, **kwargs):
    await m.answer(
        text=get_cached_general_blank_tg_bot().hello_world(),
        reply_markup=hello_world_general_inline_kb_tg_bot()
    )
    await m.answer(
        text=get_cached_general_blank_tg_bot().hello_world(),
        reply_markup=hello_world_general_static_kb_tg_bot()
    )


@tg_bot_router.callback_query(HelloWorldGeneralCD.filter())
async def _(m: aiogram.types.Message, **kwargs):
    await m.answer(text=remove_html(get_cached_general_blank_tg_bot().hello_world()))
