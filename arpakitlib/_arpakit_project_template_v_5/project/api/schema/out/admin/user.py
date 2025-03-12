from __future__ import annotations

import datetime as dt
from typing import Any

from project.api.schema.out.admin.common import SimpleDBMAdminSO
from project.sqlalchemy_db_.sqlalchemy_model import UserDBM


class UserDBMSAdminSO(SimpleDBMAdminSO):
    mail: str | None
    roles: list[str]
    is_active: bool
    tg_id: int | None
    tg_bot_last_action_dt: dt.datetime | None
    tg_data: dict[str, Any] | None
    roles_has_admin: bool
    roles_has_client: bool

    @classmethod
    def from_user_dbm(cls, *, user_dbm: UserDBM) -> UserDBMSAdminSO:
        return cls.model_validate(user_dbm.simple_dict_with_sd_properties())
