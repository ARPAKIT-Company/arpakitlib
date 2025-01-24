import logging

from src.core.util import setup_logging

_logger = logging.getLogger(__name__)


def _check_logging():
    setup_logging()
    _logger.info("logging is good")


if __name__ == '__main__':
    _check_logging()
