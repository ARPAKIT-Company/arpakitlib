from __future__ import annotations

import datetime as dt
from typing import Any

from project.api.schema.out.admin.common import SimpleDBMAdminCommonSO
from project.sqlalchemy_db_.sqlalchemy_model import OperationDBM


class OperationAdminSO(SimpleDBMAdminCommonSO):
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
    def from_operation_dbm(cls, *, operation_dbm: OperationDBM) -> OperationAdminSO:
        return cls.model_validate(operation_dbm.simple_dict_with_sd_properties())
