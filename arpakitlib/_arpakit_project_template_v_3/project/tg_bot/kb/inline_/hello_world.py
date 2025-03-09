from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from project.tg_bot.blank.common import get_cached_tg_bot_blank
from project.tg_bot.callback.general import HelloWorldGeneralCD


def hello_world_kb() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()

    kb_builder.row(InlineKeyboardButton(
        text=get_cached_tg_bot_blank().hello_world(),
        callback_data=HelloWorldGeneralCD(hello_world=True).pack()
    ))

    return kb_builder.as_markup()
