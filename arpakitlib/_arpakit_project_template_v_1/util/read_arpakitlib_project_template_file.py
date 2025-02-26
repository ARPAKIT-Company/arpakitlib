import json
from typing import Any

from core.const import ProjectPaths


def read_arpakitlib_project_template_file() -> dict[str, Any]:
    with open(ProjectPaths.arpakit_lib_project_template_info_filepath, mode="r", encoding="utf-8") as fr:
        return json.load(fp=fr)


def __example():
    print(read_arpakitlib_project_template_file())


if __name__ == '__main__':
    __example()
