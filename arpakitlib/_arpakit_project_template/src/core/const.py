import asyncio
import os
import pathlib

from arpakitlib.ar_enumeration_util import Enumeration


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


def __example():
    print(f"base_dirpath: {ProjectPaths.base_dirpath}")
    print(f"env_filename: {ProjectPaths.env_filename}")
    print(f"env_filepath: {ProjectPaths.env_filepath}")
    print(f"src_dirname: {ProjectPaths.src_dirname}")
    print(f"src_dirpath: {ProjectPaths.src_dirpath}")
    print(f"manage_dirname: {ProjectPaths.manage_dirname}")
    print(f"manage_dirpath: {ProjectPaths.manage_dirpath}")
    print(f"resource_dirname: {ProjectPaths.resource_dirname}")
    print(f"resource_dirpath: {ProjectPaths.resource_dirpath}")
    print(f"static_dirname: {ProjectPaths.static_dirname}")
    print(f"static_dirpath: {ProjectPaths.static_dirpath}")


async def __async_example():
    pass


if __name__ == '__main__':
    __example()
    asyncio.run(__async_example())
