from arpakitlib.ar_operation_execution_util import ScheduledOperation

from arpakitlib.ar_sqlalchemy_model_util import OperationDBM

SCHEDULED_OPERATIONS = []

operation = ScheduledOperation(
    type=OperationDBM.Types.healthcheck_,
    input_data={},
    is_time_func=lambda: True
)
SCHEDULED_OPERATIONS.append(operation)
