import os.path

from src.core.const import BASE_DIRPATH
from src.core.settings import Settings


def command():
    env_example = Settings.generate_env_example()
    print(env_example)
    with open(os.path.join(BASE_DIRPATH, "example.env"), mode="w") as f:
        f.write(env_example)


if __name__ == '__main__':
    command()
