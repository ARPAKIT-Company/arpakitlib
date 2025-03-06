from datetime import datetime

import sqlalchemy
from sqlalchemy import func
from sqlalchemy.orm import mapped_column, Mapped

from arpakitlib.ar_datetime_util import now_utc_dt
from arpakitlib.ar_sqlalchemy_util import get_string_info_from_declarative_base, BaseDBM
from project.sqlalchemy_db_.util import generate_default_long_id


class SimpleDBM(BaseDBM):
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        sqlalchemy.INTEGER, primary_key=True, autoincrement=True, sort_order=-13, nullable=False
    )
    long_id: Mapped[str] = mapped_column(
        sqlalchemy.TEXT, insert_default=generate_default_long_id, server_default=func.gen_random_uuid(),
        unique=True, sort_order=-12, nullable=False
    )
    slug: Mapped[str | None] = mapped_column(
        sqlalchemy.TEXT, unique=True, sort_order=-11, nullable=True
    )
    creation_dt: Mapped[datetime] = mapped_column(
        sqlalchemy.TIMESTAMP(timezone=True), insert_default=now_utc_dt, server_default=func.now(),
        index=True, sort_order=-10, nullable=False
    )

    def __repr__(self) -> str:
        if self.slug is None:
            return f"{self.__class__.__name__.removesuffix('DBM')} (id={self.id})"
        return f"{self.__class__.__name__.removesuffix('DBM')} (id={self.id}, slug={self.slug})"


def get_simple_dbm_class() -> type[SimpleDBM]:
    from project.sqlalchemy_db_.sqlalchemy_model import SimpleDBM
    return SimpleDBM


if __name__ == '__main__':
    print(get_string_info_from_declarative_base(get_simple_dbm_class()))
