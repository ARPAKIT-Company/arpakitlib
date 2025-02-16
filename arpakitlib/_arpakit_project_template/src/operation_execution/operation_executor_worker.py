from __future__ import annotations

from datetime import timedelta
from typing import Any

import sqlalchemy
from sqlalchemy import asc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from arpakitlib.ar_base_worker_util import BaseWorker
from arpakitlib.ar_sqlalchemy_util import SQLAlchemyDb
from arpakitlib.ar_type_util import raise_for_type
from src.operation_execution.operation_execution_logic import OperationExecutionLogic
from src.sqlalchemy_db.sqlalchemy_model import OperationDBM


class OperationExecutorWorker(BaseWorker):

    def __init__(
            self,
            *,
            sqlalchemy_db: SQLAlchemyDb,
            operation_executor: OperationExecutionLogic | None = None,
            filter_operation_types: str | list[str] | None = None,
            startup_funcs: list[Any] | None = None,
            **kwargs
    ):
        super().__init__(
            timeout_after_run=timedelta(seconds=0.1),
            timeout_after_err_in_run=timedelta(seconds=0.1),
            startup_funcs=startup_funcs,
        )

        self.startup_funcs.insert(0, sqlalchemy_db.init)

        raise_for_type(sqlalchemy_db, SQLAlchemyDb)
        self.sqlalchemy_db = sqlalchemy_db

        if operation_executor is None:
            operation_executor = OperationExecutionLogic(sqlalchemy_db=sqlalchemy_db)
        self.operation_executor = operation_executor

        if isinstance(filter_operation_types, str):
            filter_operation_types = [filter_operation_types]
        self.filter_operation_types = filter_operation_types

    def get_operation_for_execution(
            self,
            *,
            session: Session,
            filter_operation_types: list[str] | str | None = None,
            lock: bool = False
    ) -> OperationDBM | None:
        query = (
            session
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

    def sync_run(self):
        with self.sqlalchemy_db.new_session() as session:
            operation_dbm: OperationDBM | None = self.get_operation_for_execution(
                session=session,
                filter_operation_types=self.filter_operation_types,
                lock=True
            )
            if operation_dbm is None:
                return
            self.operation_executor.sync_safe_execute_operation(
                operation_dbm=operation_dbm, executor_name=self.worker_name, session=session
            )

    async def async_get_operation_for_execution(
            self,
            *,
            session: AsyncSession,
            filter_operation_types: list[str] | str | None = None,
            lock: bool = False
    ) -> OperationDBM | None:
        query = (
            sqlalchemy.select(OperationDBM)
            .filter(OperationDBM.status == OperationDBM.Statuses.waiting_for_execution)
            .order_by(asc(OperationDBM.creation_dt))
        )

        if filter_operation_types:
            query = query.filter(OperationDBM.type.in_(filter_operation_types))

        if lock:
            query = query.with_for_update()

        result = await session.execute(query)
        return result.scalars().first()

    async def async_run(self):
        with self.sqlalchemy_db.new_async_session() as async_session:
            operation_dbm: OperationDBM | None = await self.async_get_operation_for_execution(
                session=async_session,
                filter_operation_types=self.filter_operation_types,
                lock=True
            )
            if operation_dbm is None:
                return
            await self.operation_executor.async_safe_execute_operation(
                operation_dbm=operation_dbm, executor_name=self.worker_name, async_session=async_session
            )
