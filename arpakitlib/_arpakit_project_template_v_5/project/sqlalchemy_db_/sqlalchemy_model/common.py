from datetime import datetime
from typing import Any

import sqlalchemy
from sqlalchemy import func
from sqlalchemy.orm import mapped_column, Mapped, validates

from arpakitlib.ar_datetime_util import now_utc_dt
from arpakitlib.ar_sqlalchemy_util import get_string_info_from_declarative_base, BaseDBM
from project.sqlalchemy_db_.util import generate_default_long_id


class SimpleDBM(BaseDBM):
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        sqlalchemy.BIGINT,
        nullable=False,
        primary_key=True,
        autoincrement=True,
        sort_order=-103,
    )
    long_id: Mapped[str] = mapped_column(
        sqlalchemy.TEXT,
        nullable=False,
        unique=True,
        insert_default=generate_default_long_id,
        server_default=func.gen_random_uuid(),
        sort_order=-102,
    )
    slug: Mapped[str | None] = mapped_column(
        sqlalchemy.TEXT,
        nullable=True,
        unique=True,
        sort_order=-101,
    )
    creation_dt: Mapped[datetime] = mapped_column(
        sqlalchemy.TIMESTAMP(timezone=True),
        nullable=False,
        index=True,
        insert_default=now_utc_dt,
        server_default=func.now(),
        sort_order=-100,
    )
    extra_data: Mapped[dict[str, Any]] = mapped_column(
        sqlalchemy.JSON,
        nullable=False,
        index=False,
        insert_default={},
        server_default="{}",
        sort_order=1000,
    )

    def __repr__(self) -> str:
        if self.slug is None:
            return f"{self.entity_name} (id={self.id})"
        return f"{self.entity_name} (id={self.id}, slug={self.slug})"

    @validates("slug")
    def _validate_slug(self, key, value, *args, **kwargs):
        if value is None:
            return None
        if not isinstance(value, str):
            raise ValueError(f"{value=} is not str")
        value = value.strip()
        if " " in value:
            raise ValueError(f"slug should not contain spaces, {self.slug=}")
        return value

    @validates("extra_data")
    def _validate_extra_data(self, key, value, *args, **kwargs):
        if value is None:
            value = {}
        if not isinstance(value, dict):
            raise ValueError(f"{value=} is not str")
        return value

    @property
    def entity_name(self) -> str:
        return self.__class__.__name__.removesuffix("DBM")

    @property
    def sdp_entity_name(self) -> str:
        return self.entity_name


def get_simple_dbm_class() -> type[SimpleDBM]:
    from project.sqlalchemy_db_.sqlalchemy_model import SimpleDBM
    return SimpleDBM


if __name__ == '__main__':
    print(get_string_info_from_declarative_base(get_simple_dbm_class()))
