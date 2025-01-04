# arpakit

import asyncio
import logging
import multiprocessing
import threading
from abc import ABC
from datetime import timedelta

from arpakitlib.ar_enumeration_util import Enumeration
from arpakitlib.ar_sleep_util import sync_safe_sleep, async_safe_sleep

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


class BaseWorker(ABC):
    class SafeRunInBackgroundModes(Enumeration):
        async_task = "async_task"
        thread = "thread"
        process = "process"

    def __init__(self):
        self.worker_name = self.__class__.__name__
        self._logger = logging.getLogger(self.worker_name)
        self.timeout_after_run = timedelta(seconds=0.1).total_seconds()
        self.timeout_after_err_in_run = timedelta(seconds=1).total_seconds()

    def safe_run_in_background(self, *, safe_run_in_background_mode: str) -> (
            asyncio.Task | threading.Thread | multiprocessing.Process
    ):
        if safe_run_in_background_mode == self.SafeRunInBackgroundModes.async_task:
            res: asyncio.Task = asyncio.create_task(self.async_safe_run())
        elif safe_run_in_background_mode == self.SafeRunInBackgroundModes.thread:
            res: threading.Thread = threading.Thread(
                target=self.sync_safe_run,
                daemon=True
            )
            res.start()
        elif safe_run_in_background_mode == self.SafeRunInBackgroundModes.process:
            res: multiprocessing.Process = multiprocessing.Process(
                target=self.sync_safe_run,
                daemon=True
            )
            res.start()
        else:
            raise ValueError(f"unrecognized safe_run_mode={safe_run_in_background_mode}")
        return res

    def sync_on_startup(self):
        pass

    def sync_run(self):
        raise NotImplementedError()

    def sync_run_on_error(self, exception: BaseException, **kwargs):
        self._logger.exception(exception)

    def sync_safe_run(self):
        self._logger.info("sync_safe_run")
        self.sync_on_startup()
        while True:
            try:
                self.sync_run()
                if self.timeout_after_run is not None:
                    sync_safe_sleep(self.timeout_after_run)
            except BaseException as exception:
                self.sync_run_on_error(exception=exception)
                if self.timeout_after_err_in_run is not None:
                    sync_safe_sleep(self.timeout_after_err_in_run)

    async def async_on_startup(self):
        pass

    async def async_run(self):
        raise NotImplementedError()

    async def async_run_on_error(self, exception: BaseException, **kwargs):
        self._logger.exception(exception)

    async def async_safe_run(self):
        self._logger.info("async_safe_run")
        await self.async_on_startup()
        while True:
            try:
                await self.async_run()
                if self.timeout_after_run is not None:
                    await async_safe_sleep(self.timeout_after_run)
            except BaseException as exception:
                await self.async_run_on_error(exception=exception)
                if self.timeout_after_err_in_run is not None:
                    await async_safe_sleep(self.timeout_after_err_in_run)


def __example():
    pass


async def __async_example():
    pass


if __name__ == '__main__':
    __example()
    asyncio.run(__async_example())
