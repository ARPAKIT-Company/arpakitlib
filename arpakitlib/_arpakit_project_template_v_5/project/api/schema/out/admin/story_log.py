from __future__ import annotations

from project.api.schema.out.admin.common import SimpleDBMAdminSO
from project.sqlalchemy_db_.sqlalchemy_model import StoryLogDBM


class StoryLogAdmin1SO(SimpleDBMAdminSO):
    level: str
    type: str | None
    title: str | None

    allowed_levels: list[str]
    allowed_types: list[str]

    @classmethod
    def from_dbm(cls, *, simple_dbm: StoryLogDBM) -> StoryLogAdmin1SO:
        return cls.model_validate(simple_dbm.simple_dict_with_sd_properties(
            only_columns_and_sd_properties=cls.model_fields.keys()
        ))
