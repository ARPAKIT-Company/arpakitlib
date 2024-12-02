import logging
from typing import Any

from sqlalchemy import TEXT
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from arpakitlib.ar_enumeration import EasyEnumeration
from arpakitlib.ar_fastapi_util import BaseAPISimpleSO
from arpakitlib.ar_sqlalchemy_model_util import SimpleDBM

_ARPAKIT_LIB_MODULE_VERSION = "3.0"
_logger = logging.getLogger(__name__)


class StoryLogDBM(SimpleDBM):
    __tablename__ = "story_log"

    class Levels(EasyEnumeration):
        info = "info"
        warning = "warning"
        error = "error"

    level: Mapped[str] = mapped_column(
        TEXT, insert_default=Levels.info, server_default=Levels.info, index=True, nullable=False
    )
    title: Mapped[str | None] = mapped_column(TEXT, index=True, default=None, nullable=True)
    data: Mapped[dict[str, Any]] = mapped_column(
        JSONB, insert_default={}, server_default="{}", index=True, nullable=False
    )


class StoryLogSO(BaseAPISimpleSO):
    level: str
    title: str | None
    data: dict[str, Any]


def import_ar_story_util():
    _logger.info("import_ar_operation_execution_util")
