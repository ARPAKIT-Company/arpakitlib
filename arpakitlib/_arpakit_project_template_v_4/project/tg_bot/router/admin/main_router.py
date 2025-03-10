from aiogram import Router

from project.tg_bot.filter_.is_private_chat import IsPrivateChatTgBotFilter
from project.tg_bot.filter_.user_roles_has_admin import UserRolesHasAdminTgBotFilter
from project.tg_bot.router.admin import reinit_sqlalchemy_db, arpakitlib_project_template_info, raise_fake_error, me

main_admin_tg_bot_router = Router()
for observer in main_admin_tg_bot_router.observers.values():
    observer.filter(UserRolesHasAdminTgBotFilter())
    observer.filter(IsPrivateChatTgBotFilter())

main_admin_tg_bot_router.include_router(reinit_sqlalchemy_db.tg_bot_router)
main_admin_tg_bot_router.include_router(arpakitlib_project_template_info.tg_bot_router)
main_admin_tg_bot_router.include_router(raise_fake_error.tg_bot_router)
main_admin_tg_bot_router.include_router(me.tg_bot_router)
