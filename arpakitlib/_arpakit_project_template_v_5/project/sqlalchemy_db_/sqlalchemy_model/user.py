from __future__ import annotations

import datetime as dt
from typing import TYPE_CHECKING, Any
from uuid import uuid4

import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from arpakitlib.ar_enumeration_util import Enumeration
from arpakitlib.ar_type_util import raise_for_type
from project.sqlalchemy_db_.sqlalchemy_model.common import SimpleDBM

if TYPE_CHECKING:
    from project.sqlalchemy_db_.sqlalchemy_model.user_token import UserTokenDBM


def generate_default_user_password() -> str:
    return str(uuid4()).replace("-", "")


class UserDBM(SimpleDBM):
    __tablename__ = "user"

    class Roles(Enumeration):
        admin = "admin"
        client = "client"

    email: Mapped[str | None] = mapped_column(
        sqlalchemy.TEXT,
        nullable=True,
        unique=True
    )
    roles: Mapped[list[str]] = mapped_column(
        sqlalchemy.ARRAY(sqlalchemy.TEXT),
        nullable=False,
        insert_default=[Roles.client],
        index=True,
    )
    is_active: Mapped[bool] = mapped_column(
        sqlalchemy.Boolean,
        nullable=False,
        index=True,
        insert_default=True,
        server_default="true",
    )
    password: Mapped[str | None] = mapped_column(
        sqlalchemy.TEXT,
        index=True,
        nullable=True,
        insert_default=generate_default_user_password,
        server_default=sqlalchemy.func.gen_random_uuid(),
    )
    tg_id: Mapped[int | None] = mapped_column(
        sqlalchemy.BIGINT,
        nullable=True,
        unique=True
    )
    tg_bot_last_action_dt: Mapped[dt.datetime | None] = mapped_column(
        sqlalchemy.TIMESTAMP(timezone=True),
        nullable=True
    )
    tg_data: Mapped[dict[str, Any]] = mapped_column(
        sqlalchemy.JSON,
        nullable=False,
        index=False,
        insert_default={},
        server_default="{}",
    )

    # many to one
    user_tokens: Mapped[list[UserTokenDBM]] = relationship(
        "UserTokenDBM",
        uselist=True,
        back_populates="user",
        foreign_keys="UserTokenDBM.user_id"
    )

    def __repr__(self) -> str:
        if self.email is not None:
            res = f"{self.entity_name} (id={self.id}, email={self.email})"
        else:
            res = f"{self.entity_name} (id={self.id})"
        return res

    @property
    def sdp_allowed_roles(self) -> list[str]:
        return self.Roles.values_list()

    @property
    def roles_has_admin(self) -> bool:
        return self.Roles.admin in self.roles

    @property
    def sdp_roles_has_admin(self) -> bool:
        return self.roles_has_admin

    @property
    def roles_has_client(self) -> bool:
        return self.Roles.client in self.roles

    @property
    def sdp_roles_has_client(self) -> bool:
        return self.roles_has_client

    def compare_roles(self, roles: list[str] | str) -> bool:
        if isinstance(roles, str):
            roles = [roles]
        raise_for_type(roles, list)
        return bool(set(roles) & set(self.roles))

    @property
    def tg_data_first_name(self) -> str | None:
        if self.tg_data and "first_name" in self.tg_data:
            return self.tg_data["first_name"]
        return None

    @property
    def sdp_tg_data_first_name(self) -> str | None:
        return self.tg_data_first_name

    @property
    def tg_data_last_name(self) -> str | None:
        if self.tg_data and "last_name" in self.tg_data:
            return self.tg_data["last_name"]
        return None

    @property
    def sdp_tg_data_last_name(self) -> str | None:
        return self.tg_data_last_name

    @property
    def tg_data_language_code(self) -> str | None:
        if self.tg_data and "language_code" in self.tg_data:
            return self.tg_data["language_code"]
        return None

    @property
    def sdp_tg_data_language_code(self) -> str | None:
        return self.tg_data_language_code

    @property
    def tg_data_username(self) -> str | None:
        if self.tg_data and "username" in self.tg_data:
            return self.tg_data["username"]
        return None

    @property
    def sdp_tg_data_username(self) -> str | None:
        return self.tg_data_username

    @property
    def tg_data_at_username(self) -> str | None:
        if self.tg_data_username:
            return f"@{self.tg_data_username}"
        return None

    @property
    def sdp_tg_data_at_username(self) -> str | None:
        return self.tg_data_at_username

    @property
    def tg_data_fullname(self) -> str | None:
        if not self.tg_data_first_name and not self.tg_data_last_name:
            return None
        res = ""
        if self.tg_data_first_name:
            res += self.tg_data_first_name
        if self.tg_data_last_name:
            res += " " + self.tg_data_last_name
        return res

    @property
    def sdp_tg_data_fullname(self) -> str | None:
        return self.tg_data_fullname

    @property
    def tg_data_link_by_username(self) -> str | None:
        if not self.tg_data_username:
            return None
        return f"https://t.me/{self.tg_data_username}"

    @property
    def sdp_tg_data_link_by_username(self) -> str | None:
        return self.tg_data_link_by_username
