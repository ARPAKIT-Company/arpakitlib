import aiogram.filters

from project.tg_bot.blank.blank import get_cached_tg_bot_blank
from project.tg_bot.const import TgBotCommands
from project.tg_bot.filter_ import NotProdModeFilterTgBotFilter
from project.util.arpakitlib_project_template import get_arpakitlib_project_template_info

tg_bot_router = aiogram.Router()


@tg_bot_router.message(
    aiogram.filters.Command(TgBotCommands.arpakitlib_project_template_info),
    NotProdModeFilterTgBotFilter()
)
async def _(m: aiogram.types.Message, **kwargs):
    await m.answer(
        text=get_cached_tg_bot_blank().arpakit_project_template_info(
            arpakitlib_project_template_info=get_arpakitlib_project_template_info()
        )
    )
