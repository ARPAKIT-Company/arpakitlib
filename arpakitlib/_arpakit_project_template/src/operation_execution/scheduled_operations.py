from datetime import timedelta

from arpakitlib.ar_operation_execution_util import ScheduledOperation, is_time_func_every_timedelta
from arpakitlib.ar_sqlalchemy_model_util import BaseOperationTypes

ALL_SCHEDULED_OPERATIONS = []

healthcheck_operation = ScheduledOperation(
    type=BaseOperationTypes.healthcheck_,
    input_data={},
    is_time_func=is_time_func_every_timedelta(td=timedelta(seconds=5))
)
ALL_SCHEDULED_OPERATIONS.append(healthcheck_operation)
