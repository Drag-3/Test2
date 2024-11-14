from StreamLanguage.sl_types.meta_type.meta_base import SLMetaType

class SLIntegerType(SLMetaType):
    """
    Represents the integer type in StreamLanguage.
    """

    def __init__(self):
        super().__init__("Integer")

    def __str__(self):
        return "Integer"