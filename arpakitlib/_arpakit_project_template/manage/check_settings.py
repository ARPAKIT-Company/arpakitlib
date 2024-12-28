from src.core.settings import get_cached_settings


def command():
    print(get_cached_settings())


if __name__ == '__main__':
    command()
