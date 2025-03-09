from functools import lru_cache

from emoji import emojize

from project.tg_bot.blank.common import SimpleBlankTgBot


class GeneralBlankTgBot(SimpleBlankTgBot):
    def but_hello_world(self) -> str:
        res = "hello_world"
        return emojize(res.strip())

    def hello_world(self) -> str:
        res = ":waving_hand: <b>Hello world</b> :waving_hand:"
        return emojize(res.strip())

    def healthcheck(self) -> str:
        res = "healthcheck"
        return emojize(res.strip())


def create_general_blank_tg_bot() -> GeneralBlankTgBot:
    return GeneralBlankTgBot()


@lru_cache()
def get_cached_general_blank_tg_bot() -> GeneralBlankTgBot:
    return GeneralBlankTgBot()


def __example():
    print(get_cached_general_blank_tg_bot().hello_world())


if __name__ == '__main__':
    __example()
