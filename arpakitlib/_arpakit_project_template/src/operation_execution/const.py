from arpakitlib.ar_sqlalchemy_model_util import BaseOperationTypes


class OperationTypes(BaseOperationTypes):
    pass


if __name__ == '__main__':
    print(f"OperationTypes (len={len(OperationTypes.values_list())})")
    for v in OperationTypes.values_list():
        print(f"- {v}")
