import asyncio
import os
import pathlib

from arpakitlib.ar_enumeration_util import Enumeration
from arpakitlib.ar_json_util import safely_transfer_obj_to_json_str


class ProjectPaths(Enumeration):
    base_dirpath: str = str(pathlib.Path(__file__).parent.parent.parent)

    env_filename: str = ".env"
    env_filepath: str = os.path.join(base_dirpath, env_filename)

    src_dirname: str = "src"
    src_dirpath: str = os.path.join(base_dirpath, src_dirname)

    manage_dirname: str = "manage"
    manage_dirpath: str = os.path.join(base_dirpath, manage_dirname)

    resource_dirname: str = "resource"
    resource_dirpath: str = os.path.join(base_dirpath, resource_dirname)

    static_dirname: str = "static"
    static_dirpath: str = os.path.join(resource_dirpath, static_dirname)


# ...


def __example():
    print(safely_transfer_obj_to_json_str(ProjectPaths.key_to_value()))


async def __async_example():
    pass


if __name__ == '__main__':
    __example()
    asyncio.run(__async_example())
