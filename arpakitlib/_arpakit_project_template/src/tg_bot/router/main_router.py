from aiogram import Router

from arpakitlib.ar_aiogram_util import create_helpful_tg_bot_router
from src.core.settings import get_cached_settings
from src.tg_bot.router import error

main_tg_bot_router = Router()

# Helpful Tg Bot router

if get_cached_settings().tg_bot_include_helpful_tg_bot_router:
    main_tg_bot_router.include_router(router=create_helpful_tg_bot_router())

# Error

main_tg_bot_router.include_router(error.tg_bot_router)
