from datetime import timedelta, time

from arpakitlib.ar_operation_execution_util import ScheduledOperation, every_timedelta_is_time_func, \
    between_different_times_is_time_func
from arpakitlib.ar_sqlalchemy_model_util import BaseOperationTypes
from src.core.settings import get_cached_settings

SCHEDULED_OPERATIONS = []

if get_cached_settings().is_mode_type_not_prod:
    healthcheck_1_scheduled_operation = ScheduledOperation(
        type=BaseOperationTypes.healthcheck_,
        input_data={"healthcheck_1": "healthcheck_1"},
        is_time_func=every_timedelta_is_time_func(td=timedelta(seconds=15))
    )
    SCHEDULED_OPERATIONS.append(healthcheck_1_scheduled_operation)

healthcheck_2_scheduled_operation = ScheduledOperation(
    type=BaseOperationTypes.healthcheck_,
    input_data={"healthcheck_2": "healthcheck_2"},
    is_time_func=between_different_times_is_time_func(
        from_time=time(hour=0, minute=0),
        to_time=time(hour=0, minute=30)
    ),
    timeout_after_creation=timedelta(seconds=60)
)
SCHEDULED_OPERATIONS.append(healthcheck_2_scheduled_operation)

# ...
