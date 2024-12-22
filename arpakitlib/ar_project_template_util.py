# arpakit
import logging
import os

from arpakitlib.ar_file_util import raise_if_path_not_exists

_ARPAKIT_LIB_MODULE_VERSION = "3.0"

_logger = logging.getLogger(__name__)


def init_arpakit_project_template(
        *, project_dirpath: str, remove_if_exists: bool = False, project_name: str | None = None
):
    if project_name:
        project_name = project_name.strip()
    if not project_name:
        project_name = None

    source_template_dirpath = os.path.join(os.path.dirname(__file__), "_arpakit_project_template")

    raise_if_path_not_exists(path=source_template_dirpath)

    project_dirpath = os.path.abspath(project_dirpath)

    filepath_to_content = {}

    for root_filepath, dir_filepaths, file_filepaths in os.walk(source_template_dirpath):
        dir_filepaths[:] = [d for d in dir_filepaths if d != "__pycache__"]
        relative_filepath = os.path.relpath(root_filepath, source_template_dirpath)
        target_root_filepath = os.path.normpath(os.path.join(project_dirpath, relative_filepath))
        for file in file_filepaths:
            source_file_filepath = os.path.join(root_filepath, file)
            target_file_filepath = os.path.normpath(os.path.join(target_root_filepath, file))

            with open(source_file_filepath, "r", encoding="utf-8") as f:
                content = f.read()

            if project_name is not None:
                content = content.replace("{PROJECT_NAME}", project_name)

            filepath_to_content[target_file_filepath] = content

    if not os.path.exists(project_dirpath):
        os.makedirs(project_dirpath)

    for target_file_filepath, content in filepath_to_content.items():
        if os.path.exists(target_file_filepath) and not remove_if_exists:
            _logger.info(f"skip existing file: {target_file_filepath}")
            continue
        _logger.info(f"initing file: {target_file_filepath}")
        os.makedirs(os.path.dirname(target_file_filepath), exist_ok=True)
        with open(target_file_filepath, "w", encoding="utf-8") as f:
            f.write(content)
        _logger.info(f"file was inited: {target_file_filepath}")
