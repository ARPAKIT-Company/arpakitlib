from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from project.tg_bot.blank.general import get_cached_general_blank_tg_bot


def hello_world_general_static_tg_bot_kb() -> ReplyKeyboardMarkup:
    kb_builder = ReplyKeyboardBuilder()

    kb_builder.row(KeyboardButton(
        text=get_cached_general_blank_tg_bot().hello_world()
    ))

    return kb_builder.as_markup(resize_keyboard=True, one_time_keyboard=False)
