from __future__ import annotations

import datetime as dt
from typing import Any

from src.api.schema.base_schema import BaseSO
from src.sqlalchemy_db.sqlalchemy_model import OperationDBM, StoryLogDBM


class BaseV1SO(BaseSO):
    pass



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
