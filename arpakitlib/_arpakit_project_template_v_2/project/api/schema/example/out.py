from __future__ import annotations

import datetime as dt
from typing import Any

from project.api.schema.base_schema import BaseSO
from project.sqlalchemy_db_.sqlalchemy_model import StoryLogDBM, OperationDBM


class BaseExampleSO(BaseSO):
    pass


class SimpleDBMExampleSO(BaseExampleSO):
    id: int
    long_id: str
    slug: str | None
    creation_dt: dt.datetime


class StoryLogExampleSO(SimpleDBMExampleSO):
    level: str
    type: str | None
    title: str | None
    data: dict[str, Any]

    @classmethod
    def from_story_log_dbm(cls, *, story_log_dbm: StoryLogDBM) -> StoryLogExampleSO:
        return cls.model_validate(story_log_dbm.simple_dict_with_sd_properties())


class OperationExampleSO(SimpleDBMExampleSO):
    execution_start_dt: dt.datetime | None
    execution_finish_dt: dt.datetime | None
    status: str
    type: str
    title: str | None
    input_data: dict[str, Any]
    output_data: dict[str, Any]
    error_data: dict[str, Any]
    duration_total_seconds: float | None

    @classmethod
    def from_operation_dbm(cls, *, operation_dbm: OperationDBM) -> OperationExampleSO:
        return cls.model_validate(operation_dbm.simple_dict_with_sd_properties())
