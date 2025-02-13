from __future__ import annotations

import datetime as dt
from typing import Any

from arpakitlib.ar_fastapi_util import BaseSO
from src.sqlalchemy_db.sqlalchemy_model import OperationDBM, StoryLogDBM


class HealthcheckSO(BaseSO):
    is_ok: bool = True


class ARPAKITLIBSO(BaseSO):
    arpakitlib: bool = True


class RawDataSO(BaseSO):
    data: dict[str, Any] = {}


class APIErrorInfoSO(BaseSO):
    api_error_codes: list[str] = []
    api_error_specification_codes: list[str] = []


class DatetimeSO(BaseSO):
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


class SimpleSO(BaseSO):
    id: int
    long_id: str
    creation_dt: dt.datetime


class StoryLogSO(SimpleSO):
    level: str
    title: str | None = None
    data: dict[str, Any] = {}

    @classmethod
    def from_story_log_dbm(cls, *, story_log_dbm: StoryLogDBM) -> StoryLogSO:
        return cls.model_validate(story_log_dbm.simple_dict(include_sd_properties=True))


class OperationSO(SimpleSO):
    execution_start_dt: dt.datetime | None
    execution_finish_dt: dt.datetime | None
    status: str
    type: str
    input_data: dict[str, Any] = {}
    output_data: dict[str, Any] = {}
    error_data: dict[str, Any] = {}
    duration_total_seconds: float | None

    @classmethod
    def from_operation_dbm(cls, *, operation_dbm: OperationDBM) -> OperationSO:
        return cls.model_validate(operation_dbm.simple_dict(include_sd_properties=True))
