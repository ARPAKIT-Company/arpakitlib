import logging

from src.core.util import setup_logging

_logger = logging.getLogger(__name__)


def send_msg_to_users():
    setup_logging()
    input("r u sure?")
    _logger.info("sending")
    _logger.info("sent")


if __name__ == '__main__':
    send_msg_to_users()
