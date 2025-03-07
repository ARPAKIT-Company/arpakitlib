from functools import lru_cache
from typing import Any

from emoji import emojize

from arpakitlib.ar_blank_util import BaseBlank
from arpakitlib.ar_json_util import transfer_data_to_json_str


class TgBotBlank(BaseBlank):
    def arpakit_project_template_info(self, *, arpakitlib_project_template_info: dict[str, Any]) -> str:
        res = "<b>Используется arpakitlib</b>"
        res += f"\n\n{transfer_data_to_json_str(arpakitlib_project_template_info)}"
        res += "\n\n"
        res += "— https://pypi.org/project/arpakitlib/"
        res += "\n— https://github.com/ARPAKIT-Company/arpakitlib"
        return emojize(res.strip())

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
