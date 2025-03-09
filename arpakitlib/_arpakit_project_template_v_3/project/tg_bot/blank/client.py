from functools import lru_cache

from emoji import emojize

from project.tg_bot.blank.common import SimpleBlankTgBot


class ClientTgBotBlank(SimpleBlankTgBot):

    def command_to_desc(self) -> dict[str, str]:
        return {}

    def but_hello_world(self) -> str:
        res = "hello_world"
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


def create_client_tg_bot_blank() -> ClientTgBotBlank:
    return ClientTgBotBlank()


@lru_cache()
def get_cached_client_tg_bot_blank() -> ClientTgBotBlank:
    return ClientTgBotBlank()


def __example():
    print(get_cached_client_tg_bot_blank().welcome())


if __name__ == '__main__':
    __example()
