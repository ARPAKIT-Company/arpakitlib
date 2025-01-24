import importlib
from contextlib import suppress
from functools import lru_cache

from arpakitlib.ar_sqlalchemy_util import SQLAlchemyDB
from src.core.settings import get_cached_settings


def create_sqlalchemy_db() -> SQLAlchemyDB:
    with suppress(Exception):
        importlib.import_module("src.db.sqlalchemy_model")

    return SQLAlchemyDB(
        db_url=get_cached_settings().sql_db_url,
        db_echo=get_cached_settings().sql_db_echo
    )


@lru_cache()
def get_cached_sqlalchemy_db() -> SQLAlchemyDB:
    return create_sqlalchemy_db()

# ...
