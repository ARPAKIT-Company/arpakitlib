# arpakit

import sys

from arpakitlib.ar_need_type_util import parse_need_type, NeedTypes
from arpakitlib.ar_parse_command import parse_command
from arpakitlib.ar_project_template_util import init_arpakit_project_template
from arpakitlib.ar_str_util import raise_if_string_blank


def arpakitlib_cli(*, full_command: str | None = None):
    if full_command is None:
        full_command = " ".join(sys.argv)

    parsed_command = parse_command(text=full_command)
    parsed_command.raise_for_command(needed_command="arpakitlib", lower_=True)

    command = parsed_command.get_value_by_keys(keys=["command", "c"])
    if command:
        command = command.strip()
    if not command:
        raise Exception(f"not command, command={command}")

    if command == "help":
        print(
            "Commands:"
            "\n- init_arpakit_project_template"
            " (project_dirpath, overwrite_if_exists, project_name, ignore_paths_startswith, only_paths_startswith)"
        )

    elif command == "init_arpakit_project_template":
        project_dirpath = raise_if_string_blank(parsed_command.get_value_by_keys(keys=["pd", "project_dirpath"]))
        overwrite_if_exists: bool = parse_need_type(
            value=parsed_command.get_value_by_keys(keys=["oie", "overwrite_if_exists"]),
            need_type=NeedTypes.bool_,
            allow_none=False
        )
        project_name: str = parsed_command.get_value_by_keys(keys=["pm", "project_name"])
        project_name = project_name if project_name.strip() else None
        ignore_paths_startswith: list[str] | None = parse_need_type(
            value=parsed_command.get_value_by_keys(keys=["ipsw", "ignore_paths_startswith"]),
            need_type=NeedTypes.list_of_str,
            allow_none=True
        )
        only_paths_startswith: list[str] | None = parse_need_type(
            value=parsed_command.get_value_by_keys(keys=["ops", "only_paths_startswith"]),
            need_type=NeedTypes.list_of_str,
            allow_none=True
        )
        init_arpakit_project_template(
            project_dirpath=project_dirpath, overwrite_if_exists=overwrite_if_exists, project_name=project_name,
            ignore_paths_startswith=ignore_paths_startswith, only_paths_startswith=only_paths_startswith
        )

    else:
        raise Exception(f"not recognized command, command={command}")


if __name__ == '__main__':
    arpakitlib_cli(full_command="/arpakitlib -c help")
