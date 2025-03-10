import logging
from typing import Any, Awaitable, Callable, Dict

import aiogram
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from project.core.settings import get_cached_settings
from project.core.util import now_local_dt
from project.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db
from project.sqlalchemy_db_.sqlalchemy_model import UserDBM
from project.tg_bot.middleware.common import TgBotMiddlewareData

_logger = logging.getLogger(__name__)


class InitUserTgBotMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        _logger.info("start")

        if "tg_bot_middleware_data" in data:
            tg_bot_middleware_data = data["tg_bot_middleware_data"]
        else:
            tg_bot_middleware_data = TgBotMiddlewareData()
            data["tg_bot_middleware_data"] = tg_bot_middleware_data

        tg_user: aiogram.types.User | None = None
        if event.event_type == "message":
            tg_user = event.message.from_user
        elif event.event_type == "callback_query":
            tg_user = event.callback_query.from_user
        elif event.event_type == "inline_query":
            tg_user = event.inline_query.from_user

        if tg_user is not None:
            tg_bot_middleware_data.additional_data["tg_user_was_found"] = tg_user
            tg_bot_middleware_data.additional_data["found_tg_user_id"] = tg_user.id

        now_local_dt_ = now_local_dt()

        if tg_user is not None and get_cached_sqlalchemy_db() is not None:
            with get_cached_sqlalchemy_db().new_session() as session:
                tg_bot_middleware_data.user_dbm = (
                    session.query(UserDBM).filter(UserDBM.tg_id == tg_user.id).one_or_none()
                )
                if tg_bot_middleware_data.user_dbm is None:
                    roles = [UserDBM.Roles.client]
                    if tg_user.id in get_cached_settings().tg_bot_admin_tg_ids:
                        roles.append(UserDBM.Roles.admin)
                    tg_bot_middleware_data.user_dbm = UserDBM(
                        creation_dt=now_local_dt_,
                        roles=roles,
                        tg_id=tg_user.id,
                        tg_data=tg_user.model_dump(mode="json"),
                        tg_bot_last_action_dt=now_local_dt_
                    )
                    session.add(tg_bot_middleware_data.user_dbm)
                    session.commit()
                    session.refresh(tg_bot_middleware_data.user_dbm)
                    tg_bot_middleware_data.user_dbm_just_created = True
                    _logger.info(f"user_dbm was added, {tg_bot_middleware_data.user_dbm}")
                else:
                    tg_bot_middleware_data.user_dbm.tg_data = tg_user.model_dump(mode="json")
                    tg_bot_middleware_data.user_dbm.tg_bot_last_action_dt = now_local_dt_
                    if (
                            tg_user.id in get_cached_settings().tg_bot_admin_tg_ids
                            and UserDBM.Roles.admin not in tg_bot_middleware_data.user_dbm.roles
                    ):
                        tg_bot_middleware_data.user_dbm.roles = (
                                tg_bot_middleware_data.user_dbm.roles + [UserDBM.Roles.admin]
                        )
                    session.commit()
                    session.refresh(tg_bot_middleware_data.user_dbm)
                    tg_bot_middleware_data.user_dbm_just_created = False

        _logger.info("finish")

        return await handler(event, data)
