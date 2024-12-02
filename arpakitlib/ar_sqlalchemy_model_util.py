# arpakit

from datetime import datetime
from typing import Any
from uuid import uuid4

from sqlalchemy import inspect, INTEGER, TEXT, TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from arpakitlib.ar_datetime_util import now_utc_dt
from arpakitlib.ar_json_util import safely_transfer_to_json_str

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


class BaseDBM(DeclarativeBase):
    __abstract__ = True
    _bus_data: dict[str, Any] | None = None

    @property
    def bus_data(self) -> dict[str, Any]:
        if self._bus_data is None:
            self._bus_data = {}
        return self._bus_data

    def simple_dict(self) -> dict[str, Any]:
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    def simple_json(self) -> str:
        return safely_transfer_to_json_str(self.simple_dict())


class SimpleDBM(BaseDBM):
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        INTEGER, primary_key=True, autoincrement=True, nullable=False
    )
    long_id: Mapped[str] = mapped_column(
        TEXT, insert_default=uuid4, unique=True, nullable=False
    )
    creation_dt: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), insert_default=now_utc_dt, index=True, nullable=False
    )

    def __repr__(self):
        return f"{self.__class__.__name__.removesuffix('DBM')} (id={self.id})"
