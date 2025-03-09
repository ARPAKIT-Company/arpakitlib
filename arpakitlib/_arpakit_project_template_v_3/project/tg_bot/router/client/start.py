import logging

from aiogram import types, Router
from aiogram.filters import Command, or_f

from project.tg_bot.blank.client import get_cached_client_blank_tg_bot
from project.tg_bot.const import ClientCommandsTgBot
from project.tg_bot.filter_.message_text import MessageTextTgBotFilter

tg_bot_router = Router()
_logger = logging.getLogger(__name__)


@tg_bot_router.message(
    or_f(
        Command(ClientCommandsTgBot.start),
        MessageTextTgBotFilter([
            "начать",
            "старт",
            "привет",
            "запуск",
            "start",
        ], ignore_case=True)
    )
)
async def _(m: types.Message, **kwargs):
    await m.answer(text=get_cached_client_blank_tg_bot().welcome())
