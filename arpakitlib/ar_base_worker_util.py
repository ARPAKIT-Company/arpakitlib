# arpakit

import asyncio
import logging
from abc import ABC
from datetime import timedelta

from arpakitlib.ar_sleep_util import sync_safe_sleep, async_safe_sleep

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


class BaseWorker(ABC):

    def __init__(self):
        self.worker_name = self.__class__.__name__
        self._logger = logging.getLogger(self.worker_name)
        self.timeout_after_run = timedelta(seconds=0.1).total_seconds()
        self.timeout_after_err_in_run = timedelta(seconds=1).total_seconds()

    def sync_on_startup(self):
        pass

    def sync_run(self):
        raise NotImplementedError()

    def sync_run_on_error(self, exception: BaseException, **kwargs):
        self._logger.exception(exception)

    def sync_safe_run(self):
        self._logger.info(f"start sync_safe_run")

        self._logger.info("start sync_on_startup ")
        self.sync_on_startup()
        self._logger.info("finish sync_on_startup")

        while True:

            try:

                self._logger.info("start sync_run")
                self.sync_run()
                self._logger.info("finish sync_run")

                if self.timeout_after_run is not None:
                    sync_safe_sleep(self.timeout_after_run)

            except BaseException as exception:

                self._logger.info("start sync_run_on_error")
                self.sync_run_on_error(exception=exception)
                self._logger.info("start sync_run_on_error")

                if self.timeout_after_err_in_run is not None:
                    sync_safe_sleep(self.timeout_after_err_in_run)

    async def async_on_startup(self):
        pass

    async def async_run(self):
        raise NotImplementedError()

    async def async_run_on_error(self, exception: BaseException, **kwargs):
        self._logger.exception(exception)

    async def async_safe_run(self):
        self._logger.info(f"start async_safe_run")

        self._logger.info("start async_on_startup")
        await self.async_on_startup()
        self._logger.info("start async_on_startup")

        while True:

            try:

                await self.async_run()

                if self.timeout_after_run is not None:
                    await async_safe_sleep(self.timeout_after_run)

            except BaseException as exception:

                self._logger.info("start async_run_on_error")
                await self.async_run_on_error(exception=exception)
                self._logger.info("finish async_run_on_error")

                if self.timeout_after_err_in_run is not None:
                    await async_safe_sleep(self.timeout_after_err_in_run)


def __example():
    class TestWorker(BaseWorker):
        def __init__(self, *, timeout_after_run: int, timeout_after_err_in_run: int):
            super().__init__()
            self.timeout_after_run = timedelta(seconds=timeout_after_run).total_seconds()
            self.timeout_after_err_in_run = timedelta(hours=timeout_after_err_in_run).total_seconds()

        def sync_run(self):
            print("Sync worker started")

            raise ValueError("example error in sync_run")

        def sync_run_on_error(self, exception: BaseException, **kwargs):
            print(f"Error in sync_run: {exception}")

    worker = TestWorker(timeout_after_run=10, timeout_after_err_in_run=1)
    worker.sync_safe_run()


async def __async_example():
    class TestAsyncWorker(BaseWorker):
        def __init__(self, *, timeout_after_run: int, timeout_after_err_in_run: int):
            super().__init__()
            self.timeout_after_run = timedelta(seconds=timeout_after_run).total_seconds()
            self.timeout_after_err_in_run = timedelta(seconds=timeout_after_err_in_run).total_seconds()

        async def async_run(self):
            print("Async worker started")

            raise ValueError("example error in async_run")

        async def async_run_on_error(self, exception: BaseException, **kwargs):
            print(f"Error in async_run: {exception}")

    worker = TestAsyncWorker(timeout_after_run=1, timeout_after_err_in_run=10)
    await worker.async_safe_run()


if __name__ == '__main__':
    __example()
    asyncio.run(__async_example())
