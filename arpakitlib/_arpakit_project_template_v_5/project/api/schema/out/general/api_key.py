from __future__ import annotations

from project.api.schema.out.client.common import SimpleDBMClientSO
from project.sqlalchemy_db_.sqlalchemy_model import ApiKeyDBM


class ApiKeyGeneral1SO(SimpleDBMClientSO):
    title: str | None
    value: str
    is_active: bool

    @classmethod
    def from_dbm(cls, *, simple_dbm: ApiKeyDBM) -> ApiKeyGeneral1SO:
        return cls.model_validate(simple_dbm.simple_dict_with_sd_properties(
            only_columns_and_sd_properties=cls.model_fields.keys()
        ))
