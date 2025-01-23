from arpakitlib.ar_json_util import safely_transfer_str_to_json_obj_to_json_str


def __json_beautify():
    s = input("JSON:\n")
    print(safely_transfer_str_to_json_obj_to_json_str(s))


if __name__ == '__main__':
    __json_beautify()
