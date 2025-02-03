from emoji import emojize

from arpakitlib.ar_blank_util import BaseBlank


class TgBotBlank(BaseBlank):

    def healthcheck(self) -> str:
        res = "healthcheck"
        return emojize(res.strip())
