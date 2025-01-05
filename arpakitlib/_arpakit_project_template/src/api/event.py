import logging

from arpakitlib.ar_fastapi_util import BaseStartupAPIEvent, BaseShutdownAPIEvent
from src.api.transmitted_api_data import TransmittedAPIData

_logger = logging.getLogger(__name__)


class FirstStartupAPIEvent(BaseStartupAPIEvent):
    def __init__(self, transmitted_api_data: TransmittedAPIData):
        super().__init__()
        self.transmitted_api_data = transmitted_api_data

    async def async_on_startup(self, *args, **kwargs):
        self._logger.info(self.__class__.__name__)


class FirstShutdownAPIEvent(BaseShutdownAPIEvent):
    def __init__(self, transmitted_api_data: TransmittedAPIData):
        super().__init__()
        self.transmitted_api_data = transmitted_api_data

    async def async_on_shutdown(self, *args, **kwargs):
        self._logger.info(self.__class__.__name__)
