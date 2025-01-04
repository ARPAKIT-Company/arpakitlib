# arpakit

from __future__ import annotations

import asyncio
import logging
import traceback
from datetime import timedelta
from typing import Any, Callable

from pydantic import ConfigDict
from pydantic.v1 import BaseModel
from sqlalchemy import asc
from sqlalchemy.orm import Session

from arpakitlib.ar_base_worker_util import BaseWorker
from arpakitlib.ar_datetime_util import now_utc_dt
from arpakitlib.ar_dict_util import combine_dicts
from arpakitlib.ar_sqlalchemy_model_util import OperationDBM, StoryLogDBM, BaseOperationTypes
from arpakitlib.ar_sqlalchemy_util import SQLAlchemyDB

_ARPAKIT_LIB_MODULE_VERSION = "3.0"

_logger = logging.getLogger(__name__)


def get_operation_for_execution(
        *,
        sqlalchemy_db: SQLAlchemyDB,
        filter_operation_types: list[str] | str | None = None
) -> OperationDBM | None:
    if isinstance(filter_operation_types, str):
        filter_operation_types = [filter_operation_types]
    with sqlalchemy_db.new_session() as session:
        query = (
            session
            .query(OperationDBM)
            .filter(OperationDBM.status == OperationDBM.Statuses.waiting_for_execution)
        )
        if filter_operation_types:
            query = query.filter(OperationDBM.type.in_(filter_operation_types))
        query = query.order_by(asc(OperationDBM.creation_dt))
        operation_dbm: OperationDBM | None = query.first()
    return operation_dbm


def get_operation_by_id(
        *,
        session: Session,
        filter_operation_id: int,
        raise_if_not_found: bool = False
) -> OperationDBM | None:
    query = (
        session
        .query(OperationDBM)
        .filter(OperationDBM.id == filter_operation_id)
    )
    if raise_if_not_found:
        return query.one()
    else:
        return query.one_or_none()


