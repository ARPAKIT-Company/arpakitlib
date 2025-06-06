from project.vk_bot.vk_bot_dispatcher import VkRouter

start_router = VkRouter()

@start_router.message(lambda text: text in ["start", "начать", "привет", "старт"])
def handle_start(event, vk):
    vk.messages.send(
        user_id=event.user_id,
        message="Hello World!",
        random_id=0
    )
