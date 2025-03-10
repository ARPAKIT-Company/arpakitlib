import aiogram.types
from aiogram.filters import Filter

from project.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db
from project.sqlalchemy_db_.sqlalchemy_model import UserDBM


class UserRolesHasClientTgBotFilter(Filter):

    async def __call__(
            self, update: aiogram.types.Message | aiogram.types.CallbackQuery | aiogram.types.TelegramObject, **kwargs
    ) -> bool:
        tg_user: None | aiogram.types.User = None

        if isinstance(update, aiogram.types.Message) and update.from_user is not None:
            tg_user = update.from_user
        if isinstance(update, aiogram.types.CallbackQuery) and update.from_user is not None:
            tg_user = update.from_user

        if get_cached_sqlalchemy_db() is not None and tg_user is not None:
            with get_cached_sqlalchemy_db().new_session() as session:
                user_dbm: UserDBM | None = session.query(UserDBM).filter(UserDBM.tg_id == tg_user.id).one_or_none()
            if user_dbm is not None:
                if user_dbm.roles_has_client:
                    return True

        return False
