import logging

from src.tg_bot.transmitted_tg_data import TransmittedTgData


class StartupTgBotEvent:
    def __init__(self, *, transmitted_tg_bot_data: TransmittedTgData, **kwargs):
        self._logger = logging.getLogger()
        self.transmitted_tg_bot_data = transmitted_tg_bot_data

    async def on_startup(self, *args, **kwargs):
        self._logger.info("on_startup start")

        if self.transmitted_tg_bot_data.media_file_storage_in_dir is not None:
            self.transmitted_tg_bot_data.media_file_storage_in_dir.init()

        if self.transmitted_tg_bot_data.cache_file_storage_in_dir is not None:
            self.transmitted_tg_bot_data.cache_file_storage_in_dir.init()

        if self.transmitted_tg_bot_data.dump_file_storage_in_dir is not None:
            self.transmitted_tg_bot_data.dump_file_storage_in_dir.init()

        self._logger.info("on_startup was done")


class ShutdownTgBotEvent:
    def __init__(self, *, transmitted_tg_bot_data: TransmittedTgData, **kwargs):
        self._logger = logging.getLogger()
        self.transmitted_tg_bot_data = transmitted_tg_bot_data

    async def on_shutdown(self, *args, **kwargs):
        self._logger.info("on_shutdown start")
        self._logger.info("on_shutdown was done")
