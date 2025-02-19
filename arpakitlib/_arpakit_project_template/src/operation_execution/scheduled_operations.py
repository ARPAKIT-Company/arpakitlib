from datetime import timedelta, time
from typing import Any, Callable

from pydantic import ConfigDict
from pydantic.v1 import BaseModel

from arpakitlib.ar_datetime_util import now_utc_dt
from src.core.settings import get_cached_settings
from src.operation_execution.util import every_timedelta_is_time_func, between_different_times_is_time_func
from src.sqlalchemy_db.sqlalchemy_model import OperationDBM


class ScheduledOperation(BaseModel):
    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True, from_attributes=True)

    type: str
    input_data: dict[str, Any] | None = None
    is_time_func: Callable[[], bool]
    timeout_after_creation: timedelta | None = None


healthcheck_1_scheduled_operation = ScheduledOperation(
    type=OperationDBM.Types.healthcheck_,
    input_data={"healthcheck_1": "healthcheck_1"},
    is_time_func=every_timedelta_is_time_func(td=timedelta(seconds=0.1))
)

healthcheck_2_scheduled_operation = ScheduledOperation(
    type=OperationDBM.Types.healthcheck_,
    input_data={"healthcheck_2": "healthcheck_2"},
    is_time_func=between_different_times_is_time_func(
        from_time=time(hour=0, minute=0),
        to_time=time(hour=0, minute=1),
        now_dt_func=now_utc_dt
    ),
    timeout_after_creation=timedelta(seconds=90)
)

raise_fake_error_1_scheduled_operation = ScheduledOperation(
    type=OperationDBM.Types.raise_fake_error_,
    input_data={"raise_fake_error_1_scheduled_operation": "raise_fake_error_1_scheduled_operation"},
    is_time_func=every_timedelta_is_time_func(td=timedelta(seconds=3))
)


def get_scheduled_operations() -> list[ScheduledOperation]:
    res = []

    if get_cached_settings().is_mode_type_not_prod:
        res.append(healthcheck_1_scheduled_operation)

    res.append(healthcheck_2_scheduled_operation)

    return res
