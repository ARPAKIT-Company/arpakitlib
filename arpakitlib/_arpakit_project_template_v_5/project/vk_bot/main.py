import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

TOKEN = "vk1.a.YK9YgE-f-2wFdykFw2EI4P4ckMoX2O1t41mXfA1CsZIj78eJuV2v3W4ZDzJohzFEtS7s0LwNto44FOYPpPdiwcVldF7j0ZCVkaCdSJ3fg17TLiZlqIDPHluGys1kUERF14AYRw5FifmiEAD_0ZlKiuGJ7H1DTsLfXweeGA0APMXm9_Q5i5aSeQLiAosaomCPpHLYZbqHOm7bCW6bJeJTww"

vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

# Основной цикл бота
print("Bot start...")

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        user_id = event.user_id
        text = event.text.lower()

        # Обработка команд
        if text == "привет":
            vk.messages.send(user_id=user_id, message="Привет! 👋", random_id=0)
        elif text == "пока":
            vk.messages.send(user_id=user_id, message="Пока! 👋", random_id=0)
        else:
            vk.messages.send(user_id=user_id, message="Я тебя не понял 🤔", random_id=0)
