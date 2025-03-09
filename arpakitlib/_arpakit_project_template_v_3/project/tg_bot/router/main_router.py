from aiogram import Router

from project.tg_bot.router.admin.main_router import main_admin_tg_bot_router
from project.tg_bot.router.client.main_router import main_client_tg_bot_router

main_tg_bot_router = Router()

main_tg_bot_router.include_router(router=main_admin_tg_bot_router)

main_tg_bot_router.include_router(router=main_client_tg_bot_router)
