from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from project.tg_bot.blank.general import get_cached_general_blank_tg_bot
from project.tg_bot.callback.general import HelloWorldGeneralCD


def hello_world_general_inline_kb_tg_bot() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()

    kb_builder.row(InlineKeyboardButton(
        text=get_cached_general_blank_tg_bot().but_hello_world(),
        callback_data=HelloWorldGeneralCD(hello_world=True).pack()
    ))

    return kb_builder.as_markup()
