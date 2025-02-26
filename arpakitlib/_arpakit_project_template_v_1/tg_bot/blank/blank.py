from emoji import emojize

from arpakitlib.ar_blank_util import BaseBlank


class TgBotBlank(BaseBlank):
    def hello_world(self) -> str:
        res = ":smile: Hello world :smile:"
        return emojize(res.strip())

    def healthcheck(self) -> str:
        res = "healthcheck"
        return emojize(res.strip())
