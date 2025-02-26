import aiogram.filters

from arpakitlib.ar_json_util import safely_transfer_obj_to_json_str
from tg_bot.const import TgBotCommands
from util.read_arpakitlib_project_template_file import read_arpakitlib_project_template_file

tg_bot_router = aiogram.Router()


@tg_bot_router.message(aiogram.filters.Command(TgBotCommands.arpakitlib_project_template_info))
async def _(m: aiogram.types.Message, **kwargs):
    await m.answer(
        text=safely_transfer_obj_to_json_str(data=read_arpakitlib_project_template_file())
    )
