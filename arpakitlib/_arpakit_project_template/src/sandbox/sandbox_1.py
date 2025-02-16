import asyncio

from arpakitlib.ar_base_worker_util import BaseWorker
from src.core.util import setup_logging


class A:
    async def go(self, name: str):
        print("go")


setup_logging()
a = A()
worker = BaseWorker(startup_funcs=[a.go(name="asfasf")])
worker.sync_safe_run()


def __example():
    pass


async def __async_example():
    pass


if __name__ == '__main__':
    __example()
    asyncio.run(__async_example())
