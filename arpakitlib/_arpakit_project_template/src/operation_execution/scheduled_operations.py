from datetime import timedelta

from arpakitlib.ar_operation_execution_util import ScheduledOperation, every_timedelta
from arpakitlib.ar_sqlalchemy_model_util import BaseOperationTypes

ALL_SCHEDULED_OPERATIONS = []

operation_healthcheck = ScheduledOperation(
    type=BaseOperationTypes.healthcheck_,
    input_data={},
    is_time_func=every_timedelta(td=timedelta(seconds=5))
)
ALL_SCHEDULED_OPERATIONS.append(operation_healthcheck)
