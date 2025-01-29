from arpakitlib.ar_base_worker_util import safe_run_worker_in_background, SafeRunInBackgroundModes
from arpakitlib.ar_fastapi_util import BaseStartupAPIEvent, BaseShutdownAPIEvent
from arpakitlib.ar_operation_execution_util import OperationExecutorWorker, ScheduledOperationCreatorWorker
from arpakitlib.ar_sqlalchemy_util import SQLAlchemyDB
from arpakitlib.ar_type_util import raise_for_type
from src.api.transmitted_api_data import TransmittedAPIData
from src.operation_execution.operation_executor import OperationExecutor
from src.operation_execution.scheduled_operations import SCHEDULED_OPERATIONS


class StartupAPIEvent(BaseStartupAPIEvent):
    def __init__(self, transmitted_api_data: TransmittedAPIData, **kwargs):
        super().__init__(**kwargs)
        self.transmitted_api_data = transmitted_api_data

    async def async_on_startup(self, *args, **kwargs):
        self._logger.info("start")

        if self.transmitted_api_data.media_file_storage_in_dir is not None:
            self.transmitted_api_data.media_file_storage_in_dir.init()

        if self.transmitted_api_data.cache_file_storage_in_dir is not None:
            self.transmitted_api_data.cache_file_storage_in_dir.init()

        if self.transmitted_api_data.dump_file_storage_in_dir is not None:
            self.transmitted_api_data.dump_file_storage_in_dir.init()

        if self.transmitted_api_data.settings.api_init_sql_db_at_start:
            raise_for_type(self.transmitted_api_data.sqlalchemy_db, SQLAlchemyDB)
            self.transmitted_api_data.sqlalchemy_db.init()

        if self.transmitted_api_data.settings.api_start_operation_executor_worker:
            raise_for_type(self.transmitted_api_data.sqlalchemy_db, SQLAlchemyDB)
            _ = safe_run_worker_in_background(
                worker=OperationExecutorWorker(
                    sqlalchemy_db=self.transmitted_api_data.sqlalchemy_db,
                    operation_executor=OperationExecutor(sqlalchemy_db=self.transmitted_api_data.sqlalchemy_db),
                    filter_operation_types=None
                ),
                mode=SafeRunInBackgroundModes.thread
            )

        if self.transmitted_api_data.settings.api_start_scheduled_operation_creator_worker:
            raise_for_type(self.transmitted_api_data.sqlalchemy_db, SQLAlchemyDB)
            _ = safe_run_worker_in_background(
                worker=ScheduledOperationCreatorWorker(
                    sqlalchemy_db=self.transmitted_api_data.sqlalchemy_db,
                    scheduled_operations=SCHEDULED_OPERATIONS
                ),
                mode=SafeRunInBackgroundModes.async_task
            )

        self._logger.info("finish")


class ShutdownAPIEvent(BaseShutdownAPIEvent):
    def __init__(self, transmitted_api_data: TransmittedAPIData, **kwargs):
        super().__init__(**kwargs)
        self.transmitted_api_data = transmitted_api_data

    async def async_on_shutdown(self, *args, **kwargs):
        self._logger.info("start")
        self._logger.info("finish")
