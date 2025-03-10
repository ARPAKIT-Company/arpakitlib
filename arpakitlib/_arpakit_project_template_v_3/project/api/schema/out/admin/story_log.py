from __future__ import annotations

from typing import Any

from project.api.schema.out.admin.common import SimpleDBMAdminCommonSO
from project.sqlalchemy_db_.sqlalchemy_model import StoryLogDBM


class StoryLogAdminSO(SimpleDBMAdminCommonSO):
    level: str
    type: str | None
    title: str | None
    data: dict[str, Any]

    @classmethod
    def from_story_log_dbm(cls, *, story_log_dbm: StoryLogDBM) -> StoryLogAdminSO:
        return cls.model_validate(story_log_dbm.simple_dict_with_sd_properties())
