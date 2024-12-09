from arpakitlib.ar_json_util import safely_transfer_to_json_obj


def command():
    s = input(":")
    print(safely_transfer_to_json_obj(s)['traceback_str'])


if __name__ == '__main__':
    command()
