from functools import lru_cache
import vk_api
from vk_api.longpoll import VkLongPoll
from project.core.settings import get_cached_settings


class VkBot:
    def __init__(self, token: str):
        self.vk_session = vk_api.VkApi(token=token)
        self.vk = self.vk_session.get_api()
        self.longpoll = VkLongPoll(self.vk_session)

    def listen_longpoll(self):
        return self.longpoll.listen()


def create_vk_bot() -> VkBot:
    return VkBot(token=get_cached_settings().vk_bot_token)


@lru_cache()
def get_cached_vk_bot() -> VkBot:
    return create_vk_bot()
