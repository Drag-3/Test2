from StreamLanguage.sl_types.meta_type.meta_base import SLMetaType

class SLStackType(SLMetaType):
    """
    Represents the stack type in StreamLanguage.
    """

    def __init__(self):
        super().__init__("Stack")

    def __str__(self):
        return "Stack"