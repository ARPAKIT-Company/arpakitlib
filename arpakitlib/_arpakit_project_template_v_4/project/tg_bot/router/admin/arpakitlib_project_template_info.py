import aiogram.filters

from arpakitlib.ar_aiogram_util import as_tg_command
from arpakitlib.ar_json_util import transfer_data_to_json_str
from project.tg_bot.const import AdminTgBotCommands
from project.tg_bot.middleware.common import MiddlewareDataTgBot
from project.util.arpakitlib_project_template import get_arpakitlib_project_template_info

tg_bot_router = aiogram.Router()


@tg_bot_router.message(
    aiogram.filters.Command(AdminTgBotCommands.arpakitlib_project_template_info)
)
@as_tg_command()
async def _(
        m: aiogram.types.Message,
        middleware_data_tg_bot: MiddlewareDataTgBot,
        **kwargs
):
    await m.answer(
        text=transfer_data_to_json_str(get_arpakitlib_project_template_info(), beautify=True)
    )
