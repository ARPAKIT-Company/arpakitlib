from __future__ import annotations

import datetime as dt

from project.api.schema.common import BaseSO
from project.sqlalchemy_db_.sqlalchemy_model import SimpleDBM


class SimpleDBMAdminSO(BaseSO):
    id: int
    long_id: str
    slug: str | None
    creation_dt: dt.datetime

    @classmethod
    def from_dbm(cls, *, simple_dbm: SimpleDBM) -> SimpleDBMAdminSO:
        return cls.model_validate(simple_dbm.simple_dict_with_sd_properties())
