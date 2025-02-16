from datetime import timedelta, time
from typing import Any, Callable

from pydantic import ConfigDict
from pydantic.v1 import BaseModel

from src.core.settings import get_cached_settings
from src.operation_execution.const import OperationTypes
from src.operation_execution.util import every_timedelta_is_time_func, between_different_times_is_time_func


class ScheduledOperation(BaseModel):
    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True, from_attributes=True)

    type: str
    input_data: dict[str, Any] | None = None
    is_time_func: Callable[[], bool]
    timeout_after_creation: timedelta | None = None


SCHEDULED_OPERATIONS = []

if get_cached_settings().is_mode_type_not_prod:
    healthcheck_1_scheduled_operation = ScheduledOperation(
        type=OperationTypes.healthcheck_,
        input_data={"healthcheck_1": "healthcheck_1"},
        is_time_func=every_timedelta_is_time_func(td=timedelta(seconds=5))
    )
    SCHEDULED_OPERATIONS.append(healthcheck_1_scheduled_operation)

healthcheck_2_scheduled_operation = ScheduledOperation(
    type=OperationTypes.healthcheck_,
    input_data={"healthcheck_2": "healthcheck_2"},
    is_time_func=between_different_times_is_time_func(
        from_time=time(hour=0, minute=0),
        to_time=time(hour=0, minute=30)
    ),
    timeout_after_creation=timedelta(seconds=60)
)
SCHEDULED_OPERATIONS.append(healthcheck_2_scheduled_operation)
