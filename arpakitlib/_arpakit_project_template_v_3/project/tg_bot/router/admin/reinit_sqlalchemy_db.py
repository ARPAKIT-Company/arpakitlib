from aiogram import types, Router
from aiogram.filters import Command

from arpakitlib.ar_aiogram_util import as_tg_command
from project.core.settings import get_cached_settings
from project.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db
from project.tg_bot.blank.admin import get_cached_admin_blank_tg_bot
from project.tg_bot.const import AdminCommandsTgBot
from project.tg_bot.filter_.not_prod_mode_filter import NotProdModeTgBotFilter
from project.tg_bot.middleware.common import TgBotMiddlewareData

tg_bot_router = Router()


@tg_bot_router.message(
    Command(AdminCommandsTgBot.reinit_sqlalchemy_db),
    NotProdModeTgBotFilter()
)
@as_tg_command(passwd_validator=get_cached_settings().tg_bot_command_passwd)
async def handler(m: types.Message, tg_bot_middleware_data: TgBotMiddlewareData, **kwargs):
    get_cached_sqlalchemy_db().reinit()
    await m.answer(text=get_cached_admin_blank_tg_bot().done())
