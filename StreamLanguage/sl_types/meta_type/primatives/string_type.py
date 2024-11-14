from StreamLanguage.sl_types.meta_type.meta_base import SLMetaType

class SLStringType(SLMetaType):
    """
    Represents the string type in StreamLanguage.
    """

    def __init__(self):
        super().__init__("String")

    def __str__(self):
        return "String"