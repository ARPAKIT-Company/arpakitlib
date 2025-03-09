from aiogram import Router

from project.tg_bot.router.general import error_handler, healthcheck, hello_world

main_general_tg_bot_router = Router()

main_general_tg_bot_router.include_router(router=error_handler.tg_bot_router)

main_general_tg_bot_router.include_router(router=healthcheck.tg_bot_router)

main_general_tg_bot_router.include_router(router=hello_world.tg_bot_router)
