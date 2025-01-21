from sqlalchemy.orm import Session

from arpakitlib.ar_operation_execution_util import BaseOperationExecutor
from arpakitlib.ar_sqlalchemy_model_util import OperationDBM


class OperationExecutor(BaseOperationExecutor):
    def sync_execute_operation(self, operation_dbm: OperationDBM, session: Session) -> OperationDBM:
        # ...
        operation_dbm = super().sync_execute_operation(operation_dbm=operation_dbm, session=session)
        return operation_dbm

    async def async_execute_operation(self, operation_dbm: OperationDBM, session: Session) -> OperationDBM:
        # ...
        operation_dbm = await super().async_execute_operation(operation_dbm=operation_dbm, session=session)
        return operation_dbm
