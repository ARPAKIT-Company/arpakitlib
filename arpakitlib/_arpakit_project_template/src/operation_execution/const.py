from arpakitlib.ar_enumeration_util import Enumeration


class OperationTypes(Enumeration):
    healthcheck_ = "healthcheck"
    raise_fake_exception_ = "raise_fake_exception"


if __name__ == '__main__':
    OperationTypes.print()
