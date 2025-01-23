import logging

_logger = logging.getLogger(__name__)


def hello_world() -> str:
    _logger.info("hello world")
    return "Hello world"


if __name__ == '__main__':
    print(hello_world())
