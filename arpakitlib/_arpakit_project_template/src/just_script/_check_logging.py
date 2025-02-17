import logging

from src.core.util import setup_logging

_logger = logging.getLogger(__name__)


def _just_script():
    setup_logging()
    _logger.info("logging is good")


if __name__ == '__main__':
    _just_script()
