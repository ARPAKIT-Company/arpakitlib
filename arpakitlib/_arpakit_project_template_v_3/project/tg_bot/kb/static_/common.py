from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from project.tg_bot.blank.blank import get_cached_tg_bot_blank


def hello_world_static_kb() -> ReplyKeyboardMarkup:
    kb_builder = ReplyKeyboardBuilder()

    kb_builder.row(KeyboardButton(
        text=get_cached_tg_bot_blank().hello_world()
    ))

    return kb_builder.as_markup(resize_keyboard=True, one_time_keyboard=False)
