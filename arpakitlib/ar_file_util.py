import os


def raise_if_path_not_exists(path: str):
    if not os.path.exists(path):
        raise Exception(f"path {path} not exists")


def __example():
    try:
        raise_if_path_not_exists("C:/Users/njmin/PycharmProjects/arpakitlib/arpakitlib")
        print("There is a path")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    __example()