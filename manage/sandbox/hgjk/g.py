import logging

from arpakitlib.ar_logging_util import setup_normal_logging
from arpakitlib.ar_operation_execution_util import OperationExecutorWorker
from arpakitlib.ar_sqlalchemy_util import SQLAlchemyDB
from src.operation_execution.operation_executor import OperationExecutor


def go():
    print(__name__)
    logging.getLogger(__name__).info("hjkl;")
    OperationExecutorWorker(
        operation_executor=OperationExecutor(
            sqlalchemy_db=SQLAlchemyDB(db_url="postgresql://arpakitlib:arpakitlib@127.0.0.1:50517/arpakitlib")
        ),
        sqlalchemy_db=SQLAlchemyDB(db_url="postgresql://arpakitlib:arpakitlib@127.0.0.1:50517/arpakitlib")
    ).sync_safe_run()