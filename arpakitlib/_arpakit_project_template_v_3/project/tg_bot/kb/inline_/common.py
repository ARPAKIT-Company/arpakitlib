from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from project.tg_bot.blank.blank import get_cached_tg_bot_blank


def groups_inline_kb() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()

    kb_builder.row(InlineKeyboardButton(
        text=get_cached_tg_bot_blank().hello_world(),
        callback_data="Hello world"
    ))

    return kb_builder.as_markup()
