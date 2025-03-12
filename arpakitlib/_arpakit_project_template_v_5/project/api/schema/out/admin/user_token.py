from __future__ import annotations

from project.api.schema.out.admin.common import SimpleDBMAdminSO
from project.sqlalchemy_db_.sqlalchemy_model import UserTokenDBM


class UserTokenDBMSAdminSO(SimpleDBMAdminSO):
    value: str
    user_id: int
    is_active: bool

    @classmethod
    def from_user_token_dbm(cls, *, user_dbm: UserTokenDBM) -> UserTokenDBMSAdminSO:
        return cls.model_validate(user_dbm.simple_dict_with_sd_properties())
