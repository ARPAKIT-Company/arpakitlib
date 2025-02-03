from aiogram import Router

from src.tg_bot.router import error

main_tg_bot_router = Router()

main_tg_bot_router.include_router(error.tg_bot_router)
