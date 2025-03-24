from __future__ import annotations

from typing import TYPE_CHECKING

import sqlalchemy
from sqlalchemy.orm import mapped_column, Mapped, validates

from arpakitlib.ar_enumeration_util import Enumeration
from project.sqlalchemy_db_.sqlalchemy_model.common import SimpleDBM

if TYPE_CHECKING:
    pass


class StoryLogDBM(SimpleDBM):
    __tablename__ = "story_log"

    class Levels(Enumeration):
        info = "info"
        warning = "warning"
        error = "error"

    class Types(Enumeration):
        error_in_execute_operation = "error_in_execute_operation"
        error_in_api = "error_in_api"
        error_in_tg_bot = "error_in_tg_bot"

    level: Mapped[str] = mapped_column(
        sqlalchemy.TEXT,
        insert_default=Levels.info,
        server_default=Levels.info,
        index=True,
        nullable=False
    )
    type: Mapped[str | None] = mapped_column(
        sqlalchemy.TEXT,
        index=True,
        insert_default=None,
        nullable=True)
    title: Mapped[str | None] = mapped_column(
        sqlalchemy.TEXT,
        insert_default=None,
        nullable=True
    )

    @validates("level")
    def _validate_level(self, key, value, *args, **kwargs):
        self.Levels.parse_and_validate_values(value)

    @property
    def sdp_allowed_levels(self) -> list[str]:
        return self.Levels.values_list()

    @property
    def sdp_allowed_types(self) -> list[str]:
        return self.Types.values_list()
