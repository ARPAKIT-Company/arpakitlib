from functools import lru_cache

from emoji import emojize

from arpakitlib.ar_blank_util import BaseBlank


class TgBotBlank(BaseBlank):
    def hello_world(self) -> str:
        res = ":smile: Hello world :smile:"
        return emojize(res.strip())

    def healthcheck(self) -> str:
        res = "healthcheck"
        return emojize(res.strip())


def create_tg_bot_blank() -> TgBotBlank:
    return TgBotBlank()


@lru_cache()
def get_cached_tg_bot_blank() -> TgBotBlank:
    return create_tg_bot_blank()
