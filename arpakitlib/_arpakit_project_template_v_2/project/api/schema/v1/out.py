from __future__ import annotations

import datetime as dt
from typing import Any

from project.api.schema.base_schema import BaseSO
from project.sqlalchemy_db_.sqlalchemy_model import OperationDBM, StoryLogDBM


class BaseV1SO(BaseSO):
    pass


class HealthcheckV1SO(BaseV1SO):
    is_ok: bool = True


class _SimpleDBMV1SO(BaseV1SO):
    id: int
    long_id: str
    creation_dt: dt.datetime


class StoryLogV1SO(_SimpleDBMV1SO):
    level: str
    type: str | None = None
    title: str | None = None
    data: dict[str, Any] = {}

    @classmethod
    def from_story_log_dbm(cls, *, story_log_dbm: StoryLogDBM) -> StoryLogV1SO:
        return cls.model_validate(story_log_dbm.simple_dict_with_sd_properties())


class OperationV1SO(_SimpleDBMV1SO):
    execution_start_dt: dt.datetime | None = None
    execution_finish_dt: dt.datetime | None = None
    status: str
    type: str
    input_data: dict[str, Any] = {}
    output_data: dict[str, Any] = {}
    error_data: dict[str, Any] = {}
    duration_total_seconds: float | None = None

    @classmethod
    def from_operation_dbm(cls, *, operation_dbm: OperationDBM) -> OperationV1SO:
        return cls.model_validate(operation_dbm.simple_dict_with_sd_properties())
