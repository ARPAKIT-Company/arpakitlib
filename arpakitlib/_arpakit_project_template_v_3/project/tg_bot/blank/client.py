from functools import lru_cache

from emoji import emojize

from project.tg_bot.blank.common import SimpleBlankTgBot


class ClientBlankTgBot(SimpleBlankTgBot):
    def welcome(self) -> str:
        res = ":waving_hand: <b>Welcome</b> :waving_hand:"
        return emojize(res.strip())


def create_client_blank_tg_bot() -> ClientBlankTgBot:
    return ClientBlankTgBot()


@lru_cache()
def get_cached_client_blank_tg_bot() -> ClientBlankTgBot:
    return ClientBlankTgBot()


def __example():
    print(get_cached_client_blank_tg_bot().welcome())


if __name__ == '__main__':
    __example()
