from aiogram import Router

from project.tg_bot.router.general.main_router import main_tg_bot_general_router

main_tg_bot_router = Router()

main_tg_bot_router.include_router(router=main_tg_bot_general_router)
