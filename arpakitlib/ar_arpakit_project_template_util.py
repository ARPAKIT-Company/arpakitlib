# arpakit

import logging
import os

from arpakitlib.ar_str_util import raise_if_string_blank
from arpakitlib.ar_type_util import raise_for_type

_ARPAKIT_LIB_MODULE_VERSION = "3.0"

_logger = logging.getLogger(__name__)


def init_arpakit_project_template(
        *,
        project_dirpath: str = "./",
        overwrite_if_exists: bool = False,
        params: dict[str, str] | None = None,
        ignore_paths_startswith: list[str] | str | None = None,
        only_paths_startswith: list[str] | str | None = None,
):
    raise_if_string_blank(project_dirpath)

    raise_for_type(overwrite_if_exists, bool)

    if params is None:
        params = {}
    raise_for_type(params, dict)

    if isinstance(ignore_paths_startswith, str):
        ignore_paths_startswith = [ignore_paths_startswith]
    if ignore_paths_startswith is None:
        ignore_paths_startswith = []

    if isinstance(only_paths_startswith, str):
        only_paths_startswith = [only_paths_startswith]
    if only_paths_startswith is None:
        only_paths_startswith = []

    def _generate_filepath_to_content() -> dict[str, str]:
        arpakit_project_template_dirpath = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "_arpakit_project_template"
        )
        res = {}
        for root, dirs, files in os.walk(arpakit_project_template_dirpath):
            dirs[:] = [d for d in dirs if d != '__pycache__']
            for file in files:
                rel_path = os.path.relpath(os.path.join(root, file), arpakit_project_template_dirpath)
                if (
                        ignore_paths_startswith
                        and
                        any(rel_path.startswith(ignore_path) for ignore_path in ignore_paths_startswith)
                ):
                    _logger.info(f"ignoring file: {rel_path}")
                    continue
                if (
                        only_paths_startswith
                        and
                        not any(rel_path.startswith(only_path) for only_path in only_paths_startswith)
                ):
                    _logger.info(f"ignoring file: {rel_path}")
                    continue
                with open(os.path.join(root, file), "r", encoding="utf-8") as _file:
                    _content = _file.read()
                for key, value in params.items():
                    _content = _content.replace("{{" + key.upper().strip() + "}}", value)
                res[rel_path] = _content
        return res

    filepath_to_content = _generate_filepath_to_content()

    if not os.path.exists(project_dirpath):
        os.makedirs(project_dirpath)

    for filepath, content in filepath_to_content.items():
        full_filepath = os.path.join(project_dirpath, filepath)

        if os.path.exists(full_filepath) and not overwrite_if_exists:
            _logger.info(f"file exists and overwrite_if_exists is False, skipping: {full_filepath}")
            continue

        _logger.info(f"creating file: {full_filepath}")
        os.makedirs(os.path.dirname(full_filepath), exist_ok=True)
        with open(full_filepath, "w", encoding="utf-8") as file_:
            file_.write(content)
        _logger.info(f"file created: {full_filepath}")
