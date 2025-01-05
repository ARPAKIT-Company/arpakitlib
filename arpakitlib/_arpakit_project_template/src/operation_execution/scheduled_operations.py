from datetime import timedelta

from arpakitlib.ar_operation_execution_util import ScheduledOperation, every_timedelta_is_time_func
from arpakitlib.ar_sqlalchemy_model_util import BaseOperationTypes

ALL_SCHEDULED_OPERATIONS = []

healthcheck_scheduled_operation = ScheduledOperation(
    type=BaseOperationTypes.healthcheck_,
    input_data={},
    is_time_func=every_timedelta_is_time_func(td=timedelta(seconds=5))
)
ALL_SCHEDULED_OPERATIONS.append(healthcheck_scheduled_operation)
