from project.core.util import setup_logging
from project.vk_bot.vk_bot import get_cached_vk_bot
from project.vk_bot.vk_bot_dispatcher import create_vk_bot_dispatcher


def start_vk_bot():
    setup_logging()

    vk_session, vk, longpoll = get_cached_vk_bot()

    vk_bot_dispatcher = create_vk_bot_dispatcher(vk=vk, longpoll=longpoll)

    print("VK Bot started...")
    
    for event in longpoll.listen():
        vk_bot_dispatcher.process_event(event)


if __name__ == '__main__':
    start_vk_bot()
