from __future__ import annotations

import datetime as dt
from typing import Any

from project.api.schema.out.admin.common import SimpleDBMAdminSO
from project.sqlalchemy_db_.sqlalchemy_model import OperationDBM


class OperationAdmin1SO(SimpleDBMAdminSO):
    execution_start_dt: dt.datetime | None
    execution_finish_dt: dt.datetime | None
    status: str
    type: str
    title: str | None
    input_data: dict[str, Any]
    output_data: dict[str, Any]
    error_data: dict[str, Any]

    duration_total_seconds: float | None
    allowed_statuses: list[str]
    allowed_types: list[str]

    @classmethod
    def from_dbm(cls, *, simple_dbm: OperationDBM) -> OperationAdmin1SO:
        return cls.model_validate(simple_dbm.simple_dict_with_sd_properties(
            only_columns_and_sd_properties=cls.model_fields.keys()
        ))
