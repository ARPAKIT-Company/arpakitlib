from arpakitlib.ar_fastapi_util import BaseAPIErrorCodes, BaseAPIErrorSpecificationCodes


class APIErrorCodes(BaseAPIErrorCodes):
    pass


class APIErrorSpecificationCodes(BaseAPIErrorSpecificationCodes):
    pass


if __name__ == '__main__':
    print(APIErrorCodes.str_for_print())
