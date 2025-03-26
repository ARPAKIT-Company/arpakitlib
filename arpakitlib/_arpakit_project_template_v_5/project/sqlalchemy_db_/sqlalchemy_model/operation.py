from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, TYPE_CHECKING

import sqlalchemy
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import mapped_column, Mapped, validates

from arpakitlib.ar_enumeration_util import Enumeration
from project.sqlalchemy_db_.sqlalchemy_model.common import SimpleDBM

if TYPE_CHECKING:
    pass


class OperationDBM(SimpleDBM):
    __tablename__ = "operation"

    class Statuses(Enumeration):
        waiting_for_execution = "waiting_for_execution"
        executing = "executing"
        executed_without_error = "executed_without_error"
        executed_with_error = "executed_with_error"

    class Types(Enumeration):
        healthcheck_ = "healthcheck"
        raise_fake_error_ = "raise_fake_error"

    status: Mapped[str] = mapped_column(
        sqlalchemy.TEXT,
        nullable=False,
        index=True,
        insert_default=Statuses.waiting_for_execution,
        server_default=Statuses.waiting_for_execution
    )
    type: Mapped[str] = mapped_column(
        sqlalchemy.TEXT,
        nullable=False,
        index=True,
        insert_default=Types.healthcheck_
    )
    title: Mapped[str | None] = mapped_column(
        sqlalchemy.TEXT,
        nullable=True,
        index=False
    )
    execution_start_dt: Mapped[datetime | None] = mapped_column(
        sqlalchemy.TIMESTAMP(timezone=True),
        nullable=True,
        index=False
    )
    execution_finish_dt: Mapped[datetime | None] = mapped_column(
        sqlalchemy.TIMESTAMP(timezone=True),
        nullable=True,
        index=False
    )
    input_data: Mapped[dict[str, Any]] = mapped_column(
        postgresql.JSON,
        nullable=False,
        index=False,
        insert_default={},
        server_default="{}",
    )
    output_data: Mapped[dict[str, Any]] = mapped_column(
        postgresql.JSON,
        nullable=False,
        index=False,
        insert_default={},
        server_default="{}",
    )
    error_data: Mapped[dict[str, Any]] = mapped_column(
        postgresql.JSON,
        nullable=False,
        index=False,
        insert_default={},
        server_default="{}",
    )

    @validates("status")
    def _validate_status(self, key, value, *args, **kwargs):
        if not isinstance(value, str):
            raise ValueError(f"{value=} is not str")
        value = value.strip()
        self.Statuses.parse_and_validate_values(value)
        return value

    @validates("type")
    def _validate_type(self, key, value, *args, **kwargs):
        if not isinstance(value, str):
            raise ValueError(f"{value=} is not str")
        value = value.strip()
        return value

    @validates("title")
    def _validate_title(self, key, value, *args, **kwargs):
        if value is None:
            return None
        if not isinstance(value, str):
            raise ValueError(f"{value=} is not str")
        value = value.strip()
        return value

    @validates("input_data")
    def _validate_input_data(self, key, value, *args, **kwargs):
        if value is None:
            value = {}
        if not isinstance(value, dict):
            raise ValueError(f"{value=} is not str")
        return value

    @validates("output_data")
    def _validate_output_data(self, key, value, *args, **kwargs):
        if value is None:
            value = {}
        if not isinstance(value, dict):
            raise ValueError(f"{value=} is not str")
        return value

    @validates("error_data")
    def _validate_error_data(self, key, value, *args, **kwargs):
        if value is None:
            value = {}
        if not isinstance(value, dict):
            raise ValueError(f"{value=} is not str")
        return value

    def raise_if_executed_with_error(self):
        if self.status == self.Statuses.executed_with_error:
            raise Exception(
                f"Operation (id={self.id}, type={self.type}) executed with error, error_data={self.error_data}"
            )

    def raise_if_error_data(self):
        if self.error_data:
            raise Exception(
                f"Operation (id={self.id}, type={self.type}) has error_data, error_data={self.error_data}"
            )

    @property
    def duration(self) -> timedelta | None:
        if self.execution_start_dt is None or self.execution_finish_dt is None:
            return None
        return self.execution_finish_dt - self.execution_start_dt

    @property
    def duration_total_seconds(self) -> float | None:
        if self.duration is None:
            return None
        return self.duration.total_seconds()

    @property
    def sdp_duration_total_seconds(self) -> float | None:
        """
        При использовании у данной модели .simple_dict данное свойство будет представлено как поле.
        То есть префикс sdp_ и даёт этот бонус.
        """
        return self.duration_total_seconds

    @property
    def sdp_allowed_statuses(self) -> list[str]:
        return self.Statuses.values_list()

    @property
    def sdp_allowed_types(self) -> list[str]:
        return self.Types.values_list()
