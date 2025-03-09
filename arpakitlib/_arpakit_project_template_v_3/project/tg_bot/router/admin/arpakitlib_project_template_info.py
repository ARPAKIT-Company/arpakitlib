import aiogram.filters

from project.tg_bot.blank.admin import get_cached_admin_blank_tg_bot
from project.tg_bot.const import AdminCommandsTgBot
from project.tg_bot.filter_.not_prod_mode_filter import NotProdModeTgBotFilter
from project.util.arpakitlib_project_template import get_arpakitlib_project_template_info

tg_bot_router = aiogram.Router()


@tg_bot_router.message(
    aiogram.filters.Command(AdminCommandsTgBot.arpakitlib_project_template_info),
    NotProdModeTgBotFilter()
)
async def _(m: aiogram.types.Message, **kwargs):
    await m.answer(
        text=get_cached_admin_blank_tg_bot().arpakit_project_template_info(
            arpakitlib_project_template_info=get_arpakitlib_project_template_info()
        )
    )