class BaseOperationExecutor:
    def __init__(self, *, sqlalchemy_db: SQLAlchemyDB):
        self._logger = logging.getLogger(self.__class__.__name__)
        self.sql_alchemy_db = sqlalchemy_db

    def sync_execute_operation(self, operation_dbm: OperationDBM) -> OperationDBM:
        if operation_dbm.type == BaseOperationTypes.healthcheck_:
            self._logger.info("healthcheck")
        elif operation_dbm.type == BaseOperationTypes.raise_fake_exception_:
            self._logger.info("raise_fake_exception")
            raise Exception("raise_fake_exception")
        return operation_dbm

    def sync_safe_execute_operation(self, operation_dbm: OperationDBM) -> OperationDBM:
        self._logger.info(
            f"start sync_safe_execute_operation"
            f", operation_dbm.id={operation_dbm.id}"
            f", operation_dbm.type={operation_dbm.type}"
        )

        with self.sql_alchemy_db.new_session() as session:
            operation_dbm: OperationDBM = get_operation_by_id(
                session=session, filter_operation_id=operation_dbm.id, raise_if_not_found=True
            )
            operation_dbm.execution_start_dt = now_utc_dt()
            operation_dbm.status = OperationDBM.Statuses.executing
            session.commit()
            session.refresh(operation_dbm)

        exception: BaseException | None = None
        traceback_str: str | None = None

        try:
            self.sync_execute_operation(operation_dbm=operation_dbm)
        except BaseException as exception_:
            self._logger.error(f"Error while executing operation (id={operation_dbm.id})", exc_info=exception_)
            exception = exception_
            traceback_str = traceback.format_exc()

        with self.sql_alchemy_db.new_session() as session:

            operation_dbm: OperationDBM = get_operation_by_id(
                session=session, filter_operation_id=operation_dbm.id, raise_if_not_found=True
            )
            operation_dbm.execution_finish_dt = now_utc_dt()
            if exception:
                operation_dbm.status = OperationDBM.Statuses.executed_with_error
                operation_dbm.error_data = combine_dicts(
                    {"exception": str(exception), "traceback_str": traceback_str},
                    operation_dbm.error_data
                )
            else:
                operation_dbm.status = OperationDBM.Statuses.executed_without_error
            session.commit()

            if exception:
                story_log_dbm = StoryLogDBM(
                    level=StoryLogDBM.Levels.error,
                    title=f"Error while executing operation (id={operation_dbm.id}, type={operation_dbm.type})",
                    data={
                        "operation_id": operation_dbm.id,
                        "exception_str": str(exception),
                        "traceback_str": traceback_str
                    }
                )
                session.add(story_log_dbm)
                session.commit()
                session.refresh(story_log_dbm)

            session.refresh(operation_dbm)

        self._logger.info(
            f"finish sync_safe_execute_operation"
            f", operation_dbm.id={operation_dbm.id}"
            f", operation_dbm.type={operation_dbm.type}"
            f", operation_dbm.status={operation_dbm.status}"
            f", operation_dbm.duration={operation_dbm.duration}"
        )

        return operation_dbm

    async def async_execute_operation(self, operation_dbm: OperationDBM) -> OperationDBM:
        if operation_dbm.type == BaseOperationTypes.healthcheck_:
            self._logger.info("healthcheck")
        elif operation_dbm.type == BaseOperationTypes.raise_fake_exception_:
            self._logger.info("raise_fake_exception")
            raise Exception("raise_fake_exception")
        return operation_dbm

    async def async_safe_execute_operation(self, operation_dbm: OperationDBM) -> OperationDBM:
        self._logger.info(
            f"start async_safe_execute_operation"
            f", operation_dbm.id={operation_dbm.id}"
            f", operation_dbm.type={operation_dbm.type}"
        )

        with self.sql_alchemy_db.new_session() as session:
            operation_dbm: OperationDBM = get_operation_by_id(
                session=session, filter_operation_id=operation_dbm.id, raise_if_not_found=True
            )
            operation_dbm.execution_start_dt = now_utc_dt()
            operation_dbm.status = OperationDBM.Statuses.executing
            session.commit()
            session.refresh(operation_dbm)

        exception: BaseException | None = None
        traceback_str: str | None = None

        try:
            await self.async_execute_operation(operation_dbm=operation_dbm)
        except BaseException as exception_:
            self._logger.error(f"Error while executing operation (id={operation_dbm.id})", exc_info=exception_)
            exception = exception_
            traceback_str = traceback.format_exc()

        with self.sql_alchemy_db.new_session() as session:

            operation_dbm: OperationDBM = get_operation_by_id(
                session=session, filter_operation_id=operation_dbm.id, raise_if_not_found=True
            )
            operation_dbm.execution_finish_dt = now_utc_dt()
            if exception:
                operation_dbm.status = OperationDBM.Statuses.executed_with_error
                operation_dbm.error_data = combine_dicts(
                    {"exception": str(exception), "traceback_str": traceback_str},
                    operation_dbm.error_data
                )
            else:
                operation_dbm.status = OperationDBM.Statuses.executed_without_error
            session.commit()

            if exception:
                story_log_dbm = StoryLogDBM(
                    level=StoryLogDBM.Levels.error,
                    title=f"Error while executing operation (id={operation_dbm.id}, type={operation_dbm.type})",
                    data={
                        "operation_id": operation_dbm.id,
                        "exception_str": str(exception),
                        "traceback_str": traceback_str
                    }
                )
                session.add(story_log_dbm)
                session.commit()
                session.refresh(story_log_dbm)

            session.refresh(operation_dbm)

        self._logger.info(
            f"finish async_safe_execute_operation"
            f", operation_dbm.id={operation_dbm.id}"
            f", operation_dbm.type={operation_dbm.type}"
            f", operation_dbm.status={operation_dbm.status}"
            f", operation_dbm.duration={operation_dbm.duration}"
        )

        return operation_dbm


