from arpakitlib.ar_operation_execution_util import remove_operations
from src.core.settings import get_cached_settings
from src.core.util import setup_logging
from src.db.util import get_cached_sqlalchemy_db


def _remove_operations():
    setup_logging()
    get_cached_settings().raise_if_mode_type_prod()
    with get_cached_sqlalchemy_db() as sqlalchemy_db:
        remove_operations(sqlalchemy_db=sqlalchemy_db)


if __name__ == '__main__':
    _remove_operations()
