import asyncio
import logging
from asyncio import sleep
from datetime import timedelta
from typing import Any

import aio_pika
from aio_pika.abc import AbstractRobustConnection, AbstractRobustChannel, AbstractRobustQueue, AbstractIncomingMessage
from aio_pika.exceptions import QueueEmpty

from arpakitlib.ar_sleep_util import sync_safe_sleep, async_safe_sleep


class BaseRMQConsumer:
    def __init__(self, *, url: str = "amqp://guest:guest@localhost/", queue_name: str = "order_offer_tt", **kwargs):
        self.kwargs = kwargs
        self.url = url
        self.queue_name = queue_name
        self.connection: AbstractRobustConnection | None = None
        self.channel: AbstractRobustChannel | None = None
        self.queue: AbstractRobustQueue | None = None
        self._logger = logging.getLogger(self.__class__.__name__)
        self.__is_running = False
        self.prefetch_count = 10
        self.timeout_in_loop = timedelta(seconds=0.01)

    async def process_message(self, *, message: AbstractIncomingMessage):
        raise NotImplemented

    async def _process_message(self, *, message: AbstractIncomingMessage):
        try:
            await self.process_message(message=message)
        except BaseException as exception:
            await message.nack()
            raise exception
        await message.ack()

    async def on_startup_event(self):
        self._logger.info("start")
        await async_retry_func(async_func=self.reinit, raise_if_exception=True)
        self._logger.info("finish")

    async def on_shutdown_event(self):
        self._logger.info("start")
        self._logger.info("finish")

    async def reinit(self):
        self._logger.info("start")

        if self.connection:
            await self.connection.close()
            self.connection = None
        self.connection = await aio_pika.connect_robust(self.url)

        if self.channel:
            await self.channel.close()
            self.channel = None
        self.channel = await self.connection.channel()
        await self.channel.set_qos(prefetch_count=self.prefetch_count)

        self.queue = await self.channel.declare_queue(self.queue_name, durable=True)

        self._logger.info("finish")

    async def get_message(self) -> AbstractIncomingMessage | None:
        async_retry_func_res: AsyncRetryFuncRes | None = await async_retry_func(
            async_func=self.queue.get,
            async_func_kwargs={"timeout": timedelta(seconds=3).total_seconds()},
            raise_if_exception=False
        )
        if async_retry_func_res.exception_in_func is not None:
            if isinstance(async_retry_func_res.exception_in_func, QueueEmpty):
                return None
            else:
                raise async_retry_func_res.exception_in_func
        return async_retry_func_res.res_from_func

    async def _logic_in_loop(self):
        message = await self.get_message()
        if message is None:
            return

        await self._process_message(message=message)

        if self.timeout_in_loop is not None:
            await asyncio.sleep(self.timeout_in_loop.total_seconds())

    async def _start_loop(self, max_retries: int = 5):
        self._logger.info("start")
        while self.__is_running:
            try:
                await self._logic_in_loop()
            except BaseException as exception:
                self._logger.error(exception, exc_info=exception)
            await sleep(self.timeout_in_loop.total_seconds())
        self._logger.info("finish")

    async def start_loop(self):
        self._logger.info("start")
        await self.on_startup_event()
        self.__is_running = True
        await self._start_loop()
        await self.on_shutdown_event()
        self._logger.info("finish")

    def end_loop(self):
        self.__is_running = False


async def __async_example():
    class Consumer(BaseRMQConsumer):
        async def process_message(self, *, message: AbstractIncomingMessage):
            print("Hello world")

    await Consumer().start_loop()


if __name__ == '__main__':
    asyncio.run(__async_example())
