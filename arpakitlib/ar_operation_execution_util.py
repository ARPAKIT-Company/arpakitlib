# arpakit

from __future__ import annotations

import asyncio
import logging
import traceback
from datetime import timedelta, time
from typing import Any, Callable

from pydantic import ConfigDict
from pydantic.v1 import BaseModel
from sqlalchemy import asc
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from arpakitlib.ar_base_worker_util import BaseWorker
from arpakitlib.ar_datetime_util import now_utc_dt
from arpakitlib.ar_dict_util import combine_dicts
from arpakitlib.ar_sleep_util import sync_safe_sleep, async_safe_sleep
from arpakitlib.ar_sqlalchemy_model_util import OperationDBM, StoryLogDBM, BaseOperationTypes
from arpakitlib.ar_sqlalchemy_util import SQLAlchemyDB
from arpakitlib.ar_type_util import raise_for_type

_ARPAKIT_LIB_MODULE_VERSION = "3.0"

_logger = logging.getLogger(__name__)


def get_operation_for_execution(
        *,
        session: Session | None = None,
        sqlalchemy_db: SQLAlchemyDB | None = None,
        filter_operation_types: list[str] | str | None = None,
        lock: bool = False
) -> OperationDBM | None:
    if isinstance(filter_operation_types, str):
        filter_operation_types = [filter_operation_types]

    def func(session_: Session):
        query = (
            session_
            .query(OperationDBM)
            .filter(OperationDBM.status == OperationDBM.Statuses.waiting_for_execution)
        )
        if filter_operation_types:
            query = query.filter(OperationDBM.type.in_(filter_operation_types))

        if lock:
            query = query.with_for_update()

        query = query.order_by(asc(OperationDBM.creation_dt))
        operation_dbm: OperationDBM | None = query.first()
        return operation_dbm

    if session is not None:
        return func(session_=session)
    elif sqlalchemy_db is not None:
        with sqlalchemy_db.new_session() as session:
            return func(session_=session)
    else:
        raise ValueError("session is None and sqlalchemy_db is None")


def get_operation_by_id(
        *,
        session: Session | None = None,
        sqlalchemy_db: SQLAlchemyDB | None = None,
        filter_operation_id: int,
        raise_if_not_found: bool = False,
        lock: bool = False
) -> OperationDBM | None:
    def func(session_: Session):
        query = (
            session_
            .query(OperationDBM)
            .filter(OperationDBM.id == filter_operation_id)
        )

        if lock:
            query = query.with_for_update()

        if raise_if_not_found:
            try:
                return query.one()
            except NoResultFound:
                if raise_if_not_found:
                    raise ValueError("Operation not found")
        else:
            return query.one_or_none()

    if session is not None:
        return func(session_=session)
    elif sqlalchemy_db is not None:
        with sqlalchemy_db.new_session() as session:
            return func(session_=session)
    else:
        raise ValueError("session is None and sqlalchemy_db is None")


def remove_operations(
        *,
        session: Session | None = None,
        sqlalchemy_db: SQLAlchemyDB | None = None,
        filter_operation_ids: list[int] | int | None = None,
        filter_operation_types: list[str] | str | None = None,
        filter_operation_statuses: list[str] | str | None = None
):
    if isinstance(filter_operation_ids, int):
        filter_operation_ids = [filter_operation_ids]
    if isinstance(filter_operation_types, str):
        filter_operation_types = [filter_operation_types]
    if isinstance(filter_operation_statuses, str):
        filter_operation_statuses = [filter_operation_statuses]

    if filter_operation_ids is not None:
        raise_for_type(filter_operation_ids, list)
    if filter_operation_types is not None:
        raise_for_type(filter_operation_types, list)
    if filter_operation_statuses is not None:
        raise_for_type(filter_operation_statuses, list)

    def func(session_: Session):
        query = session_.query(OperationDBM)
        if filter_operation_ids is not None:
            query = query.filter(OperationDBM.id.in_(filter_operation_ids))
        if filter_operation_types is not None:
            query = query.filter(OperationDBM.type.in_(filter_operation_types))
        if filter_operation_statuses is not None:
            query = query.filter(OperationDBM.status.in_(filter_operation_statuses))
        query.delete()
        session_.commit()

    if session is not None:
        return func(session_=session)
    elif sqlalchemy_db is not None:
        with sqlalchemy_db.new_session() as session:
            return func(session_=session)
    else:
        raise ValueError("session is None and sqlalchemy_db is None")


