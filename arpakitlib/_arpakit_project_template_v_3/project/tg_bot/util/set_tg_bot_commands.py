import logging

from aiogram import Bot
from aiogram.exceptions import AiogramError
from aiogram.types import BotCommand, BotCommandScopeChat

from project.tg_bot.blank.client import get_cached_client_tg_bot_blank
from project.tg_bot.const import ClientTgBotCommands

_logger = logging.getLogger(__name__)

_client_tg_bot_commands = [
    BotCommand(
        command=ClientTgBotCommands.start,
        description=get_cached_client_tg_bot_blank().command_to_desc()[ClientTgBotCommands.start]
    ),
    BotCommand(
        command=PublicTgBotCommands.authors,
        description=PublicTgBotBlank.command_to_desc()[PublicTgBotCommands.authors]
    ),
    BotCommand(
        command=PublicTgBotCommands.notification,
        description=PublicTgBotBlank.command_to_desc()[PublicTgBotCommands.notification]
    ),
    BotCommand(
        command=PublicTgBotCommands.notification_off,
        description=PublicTgBotBlank.command_to_desc()[PublicTgBotCommands.notification_off]
    ),
    BotCommand(
        command=PublicTgBotCommands.support,
        description=PublicTgBotBlank.command_to_desc()[PublicTgBotCommands.support]
    ),
    BotCommand(
        command=PublicTgBotCommands.weather_in_ufa,
        description=PublicTgBotBlank.command_to_desc()[PublicTgBotCommands.weather_in_ufa]
    ),
    BotCommand(
        command=PublicTgBotCommands.current_week,
        description=PublicTgBotBlank.command_to_desc()[PublicTgBotCommands.current_week]
    ),
    BotCommand(
        command=PublicTgBotCommands.current_semester,
        description=PublicTgBotBlank.command_to_desc()[PublicTgBotCommands.current_semester]
    ),
    BotCommand(
        command=PublicTgBotCommands.about,
        description=PublicTgBotBlank.command_to_desc()[PublicTgBotCommands.about]
    ),
    BotCommand(
        command=PublicTgBotCommands.find,
        description=PublicTgBotBlank.command_to_desc()[PublicTgBotCommands.find]
    )

]

_admin_tg_bot_commands = [
    BotCommand(
        command=command,
        description=(
            PrivateTgBotBlank.command_to_desc()[command]
            if command in PrivateTgBotBlank.command_to_desc().keys()
            else command
        )
    )
    for command in PrivateTgBotCommands.values_list()
]


async def set_public_tg_bot_commands(*, tg_bot: Bot):
    _logger.info(f"set_public_tg_bot_commands")
    await tg_bot.set_my_commands(commands=_public_tg_bot_commands)
    _logger.info("public tg bot commands were set")


async def set_private_tg_bot_commands(*, tg_bot: Bot):
    _logger.info(f"set_private_tg_bot_commands")

    for admin_tg_id in get_settings().admin_tg_ids:
        try:
            await tg_bot.set_my_commands(
                commands=_private_tg_bot_commands + _public_tg_bot_commands,
                scope=BotCommandScopeChat(chat_id=admin_tg_id)
            )
        except AiogramError as e:
            _logger.warning(e)

    _logger.info("private tg bot commands were set")


def __example():
    pass


if __name__ == '__main__':
    __example()
