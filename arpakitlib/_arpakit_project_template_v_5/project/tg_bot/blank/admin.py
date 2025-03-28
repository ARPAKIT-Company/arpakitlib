from functools import lru_cache

from emoji import emojize

from arpakitlib.ar_json_util import transfer_data_to_json_str
from project.sqlalchemy_db_.sqlalchemy_model import UserDBM
from project.tg_bot.blank.common import SimpleBlankTgBot


class AdminTgBotBlank(SimpleBlankTgBot):
    def good(self) -> str:
        res = "good"
        return emojize(res.strip())

    def user_dbm(self, *, user_dbm: UserDBM | None) -> str:
        if user_dbm is None:
            return "None"
        return transfer_data_to_json_str(user_dbm.simple_dict(), beautify=True)


def create_admin_tg_bot_blank() -> AdminTgBotBlank:
    return AdminTgBotBlank()


@lru_cache()
def get_cached_admin_tg_bot_blank() -> AdminTgBotBlank:
    return AdminTgBotBlank()


def __example():
    pass


if __name__ == '__main__':
    __example()
