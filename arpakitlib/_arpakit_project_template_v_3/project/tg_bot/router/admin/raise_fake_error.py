import aiogram.filters

from arpakitlib.ar_aiogram_util import as_tg_command
from project.core.settings import get_cached_settings
from project.tg_bot.const import AdminTgBotCommands
from project.tg_bot.middleware.common import TgBotMiddlewareData

tg_bot_router = aiogram.Router()


@tg_bot_router.message(
    aiogram.filters.Command(AdminTgBotCommands.raise_fake_err)
)
@as_tg_command(passwd_validator=get_cached_settings().tg_bot_command_passwd)
async def _(
        m: aiogram.types.Message,
        tg_bot_middleware_data: TgBotMiddlewareData,
        **kwargs
):
    raise Exception("fake error")
