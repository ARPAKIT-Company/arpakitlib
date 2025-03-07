from __future__ import annotations

from typing import TYPE_CHECKING

import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from arpakitlib.ar_enumeration_util import Enumeration
from project.sqlalchemy_db_.sqlalchemy_model import SimpleDBM

if TYPE_CHECKING:
    from project.sqlalchemy_db_.sqlalchemy_model.user_token import UserTokenDBM


class UserDBM(SimpleDBM):
    __tablename__ = "user"

    class Roles(Enumeration):
        admin = "admin"
        client = "client"

    mail: Mapped[str] = mapped_column(
        sqlalchemy.TEXT,
        index=True,
        insert_default=None,
        nullable=True
    )
    roles: Mapped[list[str]] = mapped_column(
        sqlalchemy.ARRAY(sqlalchemy.TEXT),
        insert_default=[Roles.client],
        index=True,
        nullable=False
    )
    is_enabled: Mapped[bool] = mapped_column(
        sqlalchemy.Boolean,
        index=True,
        insert_default=True,
        server_default="true",
        nullable=False
    )

    user_tokens: Mapped[list[UserTokenDBM]] = relationship(
        "UserTokenDBM",
        uselist=True,
        back_populates="user",
        foreign_keys="UserTokenDBM.user_id"
    )

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
