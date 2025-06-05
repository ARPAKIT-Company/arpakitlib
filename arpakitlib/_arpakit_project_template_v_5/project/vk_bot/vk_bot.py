from functools import lru_cache
import vk_api
from vk_api.longpoll import VkLongPoll

from project.core.settings import get_cached_settings


def create_vk_bot() -> tuple[vk_api.VkApi, vk_api.vk_api.VkApiMethod, VkLongPoll]:
    vk_session = vk_api.VkApi(token=get_cached_settings().vk_bot_token)
    vk = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    return vk_session, vk, longpoll


@lru_cache()
def get_cached_vk_bot() -> tuple[vk_api.VkApi, vk_api.vk_api.VkApiMethod, VkLongPoll]:
    return create_vk_bot() 