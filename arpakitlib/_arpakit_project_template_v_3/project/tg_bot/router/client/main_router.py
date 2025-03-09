from aiogram import Router

from project.tg_bot.filter_.user_roles_has_client import UserRolesHasClientTgBotFilter
from project.tg_bot.router.client import start

main_client_tg_bot_router = Router()
for observer in main_client_tg_bot_router.observers.values():
    observer.filter(UserRolesHasClientTgBotFilter())

main_client_tg_bot_router.include_router(router=start.tg_bot_router)
