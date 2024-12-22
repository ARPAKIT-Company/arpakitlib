import os


def raise_if_path_not_exists(path: str):
    if not os.path.exists(path):
        raise Exception(f"path {path} not exists")
