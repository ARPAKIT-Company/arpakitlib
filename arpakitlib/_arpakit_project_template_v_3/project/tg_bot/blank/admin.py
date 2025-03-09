from functools import lru_cache
from typing import Any

from emoji import emojize

from arpakitlib.ar_json_util import transfer_data_to_json_str
from project.tg_bot.blank.common import SimpleBlankTgBot
from project.util.arpakitlib_project_template import get_arpakitlib_project_template_info


class AdminBlankTgBot(SimpleBlankTgBot):
    def done(self) -> str:
        res = "Done"
        return emojize(res.strip())

    def arpakit_project_template_info(self, *, arpakitlib_project_template_info: dict[str, Any]) -> str:
        res = transfer_data_to_json_str(arpakitlib_project_template_info, beautify=True)
        return emojize(res.strip())


def create_admin_blank_tg_bot() -> AdminBlankTgBot:
    return AdminBlankTgBot()


@lru_cache()
def get_cached_admin_blank_tg_bot() -> AdminBlankTgBot:
    return AdminBlankTgBot()


def __example():
    print(
        get_cached_admin_blank_tg_bot().arpakit_project_template_info(
            arpakitlib_project_template_info=get_arpakitlib_project_template_info()
        )
    )


if __name__ == '__main__':
    __example()
