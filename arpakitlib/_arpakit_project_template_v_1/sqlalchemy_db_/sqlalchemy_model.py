from datetime import datetime, timedelta
from typing import Any

import sqlalchemy
from sqlalchemy import func
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import mapped_column, Mapped

from arpakitlib.ar_datetime_util import now_utc_dt
from arpakitlib.ar_enumeration_util import Enumeration
from arpakitlib.ar_sqlalchemy_util import get_string_info_from_declarative_base, BaseDBM
from sqlalchemy_db_.util import generate_default_long_id


class SimpleDBM(BaseDBM):
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        sqlalchemy.INTEGER, primary_key=True, autoincrement=True, sort_order=-3, nullable=False
    )
    long_id: Mapped[str] = mapped_column(
        sqlalchemy.TEXT, insert_default=generate_default_long_id, server_default=func.gen_random_uuid(),
        unique=True, sort_order=-2, nullable=False
    )
    creation_dt: Mapped[datetime] = mapped_column(
        sqlalchemy.TIMESTAMP(timezone=True), insert_default=now_utc_dt, server_default=func.now(),
        index=True, sort_order=-1, nullable=False
    )

    def __repr__(self):
        return f"{self.__class__.__name__.removesuffix('DBM')} (id={self.id})"


class StoryLogDBM(SimpleDBM):
    __tablename__ = "story_log"

    class Levels(Enumeration):
        info = "info"
        warning = "warning"
        error = "error"

    class Types(Enumeration):
        error_in_execute_operation = "error_in_execute_operation"
        error_in_api_route = "error_in_api_route"

    level: Mapped[str] = mapped_column(
        sqlalchemy.TEXT, insert_default=Levels.info, server_default=Levels.info, index=True, nullable=False
    )
    type: Mapped[str | None] = mapped_column(sqlalchemy.TEXT, index=True, default=None, nullable=True)
    title: Mapped[str | None] = mapped_column(sqlalchemy.TEXT, index=True, default=None, nullable=True)
    data: Mapped[dict[str, Any]] = mapped_column(
        postgresql.JSON, insert_default={}, server_default="{}", nullable=False
    )


class OperationDBM(SimpleDBM):
    __tablename__ = "operation"

    class Statuses(Enumeration):
        waiting_for_execution = "waiting_for_execution"
        executing = "executing"
        executed_without_error = "executed_without_error"
        executed_with_error = "executed_with_error"

    class Types(Enumeration):
        healthcheck_ = "healthcheck"
        raise_fake_error_ = "raise_fake_error_"

    status: Mapped[str] = mapped_column(
        sqlalchemy.TEXT, index=True, insert_default=Statuses.waiting_for_execution,
        server_default=Statuses.waiting_for_execution, nullable=False
    )
    type: Mapped[str] = mapped_column(
        sqlalchemy.TEXT, index=True, insert_default=Types.healthcheck_, nullable=False
    )
    execution_start_dt: Mapped[datetime | None] = mapped_column(sqlalchemy.TIMESTAMP(timezone=True), nullable=True)
    execution_finish_dt: Mapped[datetime | None] = mapped_column(sqlalchemy.TIMESTAMP(timezone=True), nullable=True)
    input_data: Mapped[dict[str, Any]] = mapped_column(
        postgresql.JSON,
        insert_default={},
        server_default="{}",
        nullable=False
    )
    output_data: Mapped[dict[str, Any]] = mapped_column(
        postgresql.JSON, insert_default={}, server_default="{}", nullable=False
    )
    error_data: Mapped[dict[str, Any]] = mapped_column(
        postgresql.JSON, insert_default={}, server_default="{}", nullable=False
    )

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
        return self.duration_total_seconds


def get_simple_dbm() -> type[SimpleDBM]:
    return SimpleDBM


def import_sqlalchemy_models():
    pass


if __name__ == '__main__':
    print(get_string_info_from_declarative_base(SimpleDBM))