class ExecuteOperationWorker(BaseWorker):

    def __init__(
            self,
            *,
            sqlalchemy_db: SQLAlchemyDB,
            operation_executor: BaseOperationExecutor | None = None,
            filter_operation_types: str | list[str] | None = None,
            timeout_after_run=timedelta(seconds=0.1).total_seconds(),
            timeout_after_err_in_run=timedelta(seconds=1).total_seconds()
    ):
        super().__init__()
        self.sqlalchemy_db = sqlalchemy_db
        self.timeout_after_run = timeout_after_run
        self.timeout_after_err_in_run = timeout_after_err_in_run
        if operation_executor is None:
            operation_executor = BaseOperationExecutor(sqlalchemy_db=sqlalchemy_db)
        self.operation_executor = operation_executor
        self.filter_operation_types = filter_operation_types

    def sync_on_startup(self):
        self.sqlalchemy_db.init()

    def sync_execute_operation(self, operation_dbm: OperationDBM) -> OperationDBM:
        return self.operation_executor.sync_safe_execute_operation(operation_dbm=operation_dbm)

    def sync_run(self):
        operation_dbm: OperationDBM | None = get_operation_for_execution(
            sqlalchemy_db=self.sqlalchemy_db,
            filter_operation_types=self.filter_operation_types
        )

        if not operation_dbm:
            return

        self.sync_execute_operation(operation_dbm=operation_dbm)

    def sync_run_on_error(self, exception: BaseException, **kwargs):
        self._logger.exception(exception)

    async def async_on_startup(self):
        self.sqlalchemy_db.init()

    async def async_execute_operation(self, operation_dbm: OperationDBM) -> OperationDBM:
        return await self.operation_executor.async_safe_execute_operation(operation_dbm=operation_dbm)

    async def async_run(self):
        operation_dbm: OperationDBM | None = get_operation_for_execution(
            sqlalchemy_db=self.sqlalchemy_db,
            filter_operation_types=self.filter_operation_types
        )

        if not operation_dbm:
            return

        await self.async_execute_operation(operation_dbm=operation_dbm)

    async def async_run_on_error(self, exception: BaseException, **kwargs):
        self._logger.exception(exception)


class ScheduledOperation(BaseModel):
    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True, from_attributes=True)

    type: str
    input_data: dict[str, Any] | None = None
    is_time_func: Callable[[], bool]


class CreateScheduledOperationWorker(BaseWorker):
    def __init__(
            self,
            *,
            sqlalchemy_db: SQLAlchemyDB,
            scheduled_operations: list[ScheduledOperation] | None = None,
            timeout_after_run=timedelta(seconds=0.1).total_seconds(),
            timeout_after_err_in_run=timedelta(seconds=1).total_seconds()
    ):
        super().__init__()
        self.sqlalchemy_db = sqlalchemy_db
        self.timeout_after_run = timeout_after_run
        self.timeout_after_err_in_run = timeout_after_err_in_run
        if scheduled_operations is None:
            scheduled_operations = []
        self.scheduled_operations = scheduled_operations

    def sync_on_startup(self):
        self.sqlalchemy_db.init()

    def sync_run(self):
        for scheduled_operation in self.scheduled_operations:
            if not scheduled_operation.is_time_func():
                continue
            with self.sqlalchemy_db.new_session() as session:
                operation_dbm = OperationDBM(
                    type=scheduled_operation.type,
                    input_data=scheduled_operation.input_data
                )
                session.add(operation_dbm)
                session.commit()
                session.refresh(operation_dbm)

    def async_on_startup(self):
        self.sqlalchemy_db.init()

    def async_run(self):
        for scheduled_operation in self.scheduled_operations:
            if not scheduled_operation.is_time_func():
                continue
            with self.sqlalchemy_db.new_session() as session:
                operation_dbm = OperationDBM(
                    type=scheduled_operation.type,
                    input_data=scheduled_operation.input_data
                )
                session.add(operation_dbm)
                session.commit()
                session.refresh(operation_dbm)


def is_time_func_every_timedelta(*, td: timedelta) -> Callable:
    last_now_utc_dt = now_utc_dt()

    def func() -> bool:
        nonlocal last_now_utc_dt
        now_utc_dt_ = now_utc_dt()
        if (now_utc_dt_ - last_now_utc_dt) >= td:
            last_now_utc_dt = now_utc_dt_
            return True
        return False

    return func


def __example():
    pass


async def __async_example():
    pass


if __name__ == '__main__':
    __example()
    asyncio.run(__async_example())