class BaseOperationExecutor:
    def __init__(self, *, sqlalchemy_db: SQLAlchemyDB):
        self._logger = logging.getLogger(self.__class__.__name__)
        self.sql_alchemy_db = sqlalchemy_db

    def sync_execute_operation(self, operation_dbm: OperationDBM, session: Session) -> OperationDBM:
        if operation_dbm.type == BaseOperationTypes.healthcheck_:
            self._logger.info("healthcheck")
        elif operation_dbm.type == BaseOperationTypes.raise_fake_exception_:
            self._logger.info("raise_fake_exception")
            raise Exception("raise_fake_exception")
        return operation_dbm

    def sync_safe_execute_operation(
            self, operation_dbm: OperationDBM, worker: OperationExecutorWorker, session: Session
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
                worker.worker_fullname: True
            }
        )
        session.commit()

        exception: BaseException | None = None
        traceback_str: str | None = None

        try:
            self.sync_execute_operation(operation_dbm=operation_dbm, session=session)
        except BaseException as exception_:
            self._logger.error(
                f"error in sync_execute_operation (id={operation_dbm.id}, type={operation_dbm.type})",
                exc_info=exception_
            )
            exception = exception_
            traceback_str = traceback.format_exc()

        operation_dbm.execution_finish_dt = now_utc_dt()
        if exception:
            operation_dbm.status = OperationDBM.Statuses.executed_with_error
            operation_dbm.error_data = combine_dicts(
                {
                    "exception_str": str(exception),
                    "traceback_str": traceback_str
                },
                operation_dbm.error_data
            )
        else:
            operation_dbm.status = OperationDBM.Statuses.executed_without_error
        session.commit()

        if exception:
            story_log_dbm = StoryLogDBM(
                level=StoryLogDBM.Levels.error,
                title=f"error in sync_execute_operation (id={operation_dbm.id}, type={operation_dbm.type})",
                data={
                    "operation_id": operation_dbm.id,
                    "exception_str": str(exception),
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

    async def async_execute_operation(self, operation_dbm: OperationDBM, session: Session) -> OperationDBM:
        if operation_dbm.type == BaseOperationTypes.healthcheck_:
            self._logger.info("healthcheck")
        elif operation_dbm.type == BaseOperationTypes.raise_fake_exception_:
            self._logger.info("raise_fake_exception")
            raise Exception("raise_fake_exception")
        return operation_dbm

    async def async_safe_execute_operation(
            self, operation_dbm: OperationDBM, worker: OperationExecutorWorker, session: Session
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
                worker.worker_fullname: True
            }
        )
        session.commit()

        exception: BaseException | None = None
        traceback_str: str | None = None

        try:
            await self.async_execute_operation(operation_dbm=operation_dbm, session=session)
        except BaseException as exception_:
            self._logger.error(
                f"error in async_execute_operation (id={operation_dbm.id}, type={operation_dbm.type})",
                exc_info=exception_
            )
            exception = exception_
            traceback_str = traceback.format_exc()

        operation_dbm.execution_finish_dt = now_utc_dt()
        if exception:
            operation_dbm.status = OperationDBM.Statuses.executed_with_error
            operation_dbm.error_data = combine_dicts(
                {
                    "exception_str": str(exception),
                    "traceback_str": traceback_str
                },
                operation_dbm.error_data
            )
        else:
            operation_dbm.status = OperationDBM.Statuses.executed_without_error
        session.commit()

        if exception:
            story_log_dbm = StoryLogDBM(
                level=StoryLogDBM.Levels.error,
                title=f"error in async_execute_operation (id={operation_dbm.id}, type={operation_dbm.type})",
                data={
                    "operation_id": operation_dbm.id,
                    "exception_str": str(exception),
                    "traceback_str": traceback_str
                }
            )
            session.add(story_log_dbm)
            session.commit()

        session.refresh(operation_dbm)

        self._logger.info(
            f"finish async_safe_execute_operation, "
            f"operation_dbm.id={operation_dbm.id}, "
            f"operation_dbm.type={operation_dbm.type}, "
            f"operation_dbm.status={operation_dbm.status}, "
            f"operation_dbm.duration={operation_dbm.duration}"
        )

        return operation_dbm


class OperationExecutorWorker(BaseWorker):

    def __init__(
            self,
            *,
            sqlalchemy_db: SQLAlchemyDB,
            operation_executor: BaseOperationExecutor | None = None,
            filter_operation_types: str | list[str] | None = None,
            startup_funcs: list[Any] | None = None
    ):
        super().__init__(startup_funcs=startup_funcs)
        self.sqlalchemy_db = sqlalchemy_db
        if operation_executor is None:
            operation_executor = BaseOperationExecutor(sqlalchemy_db=sqlalchemy_db)
        self.operation_executor = operation_executor
        if isinstance(filter_operation_types, str):
            filter_operation_types = [filter_operation_types]
        self.filter_operation_types = filter_operation_types

    def sync_on_startup(self):
        self.sqlalchemy_db.init()
        self.sync_run_startup_funcs()

    def sync_execute_operation(self, operation_dbm: OperationDBM, session: Session) -> OperationDBM:
        return self.operation_executor.sync_safe_execute_operation(
            operation_dbm=operation_dbm, worker=self, session=session
        )

    def sync_run(self):
        with self.sqlalchemy_db.new_session() as session:
            operation_dbm: OperationDBM | None = get_operation_for_execution(
                session=session,
                filter_operation_types=self.filter_operation_types,
                lock=True
            )
            if not operation_dbm:
                return
            self.sync_execute_operation(operation_dbm=operation_dbm, session=session)

    async def async_on_startup(self):
        self.sqlalchemy_db.init()
        await self.async_run_startup_funcs()

    async def async_execute_operation(self, operation_dbm: OperationDBM, session: Session) -> OperationDBM:
        return await self.operation_executor.async_safe_execute_operation(
            operation_dbm=operation_dbm, worker=self, session=session
        )

    async def async_run(self):
        with self.sqlalchemy_db.new_session() as session:
            operation_dbm: OperationDBM | None = get_operation_for_execution(
                sqlalchemy_db=self.sqlalchemy_db,
                filter_operation_types=self.filter_operation_types,
                lock=True
            )
            if not operation_dbm:
                return
            await self.async_execute_operation(operation_dbm=operation_dbm, session=session)


class ScheduledOperation(BaseModel):
    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True, from_attributes=True)

    type: str
    input_data: dict[str, Any] | None = None
    is_time_func: Callable[[], bool]
    timeout_after_creation: timedelta | None = None


