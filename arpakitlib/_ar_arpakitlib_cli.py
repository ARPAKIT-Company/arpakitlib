# arpakit

import logging
import sys

from arpakitlib.ar_need_type_util import parse_need_type, NeedTypes
from arpakitlib.ar_parse_command import parse_command
from arpakitlib.ar_project_template_util import init_arpakit_project_template
from arpakitlib.ar_str_util import raise_if_string_blank

_logger = logging.getLogger(__name__)


def _arpakitlib_cli(*, full_command: str):
    _logger.info("start _arpakitlib_cli")

    parsed_command = parse_command(text=full_command)
    parsed_command.raise_for_command(needed_command="arpakitlib", lower_=True)

    command = parsed_command.get_value_by_keys(keys=["command", "c"])
    if command:
        command = command.strip()
    if not command:
        raise Exception(f"not command, command={command}")

    _logger.info(f"start {command}")

    if command == "help":
        pass

    elif command == "init_arpakit_project_template":
        project_dirpath = raise_if_string_blank(parsed_command.get_value_by_keys(keys=["pd", "project_dirpath"]))
        remove_if_exists: bool = parse_need_type(
            value=parsed_command.get_value_by_keys(keys=["rie", "remove_if_exists"]),
            need_type=NeedTypes.bool_
        )
        project_name = raise_if_string_blank(parsed_command.get_value_by_keys(keys=["pm", "project_name"]))
        init_arpakit_project_template(
            project_dirpath=project_dirpath, remove_if_exists=remove_if_exists, project_name=project_name
        )

    else:
        raise Exception(f"not recognized command, command={command}")

    _logger.info(f"finish {command}")

    _logger.info("finish _arpakitlib_cli")


if __name__ == '__main__':
    _arpakitlib_cli(full_command=" ".join(sys.argv))
