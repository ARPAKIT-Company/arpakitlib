from aiogram import Router

from tg_bot.router import error, arpakitlib_project_template_info
from tg_bot.router import healthcheck

main_tg_bot_router = Router()

# Error

main_tg_bot_router.include_router(router=error.tg_bot_router)

# Healthcheck

main_tg_bot_router.include_router(router=healthcheck.tg_bot_router)

# arpakit project template

main_tg_bot_router.include_router(router=arpakitlib_project_template_info.tg_bot_router)
