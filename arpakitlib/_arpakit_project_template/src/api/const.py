from arpakitlib.ar_fastapi_util import BaseAPIErrorCodes


class APIErrorCodes(BaseAPIErrorCodes):
    pass


if __name__ == '__main__':
    print(APIErrorCodes.str_for_print())
