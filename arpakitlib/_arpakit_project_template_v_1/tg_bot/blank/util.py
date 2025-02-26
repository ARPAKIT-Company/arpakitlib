from functools import lru_cache

from tg_bot.blank.blank import TgBotBlank


def create_tg_bot_blank() -> TgBotBlank:
    return TgBotBlank()


@lru_cache()
def get_cached_tg_bot_blank() -> TgBotBlank:
    return create_tg_bot_blank()
