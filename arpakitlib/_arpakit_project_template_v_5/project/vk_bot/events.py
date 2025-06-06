def add_events_to_vk_bot_dispatcher(vk_bot_dispatcher):

    @vk_bot_dispatcher.message_handler(commands=["start", "начать", "привет"])
    def start_command(event):
        user_id = event.user_id
        vk_bot_dispatcher.vk.messages.send(
            user_id=user_id,
            message="Hello World!",
            random_id=0
        )