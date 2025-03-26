from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import uuid4

import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from arpakitlib.ar_datetime_util import now_utc_dt
from project.sqlalchemy_db_.sqlalchemy_model.common import SimpleDBM

if TYPE_CHECKING:
    from project.sqlalchemy_db_.sqlalchemy_model.user import UserDBM


def generate_default_user_token_value() -> str:
    return (
        f"usertoken"
        f"{str(uuid4()).replace('-', '')}"
        f"{str(now_utc_dt().timestamp()).replace('.', '')}"
    )


class UserTokenDBM(SimpleDBM):
    __tablename__ = "user_token"

    value: Mapped[str] = mapped_column(
        sqlalchemy.TEXT,
        nullable=False,
        unique=True,
        insert_default=generate_default_user_token_value,
        server_default=sqlalchemy.func.gen_random_uuid(),
    )
    user_id: Mapped[int] = mapped_column(
        sqlalchemy.BIGINT,
        sqlalchemy.ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    is_active: Mapped[bool] = mapped_column(
        sqlalchemy.Boolean,
        nullable=False,
        index=True,
        insert_default=True,
        server_default="true",
    )

    # one to many
    user: Mapped[UserDBM] = relationship(
        "UserDBM",
        uselist=False,
        back_populates="user_tokens",
        foreign_keys=[user_id]
    )

    def __repr__(self) -> str:
        res = f"{self.entity_name} (id={self.id}, user_id={self.user_id})"
        return res

    @validates("value")
    def _validate_value(self, key, value, *args, **kwargs):
        if not isinstance(value, str):
            raise ValueError(f"{value=} is not str")
        value = value.strip()
        return value

    @property
    def sdp_user(self) -> UserDBM:
        return self.user
