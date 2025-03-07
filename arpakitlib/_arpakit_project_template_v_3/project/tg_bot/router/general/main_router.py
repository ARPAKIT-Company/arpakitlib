from aiogram import Router

from project.tg_bot.router.general import error, healthcheck, arpakitlib_project_template_info

main_tg_bot_general_router = Router()

main_tg_bot_general_router.include_router(router=error.tg_bot_router)

main_tg_bot_general_router.include_router(router=healthcheck.tg_bot_router)

main_tg_bot_general_router.include_router(router=arpakitlib_project_template_info.tg_bot_router)
