from functools import lru_cache
from typing import Any

from emoji import emojize

from arpakitlib.ar_json_util import transfer_data_to_json_str
from project.sqlalchemy_db_.sqlalchemy_model import UserDBM
from project.tg_bot.blank.common import SimpleBlankTgBot
from project.util.arpakitlib_project_template import get_arpakitlib_project_template_info


class AdminTgBotBlank(SimpleBlankTgBot):
    def done(self) -> str:
        res = "Done"
        return emojize(res.strip())

    def arpakit_project_template_info(self, *, arpakitlib_project_template_info: dict[str, Any]) -> str:
        res = transfer_data_to_json_str(arpakitlib_project_template_info, beautify=True)
        return emojize(res.strip())

    def user_dbm(self, *, user_dbm: UserDBM | None) -> str:
        if user_dbm is None:
            return "None"
        return user_dbm.simple_dict_json(include_sd_properties=True)


def create_admin_tg_bot_blank() -> AdminTgBotBlank:
    return AdminTgBotBlank()


@lru_cache()
def get_cached_admin_tg_bot_blank() -> AdminTgBotBlank:
    return AdminTgBotBlank()


def __example():
    print(
        get_cached_admin_tg_bot_blank().arpakit_project_template_info(
            arpakitlib_project_template_info=get_arpakitlib_project_template_info()
        )
    )


if __name__ == '__main__':
    __example()
