import aiogram

from tg_bot.middleware.init_user import InitUserTgBotMiddleware


def register_middlewares_to_tg_bot(
        *,
        tg_bot_dispatcher: aiogram.Dispatcher,
        **kwargs
) -> aiogram.Dispatcher:
    tg_bot_dispatcher.update.outer_middleware.register(InitUserTgBotMiddleware())
    return tg_bot_dispatcher
