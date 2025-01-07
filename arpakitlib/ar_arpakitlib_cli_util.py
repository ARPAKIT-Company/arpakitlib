# arpakit

import sys

from arpakitlib.ar_arpakit_project_template_util import init_arpakit_project_template
from arpakitlib.ar_need_type_util import parse_need_type, NeedTypes
from arpakitlib.ar_parse_command import parse_command
from arpakitlib.ar_str_util import raise_if_string_blank


def execute_arpakitlib_cli(*, full_command: str | None = None):
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
        print("Commands:")
        print()
        print("-c init_arpakit_project_template")
        print("-project_dirpath ...")
        print("-overwrite_if_exists ...")
        print("-project_name ...")
        print("-sql_db_port ...")
        print("-api_port ...")
        print("-ignore_paths_startswith ...")
        print("-only_paths_startswith ...")
        print("\n")

    elif command == "init_arpakit_project_template":
        project_dirpath = raise_if_string_blank(parsed_command.get_value_by_keys(keys=["pd", "project_dirpath"]))
        overwrite_if_exists: bool = parse_need_type(
            value=parsed_command.get_value_by_keys(keys=["oie", "overwrite_if_exists"]),
            need_type=NeedTypes.bool_,
            allow_none=False
        )
        project_name: str = parsed_command.get_value_by_keys(keys=["pm", "project_name"])
        project_name = project_name.strip() if project_name.strip() else None
        sql_db_port: int | None = parse_need_type(
            value=parsed_command.get_value_by_keys(keys=["sdp", "sql_db_port"]),
            need_type=NeedTypes.int_,
            allow_none=True
        )
        api_port: int | None = parse_need_type(
            value=parsed_command.get_value_by_keys(keys=["ap", "api_port"]),
            need_type=NeedTypes.int_,
            allow_none=True
        )
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
            project_dirpath=project_dirpath, overwrite_if_exists=overwrite_if_exists,
            project_name=project_name, sql_db_port=sql_db_port, api_port=api_port,
            ignore_paths_startswith=ignore_paths_startswith, only_paths_startswith=only_paths_startswith
        )

    else:
        raise Exception(f"not recognized command, command={command}")


if __name__ == '__main__':
    execute_arpakitlib_cli(full_command="/arpakitlib -c help")
