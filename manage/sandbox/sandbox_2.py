import asyncio

from arpakitlib.ar_http_request_util import sync_make_http_request
from arpakitlib.ar_type_util import raise_for_type


def command():
    for a in range(100):
        res = sync_make_http_request(url="http://127.0.0.1:8000/create_healthcheck")
        print(res.status_code)


async def async_command():
    pass


if __name__ == '__main__':
    command()
    asyncio.run(async_command())
