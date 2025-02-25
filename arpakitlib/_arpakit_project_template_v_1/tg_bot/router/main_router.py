from aiogram import Router

from tg_bot.router import error
from tg_bot.router import healthcheck

main_tg_bot_router = Router()

# Healthcheck

main_tg_bot_router.include_router(router=healthcheck.tg_bot_router)

# Error

main_tg_bot_router.include_router(router=error.tg_bot_router)
