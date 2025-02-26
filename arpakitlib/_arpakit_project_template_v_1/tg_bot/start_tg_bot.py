import aiohttp
import aiohttp.web
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from arpakitlib.ar_aiogram_util import start_aiogram_tg_bot_with_webhook
from core.settings import get_cached_settings
from core.util import setup_logging
from tg_bot.tg_bot import create_tg_bot
from tg_bot.tg_bot_dispatcher import create_tg_bot_dispatcher


def start_tg_bot():
    setup_logging()

    tg_bot = create_tg_bot()

    tg_bot_dispatcher = create_tg_bot_dispatcher()

    if get_cached_settings().tg_bot_webhook_enabled:
        tg_bot_dispatcher.start_polling(tg_bot)
    else:
        start_aiogram_tg_bot_with_webhook(
            dispatcher=tg_bot_dispatcher,
            bot=tg_bot,
            webhook_secret=get_cached_settings().tg_bot_webhook_secret,
            webhook_path=get_cached_settings().tg_bot_webhook_path,
            webhook_server_hostname=get_cached_settings().tg_bot_webhook_server_hostname,
            webhook_server_port=get_cached_settings().tg_bot_webhook_server_port
        )
        app = aiohttp.web.Application()
        simple_requests_handler = SimpleRequestHandler(
            dispatcher=tg_bot_dispatcher,
            bot=tg_bot,
            secret_token=get_cached_settings().tg_bot_webhook_secret
        )
        simple_requests_handler.register(app, path=get_cached_settings().tg_bot_webhook_path)
        setup_application(app, tg_bot_dispatcher, bot=tg_bot)
        aiohttp.web.run_app(
            app=app,
            host=get_cached_settings().tg_bot_webhook_server_hostname,
            port=get_cached_settings().tg_bot_webhook_server_port
        )


if __name__ == '__main__':
    start_tg_bot()
