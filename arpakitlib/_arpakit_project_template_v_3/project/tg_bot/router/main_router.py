from aiogram import Router

from project.tg_bot.router import arpakitlib_project_template_info
from project.tg_bot.router import error, healthcheck

main_tg_bot_router = Router()

main_tg_bot_router.include_router(router=error.tg_bot_router)

main_tg_bot_router.include_router(router=healthcheck.tg_bot_router)

main_tg_bot_router.include_router(router=arpakitlib_project_template_info.tg_bot_router)
