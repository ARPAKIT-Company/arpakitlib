from __future__ import annotations

import datetime as dt
from typing import Any

from api.schema.base_schema import BaseSO
from sqlalchemy_db.sqlalchemy_model import OperationDBM, StoryLogDBM


class BaseV1SO(BaseSO):
    pass


class HealthcheckV1SO(BaseV1SO):
    is_ok: bool = True


class ARPAKITLIBInfoV1SO(BaseV1SO):
    arpakitlib: bool = True
    arpakitlib_project_template_version: str
    data: dict[str, Any] = {}


class RawDataV1SO(BaseV1SO):
    data: dict[str, Any] = {}


class ErrorsInfoV1SO(BaseV1SO):
    api_error_codes: list[str] = []
    api_error_specification_codes: list[str] = []


class DatetimeV1SO(BaseV1SO):
    date: dt.date
    datetime: dt.datetime | None = None
    year: int
    month: int
    day: int
    hour: int | None = None
    minute: int | None = None
    second: int | None = None
    microsecond: int | None = None

    @classmethod
    def from_datetime(cls, datetime_: dt.datetime):
        return cls(
            date=datetime_.date(),
            datetime=datetime_,
            year=datetime_.year,
            month=datetime_.month,
            day=datetime_.day,
            hour=datetime_.hour,
            minute=datetime_.minute,
            second=datetime_.second,
            microsecond=datetime_.microsecond
        )

    @classmethod
    def from_date(cls, date_: dt.date):
        return cls(
            date=date_,
            year=date_.year,
            month=date_.month,
            day=date_.day
        )


class SimpleDBMV1SO(BaseV1SO):
    id: int
    long_id: str
    creation_dt: dt.datetime


class StoryLogV1SO(SimpleDBMV1SO):
    level: str
    type: str | None = None
    title: str | None = None
    data: dict[str, Any] = {}

    @classmethod
    def from_story_log_dbm(cls, *, story_log_dbm: StoryLogDBM) -> StoryLogV1SO:
        return cls.model_validate(story_log_dbm.simple_dict_with_sd_properties())


class OperationV1SO(SimpleDBMV1SO):
    execution_start_dt: dt.datetime | None
    execution_finish_dt: dt.datetime | None
    status: str
    type: str
    input_data: dict[str, Any] = {}
    output_data: dict[str, Any] = {}
    error_data: dict[str, Any] = {}
    duration_total_seconds: float | None = None

    @classmethod
    def from_operation_dbm(cls, *, operation_dbm: OperationDBM) -> OperationV1SO:
        return cls.model_validate(operation_dbm.simple_dict_with_sd_properties())
