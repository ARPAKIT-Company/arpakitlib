from dataclasses import dataclass
from typing import Callable, Dict

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from project.vk_bot.events import add_events_to_vk_bot_dispatcher


@dataclass
class VkBotDispatcher:
    vk: vk_api.vk_api.VkApiMethod
    longpoll: VkLongPoll
    message_handlers: Dict[str, Callable] = None

    def __post_init__(self):
        self.message_handlers = {}

    def message_handler(self, commands: list[str]):
        def decorator(handler: Callable):
            for command in commands:
                self.message_handlers[command] = handler
            return handler
        return decorator

    def process_event(self, event):
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            text = event.text.lower()
            if text in self.message_handlers:
                self.message_handlers[text](event)


def create_vk_bot_dispatcher(vk: vk_api.vk_api.VkApiMethod, longpoll: VkLongPoll) -> VkBotDispatcher:
    vk_bot_dispatcher = VkBotDispatcher(
        vk=vk,
        longpoll=longpoll
    )

    add_events_to_vk_bot_dispatcher(vk_bot_dispatcher=vk_bot_dispatcher)

    return vk_bot_dispatcher 