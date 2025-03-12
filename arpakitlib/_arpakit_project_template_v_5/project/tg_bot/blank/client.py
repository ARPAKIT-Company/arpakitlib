from functools import lru_cache

from emoji import emojize

from project.tg_bot.blank.common import SimpleBlankTgBot
from project.tg_bot.const import ClientTgBotCommands


class ClientTgBotBlank(SimpleBlankTgBot):
    def command_to_desc(self) -> dict[str, str]:
        return {
            ClientTgBotCommands.start: emojize(":waving_hand: Начать"),
            ClientTgBotCommands.about: emojize(":information: О проекте")
        }

    def but_hello_world(self) -> str:
        res = "hello_world"
        return emojize(res.strip())

    def error(self) -> str:
        res = ":warning: <b>Произошла неполадка</b> :warning:"
        res += "\n\n:wrench: Мы уже работаем над исправлением"
        res += "\n\n:red_heart: Просим прощения :red_heart:"
        return emojize(res.strip())

    def hello_world(self) -> str:
        res = ":waving_hand: <b>Hello world</b> :waving_hand:"
        return emojize(res.strip())

    def healthcheck(self) -> str:
        res = "healthcheck"
        return emojize(res.strip())

    def welcome(self) -> str:
        res = ":waving_hand: <b>Welcome</b> :waving_hand:"
        return emojize(res.strip())

    def raw_message(self) -> str:
        res = ":warning: <b>Сообщние не обработано</b> :warning:"
        return emojize(res.strip())

    def about_project(self) -> str:
        res = ":information: <b>О проекте</b>"
        return emojize(res.strip())

    def support_info(self) -> str:
        res = ":red_heart: <b>Поддержка</b>"
        return emojize(res.strip())

    def keyboard_is_old(self) -> str:
        res = ":information: Данная клавиатура устарела :information:"
        return emojize(res.strip())


def create_client_tg_bot_blank() -> ClientTgBotBlank:
    return ClientTgBotBlank()


@lru_cache()
def get_cached_client_tg_bot_blank() -> ClientTgBotBlank:
    return ClientTgBotBlank()


def __example():
    print(get_cached_client_tg_bot_blank().welcome())


if __name__ == '__main__':
    __example()
