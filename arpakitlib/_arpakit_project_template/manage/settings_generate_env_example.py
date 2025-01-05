import os.path

from src.core.const import BASE_DIRPATH
from src.core.settings import Settings


def command():
    print(Settings.generate_env_example())
    Settings.save_env_example_to_file(filepath=os.path.join(BASE_DIRPATH, "example.env"))


if __name__ == '__main__':
    command()
