import importlib
from contextlib import suppress
from functools import lru_cache
from typing import Any

from arpakitlib.ar_sqlalchemy_util import SQLAlchemyDB
from src.core.settings import get_cached_settings


def get_base_dbm() -> Any:
    with suppress(Exception):
        importlib.import_module("src.db.sqlalchemy_model")

    from arpakitlib.ar_sqlalchemy_model_util import BaseDBM
    return BaseDBM


def create_sqlalchemy_db() -> SQLAlchemyDB:
    from arpakitlib.ar_sqlalchemy_model_util import OperationDBM, StoryLogDBM

    return SQLAlchemyDB(
        db_url=get_cached_settings().sql_db_url,
        db_echo=get_cached_settings().sql_db_echo,
        base_declarative_base=get_base_dbm(),
        db_models=[OperationDBM, StoryLogDBM]
    )


@lru_cache()
def get_cached_sqlalchemy_db() -> SQLAlchemyDB:
    return create_sqlalchemy_db()

# ...
