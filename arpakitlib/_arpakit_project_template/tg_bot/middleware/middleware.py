import aiogram

from tg_bot.middleware.init_user import InitUserTgBotMiddleware


def register_tg_bot_middleware(
        *,
        tg_bot_dp: aiogram.Dispatcher,
        **kwargs
) -> aiogram.Dispatcher:
    tg_bot_dp.update.outer_middleware.register(InitUserTgBotMiddleware())
    return tg_bot_dp
