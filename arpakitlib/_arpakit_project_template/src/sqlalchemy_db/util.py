from functools import lru_cache

from arpakitlib.ar_sqlalchemy_model_util import BaseDBM
from arpakitlib.ar_sqlalchemy_util import SQLAlchemyDb
from src.core.settings import get_cached_settings


def get_base_dbm() -> type[BaseDBM]:
    from arpakitlib.ar_sqlalchemy_model_util import import_ar_sqlalchemy_models
    import_ar_sqlalchemy_models()
    from src.sqlalchemy_db.sqlalchemy_model import import_project_sqlalchemy_models
    import_project_sqlalchemy_models()
    return BaseDBM


def create_sqlalchemy_db() -> SQLAlchemyDb:
    return SQLAlchemyDb(
        sync_db_url=get_cached_settings().sqlalchemy_sync_db_url,
        async_db_url=get_cached_settings().sqlalchemy_async_db_url,
        db_echo=get_cached_settings().sqlalchemy_db_echo,
        base_dbm=get_base_dbm()
    )


@lru_cache()
def get_cached_sqlalchemy_db() -> SQLAlchemyDb:
    return create_sqlalchemy_db()
