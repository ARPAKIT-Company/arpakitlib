# arpakit

from __future__ import annotations

import logging
import traceback
from datetime import datetime, timedelta
from typing import Any

from sqlalchemy import TIMESTAMP, TEXT, asc
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, Session

from arpakitlib.ar_base_worker import BaseWorker
from arpakitlib.ar_datetime_util import now_utc_dt
from arpakitlib.ar_dict_util import combine_dicts
from arpakitlib.ar_easy_sqlalchemy_util import EasySQLAlchemyDB
from arpakitlib.ar_enumeration import EasyEnumeration
from arpakitlib.ar_fastapi_util import BaseAPISimpleSO
from arpakitlib.ar_sqlalchemy_model_util import SimpleDBM
from arpakitlib.ar_story_log_util import StoryLogDBM

_ARPAKIT_LIB_MODULE_VERSION = "3.0"

_logger = logging.getLogger(__name__)


class OperationDBM(SimpleDBM):
    __tablename__ = "operation"

    class Statuses(EasyEnumeration):
        waiting_for_execution = "waiting_for_execution"
        executing = "executing"
        executed_without_error = "executed_without_error"
        executed_with_error = "executed_with_error"

    class Types(EasyEnumeration):
        healthcheck_ = "healthcheck"
        raise_fake_exception = "raise_fake_exception"

    status: Mapped[str] = mapped_column(
        TEXT, index=True, insert_default=Statuses.waiting_for_execution,
        server_default=Statuses.waiting_for_execution, nullable=False
    )
    type: Mapped[str] = mapped_column(
        TEXT, index=True, insert_default=Types.healthcheck_, nullable=False
    )
    execution_start_dt: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    execution_finish_dt: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    input_data: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        insert_default={},
        server_default="{}",
        nullable=False
    )
    output_data: Mapped[dict[str, Any]] = mapped_column(JSONB, insert_default={}, server_default="{}", nullable=False)
    error_data: Mapped[dict[str, Any]] = mapped_column(JSONB, insert_default={}, server_default="{}", nullable=False)

    def raise_if_executed_with_error(self):
        if self.status == self.Statuses.executed_with_error:
            raise Exception(
                f"Operation (id={self.id}, type={self.type}) executed with error, error_data={self.error_data}"
            )

    def raise_if_error_data(self):
        if self.status == self.Statuses.executed_with_error:
            raise Exception(
                f"Operation (id={self.id}, type={self.type}) has error_data, error_data={self.error_data}"
            )

    @property
    def duration(self) -> timedelta | None:
        if self.execution_start_dt is None or self.execution_finish_dt is None:
            return None
        return self.execution_finish_dt - self.execution_start_dt

    @property
    def duration_total_seconds(self) -> float | None:
        if self.duration is None:
            return None
        return self.duration.total_seconds()


class OperationSO(BaseAPISimpleSO):
    execution_start_dt: datetime | None
    execution_finish_dt: datetime | None
    status: str
    type: str
    input_data: dict[str, Any]
    output_data: dict[str, Any]
    error_data: dict[str, Any]
    duration_total_seconds: float | None


def get_operation_for_execution(
        *,
        easy_sql_alchemy_db: EasySQLAlchemyDB,
        filter_operation_type: str | None = None
) -> OperationDBM | None:
    with easy_sql_alchemy_db.new_session() as session:
        query = (
            session
            .query(OperationDBM)
            .filter(OperationDBM.status == OperationDBM.Statuses.waiting_for_execution)
        )
        if filter_operation_type:
            query = query.filter(OperationDBM.type == filter_operation_type)
        query = query.order_by(asc(OperationDBM.creation_dt))
        operation_dbm: OperationDBM | None = query.first()
    return operation_dbm


def get_operation_by_id(
        *,
        session: Session,
        filter_operation_id: int,
        strict: bool = False
) -> OperationDBM | None:
    query = (
        session
        .query(OperationDBM)
        .filter(OperationDBM.id == filter_operation_id)
    )
    if strict:
        return query.one()
    else:
        return query.one_or_none()


