import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from pydantic import Field

from arpakitlib.ar_aiogram_as_tg_command_2_util import BaseTgCommandModel, as_tg_command_handler, ExampleTgCommandModel
from arpakitlib.ar_logging_util import setup_normal_easy_logging

setup_normal_easy_logging()

logging.basicConfig(level=logging.INFO)
bot = Bot("6658127097:AAGZsLD2p4sbKghTYwyT4TbzU1I9-QoOUao", default=DefaultBotProperties(
    parse_mode=ParseMode.HTML
))
dp = Dispatcher()


class A(ExampleTgCommandModel):
    """USER"""

    name: str = None
    surname: str = None


# ======== команда =========
@dp.message(Command("hello"))
@as_tg_command_handler(tg_command_format_class=A)
async def cmd_hello(message: types.Message, tg_command_format_obj: A, **kwargs):
    model = tg_command_format_obj
    await message.answer(str(tg_command_format_obj))


# ======== запуск =========
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
