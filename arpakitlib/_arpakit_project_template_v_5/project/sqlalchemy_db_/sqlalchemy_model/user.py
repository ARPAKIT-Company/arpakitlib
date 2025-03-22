from __future__ import annotations

import datetime as dt
from typing import TYPE_CHECKING, Any

import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from arpakitlib.ar_enumeration_util import Enumeration
from arpakitlib.ar_type_util import raise_for_type
from project.sqlalchemy_db_.sqlalchemy_model.common import SimpleDBM

if TYPE_CHECKING:
    from project.sqlalchemy_db_.sqlalchemy_model.user_token import UserTokenDBM


class UserDBM(SimpleDBM):
    __tablename__ = "user"

    class Roles(Enumeration):
        admin = "admin"
        client = "client"

    email: Mapped[str | None] = mapped_column(
        sqlalchemy.TEXT,
        unique=True,
        insert_default=None,
        nullable=True
    )
    roles: Mapped[list[str]] = mapped_column(
        sqlalchemy.ARRAY(sqlalchemy.TEXT),
        insert_default=[Roles.client],
        index=True,
        nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        sqlalchemy.Boolean,
        index=True,
        insert_default=True,
        server_default="true",
        nullable=False
    )
    tg_id: Mapped[int | None] = mapped_column(
        sqlalchemy.BIGINT,
        unique=True,
        nullable=True
    )
    tg_bot_last_action_dt: Mapped[dt.datetime | None] = mapped_column(
        sqlalchemy.TIMESTAMP(timezone=True),
        insert_default=None,
        nullable=True
    )
    tg_data: Mapped[dict[str, Any] | None] = mapped_column(
        sqlalchemy.JSON,
        insert_default={},
        server_default="{}",
        nullable=True
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
    def tg_first_name(self) -> str | None:
        if self.tg_data and "first_name" in self.tg_data:
            return self.tg_data["first_name"]
        return None

    @property
    def sdp_tg_first_name(self) -> str | None:
        return self.tg_first_name

    @property
    def tg_last_name(self) -> str | None:
        if self.tg_data and "last_name" in self.tg_data:
            return self.tg_data["last_name"]
        return None

    @property
    def sdp_tg_last_name(self) -> str | None:
        return self.tg_last_name

    @property
    def tg_language_code(self) -> str | None:
        if self.tg_data and "language_code" in self.tg_data:
            return self.tg_data["language_code"]
        return None

    @property
    def sdp_tg_language_code(self) -> str | None:
        return self.tg_language_code

    @property
    def tg_username(self) -> str | None:
        if self.tg_data and "username" in self.tg_data:
            return self.tg_data["username"]
        return None

    @property
    def sdp_tg_username(self) -> str | None:
        return self.tg_username

    @property
    def tg_at_username(self) -> str | None:
        if self.tg_username:
            return f"@{self.tg_username}"
        return None

    @property
    def sdp_tg_at_username(self) -> str | None:
        return self.tg_at_username

    @property
    def tg_fullname(self) -> str | None:
        if not self.tg_first_name and not self.tg_last_name:
            return None
        res = ""
        if self.tg_first_name:
            res += self.tg_first_name
        if self.tg_last_name:
            res += " " + self.tg_last_name
        return res

    @property
    def sdp_tg_fullname(self) -> str | None:
        return self.tg_fullname

    @property
    def tg_link_by_username(self) -> str | None:
        if not self.tg_username:
            return None
        return f"https://t.me/{self.tg_username}"

    @property
    def sdp_tg_link_by_username(self) -> str | None:
        return self.tg_link_by_username
