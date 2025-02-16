from functools import lru_cache

from arpakitlib.ar_sqlalchemy_util import SQLAlchemyDb
from src.core.settings import get_cached_settings
from src.sqlalchemy_db.sqlalchemy_model import get_simple_dbm


def create_sqlalchemy_db() -> SQLAlchemyDb:
    return SQLAlchemyDb(
        sync_db_url=get_cached_settings().sqlalchemy_sync_db_url,
        async_db_url=get_cached_settings().sqlalchemy_async_db_url,
        db_echo=get_cached_settings().sqlalchemy_db_echo,
        base_dbm=get_simple_dbm()
    )


@lru_cache()
def get_cached_sqlalchemy_db() -> SQLAlchemyDb:
    return create_sqlalchemy_db()