class ScheduledOperationCreatorWorker(BaseWorker):
    def __init__(
            self,
            *,
            sqlalchemy_db: SQLAlchemyDB,
            scheduled_operations: ScheduledOperation | list[ScheduledOperation] | None = None,
            startup_funcs: list[Any] | None = None
    ):
        super().__init__(startup_funcs=startup_funcs)
        self.sqlalchemy_db = sqlalchemy_db
        if scheduled_operations is None:
            scheduled_operations = []
        if isinstance(scheduled_operations, ScheduledOperation):
            scheduled_operations = [scheduled_operations]
        self.scheduled_operations = scheduled_operations

    def sync_on_startup(self):
        self.sqlalchemy_db.init()
        self.sync_run_startup_funcs()

    def sync_run(self):
        timeout = None

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
                self._logger.info(f"scheduled operation (id={operation_dbm.id}) was created")

            if scheduled_operation.timeout_after_creation is not None:
                if timeout is not None:
                    if scheduled_operation.timeout_after_creation > timeout:
                        timeout = scheduled_operation.timeout_after_creation
                else:
                    timeout = scheduled_operation.timeout_after_creation

        if timeout is not None:
            sync_safe_sleep(n=timeout)

    async def async_on_startup(self):
        self.sqlalchemy_db.init()
        await self.async_run_startup_funcs()

    async def async_run(self):
        timeout: timedelta | None = None

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

            if scheduled_operation.timeout_after_creation is not None:
                if timeout is not None:
                    if scheduled_operation.timeout_after_creation > timeout:
                        timeout = scheduled_operation.timeout_after_creation
                else:
                    timeout = scheduled_operation.timeout_after_creation

        if timeout is not None:
            await async_safe_sleep(n=timeout)


def every_timedelta_is_time_func(*, td: timedelta, now_dt_func: Callable = now_utc_dt) -> Callable:
    last_now_utc_dt = now_utc_dt()

    def func() -> bool:
        nonlocal last_now_utc_dt
        now_dt_func_ = now_dt_func()
        if (now_dt_func_ - last_now_utc_dt) >= td:
            last_now_utc_dt = now_dt_func_
            return True
        return False

    return func


def between_different_times_is_time_func(
        *, from_time: time, to_time: time, now_dt_func: Callable = now_utc_dt
) -> Callable:
    def func() -> bool:
        if from_time <= now_dt_func().time() <= to_time:
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