class BaseOperationExecutor:
    def __init__(self, *, easy_sql_alchemy_db: EasySQLAlchemyDB):
        self._logger = logging.getLogger(self.__class__.__name__)
        self.easy_sql_alchemy_db = easy_sql_alchemy_db

    async def async_execute_operation(self, operation_dbm: OperationDBM) -> OperationDBM:
        if operation_dbm.type == OperationDBM.Types.healthcheck_:
            self._logger.info("healthcheck")
        elif operation_dbm.type == OperationDBM.Types.raise_fake_exception:
            self._logger.info("raise_fake_exception")
            raise Exception("raise_fake_exception")
        else:
            raise ValueError(f"unknown operation.type = {operation_dbm.type}")
        return operation_dbm

    async def async_safe_execute_operation(self, operation_dbm: OperationDBM) -> OperationDBM:
        self._logger.info(
            f"start async_safe_execute_operation"
            f", operation_dbm.id={operation_dbm.id}"
            f", operation_dbm.type={operation_dbm.type}"
        )

        with self.easy_sql_alchemy_db.new_session() as session:
            operation_dbm: OperationDBM = get_operation_by_id(
                session=session, filter_operation_id=operation_dbm.id, strict=True
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
            self._logger.exception(exception_)
            exception = exception_
            traceback_str = traceback.format_exc()

        with self.easy_sql_alchemy_db.new_session() as session:
            operation_dbm: OperationDBM = get_operation_by_id(
                session=session, filter_operation_id=operation_dbm.id, strict=True
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
            session.refresh(operation_dbm)

        self._logger.info(
            f"finish async_safe_execute_operation"
            f", operation_dbm.id={operation_dbm.id}"
            f", operation_dbm.type={operation_dbm.type}"
        )

        return operation_dbm

    def sync_execute_operation(self, operation_dbm: OperationDBM) -> OperationDBM:
        if operation_dbm.type == OperationDBM.Types.healthcheck_:
            self._logger.info("healthcheck")
        elif operation_dbm.type == OperationDBM.Types.raise_fake_exception:
            self._logger.info("raise_fake_exception")
            raise Exception("raise_fake_exception")
        else:
            raise ValueError(f"unknown operation.type = {operation_dbm.type}")
        return operation_dbm

    def sync_safe_execute_operation(self, operation_dbm: OperationDBM) -> OperationDBM:
        self._logger.info(
            f"start sync_safe_execute_operation"
            f", operation_dbm.id={operation_dbm.id}"
            f", operation_dbm.type={operation_dbm.type}"
        )

        with self.easy_sql_alchemy_db.new_session() as session:
            operation_dbm: OperationDBM = get_operation_by_id(
                session=session, filter_operation_id=operation_dbm.id, strict=True
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
            self._logger.exception(exception_)
            exception = exception_
            traceback_str = traceback.format_exc()

        with self.easy_sql_alchemy_db.new_session() as session:

            operation_dbm: OperationDBM = get_operation_by_id(
                session=session, filter_operation_id=operation_dbm.id, strict=True
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

            story_log_dbm = StoryLogDBM(
                level=StoryLogDBM.Levels.error,
                title="Error in sync_execute_operation",
                data={
                    "operation_id": operation_dbm.id,
                    "exception": str(exception),
                    "traceback_str": traceback_str
                }
            )
            session.add(story_log_dbm)
            session.commit()

            session.refresh(operation_dbm)
            session.refresh(story_log_dbm)

        self._logger.info(
            f"finish sync_safe_execute_operation"
            f", operation_dbm.id={operation_dbm.id}"
            f", operation_dbm.type={operation_dbm.type}"
            f", operation_dbm.duration={operation_dbm.duration}"
        )

        return operation_dbm


class ExecuteOperationWorker(BaseWorker):

    def __init__(
            self,
            *,
            easy_sql_alchemy_db: EasySQLAlchemyDB,
            operation_executor: BaseOperationExecutor,
            need_operation_type: str | None = None
    ):
        super().__init__()
        self.easy_sql_alchemy_db = easy_sql_alchemy_db
        self.timeout_after_run = timedelta(seconds=0.1).total_seconds()
        self.timeout_after_err_in_run = timedelta(seconds=1).total_seconds()
        self.operation_executor = operation_executor
        self.need_operation_type = need_operation_type

    async def async_on_startup(self):
        self.easy_sql_alchemy_db.init()

    async def async_execute_operation(self, operation_dbm: OperationDBM) -> OperationDBM:
        return await self.operation_executor.async_safe_execute_operation(operation_dbm=operation_dbm)

    async def async_run(self):
        operation_dbm: OperationDBM | None = get_operation_for_execution(
            easy_sql_alchemy_db=self.easy_sql_alchemy_db,
            filter_operation_type=self.need_operation_type
        )

        if not operation_dbm:
            return

        await self.async_execute_operation(operation_dbm=operation_dbm)

    async def async_run_on_error(self, exception: BaseException, kwargs: dict[str, Any]):
        self._logger.exception(exception)

    def sync_on_startup(self):
        self.easy_sql_alchemy_db.init()

    def sync_execute_operation(self, operation_dbm: OperationDBM) -> OperationDBM:
        return self.operation_executor.sync_safe_execute_operation(operation_dbm=operation_dbm)

    def sync_run(self):
        operation_dbm: OperationDBM | None = get_operation_for_execution(
            easy_sql_alchemy_db=self.easy_sql_alchemy_db,
            filter_operation_type=self.need_operation_type
        )

        if not operation_dbm:
            return

        self.sync_execute_operation(operation_dbm=operation_dbm)

    def sync_run_on_error(self, exception: BaseException, kwargs: dict[str, Any]):
        self._logger.exception(exception)


def import_ar_operation_execution_util():
    _logger.info("import_ar_operation_execution_util")
