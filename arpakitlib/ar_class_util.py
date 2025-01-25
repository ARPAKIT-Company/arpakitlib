# arpakit


_ARPAKIT_LIB_MODULE_VERSION = "3.0"


class CollectingSubclassesMeta(type):
    """
    Метакласс для автоматического сбора всех наследников в поле ALL_SUBCLASSES.
    """

    def __init__(cls, name, bases, dct, **kwargs):
        super().__init__(name, bases, dct, **kwargs)
        if not hasattr(cls, "all_subclasses"):
            cls.all_subclasses = []
        elif bases:
            cls.all_subclasses.append(cls)
