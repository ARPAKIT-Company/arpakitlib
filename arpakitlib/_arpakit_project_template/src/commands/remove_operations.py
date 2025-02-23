from src.business_service.remove_operations import remove_operations
from src.core.settings import get_cached_settings
from src.core.util import setup_logging


def __command():
    setup_logging()
    get_cached_settings().raise_if_mode_type_prod()
    remove_operations()


if __name__ == '__main__':
    __command()
