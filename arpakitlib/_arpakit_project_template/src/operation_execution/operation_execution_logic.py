import logging
import traceback

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from arpakitlib.ar_datetime_util import now_utc_dt
from arpakitlib.ar_dict_util import combine_dicts
from arpakitlib.ar_sqlalchemy_util import SQLAlchemyDb
from src.operation_execution.const import OperationTypes
from src.sqlalchemy_db.sqlalchemy_model import OperationDBM, StoryLogDBM


class OperationExecutionLogic:
    def __init__(self, *, sqlalchemy_db: SQLAlchemyDb, **kwargs):
        self._logger = logging.getLogger(self.__class__.__name__)
        self.sqlalchemy_db = sqlalchemy_db

    def sync_execute_operation(self, operation_dbm: OperationDBM, session: Session) -> OperationDBM:
        if operation_dbm.type == OperationTypes.healthcheck_:
            self._logger.info("healthcheck")
        elif operation_dbm.type == OperationTypes.raise_fake_exception_:
            self._logger.info("raise_fake_exception")
            raise Exception("raise_fake_exception")
        return operation_dbm

    def sync_safe_execute_operation(
            self, *, operation_dbm: OperationDBM, executor_name: str, session: Session
    ) -> OperationDBM:
        self._logger.info(
            f"start "
            f"operation_dbm.id={operation_dbm.id}, "
            f"operation_dbm.type={operation_dbm.type}, "
            f"operation_dbm.status={operation_dbm.status}"
        )

        operation_dbm.execution_start_dt = now_utc_dt()
        operation_dbm.status = OperationDBM.Statuses.executing
        operation_dbm.output_data = combine_dicts(
            operation_dbm.output_data,
            {
                executor_name: True
            }
        )
        session.commit()

        exception_in_sync_execute_operation: Exception | None = None
        traceback_str: str | None = None

        try:
            self.sync_execute_operation(operation_dbm=operation_dbm, session=session)
        except Exception as exception_:
            self._logger.error(
                f"exception in sync_execute_operation (id={operation_dbm.id}, type={operation_dbm.type})",
                exc_info=True
            )
            exception_in_sync_execute_operation = exception_
            traceback_str = traceback.format_exc()

        operation_dbm.execution_finish_dt = now_utc_dt()
        if exception_in_sync_execute_operation:
            operation_dbm.status = OperationDBM.Statuses.executed_with_error
            operation_dbm.error_data = combine_dicts(
                {
                    "exception_str": str(exception_in_sync_execute_operation),
                    "traceback_str": traceback_str,
                    "sync_safe_execute_operation": True
                },
                operation_dbm.error_data
            )
        else:
            operation_dbm.status = OperationDBM.Statuses.executed_without_error
        session.commit()

        if exception_in_sync_execute_operation:
            story_log_dbm = StoryLogDBM(
                level=StoryLogDBM.Levels.error,
                title=f"error in sync_execute_operation (id={operation_dbm.id}, type={operation_dbm.type})",
                data={
                    "operation_id": operation_dbm.id,
                    "exception_str": str(exception_in_sync_execute_operation),
                    "traceback_str": traceback_str
                }
            )
            session.add(story_log_dbm)
            session.commit()

        session.refresh(operation_dbm)

        self._logger.info(
            f"finish sync_safe_execute_operation, "
            f"operation_dbm.id={operation_dbm.id}, "
            f"operation_dbm.type={operation_dbm.type}, "
            f"operation_dbm.status={operation_dbm.status}, "
            f"operation_dbm.duration={operation_dbm.duration}"
        )

        return operation_dbm

    async def async_execute_operation(
            self, *, operation_dbm: OperationDBM, async_session: AsyncSession
    ) -> OperationDBM:
        if operation_dbm.type == OperationTypes.healthcheck_:
            self._logger.info("healthcheck")
        elif operation_dbm.type == OperationTypes.raise_fake_exception_:
            self._logger.info("raise_fake_exception")
            raise Exception("raise_fake_exception")
        return operation_dbm

    async def async_safe_execute_operation(
            self, *, operation_dbm: OperationDBM, executor_name: str, async_session: AsyncSession
    ) -> OperationDBM:
        self._logger.info(
            f"start "
            f"operation_dbm.id={operation_dbm.id}, "
            f"operation_dbm.type={operation_dbm.type}, "
            f"operation_dbm.status={operation_dbm.status}"
        )

        operation_dbm.execution_start_dt = now_utc_dt()
        operation_dbm.status = OperationDBM.Statuses.executing
        operation_dbm.output_data = combine_dicts(
            operation_dbm.output_data,
            {
                executor_name: True
            }
        )
        await async_session.commit()

        exception_in_async_execute_operation: Exception | None = None
        traceback_str: str | None = None

        try:
            await self.async_execute_operation(operation_dbm=operation_dbm, async_session=async_session)
        except Exception as exception_:
            self._logger.error(
                f"exception in async_execute_operation (id={operation_dbm.id}, type={operation_dbm.type})",
                exc_info=True
            )
            exception_in_async_execute_operation = exception_
            traceback_str = traceback.format_exc()

        operation_dbm.execution_finish_dt = now_utc_dt()
        if exception_in_async_execute_operation:
            operation_dbm.status = OperationDBM.Statuses.executed_with_error
            operation_dbm.error_data = combine_dicts(
                {
                    "exception_str": str(exception_in_async_execute_operation),
                    "traceback_str": traceback_str,
                    "async_safe_execute_operation": True
                },
                operation_dbm.error_data
            )
        else:
            operation_dbm.status = OperationDBM.Statuses.executed_without_error
        await async_session.commit()

        if exception_in_async_execute_operation:
            story_log_dbm = StoryLogDBM(
                level=StoryLogDBM.Levels.error,
                title=f"error in async_execute_operation (id={operation_dbm.id}, type={operation_dbm.type})",
                data={
                    "operation_id": operation_dbm.id,
                    "exception_str": str(exception_in_async_execute_operation),
                    "traceback_str": traceback_str
                }
            )
            async_session.add(story_log_dbm)
            await async_session.commit()

        await async_session.refresh(operation_dbm)

        self._logger.info(
            f"finish async_safe_execute_operation, "
            f"operation_dbm.id={operation_dbm.id}, "
            f"operation_dbm.type={operation_dbm.type}, "
            f"operation_dbm.status={operation_dbm.status}, "
            f"operation_dbm.duration={operation_dbm.duration}"
        )

        return operation_dbm
