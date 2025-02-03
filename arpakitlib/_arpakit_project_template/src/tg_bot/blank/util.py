from functools import lru_cache

from src.tg_bot.blank.blank import TgBotBlank


def get_create_tg_bot_blank() -> TgBotBlank:
    return TgBotBlank()


@lru_cache()
def get_cached_tg_bot_blank() -> TgBotBlank:
    return get_create_tg_bot_blank()
