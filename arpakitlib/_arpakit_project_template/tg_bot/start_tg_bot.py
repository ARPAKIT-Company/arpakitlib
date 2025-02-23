from arpakitlib.ar_aiogram_util import start_aiogram_tg_bot_with_webhook
from core.util import setup_logging
from tg_bot.event import add_events_to_tg_bot_dispatcher
from tg_bot.tg_bot import create_tg_bot
from tg_bot.tg_bot_dispatcher import create_tg_bot_dispatcher
from tg_bot.transmitted_tg_data import get_cached_transmitted_tg_bot_data


def start_tg_bot():
    setup_logging()

    transmitted_tg_bot_data = get_cached_transmitted_tg_bot_data()

    tg_bot = create_tg_bot()

    tg_bot_dispatcher = create_tg_bot_dispatcher()

    add_events_to_tg_bot_dispatcher(tg_bot_dispatcher=tg_bot_dispatcher)

    if transmitted_tg_bot_data.settings.tg_bot_webhook_enabled:
        tg_bot_dispatcher.start_polling(tg_bot)
    else:
        start_aiogram_tg_bot_with_webhook(
            dispatcher=tg_bot_dispatcher,
            bot=tg_bot,
            webhook_secret=transmitted_tg_bot_data.settings.tg_bot_webhook_secret,
            webhook_path=transmitted_tg_bot_data.settings.tg_bot_webhook_path,
            webhook_server_hostname=transmitted_tg_bot_data.settings.tg_bot_webhook_server_hostname,
            webhook_server_port=transmitted_tg_bot_data.settings.tg_bot_webhook_server_port
        )


if __name__ == '__main__':
    start_tg_bot()
