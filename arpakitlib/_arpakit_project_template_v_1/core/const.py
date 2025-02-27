import asyncio
import os
import pathlib

from arpakitlib.ar_enumeration_util import Enumeration
from arpakitlib.ar_json_util import safely_transfer_obj_to_json_str


class ProjectPaths(Enumeration):
    base_dirpath: str = str(pathlib.Path(__file__).parent.parent)

    env_filepath: str = os.path.join(base_dirpath, ".env")

    resource_dirpath: str = os.path.join(base_dirpath, "resource")

    static_dirpath: str = os.path.join(resource_dirpath, "static")

    templates_dirpath: str = os.path.join(resource_dirpath, "templates")

    arpakit_lib_project_template_info_filepath: str = os.path.join(
        base_dirpath, "arpakitlib_project_template_info.json"
    )


def __example():
    print(safely_transfer_obj_to_json_str(ProjectPaths.key_to_value()))


async def __async_example():
    pass


if __name__ == '__main__':
    __example()
    asyncio.run(__async_example())
