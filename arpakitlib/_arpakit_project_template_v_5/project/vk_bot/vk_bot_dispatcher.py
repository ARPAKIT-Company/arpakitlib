# vk_bot_dispatcher.py

from typing import Callable, List, Tuple

import vk_api
from vk_api.vk_api import VkApiMethod
from vk_api.longpoll import VkEventType


class VkRouter:
    def __init__(self):
        self.message_handlers: List[Tuple[Callable[[str], bool], Callable]] = []

    def message(self, filter_fn: Callable[[str], bool]):
        def decorator(handler: Callable):
            self.message_handlers.append((filter_fn, handler))
            return handler
        return decorator

    def handle(self, event, vk: VkApiMethod) -> bool:
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            text = event.text.lower()
            for filter_fn, handler in self.message_handlers:
                if filter_fn(text):
                    handler(event, vk)
                    return True
        return False


class VkBotDispatcher:
    def __init__(self, vk: VkApiMethod):
        self.vk = vk
        self.routers: List[VkRouter] = []

    def include_router(self, router: VkRouter):
        self.routers.append(router)

    def process_event(self, event):
        for router in self.routers:
            if router.handle(event, self.vk):
                break


def create_vk_bot_dispatcher(vk: VkApiMethod) -> VkBotDispatcher:
    from project.vk_bot.router.main_router import main_vk_router

    dispatcher = VkBotDispatcher(vk)
    dispatcher.include_router(main_vk_router)
    return dispatcher
