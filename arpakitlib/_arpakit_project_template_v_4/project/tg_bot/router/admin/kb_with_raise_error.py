import aiogram.filters
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from arpakitlib.ar_aiogram_util import as_tg_command
from project.tg_bot.blank.admin import get_cached_admin_tg_bot_blank
from project.tg_bot.callback.common import BaseCD
from project.tg_bot.const import AdminTgBotCommands
from project.tg_bot.middleware.common import MiddlewareDataTgBot

tg_bot_router = aiogram.Router()


class _CD(BaseCD, prefix=AdminTgBotCommands.kb_with_raise_error):
    pass


@tg_bot_router.message(
    aiogram.filters.Command(AdminTgBotCommands.kb_with_raise_error)
)
@as_tg_command()
async def _(
        m: aiogram.types.Message,
        middleware_data_tg_bot: MiddlewareDataTgBot,
        **kwargs
):
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(InlineKeyboardButton(
        text="Raise fake error",
        callback_data=_CD().pack()
    ))
    await m.answer(
        text=get_cached_admin_tg_bot_blank().good(),
        reply_markup=kb_builder.as_markup()
    )


@tg_bot_router.callback_query(_CD.filter())
async def _(
        m: aiogram.types.Message,
        middleware_data_tg_bot: MiddlewareDataTgBot,
        **kwargs
):
    raise Exception("fake error")
