import logging

from src.core.util import setup_logging

_logger = logging.getLogger(__name__)


def command():
    setup_logging()
    _logger.info("checking logging")


if __name__ == '__main__':
    command()
