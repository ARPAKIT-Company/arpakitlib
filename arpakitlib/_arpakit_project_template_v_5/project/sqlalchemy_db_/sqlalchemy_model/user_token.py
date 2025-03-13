from __future__ import annotations

from typing import TYPE_CHECKING

import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.sqlalchemy_db_.sqlalchemy_model.common import SimpleDBM

if TYPE_CHECKING:
    from project.sqlalchemy_db_.sqlalchemy_model.user import UserDBM


class UserTokenDBM(SimpleDBM):
    __tablename__ = "user_token"

    value: Mapped[str] = mapped_column(
        sqlalchemy.TEXT,
        unique=True,
        nullable=False,
    )
    user_id: Mapped[int] = mapped_column(
        sqlalchemy.INTEGER,
        sqlalchemy.ForeignKey("user.id", ondelete="CASCADE"),
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

    user: Mapped[UserDBM] = relationship(
        "UserDBM",
        uselist=False,
        back_populates="user_tokens",
        foreign_keys=[user_id]
    )
