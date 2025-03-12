import aiogram
from aiogram import Router
from aiogram.filters import Command

from arpakitlib.ar_aiogram_util import as_tg_command
from project.tg_bot.blank.admin import get_cached_admin_tg_bot_blank
from project.tg_bot.const import AdminTgBotCommands
from project.tg_bot.middleware.common import MiddlewareDataTgBot
from project.tg_bot.util.set_tg_bot_commands import set_all_tg_bot_commands

tg_bot_router = Router()


@tg_bot_router.message(
    Command(AdminTgBotCommands.set_all_tg_bot_commands)
)
@as_tg_command()
async def _(
        m: aiogram.types.Message,
        middleware_data_tg_bot: MiddlewareDataTgBot,
        **kwargs
):
    await set_all_tg_bot_commands()
    await m.answer(get_cached_admin_tg_bot_blank().good())
