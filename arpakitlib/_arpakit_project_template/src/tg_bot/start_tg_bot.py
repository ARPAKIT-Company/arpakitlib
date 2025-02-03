from src.core.settings import get_cached_settings
from src.core.util import setup_logging


def start_tg_bot():
    setup_logging()

    settings = get_cached_settings()


if __name__ == '__main__':
    start_tg_bot()
