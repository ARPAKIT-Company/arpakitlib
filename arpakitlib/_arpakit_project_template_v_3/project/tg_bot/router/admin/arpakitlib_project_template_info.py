import aiogram.filters

from arpakitlib.ar_aiogram_util import as_tg_command
from project.tg_bot.blank.admin import get_cached_admin_blank_tg_bot
from project.tg_bot.const import AdminCommandsTgBot
from project.util.arpakitlib_project_template import get_arpakitlib_project_template_info

tg_bot_router = aiogram.Router()


@tg_bot_router.message(
    aiogram.filters.Command(AdminCommandsTgBot.arpakitlib_project_template_info)
)
@as_tg_command()
async def _(m: aiogram.types.Message, **kwargs):
    await m.answer(
        text=get_cached_admin_blank_tg_bot().arpakit_project_template_info(
            arpakitlib_project_template_info=get_arpakitlib_project_template_info()
        )
    )
