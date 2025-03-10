import aiogram
from aiogram import Router
from aiogram.filters import Command

from arpakitlib.ar_aiogram_util import as_tg_command
from project.core.settings import get_cached_settings
from project.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db
from project.tg_bot.blank.admin import get_cached_admin_tg_bot_blank
from project.tg_bot.const import AdminTgBotCommands
from project.tg_bot.filter_.not_prod_mode_filter import NotProdModeTgBotFilter
from project.tg_bot.middleware.common import MiddlewareDataTgBot

tg_bot_router = Router()


@tg_bot_router.message(
    Command(AdminTgBotCommands.reinit_sqlalchemy_db),
    NotProdModeTgBotFilter()
)
@as_tg_command(passwd_validator=get_cached_settings().tg_bot_command_passwd)
async def handler(
        m: aiogram.types.Message,
        middleware_data_tg_bot: MiddlewareDataTgBot,
        **kwargs
):
    get_cached_sqlalchemy_db().reinit()
    await m.answer(text=get_cached_admin_tg_bot_blank().done())
