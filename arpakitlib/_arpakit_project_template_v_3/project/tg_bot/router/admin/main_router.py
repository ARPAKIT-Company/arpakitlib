from aiogram import Router

from project.tg_bot.filter_.user_roles_has_admin import UserRolesHasAdminTgBotFilter
from project.tg_bot.router.admin import reinit_sqlalchemy_db, arpakitlib_project_template_info

main_admin_tg_bot_router = Router()
for observer in main_admin_tg_bot_router.observers.values():
    observer.filter(UserRolesHasAdminTgBotFilter())

main_admin_tg_bot_router.include_router(reinit_sqlalchemy_db.tg_bot_router)
main_admin_tg_bot_router.include_router(arpakitlib_project_template_info.tg_bot_router)
