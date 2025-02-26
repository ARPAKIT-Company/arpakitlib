from functools import lru_cache

from arpakitlib.ar_sqlalchemy_util import SQLAlchemyDb
from core.settings import get_cached_settings
from sqlalchemy_db_.sqlalchemy_model import get_simple_dbm


def create_sqlalchemy_db() -> SQLAlchemyDb | None:
    if not get_cached_settings().sqlalchemy_sync_db_url or not get_cached_settings().sqlalchemy_async_db_url:
        return None

    return SQLAlchemyDb(
        sync_db_url=get_cached_settings().sqlalchemy_sync_db_url,
        async_db_url=get_cached_settings().sqlalchemy_async_db_url,
        db_echo=get_cached_settings().sqlalchemy_db_echo,
        base_dbm=get_simple_dbm()
    )


@lru_cache()
def get_cached_sqlalchemy_db() -> SQLAlchemyDb | None:
    return create_sqlalchemy_db()
